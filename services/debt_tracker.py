"""
debt_tracker.py
Module logika hutang dan pelunasan bertahap.

Struktur Kolom Tabel Transaksi (sesuai spesifikasi):
  A=Tanggal | B=Nama | C=Barang | D=Jumlah | E=Harga Satuan | F=Total Harga
  G=Status  | H=Metode Bayar
  I=Jumlah Tagihan   (gspread col 9,  list index 8)  ← Sisa yang masih harus dibayar
  J=Jumlah Uang Masuk (gspread col 10, list index 9)  ← Akumulasi uang yang sudah diterima

Logika Bisnis:
  Lunas       → Tagihan = 0,     Uang Masuk = Total Harga
  Nyicil/DP   → Tagihan = Total - Nominal Bayar,  Uang Masuk = Nominal Bayar
  Belum Lunas → Tagihan = Total, Uang Masuk = 0
  Pelunasan   → Tagihan baru = Tagihan lama - Nominal,  Uang Masuk baru = Uang Masuk lama + Nominal
"""

from datetime import datetime

from core.master_data import format_rupiah, parse_rupiah
from database import db_client


# =====================================================
# KALKULASI JUMLAH TAGIHAN & UANG MASUK (STATELESS)
# =====================================================
def hitung_sisa_tagihan(total_harga, nominal_bayar=0, status=None):
    """
    Hitung jumlah_tagihan dan jumlah_uang_masuk berdasarkan status transaksi.

    Parameter:
        total_harga   : Total harga transaksi (int/str Rupiah)
        nominal_bayar : Uang yang dibayarkan saat ini (int/str)
        status        : Status NLP ('Lunas', 'Nyicil', 'Belum Lunas', 'Pre-Order')

    Return: (jumlah_tagihan:int, jumlah_uang_masuk:int, status_final:str)

        jumlah_tagihan   → Kolom I (sisa hutang/piutang)
        jumlah_uang_masuk → Kolom J (total uang yang sudah diterima)
    """
    total = parse_rupiah(total_harga)
    dibayar = parse_rupiah(nominal_bayar) if nominal_bayar else 0

    if status == "Lunas":
        # Pembayaran penuh — tagihan nol, uang masuk = total
        return (0, total, "Lunas")

    elif status in ("Dicicil", "Nyicil"):  # terima kedua bentuk untuk backward compat
        # DP/cicilan — tagihan = total - yang dibayar
        tagihan = max(0, total - dibayar)
        uang_masuk = dibayar
        return (tagihan, uang_masuk, "Lunas" if tagihan == 0 else "Dicicil")

    elif status in ("Hutang", "Belum Lunas"):  # terima kedua bentuk
        # Hutang penuh — belum ada uang masuk
        return (total, 0, "Hutang")

    elif status == "Pre-Order":
        return (total, 0, "Pre-Order")

    else:
        return (0, 0, status or "Unset")


# =====================================================
# CARI HUTANG AKTIF BERDASARKAN NAMA
# =====================================================
def cari_hutang_aktif(db_transaksi, nama_target, cocokkan_nama_fn):
    """
    Cari semua baris di sheet Transaksi yang masih memiliki Jumlah Tagihan > 0
    untuk nama pelanggan tertentu.

    Jumlah Tagihan dibaca dari Supabase (kolom tagihan), if not available compute from total-uang_masuk.
    Also, include transactions with status "Hutang" or "Dicicil".

    Return: list of dict dengan info baris.
    """
    import logging

    logger = logging.getLogger("bot_logger")
    try:
        # Ambil semua transaksi, filter later for memory efficiency?
        semua_data = db_client.get_semua_transaksi_db()
        logger.info(f"[DEBUG] cari_hutang_aktif: Got {len(semua_data)} total transactions")
    except Exception as e:
        logger.error(f"Error cari_hutang_aktif DB: {e}")
        return []

    hasil = []
    for row in semua_data:
        nama_db = row.get("nama_pelanggan", "")
        logger.info(
            f"[DEBUG] Checking transaction: id={row.get('id')}, nama_pelanggan={repr(nama_db)}, nama_target={repr(nama_target)}"
        )
        if not cocokkan_nama_fn(nama_target, nama_db):
            logger.info("[DEBUG] cocokkan_nama_fn returned False, skipping")
            continue

        status = row.get("status", "").lower()
        total = float(row.get("total", 0) or 0)
        uang_masuk = float(row.get("uang_masuk", 0) or 0)
        tagihan = float(row.get("tagihan", 0) or 0)
        logger.info(
            f"[DEBUG] Transaction: id={row.get('id')}, status={status}, total={total}, uang_masuk={uang_masuk}, tagihan={tagihan}"
        )

        # Compute tagihan from total - uang_masuk if not set or incorrect
        if tagihan <= 0 and status in ["hutang", "dicicil", "belum lunas"]:
            tagihan = max(0, total - uang_masuk)
            logger.info(f"[DEBUG] Recalculated tagihan: {tagihan}")

        if tagihan <= 0:
            logger.info("[DEBUG] tagihan <=0, skipping")
            continue

        hasil.append(
            {
                "row_index": row["id"],  # Menggunakan ID DB
                "nama": nama_db,
                "barang": row.get("barang", ""),
                "tanggal": row.get("tanggal", ""),
                "total": format_rupiah(row.get("total", 0)),
                "tagihan": tagihan,
                "tagihan_str": format_rupiah(tagihan),
                "uang_masuk": uang_masuk,
                "uang_masuk_str": format_rupiah(uang_masuk),
                "status": row.get("status", ""),
                "metode": row.get("metode_pembayaran", "-"),
                "row_full": row,
            }
        )

    logger.info(f"[DEBUG] Found {len(hasil)} active debts for {nama_target}")
    return hasil


# =====================================================
# PROSES PEMBAYARAN TAMBAHAN (CICILAN / PELUNASAN)
# =====================================================
def proses_bayar_tambahan(
    db_transaksi, db_histori, row_idx, nominal_bayar, nama_pelanggan, catatan=""
):
    """
    Catat pembayaran cicilan atau pelunasan pada transaksi (berdasarkan ID).

    Return: dict {sukses, tagihan_lama, tagihan_baru, uang_masuk_baru, status_baru}
    """
    try:
        # Ambil data transaksi lama
        supabase = db_client.get_supabase()
        res = supabase.table("transaksi").select("*").eq("id", row_idx).execute()
        if not res.data:
            return {"sukses": False, "error": "Transaksi tidak ditemukan"}

        transaksi = res.data[0]
        tagihan_lama = float(transaksi.get("tagihan", 0) or 0)
        uang_masuk_lama = float(transaksi.get("uang_masuk", 0) or 0)

        tagihan_baru = max(0, tagihan_lama - nominal_bayar)
        uang_masuk_baru = uang_masuk_lama + nominal_bayar
        status_baru = "Lunas" if tagihan_baru == 0 else "Dicicil"

        # Update Transaksi
        update_data = {
            "status": status_baru,
            "tagihan": tagihan_baru,
            "uang_masuk": uang_masuk_baru,
        }
        db_client.update_transaksi_db(row_idx, update_data)

        # Catat ke Histori Pelunasan (only if db_histori or db_client available)
        try:
            tgl_bayar = datetime.now().strftime("%d-%m-%Y")
            keterangan = catatan or f"Cicilan {format_rupiah(nominal_bayar)}"

            histori_data = {
                "transaksi_id": row_idx,
                "tanggal_bayar": tgl_bayar,
                "nominal_bayar": nominal_bayar,
                "sisa_tagihan": tagihan_baru,
                "metode_pembayaran": keterangan,  # Menyimpan keterangan di field metode untuk sementara jika tidak ada kolom catatan khusus, atau kita bisa adjust skema tabel.
            }
            db_client.insert_histori_pelunasan_db(histori_data)
        except Exception as e:
            print(f"Warning: Could not save payment history: {e}")
            pass

        return {
            "sukses": True,
            "tagihan_lama": tagihan_lama,
            "tagihan_baru": tagihan_baru,
            "uang_masuk_baru": uang_masuk_baru,
            "status_baru": status_baru,
        }

    except Exception as e:
        print(f"Error proses_bayar_tambahan DB: {e}")
        return {"sukses": False, "error": str(e)}
