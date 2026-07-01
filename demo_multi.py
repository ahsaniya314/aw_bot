"""
Demo Multiple Entry
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.processor import proses_nlp


def demo_multiple():
    contoh = "pak budi order meses 5 dus, bulus 3 bungkus belum bayar"

    print("="*60)
    print("DEMO MULTIPLE ENTRY")
    print("="*60)
    print(f"\nInput: {contoh}")

    print("\n" + "="*60)
    print("HASIL FULL PROCESSING")
    print("="*60)

    hasil = proses_nlp(contoh)

    print(f"\nJumlah transaksi: {len(hasil)}")

    for i, trans in enumerate(hasil, 1):
        print(f"\n--- TRANSAKSI {i} ---")
        print(f"Intent: {trans['intent']}")
        print("Entitas:")
        for key, val in trans['entitas'].items():
            if val not in (None, False):
                print(f"  {key:20}: {val}")


if __name__ == "__main__":
    demo_multiple()
