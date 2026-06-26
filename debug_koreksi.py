from nlp.normalizer import koreksi_teks
from nlp.dictionaries import KAMUS_ALIAS, DAFTAR_KATA_KUNCI
from rapidfuzz import process, fuzz

test_input1 = "mses 5 bks"
test_input2 = "will0 3 dus belum lunwas semua"
test_input3 = "prmen1 10 dus"

print("="*70)
print("DEBUG KOREKSI TEKS")
print("="*70)
print(f"\nKAMUS_ALIAS.keys()[:20]: {list(KAMUS_ALIAS.keys())[:20]}")
print(f"\nDAFTAR_KATA_KUNCI[:20]: {DAFTAR_KATA_KUNCI[:20]}")
print(f"\nApakah 'mses' di KAMUS_ALIAS?: {'mses' in KAMUS_ALIAS}")
print(f"KAMUS_ALIAS['mses'] = {KAMUS_ALIAS['mses']}")
print(f"\nApakah 'mses' di DAFTAR_KATA_KUNCI?: {'mses' in DAFTAR_KATA_KUNCI}")

print(f"\n{'='*70}")
print(f"Test koreksi('{test_input1}'): '{koreksi_teks(test_input1)}'")
print(f"Test koreksi('{test_input2}'): '{koreksi_teks(test_input2)}'")
print(f"Test koreksi('{test_input3}'): '{koreksi_teks(test_input3)}'")

# Test fuzzy ratio antara "mses" vs "meses"
print(f"\n{'='*70}")
print("FUZZY TEST:")
print(f"fuzz.ratio('mses', 'Meses') = {fuzz.ratio('mses', 'Meses')}")
print(f"process.extractOne('mses', DAFTAR_KATA_KUNCI, scorer=fuzz.ratio) = {process.extractOne('mses', DAFTAR_KATA_KUNCI, scorer=fuzz.ratio)}")
