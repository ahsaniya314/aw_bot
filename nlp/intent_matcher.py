import logging
from rapidfuzz import process, fuzz

from nlp.embedded_data import INTENT_PATTERNS, NLP_TRAINING_EXAMPLES

logger = logging.getLogger(__name__)

# Alias untuk kompatibilitas dengan kode lama
DATASET = NLP_TRAINING_EXAMPLES

# ═══════════════════════════════════════════════════════════
# DATASET-TO-SYSTEM INTENT MAPPING
# ═══════════════════════════════════════════════════════════
DATASET_TO_SYSTEM_INTENT = {
    "greeting": "Chit_Chat",
    "cek_penjualan_hari_ini": "Read_Analitik_Penjualan",
    "tambah_transaksi_lunas_cash": "Catat_Penjualan_Lunas",
    "tambah_transaksi_lunas_transfer": "Catat_Penjualan_Lunas",
    "tambah_transaksi_cicilan_cash": "Catat_Penjualan_Cicil",
    "tambah_transaksi_cicilan_transfer": "Catat_Penjualan_Cicil",
    "tambah_transaksi_tanggal_spesifik": "Catat_Penjualan_Lunas",
    "tambah_transaksi_cicilan_tanggal_spesifik": "Catat_Penjualan_Cicil",
    "tampilkan_semua_transaksi": "Read_Transaksi_Spesifik",
    "tampilkan_transaksi_hari_ini": "Read_Transaksi_Spesifik",
    "tampilkan_transaksi_kemarin": "Read_Transaksi_Spesifik",
    "tampilkan_transaksi_tanggal": "Read_Transaksi_Spesifik",
    "cek_pesanan_pelanggan": "Read_Transaksi_Spesifik",
    "hapus_transaksi": "Update_Delete_Transaksi",
    "update_transaksi": "Update_Delete_Transaksi",
    "tampilkan_produk": "CRUD_Barang",
    "cek_harga_produk_spesifik": "CRUD_Barang",
    "tambah_produk": "CRUD_Barang",
    "edit_produk": "CRUD_Barang",
    "hapus_produk": "CRUD_Barang",
    "filter_belum_lunas": "Read_Transaksi_Spesifik",
    "filter_bayar_cash": "Read_Transaksi_Spesifik",
    "filter_bayar_transfer": "Read_Transaksi_Spesifik",
    "total_transaksi": "Read_Analitik_Penjualan",
    "total_uang_masuk": "Read_Analitik_Penjualan",
    "total_tagihan": "Read_Analitik_Hutang",
    "total_tunggakan": "Read_Analitik_Hutang",
    "pembeli_terbanyak": "Read_Analitik_Penjualan",
    "hutang_terbanyak": "Read_Analitik_Hutang",
    "bayar_hutang": "Pelunasan_Hutang",
    "tambah_transaksi_multi_item": "Catat_Penjualan_Lunas",
    "Pelunasan_Hutang": "Pelunasan_Hutang",
    "cek_semua_penjualan": "Read_Transaksi_Spesifik",
    "lihat_semua_transaksi": "Read_Transaksi_Spesifik",
    "cek_hutang": "Read_Analitik_Hutang",
    "cek_tagihan": "Read_Analitik_Hutang",
}


def match_intent_from_dataset(text):
    """
    Fuzzy-match input terhadap semua patterns di INTENT_PATTERNS.
    Return (system_intent, score) atau (None, 0) jika tidak cocok.
    """
    if not INTENT_PATTERNS:
        return None, 0

    text_clean = text.lower().strip()
    best_score = 0
    best_tag = None

    for tag, patterns in INTENT_PATTERNS.items():
        if not patterns:
            continue
        result = process.extractOne(text_clean, patterns, scorer=fuzz.token_set_ratio)
        if result and result[1] > best_score:
            best_score = result[1]
            best_tag = tag

    if best_score >= 80 and best_tag:
        system_intent = DATASET_TO_SYSTEM_INTENT.get(best_tag, best_tag)
        return system_intent, int(round(best_score))
    return None, 0


def tentukan_intent_manual(text):
    """
    Determines intent using manual rules as fallback.
    """
    text_clean = text.lower().strip()
    if any(k in text_clean for k in ["semua", "seluruh", "total"]):
        if any(k in text_clean for k in ["penjualan", "transaksi", "data"]):
            return "Read_Transaksi_Spesifik"
        if any(k in text_clean for k in ["hutang", "tagihan", "piutang"]):
            return "Read_Analitik_Hutang"

    if any(k in text_clean for k in ["halo", "hi", "siang", "pagi"]):
        return "Chit_Chat"
    return "Unknown"


def fuzzy_intent_fallback(text):
    """
    Mencari entri dataset yang paling mirip untuk memberikan hint entitas.
    """
    if not DATASET:
        return None

    examples = [d["text"] for d in DATASET]
    match = process.extractOne(text.lower(), examples, scorer=fuzz.token_set_ratio)

    if match and match[1] > 80:
        for d in DATASET:
            if d["text"] == match[0]:
                return d
    return None
