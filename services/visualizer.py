import io
import os
from datetime import datetime

import matplotlib.pyplot as plt

from core.master_data import format_rupiah


def generate_dashboard_chart(dashboard_data):
    """
    Menghasilkan grafik pie chart untuk rasio pembayaran (Uang Masuk vs Piutang)
    dan menyimpannya ke buffer memori sebagai image.
    """
    total_uang_masuk = dashboard_data.get("total_uang_masuk", 0)
    total_tunggakan = dashboard_data.get("total_tunggakan", 0)

    if total_uang_masuk == 0 and total_tunggakan == 0:
        return None

    # Data untuk chart
    labels = ["Uang Masuk", "Piutang"]
    sizes = [total_uang_masuk, total_tunggakan]
    colors = ["#2ecc71", "#e74c3c"]  # Hijau dan Merah
    explode = (0.1, 0)  # Potong bagian uang masuk sedikit

    plt.figure(figsize=(8, 6))
    plt.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=140,
        textprops={"fontsize": 14, "weight": "bold"},
    )

    plt.title(f"Rasio Keuangan - {dashboard_data.get('tanggal_display', '')}", fontsize=16, pad=20)
    plt.axis("equal")  # Memastikan pie chart berbentuk lingkaran

    # Simpan ke buffer memori
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)
    plt.close()

    return buf


def generate_performance_chart(db_transaksi, limit_days=7):
    """
    Menghasilkan grafik line chart untuk performa uang masuk selama 7 hari terakhir.
    """
    # Logic untuk mengambil data histori 7 hari terakhir bisa ditambahkan di sini
    # Untuk saat ini kita fokus pada rasio harian yang paling dibutuhkan user
    pass
