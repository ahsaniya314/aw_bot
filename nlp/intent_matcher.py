import logging
import re

from rapidfuzz import fuzz, process

from nlp.embedded_data import INTENT_PATTERNS, NLP_TRAINING_EXAMPLES

logger = logging.getLogger(__name__)

# Alias untuk kompatibel dengan kode lama
DATASET = NLP_TRAINING_EXAMPLES

# ════════════════════════════════════════════════════════════
# DATASET-TO-SYSTEM INTENT MAPPING
# ════════════════════════════════════════════════════════════
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

# ════════════════════════════════════════════════════════════
# INTENT PRIORITY AND CONFIDENCE THRESHOLDS
# ════════════════════════════════════════════════════════════
# Higher priority intents are checked first
INTENT_PRIORITY = [
    "bayar_hutang",
    "Pelunasan_Hutang",
    "hapus_transaksi",
    "update_transaksi",
    "tambah_transaksi_cicilan_cash",
    "tambah_transaksi_cicilan_transfer",
    "tambah_transaksi_cicilan_tanggal_spesifik",
    "tambah_transaksi_lunas_cash",
    "tambah_transaksi_lunas_transfer",
    "tambah_transaksi_tanggal_spesifik",
    "tambah_transaksi_multi_item",
    "tambah_produk",
    "edit_produk",
    "hapus_produk",
    "cek_harga_produk_spesifik",
    "tampilkan_produk",
    "filter_belum_lunas",
    "filter_bayar_cash",
    "filter_bayar_transfer",
    "cek_penjualan_hari_ini",
    "total_transaksi",
    "total_uang_masuk",
    "total_tagihan",
    "total_tunggakan",
    "pembeli_terbanyak",
    "hutang_terbanyak",
    "cek_pesanan_pelanggan",
    "tampilkan_transaksi_tanggal",
    "tampilkan_transaksi_kemarin",
    "tampilkan_transaksi_hari_ini",
    "tampilkan_semua_transaksi",
    "greeting",
]

# Adaptive confidence thresholds per intent
INTENT_THRESHOLDS = {
    "greeting": 65,
    "tampilkan_semua_transaksi": 70,
    "tampilkan_transaksi_hari_ini": 70,
    "tampilkan_transaksi_kemarin": 70,
    "tampilkan_transaksi_tanggal": 70,
    "cek_pesanan_pelanggan": 70,
    "cek_penjualan_hari_ini": 70,
    "tambah_transaksi_lunas_cash": 70,
    "tambah_transaksi_lunas_transfer": 70,
    "tambah_transaksi_cicilan_cash": 70,
    "tambah_transaksi_cicilan_transfer": 70,
    "tambah_transaksi_tanggal_spesifik": 70,
    "tambah_transaksi_cicilan_tanggal_spesifik": 70,
    "tambah_transaksi_multi_item": 70,
    "hapus_transaksi": 70,
    "update_transaksi": 70,
    "tampilkan_produk": 70,
    "cek_harga_produk_spesifik": 70,
    "tambah_produk": 70,
    "edit_produk": 70,
    "hapus_produk": 70,
    "filter_belum_lunas": 70,
    "filter_bayar_cash": 70,
    "filter_bayar_transfer": 70,
    "total_transaksi": 70,
    "total_uang_masuk": 70,
    "total_tagihan": 70,
    "total_tunggakan": 70,
    "pembeli_terbanyak": 70,
    "hutang_terbanyak": 70,
    "bayar_hutang": 70,
    "Pelunasan_Hutang": 70,
    "cek_semua_penjualan": 70,
    "lihat_semua_transaksi": 70,
    "cek_hutang": 70,
    "cek_tagihan": 70,
}


def calculate_combined_score(text_clean, pattern):
    """
    Calculate combined score using multiple fuzzy matching algorithms
    for better accuracy.
    """
    scores = []
    
    # Token set ratio - good for partial matches
    token_set_score = fuzz.token_set_ratio(text_clean, pattern)
    scores.append(token_set_score)
    
    # Token sort ratio - good when word order doesn't matter
    token_sort_score = fuzz.token_sort_ratio(text_clean, pattern)
    scores.append(token_sort_score)
    
    # Partial ratio - good for matching parts of longer text
    partial_ratio = fuzz.partial_ratio(text_clean, pattern)
    scores.append(partial_ratio)
    
    # Weighted average - give more weight to token_set_ratio
    weighted_score = (
        token_set_score * 0.5 +
        token_sort_score * 0.3 +
        partial_ratio * 0.2
    )
    
    return weighted_score


def _normalize_intent_text(text):
    text_clean = text.lower().strip()
    # normalize punctuation and remove excessive whitespace
    text_clean = re.sub(r"[^a-z0-9\s]", " ", text_clean)
    text_clean = re.sub(r"\s+", " ", text_clean)
    return text_clean


def match_intent_from_dataset(text):
    """
    Enhanced fuzzy-match input using multiple scoring algorithms and intent priority.
    Return (system_intent, score) atau (None, 0) jika tidak cocok.
    """
    if not INTENT_PATTERNS:
        return None, 0

    text_clean = _normalize_intent_text(text)
    best_score = 0
    best_tag = None

    # early rules for stronger intent detection
    if re.search(r"\b(siapa yang masih hutang|siapa yang belum bayar|siapa yang cicilan|siapa yang masih nyicil|siapa yang punya hutang|daftar hutang|daftar tunggakan|cek hutang pelanggan|piutang pelanggan|cek piutang)\b", text_clean):
        return "Read_Analitik_Hutang", 100

    if re.search(r"\b(tampilkan tagihan|total tagihan|total tunggakan|berapa tagihan|tagihan hari ini|tagihan pelanggan|cek tagihan|total uang tagihan)\b", text_clean):
        return "Read_Analitik_Hutang", 100

    if re.search(r"\b(tampilkan tagihan|total tagihan|total tunggakan|berapa tagihan|tagihan hari ini|tagihan pelanggan|cek tagihan|total uang tagihan)\b", text_clean):
        return "Read_Analitik_Hutang", 100

    if re.search(r"\b(tampilkan semua transaksi|cek transaksi hari ini|lihat semua transaksi|tampilkan transaksi|cek semua transaksi|lihat data penjualan|tampil semua transaksi|tampilkan semua data)\b", text_clean):
        return "Read_Transaksi_Spesifik", 100

    if re.search(r"\b(total uang masuk|total transaksi|pembeli terbanyak|total penjualan hari ini|omzet hari ini|berapa laku hari ini|laporan penjualan hari ini|rekap penjualan hari ini)\b", text_clean):
        return "Read_Analitik_Penjualan", 100

    # Early transaction sales detection
    transaction_action = re.search(r"\b(ambil|pesan|beli|order|orderan)\b", text_clean)
    payment_words = re.search(r"\b(lunas|tunai|cash|dibayar|bayar cash|bayar tunai|sudah dibayar|bayar)\b", text_clean)
    cicil_words = re.search(r"\b(cicil|dicicil|cicilan|dp|uang muka|angsuran)\b", text_clean)
    debt_words = re.search(r"\b(hutang|utang|tagihan|piutang|tunggakan|cicilan)\b", text_clean)

    if transaction_action and cicil_words:
        return "Catat_Penjualan_Cicil", 100

    if transaction_action and payment_words and not debt_words:
        return "Catat_Penjualan_Lunas", 100

    if payment_words and debt_words:
        # pay debt or tagihan => Pelunasan Hutang
        return "Pelunasan_Hutang", 100

    if re.search(r"\b(lunasi|lunasin|pelunasan)\b", text_clean) and debt_words:
        return "Pelunasan_Hutang", 100

    # fuzzy matching fallback
    # Check intents in priority order
    for tag in INTENT_PRIORITY:
        if tag not in INTENT_PATTERNS:
            continue
            
        patterns = INTENT_PATTERNS[tag]
        if not patterns:
            continue
            
        # Calculate best score for this intent
        intent_best_score = 0
        for pattern in patterns:
            score = calculate_combined_score(text_clean, pattern)
            if score > intent_best_score:
                intent_best_score = score
                
        # Get threshold for this intent
        threshold = INTENT_THRESHOLDS.get(tag, 75)
        
        # If this intent's score is good enough and better than current best
        if intent_best_score >= threshold and intent_best_score > best_score:
            best_score = intent_best_score
            best_tag = tag
            # Early exit for high confidence matches
            if best_score >= 90:
                break

    if best_score > 0 and best_tag:
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
