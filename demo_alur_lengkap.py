
"""
Alur Lengkap Pemrosesan Data NLP - Versi Lengkap
---------------------------------------------
Script ini menunjukkan setiap langkah secara detail dan dapat
dijalankan langsung di terminal tanpa Jupyter Notebook.
- Menunjukkan logika untuk laporan bagian PENYUSUNAN DATA TRANSAKSI
"""

import os
import sys

# Fix encoding di Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tambahkan root direktori ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re

from core.master_data import cari_harga_default, format_rupiah, parse_rupiah
from nlp.dictionaries import DAFTAR_KATA_KUNCI, KAMUS_ALIAS, NORMALIZATION_DICT
from nlp.extractor import ekstrak_entitas
from nlp.normalizer import koreksi_teks
from nlp.processor import _apply_multi_overrides, proses_nlp, split_multi_entries


def print_separator(title):
    """Print separator dengan judul."""
    print("\n\n\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def langkah_0_persiapan():
    """Langkah 0: Persiapan dan inisialisasi."""
    print_separator("LANGKAH 0: PERSIAPAN & INISIALISASI")
    print("[OK] Semua modul berhasil diimport!")
    print("[OK] Sistem siap digunakan!")


def langkah_1_input_data():
    """Langkah 1: Input Data."""
    global INPUT_TEKS
    # Input contoh dengan 3 entri, nama Pak Andi, menggunakan "l0lipp"
    INPUT_TEKS = "pak anDi Pesan l0lipp 10 dus, mses 5 bks, will0 3 dus belum lunwas semua"
    
    print_separator("LANGKAH 1: INPUT DATA MENTAH")
    print(f"Input: {INPUT_TEKS}")


def langkah_2_pemisahan_multi_entry():
    """Langkah 2: Pemisahan Multi-Entry."""
    global entries
    entries = split_multi_entries(INPUT_TEKS)
    
    print_separator("LANGKAH 2: PEMISAHAN MULTI-ENTRY")
    print(f"Jumlah entri: {len(entries)}")
    for i, entry in enumerate(entries, 1):
        print(f"\nEntri {i}:")
        print(f"  Teks: {entry}")


def langkah_3_text_cleaning():
    """Langkah 3: Text Cleaning."""
    global teks_clean
    entri_contoh = entries[0]
    
    print_separator("LANGKAH 3: TEXT CLEANING")
    print(f"\n1. Teks asli: {entri_contoh}")
    
    teks_clean = re.sub(r'[^\w\s]', '', entri_contoh)
    print(f"2. Setelah cleaning: {teks_clean}")

def langkah_4_lowercase():
    """Langkah 4: Lowercase."""
    global teks_bersih
    print_separator("LANGKAH 4: LOWERCASE")
    print(f"\n1. Teks sebelumnya: {teks_clean}")
    
    teks_bersih = teks_clean.lower()
    print(f"2. Setelah lowercase: {teks_bersih}")


def langkah_5_tokenization():
    """Langkah 5: Tokenization."""
    global tokens
    tokens = teks_bersih.split()
    
    print_separator("LANGKAH 5: TOKENIZATION")
    print(f"\nTeks: {teks_bersih}")
    print(f"\nTokens:")
    for i, token in enumerate(tokens, 1):
        print(f"  Token {i}: '{token}'")


def langkah_6_normalization_fuzzy_matching():
    """Langkah 6: Normalization & Fuzzy Matching."""
    print_separator("LANGKAH 6: NORMALIZATION & FUZZY MATCHING")
    
    print("\n--- Bagian A: DICTIONARY LOOKUP & PREPROCESSING ---")
    print("\nContoh KAMUS_ALIAS (nama barang):")
    contoh_barang = list(KAMUS_ALIAS.items())[:10]
    for typo, benar in contoh_barang:
        print(f"  '{typo}' menjadi '{benar}'")
    
    print("\n--- Bagian B: LANGKAH-LANGKAH KOREKSI TYPO SEPERTI SISTEM NYATA ---")
    from rapidfuzz import fuzz, process

    # Proses satu per satu entri untuk menunjukkan alur
    for idx_entri, entry in enumerate(entries, 1):
        print(f"\n=== MENGKOREKSI ENTRI {idx_entri}: '{entry}' ===")
        teks_proses = entry
        
        # PASS 0 & 1: Preprocess angka 0→o, 1→l
        print(f"\n1. Preprocessing angka 0→o dan 1→l:")
        print(f"   Sebelum: '{teks_proses}'")
        teks_proses = re.sub(r'(\b[a-zA-Z]+)([01])\b', r'\1', teks_proses, flags=re.IGNORECASE)
        teks_proses = re.sub(r'([a-zA-Z])0([a-zA-Z]*)', r'\1o\2', teks_proses, flags=re.IGNORECASE)
        teks_proses = re.sub(r'([a-zA-Z])1([a-zA-Z]*)', r'\1l\2', teks_proses, flags=re.IGNORECASE)
        words_pre = teks_proses.split()
        normalized_words = []
        for w in words_pre:
            w_low = w.lower()
            if not w.isdigit():
                w_normalized = w_low.replace('0', 'o').replace('1', 'l')
                normalized_words.append(w_normalized)
            else:
                normalized_words.append(w)
        teks_proses = " ".join(normalized_words)
        print(f"   Sesudah: '{teks_proses}'")
        
        # PASS 1.5: KAMUS_ALIAS lookup
        print(f"\n2. Cek KAMUS_ALIAS:")
        words_pre = teks_proses.split()
        replaced_words = []
        ignore_words = {"pak", "bu", "mas", "atas", "nama", "hari", "bulan", "tahun", "kemarin", "besok", "lusa", "minggu", "belum", "sudah", "semua", "setengah", "cicil", "transfer", "tunai", "cash", "dp", "kontan", "langsung", "lunas", "hutang", "utang", "bayar", "dibayar", "ngutang", "kasbon"}
        for w in words_pre:
            w_low = w.lower()
            if w_low in ignore_words:
                replaced_words.append(w)
            elif w_low in KAMUS_ALIAS:
                print(f"   ✅ '{w_low}' ditemukan di KAMUS_ALIAS → '{KAMUS_ALIAS[w_low]}'")
                replaced_words.append(KAMUS_ALIAS[w_low])
            else:
                replaced_words.append(w)
        teks_proses = " ".join(replaced_words)
        print(f"   Hasil: '{teks_proses}'")
        
        # PASS 3: Fuzzy matching untuk sisa kata
        print(f"\n3. Fuzzy Matching untuk kata yang belum ditemukan:")
        words = teks_proses.split()
        corrected_words = []
        i = 0
        while i < len(words):
            w_lower = words[i].lower()
            match_found = False
            # Cek status keywords typo (misal: lunwas → lunas)
            status_keywords = {"lunas", "hutang", "belum", "sudah", "setengah"}
            if w_lower not in ignore_words and len(w_lower) >=4 and not w_lower.isdigit():
                status_res = process.extractOne(w_lower, list(status_keywords), scorer=fuzz.ratio)
                if status_res and status_res[1] >=80:
                    print(f"   ✅ '{words[i]}' mirip dengan '{status_res[0]}' (similarity {status_res[1]:.1f}%)")
                    corrected_words.append(status_res[0])
                    i +=1
                    continue
            # Cek unigram fuzzy matching
            if len(words[i]) >=4 and not words[i].isdigit() and w_lower not in ignore_words:
                res_1 = process.extractOne(words[i], DAFTAR_KATA_KUNCI, scorer=fuzz.ratio)
                if res_1 and res_1[1] >=85:
                    terbaik_1 = res_1[0]
                    skor_1 = res_1[1]
                    if terbaik_1 in KAMUS_ALIAS:
                        print(f"   ✅ '{words[i]}' mirip dengan '{terbaik_1}' → '{KAMUS_ALIAS[terbaik_1]}' (similarity {skor_1:.1f}%)")
                        corrected_words.append(KAMUS_ALIAS[terbaik_1])
                    else:
                        print(f"   ✅ '{words[i]}' mirip dengan '{terbaik_1}' (similarity {skor_1:.1f}%)")
                        corrected_words.append(terbaik_1)
                    match_found = True
                    i +=1
                    continue
            if not match_found:
                corrected_words.append(words[i])
                i +=1
        teks_final = " ".join(corrected_words)
        print(f"\n4. Hasil akhir koreksi: '{teks_final}'")
    
    print("\n--- Bagian C: RINGKASAN HASIL KOREKSI SEMUA ENTRI ---")
    for i, entry in enumerate(entries, 1):
        teks_dikoreksi = koreksi_teks(entry)
        print(f"\nEntri {i}:")
        print(f"  Sebelum: '{entry}'")
        print(f"  Sesudah: '{teks_dikoreksi}'")


def langkah_7_entity_extraction():
    """Langkah 7: Ekstraksi entitas dengan Regex."""
    global hasil_ekstraksi_list
    hasil_ekstraksi_list = []
    
    print_separator("LANGKAH 7: Ekstraksi entitas dengan Regex")
    
    for i, entry in enumerate(entries, 1):
        teks_koreksi = koreksi_teks(entry)
        hasil_ekstraksi = ekstrak_entitas(teks_koreksi, teks_asli=entry)
        
        hasil_ekstraksi_list.append(hasil_ekstraksi)
        
        print(f"\n--- ENTITAS ENTRI {i} ---")
        print(f"\nEntitas yang diekstrak:")
        
        entitas = hasil_ekstraksi['entitas']
        for key, value in entitas.items():
            if value not in (None, False, []):
                print(f"  {key:20s} : {value}")


def langkah_8_context_inheritance_multi_entry():
    """Langkah 8: Context Inheritance & Penyusunan Data Transaksi."""
    print_separator("LANGKAH 8: Penyusunan Data Transaksi")
    print("\nLOGIKA:")
    print("1. Sistem mencari konteks (nama, tanggal) dari entri pertama yang memilikinya.")
    print("2. Lalu menerapkan ke entri lain yang KOSONG.")
    print("3. Jika TANGGAL tidak ada, sistem otomatis gunakan tanggal HARI INI!")
    print("4. Ini untuk kasus: satu pesanan, satu nama pembeli!")
    
    # Simulasi langkah demi langkah
    print("\n--- HASIL PENYUSUNAN DATA TRANSAKSI:")
    
    # 1. Buat list hasil sementara
    temp_results = []
    for i, entry in enumerate(entries, 1):
        teks_koreksi = koreksi_teks(entry)
        hasil_ekstraksi = ekstrak_entitas(teks_koreksi, teks_asli=entry)
        temp_results.append({
            "entitas": hasil_ekstraksi['entitas'],
            "original_text": entry
        })
    
    # 2. Terapkan _apply_multi_overrides
    final_results = _apply_multi_overrides(temp_results)
    
    # 3. Tambahkan tanggal hari ini secara otomatis
    from datetime import datetime
    today = datetime.now().strftime("%d-%m-%Y")
    for trans in final_results:
        if not trans["entitas"].get("TANGGAL"):
            trans["entitas"]["TANGGAL"] = today
    
    for i, trans in enumerate(final_results, 1):
        print(f"\n--- TRANSAKSI {i} ---")
        entitas = trans["entitas"]
        for key, value in entitas.items():
            if value not in (None, False, []):
                print(f"  {key:20s} : {value}")


def langkah_9_perhitungan_total_harga():
    """Langkah 9: Perhitungan Total Harga & Penanganan Data Kosong."""
    print_separator("LANGKAH 9: PERHITUNGAN TOTAL HARGA & PENANGANAN DATA KOSONG")
    
    print("\n--- LOGIKA PERHITUNGAN TOTAL ---")
    print("1. Cari harga satuan dari Master Data dengan fuzzy matching.")
    print("2. Skip barang dengan harga 0!")
    print("3. Jika satuan tidak cocok, gunakan satuan pertama yang tersedia untuk barang tersebut!")
    print("4. Hitung: Total = Jumlah × Harga Satuan.")
    print("5. Jika TANGGAL tidak ada, sistem otomatis gunakan tanggal HARI INI!")
    print("6. Jika status 'Hutang' → Metode Pembayaran tidak wajib!")
    
    # Dummy master data untuk demonstrasi (mirip master data asli!)
    dummy_master_barang = [
        {"nama": "Lolipop", "satuan": "pack", "harga": 15000},
        {"nama": "Lolipop", "satuan": "dus", "harga": 150000},
        {"nama": "meses", "satuan": "bks", "harga": 14000},
        {"nama": "meses", "satuan": "bungkus", "harga": 14000},
        {"nama": "Willo", "satuan": "dus", "harga": 504000}
    ]
    
    # Simulasi perhitungan
    temp_results = []
    for i, entry in enumerate(entries, 1):
        teks_koreksi = koreksi_teks(entry)
        hasil_ekstraksi = ekstrak_entitas(teks_koreksi, teks_asli=entry)
        temp_results.append({
            "entitas": hasil_ekstraksi['entitas'],
            "original_text": entry
        })
    
    final_results = _apply_multi_overrides(temp_results)
    
    # Tambahkan tanggal hari ini
    from datetime import datetime
    today = datetime.now().strftime("%d-%m-%Y")
    for trans in final_results:
        if not trans["entitas"].get("TANGGAL"):
            trans["entitas"]["TANGGAL"] = today
    
    print("\n--- HASIL PERHITUNGAN TOTAL:")
    for i, trans in enumerate(final_results, 1):
        ent = trans["entitas"]
        
        # Cari harga (mirip dengan cari_harga_default!)
        barang = ent.get("BARANG")
        satuan = ent.get("SATUAN")
        harga_satuan = None
        
        if barang:
            barang_lookup = barang.lower()
            
            # First try exact match nama + satuan
            for b in dummy_master_barang:
                if b["harga"] <= 0:
                    continue  # Skip barang dengan harga <= 0!
                if b["nama"].lower() == barang_lookup and b["satuan"].lower() == (satuan.lower() if satuan else ""):
                    harga_satuan = b["harga"]
                    break
            
            # If not found, try just nama
            if not harga_satuan:
                for b in dummy_master_barang:
                    if b["harga"] <= 0:
                        continue  # Skip barang dengan harga <= 0!
                    if b["nama"].lower() == barang_lookup:
                        harga_satuan = b["harga"]
                        break
        
        # Hitung total
        total = None
        if harga_satuan and ent.get("JUMLAH"):
            m_jml = re.search(r"\d+", str(ent["JUMLAH"]))
            if m_jml:
                jml_num = int(m_jml.group())
                total = jml_num * harga_satuan
                ent["TOTAL"] = format_rupiah(total)
                if harga_satuan:
                    ent["HARGA"] = format_rupiah(harga_satuan)
        
        # Tampilkan
        print(f"\nTRANSAKSI {i} - {barang}")
        print(f"  Tanggal       : {ent.get('TANGGAL')}")
        print(f"  Barang        : {barang}")
        print(f"  Jumlah        : {ent.get('JUMLAH')}")
        print(f"  Harga Satuan  : {format_rupiah(harga_satuan) if harga_satuan else '[KOSONG - tambahkan ke master data!]'}")
        print(f"  TOTAL         : {format_rupiah(total) if total else '[KOSONG]'}")
        print(f"  Status        : {ent.get('STATUS')}")
        if ent.get("STATUS") == "Hutang":
            print("  ⚠️ Metode Pembayaran tidak wajib karena status Hutang!")


def langkah_10_full_processing():
    """Langkah 10: Full Processing & Penyusunan Data Transaksi."""
    print_separator("LANGKAH 10: FULL PROCESSING & PENYUSUNAN DATA TRANSAKSI")
    print("(Data siap dikirim ke database!)")
    print("\nCATATAN: Demo ini tidak terhubung ke database, tapi logika sama persis!")
    
    hasil_lengkap = proses_nlp(INPUT_TEKS)
    
    # Tambahkan tanggal hari ini (seperti di sistem nyata!)
    from datetime import datetime
    today = datetime.now().strftime("%d-%m-%Y")
    for trans in hasil_lengkap:
        if not trans["entitas"].get("TANGGAL"):
            trans["entitas"]["TANGGAL"] = today
    
    print(f"\nInput: {INPUT_TEKS}")
    print(f"\nJumlah transaksi: {len(hasil_lengkap)}")
    
    for i, transaksi in enumerate(hasil_lengkap, 1):
        print(f"\n--- TRANSAKSI {i} ---")
        print(f"\n1. Intent: {transaksi['intent']}")
        print(f"\n2. Entitas:")
        for key, value in transaksi['entitas'].items():
            if value not in (None, False):
                print(f"   {key:20s} : {value}")
        # Check status
        if transaksi['entitas'].get('STATUS') == 'Hutang':
            print("\n   ⚠️ Metode Pembayaran tidak wajib karena status Hutang!")


def main():
    """Fungsi utama yang menjalankan semua langkah."""
    print("\n" + "="*80)
    print("  PANDUAN LENGKAP: ALUR PEMROSESAN DATA NLP")
    print("="*80)
    print("  [UNTUK LAPORAN - PENYUSUNAN DATA TRANSAKSI]")
    
    langkah_0_persiapan()
    langkah_1_input_data()
    langkah_2_pemisahan_multi_entry()
    langkah_3_text_cleaning()
    langkah_4_lowercase()
    langkah_5_tokenization()
    langkah_6_normalization_fuzzy_matching()
    langkah_7_entity_extraction()
    langkah_8_context_inheritance_multi_entry()
    langkah_9_perhitungan_total_harga()
    langkah_10_full_processing()
    
    print("\n" + "="*80)
    print("  [SELESAI] SEMUA LANGKAH SELESAI!")
    print("="*80)
    print("\nRingkasan Logika untuk Laporan:")
    print("1. Input → Teks mentah dari user.")
    print("2. Preprocessing → Cleaning, Lowercase, Tokenization, Normalization.")
    print("3. Fuzzy Matching → Koreksi typo dengan Levenshtein Distance & Similarity Score.")
    print("4. Entity Extraction → Ekstrak entitas dengan Regex.")
    print("5. Context Inheritance → Wariskan nama/tanggal ke entri lain (multi-entry satu pesanan).")
    print("6. Auto Tanggal → Jika TANGGAL kosong, sistem otomatis gunakan TANGGAL HARI INI!")
    print("7. Perhitungan Total → Total = Jumlah × Harga Satuan.")
    print("8. Master Data Lookup → Cari harga dari master data, skip barang dengan harga 0!")
    print("9. Flexibel Satuan → Jika satuan tidak cocok, gunakan satuan pertama yang tersedia!")
    print("10. Status Pembayaran → Jika 'Hutang' → Metode Pembayaran tidak wajib!")
    print("11. Data Transaksi → Data terstruktur siap database!")


if __name__ == "__main__":
    main()

