import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re
from rapidfuzz import process, fuzz
from nlp.dictionaries import DAFTAR_KATA_KUNCI, NORMALIZATION_DICT, KAMUS_ALIAS

ignore_words = {
    "pak", "bu", "mas", "atas", "nama", "hari", "bulan", "tahun", "kemarin", "besok", "lusa", "minggu",
    "belum", "sudah", "semua", "setengah", "cicil", "transfer", "tunai", "cash", "dp", "kontan", "langsung",
    "lunas", "hutang", "utang", "bayar", "dibayar", "ngutang", "kasbon",
}
status_keywords = {"lunas", "hutang", "belum", "sudah", "setengah"}


def debug_koreksi_teks(teks_kotor):
    print(f"\n=== START DEBUG: '{teks_kotor}' ===")

    # PASS 0
    teks_kotor = re.sub(r'(\b[a-zA-Z]+)([01])\b', r'\1', teks_kotor, flags=re.IGNORECASE)
    teks_kotor = re.sub(r'([a-zA-Z])0([a-zA-Z]*)', r'\1o\2', teks_kotor, flags=re.IGNORECASE)
    teks_kotor = re.sub(r'([a-zA-Z])1([a-zA-Z]*)', r'\1l\2', teks_kotor, flags=re.IGNORECASE)
    print(f"After PASS 0: '{teks_kotor}'")

    # PASS 1
    words_pre = teks_kotor.split()
    normalized_words = []
    for w in words_pre:
        w_low = w.lower()
        if not w.isdigit():
            w_normalized = w_low.replace('0', 'o').replace('1', 'l')
            normalized_words.append(w_normalized)
        else:
            normalized_words.append(w)
    teks_kotor = " ".join(normalized_words)
    print(f"After PASS 1: '{teks_kotor}'")

    # PASS 2
    _typo_map = NORMALIZATION_DICT.get("typo_corrections", {})
    _abbr_map = NORMALIZATION_DICT.get("abbreviations", {})
    if _typo_map or _abbr_map:
        words_pre = teks_kotor.split()
        replaced_words = []
        for w in words_pre:
            w_low = w.lower()
            if w_low in ignore_words:
                replaced_words.append(w)
            elif w_low in _typo_map:
                replaced_words.append(_typo_map[w_low])
            elif w_low in _abbr_map:
                replaced_words.append(_abbr_map[w_low])
            else:
                replaced_words.append(w)
        teks_kotor = " ".join(replaced_words)
    print(f"After PASS 2: '{teks_kotor}'")

    # PASS 3: Fuzzy bigram/unigram matching
    words = teks_kotor.split()
    corrected_words = []
    i = 0
    while i < len(words):
        print(f"\nPASS 3: i = {i}, word = '{words[i]}'")
        match_found = False
        w_lower = words[i].lower()
        print(f"  w_lower: '{w_lower}'")
        print(f"  '{w_lower}' in KAMUS_ALIAS? {w_lower in KAMUS_ALIAS}")
        if w_lower in KAMUS_ALIAS:
            print(f"  Value: {KAMUS_ALIAS[w_lower]}")

        keywords_target = DAFTAR_KATA_KUNCI
        print(f"  Number of keywords: {len(keywords_target)}")

        # Status check
        if w_lower not in ignore_words and len(w_lower) >= 4 and not w_lower.isdigit():
            status_res = process.extractOne(w_lower, list(status_keywords), scorer=fuzz.ratio)
            if status_res and status_res[1] >= 80:
                print(f"  Status match: {status_res}")
                corrected_words.append(status_res[0])
                i += 1
                continue

        # Bigram check
        if i < len(words) - 1 and not words[i+1].isdigit():
            phrase_2 = f"{words[i]} {words[i+1]}"
            if w_lower not in ignore_words and words[i+1].lower() not in ignore_words:
                print(f"  Checking bigram: '{phrase_2}'")
                res_2 = process.extractOne(phrase_2, keywords_target, scorer=fuzz.ratio)
                if res_2:
                    terbaik_2, skor_2 = res_2[0], res_2[1]
                    print(f"  Bigram result: {terbaik_2} ({skor_2})")
                    if skor_2 >= 90:
                        if terbaik_2 in KAMUS_ALIAS:
                            corrected_words.append(KAMUS_ALIAS[terbaik_2])
                        else:
                            corrected_words.append(terbaik_2)
                        i += 2
                        match_found = True
                        continue

        # Unigram check
        if not match_found:
            phrase_1 = words[i]
            print(f"  Checking unigram: '{phrase_1}'")
            if len(phrase_1) >= 4 and not phrase_1.isdigit() and w_lower not in ignore_words:
                res_1 = process.extractOne(phrase_1, keywords_target, scorer=fuzz.ratio)
                if res_1:
                    terbaik_1, skor_1 = res_1[0], res_1[1]
                    print(f"  Unigram result: {terbaik_1} ({skor_1})")
                    if skor_1 >= 85:
                        if terbaik_1 in KAMUS_ALIAS:
                            print(f"  Taking KAMUS_ALIAS value: {KAMUS_ALIAS[terbaik_1]}")
                            corrected_words.append(KAMUS_ALIAS[terbaik_1])
                        else:
                            corrected_words.append(terbaik_1)
                        i += 1
                        match_found = True
                        continue

        if not match_found:
            corrected_words.append(words[i])
            i += 1

    teks_hasil = " ".join(corrected_words)
    print(f"\n=== END DEBUG: Result = '{teks_hasil}' ===")
    return teks_hasil


debug_koreksi_teks("prmen")
