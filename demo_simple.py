"""
Demonstrasi Alur Pemrosesan Data NLP - Versi Sederhana
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.extractor import ekstrak_entitas
from nlp.normalizer import koreksi_teks
from nlp.processor import proses_nlp, split_multi_entries


def print_separator(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_simple():
    # Contoh input
    contoh = "hari ini pak andi pesan permen 10 dus lunas tunai"

    print_separator("1. INPUT DATA")
    print(f"Input: {contoh}")

    print_separator("2. PEMISAHAN MULTI-ENTRY")
    entries = split_multi_entries(contoh)
    print(f"Jumlah entri: {len(entries)}")
    for i, e in enumerate(entries, 1):
        print(f"  {i}. {e}")

    print_separator("3. TEXT CLEANING & FUZZY MATCHING")
    for i, e in enumerate(entries, 1):
        cleaned = koreksi_teks(e)
        print(f"  Entri {i} asli  : {e}")
        print(f"  Entri {i} bersih: {cleaned}")

    print_separator("4. EKSTRAKSI ENTITAS")
    for i, e in enumerate(entries, 1):
        cleaned = koreksi_teks(e)
        result = ekstrak_entitas(cleaned, teks_asli=e)
        print(f"\n  Entri {i}:")
        for key, val in result["entitas"].items():
            if val not in (None, False):
                print(f"    {key:20}: {val}")

    print_separator("5. FULL PROCESSING")
    full_result = proses_nlp(contoh)
    print(f"Jumlah transaksi: {len(full_result)}")
    for i, trans in enumerate(full_result, 1):
        print(f"\n  Transaksi {i}:")
        print(f"    Intent: {trans['intent']}")
        print(f"    Entitas:")
        for key, val in trans["entitas"].items():
            if val not in (None, False):
                print(f"      {key:20}: {val}")

    print_separator("SELESAI")


if __name__ == "__main__":
    demo_simple()
