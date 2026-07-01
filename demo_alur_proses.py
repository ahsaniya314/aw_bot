"""
Demonstrasi Alur Pemrosesan Data NLP
----------------------------------
Script ini menunjukkan bagaimana data diproses dari input mentah menjadi data terstruktur
"""

import os
import sys

# Fix encoding issue di Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tambahkan direktori proyek ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.dictionaries import KAMUS_ALIAS
from nlp.extractor import ekstrak_entitas
from nlp.normalizer import koreksi_teks
from nlp.processor import proses_nlp


def demonstrasi_proses(input_teks):
    print("=" * 80)
    print(f"INPUT ASLI:")
    print(f"  '{input_teks}'")
    print("=" * 80)
    print()

    # Langkah 1: Pemisahan Multi-Entry (jika ada)
    print("[1] LANGKAH 1: Pemisahan Multi-Entry")
    print("-" * 80)
    from nlp.processor import split_multi_entries
    entries = split_multi_entries(input_teks)
    print(f"Jumlah entri yang terdeteksi: {len(entries)}")
    for i, entry in enumerate(entries, 1):
        print(f"  Entri {i}: '{entry}'")
    print()

    # Langkah 2: Koreksi Teks (Fuzzy Matching)
    print("[2] LANGKAH 2: Koreksi Teks (Fuzzy Matching)")
    print("-" * 80)
    for i, entry in enumerate(entries, 1):
        koreksi = koreksi_teks(entry)
        print(f"Entri {i} asli   : '{entry}'")
        print(f"Entri {i} dikoreksi: '{koreksi}'")
        if entry != koreksi:
            print("  -> Perubahan terdeteksi!")
        print()

    # Langkah 3: Ekstraksi Entitas
    print("[3] LANGKAH 3: Ekstraksi Entitas (Regex & Rule-Based)")
    print("-" * 80)
    for i, entry in enumerate(entries, 1):
        koreksi = koreksi_teks(entry)
        hasil = ekstrak_entitas(koreksi, teks_asli=entry)
        print(f"\nEntri {i}:")
        for key, value in hasil["entitas"].items():
            if value is not None and value is not False:
                print(f"  {key:20s}: {value}")
    print()

    # Langkah 4: Full Processing (Proses Lengkap)
    print("[4] LANGKAH 4: Full Processing (Proses Lengkap & Post-Processing")
    print("-" * 80)
    hasil_lengkap = proses_nlp(input_teks)
    print(f"Jumlah transaksi terdeteksi: {len(hasil_lengkap)}")
    print()

    for i, transaksi in enumerate(hasil_lengkap, 1):
        print(f"\n[*] TRANSAKSI {i}:")
        print(f"  Intent       : {transaksi['intent']}")
        print(f"  Original Text: '{transaksi['original_text']}'")
        print(f"  Entitas:")
        for key, value in transaksi['entitas'].items():
            if value is not None and value is not False:
                print(f"    {key:20s}: {value}")

    print()
    print("=" * 80)
    return hasil_lengkap


if __name__ == "__main__":
    print("""
================================================================================
                       DEMO ALUR PEMROSESAN DATA NLP
================================================================================
  Alur Kerja:
  1. Input Data -> Teks mentah dari user
  2. Text Cleaning -> Normalisasi slang & typo
  3. Lowercase -> Konversi ke huruf kecil
  4. Tokenization -> Pisah menjadi kata-kata
  5. Fuzzy Matching -> Koreksi typo dengan Levenshtein Distance
  6. Ekstraksi Entitas -> Regex untuk nama barang, qty, harga, dll
  7. Penyusunan Data -> Strukturkan menjadi transaksi
  8. Simpan ke Database -> (Dalam contoh ini hanya ditampilkan
================================================================================
    """)

    # Contoh input
    contoh_input = [
        "hari ini pak andi pesan permen 10 dus lunas tunai",
        "pak budi order meses 5 dus, bulus 3 bungkus belum bayar",
        "tambah barang keripik 20 pack harga 15000",
        "laporan hari ini",
    ]

    for i, contoh in enumerate(contoh_input, 1):
        print(f"\n\n{'='*80}")
        print(f"CONTOH {i}")
        print(f"{'='*80}")
        demonstrasi_proses(contoh)
        print("\n" + "="*80 + "\n")

    print("\n💡 Silakan coba dengan input Anda sendiri!")
    print("Ketik 'selesai' untuk berhenti.\n")

    while True:
        try:
            user_input = input("Masukkan teks: ").strip()
            if user_input.lower() in ['selesai', 'exit', 'quit', 'q']:
                print("Terima kasih!")
                break
            if user_input:
                demonstrasi_proses(user_input)
        except KeyboardInterrupt:
            print("\nTerima kasih!")
            break
