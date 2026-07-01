import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rapidfuzz import fuzz, process

from nlp.dictionaries import KAMUS_ALIAS
from nlp.normalizer import koreksi_teks

print("=== KAMUS_ALIAS for 'permen' ===")
print("'permen' in KAMUS_ALIAS?", 'permen' in KAMUS_ALIAS)
if 'permen' in KAMUS_ALIAS:
    print(f"Value: {KAMUS_ALIAS['permen']}")

print("\n=== Testing koreksi_teks('permen') ===")
result = koreksi_teks("permen")
print(f"Result: {result}")