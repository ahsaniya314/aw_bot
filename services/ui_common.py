"""
UI Common - Utility functions yang dibagikan antar module UI
"""
import logging
logger = logging.getLogger("bot_logger")


def _missing_keys_single(entitas):
    """
    Cek field wajib yang hilang untuk single transaksi
    """
    field_wajib = ["TANGGAL", "NAMA", "BARANG", "JUMLAH", "TOTAL", "STATUS"]
    # Only require METODE_PEMBAYARAN if status is Lunas or Dicicil
    status = entitas.get("STATUS", "").strip().lower()
    if status in ["lunas", "dicicil"]:
        field_wajib.append("METODE_PEMBAYARAN")
    return [f for f in field_wajib if not entitas.get(f)]


def _missing_keys_multi(entitas):
    """
    Cek field wajib yang hilang untuk multi transaksi
    """
    field_wajib = ["TANGGAL", "NAMA", "BARANG", "JUMLAH", "TOTAL", "STATUS"]
    # Only require METODE_PEMBAYARAN if status is Lunas or Dicicil
    status = entitas.get("STATUS", "").strip().lower()
    if status in ["lunas", "dicicil"]:
        field_wajib.append("METODE_PEMBAYARAN")
    return [f for f in field_wajib if not entitas.get(f)]


def _friendly_field_name(field_key):
    """
    Ubah nama field menjadi bahasa Indonesia yang ramah
    """
    mapping = {
        "TANGGAL": "Tanggal",
        "NAMA": "Nama Pelanggan",
        "BARANG": "Nama Barang",
        "JUMLAH": "Jumlah",
        "SATUAN": "Satuan",
        "HARGA": "Harga Satuan",
        "TOTAL": "Total Harga",
        "STATUS": "Status Pembayaran",
        "METODE_PEMBAYARAN": "Metode Pembayaran",
        "NOMINAL_BAYAR": "DP/Cicilan"
    }
    return mapping.get(field_key, field_key)
