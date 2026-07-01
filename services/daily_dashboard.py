"""
daily_dashboard.py
Module untuk menampilkan dashboard harian: total uang masuk dan tunggakan hari ini.
"""
import re
from datetime import datetime

from core.master_data import format_rupiah, normalisasi_tanggal_gs, parse_rupiah
from database import db_client


def get_dashboard_data_core(db_transaksi, target_date):
    """
    Fungsi inti untuk mengambil data dashboard dari database berdasarkan tanggal.
    """
    try:
        # Optimasi: Hanya ambil data yang mengandung tanggal target
        semua_data = db_client.get_transaksi_by_filter("tanggal", target_date, "ilike")
    except Exception as e:
        return {"error": True, "message": f"Gagal mengakses database: {e}"}

    # Variabel akumulasi
    total_uang_masuk = 0
    total_tunggakan = 0
    total_transaksi = 0

    breakdown = {
        "lunas": {"count": 0, "total": 0},
        "cicil": {"count": 0, "total": 0},
        "hutang": {"count": 0, "total": 0},
    }

    transaksi_list = []

    for row in semua_data:
        tanggal_gs = row.get("tanggal", "")
        # Normalisasi tanggal dari database
        tanggal_normalized = normalisasi_tanggal_gs(tanggal_gs)

        # Filter berdasarkan tanggal target
        if tanggal_normalized != target_date:
            continue

        # Parse data
        nama_gs = row.get("nama_pelanggan", "")
        barang_gs = row.get("barang", "")
        jumlah_gs = row.get("jumlah_satuan", "")
        status_gs = row.get("status", "")
        metode_gs = row.get("metode_pembayaran", "")

        # Parse nilai numerik secara aman menggunakan parse_rupiah
        tagihan_val = parse_rupiah(row.get("tagihan", 0))
        uang_masuk_val = parse_rupiah(row.get("uang_masuk", 0))
        total_harga_val = parse_rupiah(row.get("total", 0))

        # Akumulasi total
        total_uang_masuk += uang_masuk_val
        total_tunggakan += tagihan_val
        total_transaksi += 1

        # Kategorisasi status
        status_lower = str(status_gs).lower()
        if "lunas" in status_lower:
            breakdown["lunas"]["count"] += 1
            breakdown["lunas"]["total"] += total_harga_val
        elif any(k in status_lower for k in ["cicil", "dicicil", "nyicil", "dp"]):
            breakdown["cicil"]["count"] += 1
            breakdown["cicil"]["total"] += total_harga_val
        else:
            breakdown["hutang"]["count"] += 1
            breakdown["hutang"]["total"] += total_harga_val

        # Simpan detail transaksi
        transaksi_list.append(
            {
                "nama": nama_gs,
                "barang": barang_gs,
                "jumlah": jumlah_gs,
                "total": format_rupiah(total_harga_val),
                "status": status_gs,
                "metode": metode_gs,
                "tagihan": format_rupiah(tagihan_val),
                "uang_masuk": format_rupiah(uang_masuk_val),
            }
        )

    # Parse tanggal untuk display
    try:
        date_obj = datetime.strptime(target_date, "%d-%m-%Y")
        tanggal_display = date_obj.strftime("%d %B %Y")
    except:
        tanggal_display = target_date

    return {
        "error": False,
        "tanggal": target_date,
        "tanggal_display": tanggal_display,
        "total_uang_masuk": total_uang_masuk,
        "total_tunggakan": total_tunggakan,
        "total_transaksi": total_transaksi,
        "breakdown": breakdown,
        "transaksi_list": transaksi_list,
    }


def render_dashboard_text(dashboard_data):
    """
    Render dashboard data menjadi text Telegram dengan format yang cantik dan modern.
    """
    if dashboard_data.get("error"):
        return f"❌ <b>Error:</b> {dashboard_data.get('message', 'Unknown error')}"

    tanggal_display = dashboard_data["tanggal_display"]
    total_uang_masuk = dashboard_data["total_uang_masuk"]
    total_tunggakan = dashboard_data["total_tunggakan"]
    total_transaksi = dashboard_data["total_transaksi"]
    breakdown = dashboard_data["breakdown"]

    # Format rupiah
    uang_masuk_fmt = format_rupiah(total_uang_masuk)
    tunggakan_fmt = format_rupiah(total_tunggakan)
    total_nilai = total_uang_masuk + total_tunggakan

    # Visual Progress Bar (Emoji based)
    def generate_progress_bar(val1, val2):
        total = val1 + val2
        if total == 0:
            return "⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪ (0%)"
        p1 = int((val1 / total) * 10)
        p2 = 10 - p1
        bar = "🟩" * p1 + "🟥" * p2
        persen = (val1 / total) * 100
        return f"{bar} ({persen:.1f}%)"

    progress_bar = generate_progress_bar(total_uang_masuk, total_tunggakan)

    text = f"""📊 <b>RINGKASAN EKSEKUTIF</b>
━━━━━━━━━━━━━━━━━━━━━━
📅 <b>Periode:</b> {tanggal_display}
📈 <b>Total Transaksi:</b> {total_transaksi} Nota
━━━━━━━━━━━━━━━━━━━━━━

💰 <b>UANG MASUK (KAS)</b>
└ <code>{uang_masuk_fmt}</code>

⚠️ <b>PIUTANG (BELUM BAYAR)</b>
└ <code>{tunggakan_fmt}</code>

📊 <b>RASIO PEMBAYARAN</b>
{progress_bar}
<i>(Hijau: Masuk, Merah: Piutang)</i>

━━━━━━━━━━━━━━━━━━━━━━
📋 <b>STATUS PEMBAYARAN</b>

✅ <b>Lunas</b>
   ├ {breakdown['lunas']['count']} Nota
   └ <code>{format_rupiah(breakdown['lunas']['total'])}</code>

⏳ <b>Cicilan / DP</b>
   ├ {breakdown['cicil']['count']} Nota
   └ <code>{format_rupiah(breakdown['cicil']['total'])}</code>

🔴 <b>Belum Bayar</b>
   ├ {breakdown['hutang']['count']} Nota
   └ <code>{format_rupiah(breakdown['hutang']['total'])}</code>

━━━━━━━━━━━━━━━━━━━━━━
💡 <i>Data sinkron otomatis dengan Supabase</i>
"""
    return text


def get_dashboard_harian(db_transaksi, target_date=None):
    """
    Mengambil data dashboard untuk hari ini.
    """
    if not target_date:
        target_date = datetime.now().strftime("%d-%m-%Y")
    return get_dashboard_data_core(db_transaksi, target_date)


def get_dashboard_custom_date(db_transaksi, target_date, cocokkan_nama_fn=None):
    """
    Mengambil dashboard untuk tanggal tertentu.
    """
    return get_dashboard_data_core(db_transaksi, target_date)
