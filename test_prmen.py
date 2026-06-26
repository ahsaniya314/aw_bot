import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.normalizer import koreksi_teks
from nlp.dictionaries import KAMUS_ALIAS
from rapidfuzz import process, fuzz

print("=== KAMUS_ALIAS for 'prmen' ===")
print("'prmen' in KAMUS_ALIAS?", 'prmen' in KAMUS_ALIAS)
if 'prmen' in KAMUS_ALIAS:
    print(f"Value: {KAMUS_ALIAS['prmen']}")

print("\n=== Testing koreksi_teks('prmen') ===")
result = koreksi_teks("prmen")
print(f"Result: {result}")

print("\n=== Testing fuzzy match for 'prmen' in DAFTAR_KATA_KUNCI ===")
from nlp.dictionaries import DAFTAR_KATA_KUNCI
res = process.extractOne("prmen", DAFTAR_KATA_KUNCI, scorer=fuzz.ratio)
if res:
    print(f"Best match: {res[0]}, score: {res[1]}")
