import logging
import re
import urllib.parse
from datetime import date, datetime

from database import db_client

logger = logging.getLogger(__name__)


def parse_db_date(date_str):
    """
    Mengubah string tanggal (DD-MM-YYYY) menjadi object date.
    Mendukung penanganan fallback jika formatnya berbeda.
    """
    if not date_str:
        return None

    # Coba bersihkan karakter tak terlihat
    date_str = str(date_str).strip()

    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    # Jika gagal total, coba deteksi dengan regex sederhana
    match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", date_str)
    if match:
        try:
            d, m, y = match.groups()
            return date(int(y), int(m), int(d))
        except ValueError:
            pass

    return None


def cek_hutang_jatuh_tempo():
    """
    Memindai database pesanan untuk mencari hutang aktif (tagihan > 0)
    yang berusia tepat 3 hari atau 7 hari hari ini.
    """
    try:
        supabase = db_client.get_supabase()
        # Query pesanan yang belum lunas (tagihan > 0)
        # Ambil relasi pelanggan untuk mengambil nama dan nomor HP
        res = supabase.table("pesanan").select("*, pelanggan(*)").gt("tagihan", 0).execute()
        pesanan_list = res.data or []

        hari_ini = date.today()
        pengingat_3_hari = []
        pengingat_7_hari = []

        for pes in pesanan_list:
            tgl_pesanan = parse_db_date(pes.get("tanggal"))
            if not tgl_pesanan:
                continue

            selisih_hari = (hari_ini - tgl_pesanan).days

            pelanggan_info = pes.get("pelanggan") or {}
            nama_pelanggan = pelanggan_info.get("nama") or "Tanpa Nama"
            no_hp = pelanggan_info.get("no_hp") or ""

            # Buat teks template pesan penagihan WhatsApp
            tagihan_num = pes.get("tagihan", 0)
            tagihan_formatted = f"Rp {tagihan_num:,}".replace(",", ".")

            draft_wa = (
                f"Halo Kak {nama_pelanggan}, kami dari A&W Production ingin mengonfirmasi "
                f"terkait sisa tagihan pesanan Kakak pada tanggal {pes.get('tanggal')} "
                f"sebesar *{tagihan_formatted}*.\n\n"
                f"Mohon kesediaannya untuk melakukan pembayaran melalui transfer bank "
                f"atau langsung ke kasir toko kami. Terima kasih banyak atas kepercayaannya! 🙏"
            )

            wa_link = ""
            if no_hp:
                # Bersihkan nomor hp agar hanya angka saja
                no_clean = re.sub(r"[^\d]", "", str(no_hp))
                if no_clean.startswith("0"):
                    no_clean = "62" + no_clean[1:]
                elif no_clean.startswith("8"):
                    no_clean = "62" + no_clean

                encoded_text = urllib.parse.quote(draft_wa)
                wa_link = f"https://wa.me/{no_clean}?text={encoded_text}"

            pes_item = {
                "id_pesanan": pes.get("id"),
                "tanggal": pes.get("tanggal"),
                "nama": nama_pelanggan,
                "tagihan": tagihan_num,
                "wa_link": wa_link,
                "selisih": selisih_hari,
            }

            if selisih_hari == 3:
                pengingat_3_hari.append(pes_item)
            elif selisih_hari == 7:
                pengingat_7_hari.append(pes_item)

        return pengingat_3_hari, pengingat_7_hari

    except Exception as e:
        logger.error(f"Error saat mengecek hutang jatuh tempo: {e}")
        return [], []


def format_laporan_pengingat(pengingat_3_hari, pengingat_7_hari):
    """
    Format teks laporan pengingat hutang ke dalam markdown HTML Telegram yang cantik.
    """
    if not pengingat_3_hari and not pengingat_7_hari:
        return None

    teks = "🔔 <b>LAPORAN PENGINGAT PIUTANG HARIAN</b>\n"
    teks += f"📅 Tanggal: {date.today().strftime('%d-%m-%Y')}\n"
    teks += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if pengingat_3_hari:
        teks += "⚠️ <b>Jatuh Tempo 3 Hari (H+3):</b>\n"
        for p in pengingat_3_hari:
            teks += f"• 👤 <b>{p['nama']}</b>\n"
            teks += f"  📅 Tgl Nota: {p['tanggal']}\n"
            teks += f"  💸 Tagihan: <code>Rp {p['tagihan']:,}</code>\n".replace(",", ".")
            if p["wa_link"]:
                teks += f"  📲 <a href='{p['wa_link']}'>Hubungi via WhatsApp</a>\n"
            else:
                teks += "  ❌ No. HP tidak terdaftar\n"
            teks += "\n"

    if pengingat_7_hari:
        teks += "🚨 <b>Jatuh Tempo 7 Hari (H+7 - Sangat Penting!):</b>\n"
        for p in pengingat_7_hari:
            teks += f"• 👤 <b>{p['nama']}</b>\n"
            teks += f"  📅 Tgl Nota: {p['tanggal']}\n"
            teks += f"  💸 Tagihan: <code>Rp {p['tagihan']:,}</code>\n".replace(",", ".")
            if p["wa_link"]:
                teks += f"  📲 <a href='{p['wa_link']}'>Hubungi via WhatsApp</a>\n"
            else:
                teks += "  ❌ No. HP tidak terdaftar\n"
            teks += "\n"

    teks += "━━━━━━━━━━━━━━━━━━━━━━\n"
    teks += "<i>Silakan klik tautan WhatsApp di atas untuk langsung mengirim draf pesan penagihan otomatis yang sopan.</i>"

    return teks


def jalankan_notifikasi_reminder(bot, admin_ids):
    """
    Fungsi trigger utama untuk mengecek piutang dan mengirim notifikasi ke admin.
    """
    logger.info("Memulai pengecekan pengingat piutang harian...")
    pengingat_3, pengingat_7 = cek_hutang_jatuh_tempo()

    laporan_teks = format_laporan_pengingat(pengingat_3, pengingat_7)

    if not laporan_teks:
        logger.info("Tidak ada piutang yang jatuh tempo hari ini.")
        return False

    for admin_id in admin_ids:
        try:
            bot.send_message(
                admin_id, laporan_teks, parse_mode="HTML", disable_web_page_preview=True
            )
            logger.info(f"Notifikasi pengingat berhasil dikirim ke Admin {admin_id}")
        except Exception as e:
            logger.error(f"Gagal mengirim pengingat ke Admin {admin_id}: {e}")

    return True
