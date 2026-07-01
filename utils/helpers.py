"""
Helper Utilities — Nama Matching, Total Calculation
"""

import logging
import re

from rapidfuzz import fuzz

from core.master_data import format_rupiah

logger = logging.getLogger("bot_logger")


def bersihkan_nama(nama):
    if not nama:
        return ""
    nama_bersih = str(nama).lower().strip()
    for gelar in ["bapak ", "pak ", "ibu ", "bu ", "mas ", "mbak ", "atas nama "]:
        if nama_bersih.startswith(gelar):
            nama_bersih = nama_bersih[len(gelar) :].strip()
    return nama_bersih


def cocokkan_nama(nama_cari, nama_db):
    """
    Pencocokan nama berlapis yang KETAT:
    1. Exact match (100% cocok)
    2. Salah satu mengandung yang lain secara utuh (substring match)
    3. Token sort ratio >= 80 (untuk mencocokkan urutan nama yang berbeda)

    PENTING: Tidak menggunakan partial_ratio karena 'udin' vs 'budi'
    menghasilkan false positive (substring 'udi' cocok di keduanya).
    """
    a = bersihkan_nama(nama_cari)
    b = bersihkan_nama(nama_db)

    if not a or not b:
        return False

    # 1. Exact match
    if a == b:
        return True

    # 2. Salah satu mengandung yang lain SECARA UTUH sebagai kata
    #    "udin" in "pak udin jaya" → True
    #    "udin" in "budi"          → False (bukan kata utuh)
    a_words = set(a.split())
    b_words = set(b.split())
    if a_words.issubset(b_words) or b_words.issubset(a_words):
        return True

    # 3. Token sort ratio (membandingkan keseluruhan string, bukan substring)
    score = fuzz.token_sort_ratio(a, b)
    return score >= 80


def hitung_ulang_total_dinamis(entitas):
    """Mengkalkulasi ulang harga total & sinkronisasi Satuan jika sedang dilakukan pengeditan"""
    try:
        jumlah_str = str(entitas.get("JUMLAH") or "0")
        harga_str = str(entitas.get("HARGA") or "0")
        satuan_ref = entitas.get("SATUAN")

        # Ekstrak angka murni
        j_num = 0
        match_j = re.search(r"(\d+)", jumlah_str)
        if match_j:
            j_num = int(match_j.group(1))

        h_num = int(re.sub(r"[^\d]", "", harga_str)) if re.search(r"\d", harga_str) else 0

        # ── Sinkronisasi Satuan di Label Jumlah ──
        if satuan_ref and j_num > 0:
            # Jika di jumlah_str tidak ada satuan_ref, atau ada satuan lain, kita paksa ganti
            # Contoh: "30 toples" -> "30 bungkus"
            entitas["JUMLAH"] = f"{j_num} {satuan_ref}"

        # ── Hitung Total ──
        if j_num > 0 and h_num > 0:
            total_calc = j_num * h_num
            entitas["TOTAL"] = format_rupiah(total_calc)
    except Exception as e:
        logger.debug(f"Gagal hitung total dinamis: {e}")
