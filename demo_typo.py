"""
Demo Fuzzy Matching & Koreksi Typo
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.normalizer import koreksi_teks
from nlp.processor import proses_nlp


def demo_typo():
    # Contoh dengan typo
    contoh_dengan_typo = [
        "prmen 10 dus",
        "mses 5 bks",
        "willo 3 pack",
        "bronis 2 dus",
    ]

    print("="*60)
    print("DEMO FUZZY MATCHING & KOREKSI TYPO")
    print("="*60)

    for teks in contoh_dengan_typo:
        print(f"\n--- Input: '{teks}' ---")

        # Koreksi teks
        dikoreksi = koreksi_teks(teks)
        print(f"Koreksi: '{dikoreksi}'")

        if teks != dikoreksi:
            print("-> Perubahan terdeteksi!")

        # Full processing
        hasil = proses_nlp(teks)
        if hasil:
            print("\nHasil ekstraksi:")
            for trans in hasil:
                barang = trans['entitas'].get('BARANG', '-')
                jumlah = trans['entitas'].get('JUMLAH', '-')
                print(f"  Barang: {barang}")
                print(f"  Jumlah: {jumlah}")


if __name__ == "__main__":
    demo_typo()
