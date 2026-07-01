import re

from rapidfuzz import fuzz, process

from nlp.dictionaries import DAFTAR_KATA_KUNCI, KAMUS_ALIAS, NORMALIZATION_DICT

_GENERIC_ALIAS_KEYWORDS = {"permen", "roti", "pia", "serbuk", "roti pia"}


def _preserve_generic_alias(keyword):
    return str(keyword or "").strip().lower() in _GENERIC_ALIAS_KEYWORDS


def koreksi_teks(teks_kotor, daftar_barang=None):
    """
    Memperbaiki logika Error Correction.
    TIDAK menghapus kata yang bukan merupakan item barang.
    Sistem akan mengecek per kata (atau kombinasi 2 kata beruntun)
    untuk mendeteksi dan mengganti teks yang typo menjadi item di KAMUS_BARANG.
    """
    # PASS 0: Preprocess - Tangani typo angka di akhir kata (misal: prmen1 → prmen, will0 → willo)
    # Hanya hapus angka 0 atau 1 yang menempel di kata (bukan angka penuh)
    teks_kotor = re.sub(r"(\b[a-zA-Z]+)([01])\b", r"\1", teks_kotor, flags=re.IGNORECASE)

    # PASS 1: Convert everything to lowercase first for consistent processing!
    teks_kotor = teks_kotor.lower()

    # PASS 2: Ganti angka 0 dengan o dan 1 dengan l di dalam kata (misal: will0 → willo)
    teks_kotor = re.sub(r"([a-zA-Z])0([a-zA-Z]*)", r"\1o\2", teks_kotor)
    teks_kotor = re.sub(r"([a-zA-Z])1([a-zA-Z]*)", r"\1l\2", teks_kotor)

    # PASS 3: Replace 0 and 1 in words
    words_pre = teks_kotor.split()
    normalized_words = []
    for w in words_pre:
        if not w.isdigit():
            w_normalized = w.replace("0", "o").replace("1", "l")
            normalized_words.append(w_normalized)
        else:
            normalized_words.append(w)
    teks_kotor = " ".join(normalized_words)

    # Kata-kata yang harus diabaikan dari normalisasi typo/abbreviation
    ignore_words = {
        "pak",
        "bu",
        "mas",
        "atas",
        "nama",
        "hari",
        "bulan",
        "tahun",
        "kemarin",
        "besok",
        "lusa",
        "minggu",
        "belum",
        "sudah",
        "semua",
        "setengah",
        "cicil",
        "transfer",
        "tunai",
        "cash",
        "dp",
        "kontan",
        "langsung",
        "lunas",
        "hutang",
        "utang",
        "bayar",
        "dibayar",
        "ngutang",
        "kasbon",
    }
    status_keywords = {"lunas", "hutang", "belum", "sudah", "setengah"}

    # Lindungi frasa status multi-kata agar tidak rusak oleh fuzzy/abbrev (mis: "belum lunas" → "belum sudah lunas")
    _status_phrase_placeholders = {}
    for idx, phrase in enumerate(
        ["belum lunas", "belum bayar", "belum dibayar", "sudah lunas", "sudah bayar"]
    ):
        token = f"__STATUSPHRASE{idx}__"
        if phrase in teks_kotor.lower():
            teks_kotor = re.sub(re.escape(phrase), token, teks_kotor, flags=re.IGNORECASE)
            _status_phrase_placeholders[token] = phrase

    # PASS 1.5: PRIORITAS KAMUS_ALIAS! Cek dulu apakah kata ada di KAMUS_ALIAS sebelum typo correction!
    words_pre = teks_kotor.split()
    replaced_words = []
    for w in words_pre:
        # Separate leading/trailing punctuation
        match = re.match(r"^([^\w]*)(\w+)([^\w]*)$", w)
        if not match:
            # If no word part, keep as is
            replaced_words.append(w)
            continue

        prefix, word_part, suffix = match.groups()
        w_low = word_part.lower()

        if w_low in ignore_words:
            replaced_words.append(w)
        elif w_low in KAMUS_ALIAS:
            replacement = w_low if _preserve_generic_alias(w_low) else KAMUS_ALIAS[w_low]
            replaced_words.append(f"{prefix}{replacement}{suffix}")
        else:
            replaced_words.append(w)
    teks_kotor = " ".join(replaced_words)

    # PASS 2: Direct word-replacement from normalization dict (typo_corrections + abbreviations)
    _typo_map = NORMALIZATION_DICT.get("typo_corrections", {})
    _abbr_map = NORMALIZATION_DICT.get("abbreviations", {})
    if _typo_map or _abbr_map:
        words_pre = teks_kotor.split()
        replaced_words = []
        for w in words_pre:
            # Separate leading/trailing punctuation
            match = re.match(r"^([^\w]*)(\w+)([^\w]*)$", w)
            if not match:
                # If no word part, keep as is
                replaced_words.append(w)
                continue

            prefix, word_part, suffix = match.groups()
            w_low = word_part.lower()

            # Jangan ganti kata yang sudah di-replace oleh KAMUS_ALIAS atau di ignore_words
            if w_low in ignore_words:
                replaced_words.append(w)
            # Jangan apply typo correction jika kata sudah merupakan key atau value di KAMUS_ALIAS
            elif w_low in [k.lower() for k in KAMUS_ALIAS.keys()] or w_low in [
                v.lower() for v in KAMUS_ALIAS.values()
            ]:
                replaced_words.append(w)
            elif w_low in _typo_map:
                replaced_words.append(f"{prefix}{_typo_map[w_low]}{suffix}")
            elif w_low in _abbr_map:
                replaced_words.append(f"{prefix}{_abbr_map[w_low]}{suffix}")
            else:
                replaced_words.append(w)
        teks_kotor = " ".join(replaced_words)

    # PASS 3: Fuzzy bigram/unigram matching (existing logic)
    words = teks_kotor.split()
    corrected_words = []

    i = 0
    while i < len(words):
        match_found = False
        w_lower = words[i].lower()

        # Gabungkan Kata Kunci: Kamus Alias + Daftar Barang Resmi
        keywords_target = DAFTAR_KATA_KUNCI
        if daftar_barang:
            keywords_target = list(set(DAFTAR_KATA_KUNCI + [b.lower() for b in daftar_barang]))

        # Cek apakah kata ini adalah status keyword typo (contoh: lunwas → lunas)
        if w_lower not in ignore_words and len(w_lower) >= 4 and not w_lower.isdigit():
            status_res = process.extractOne(w_lower, list(status_keywords), scorer=fuzz.ratio)
            if status_res and status_res[1] >= 80:
                corrected_words.append(status_res[0])
                i += 1
                continue

        # 1. Cek kombinasi 2 kata (Bigram) — HANYA jika kedua kata adalah teks (bukan angka)
        if i < len(words) - 1 and not words[i + 1].isdigit():
            phrase_2 = f"{words[i]} {words[i+1]}"
            if w_lower not in ignore_words and words[i + 1].lower() not in ignore_words:
                res_2 = process.extractOne(phrase_2, keywords_target, scorer=fuzz.ratio)
                if res_2:
                    terbaik_2, skor_2 = res_2[0], res_2[1]
                    if skor_2 >= 90:  # Threshold dinaikkan ke 90 agar tidak "menelan" kata tetangga
                        # Ambil nilai dari KAMUS_ALIAS jika ada!
                        if terbaik_2 in KAMUS_ALIAS:
                            corrected_words.append(
                                terbaik_2
                                if _preserve_generic_alias(terbaik_2)
                                else KAMUS_ALIAS[terbaik_2]
                            )
                        else:
                            corrected_words.append(terbaik_2)
                        i += 2
                        match_found = True
                        continue

        # 2. Cek kombinasi 1 kata (Unigram)
        if not match_found:
            phrase_1 = words[i]
            # Mencegah kata pendek, angka murni, dan stop words salah diprediksi
            if len(phrase_1) >= 4 and not phrase_1.isdigit() and w_lower not in ignore_words:
                res_1 = process.extractOne(phrase_1, keywords_target, scorer=fuzz.ratio)
                if res_1:
                    terbaik_1, skor_1 = res_1[0], res_1[1]
                    if skor_1 >= 85:
                        # Ambil nilai dari KAMUS_ALIAS jika ada!
                        if terbaik_1 in KAMUS_ALIAS:
                            corrected_words.append(
                                terbaik_1
                                if _preserve_generic_alias(terbaik_1)
                                else KAMUS_ALIAS[terbaik_1]
                            )
                        else:
                            corrected_words.append(terbaik_1)
                        i += 1
                        match_found = True
                        continue

        # 3. Jika tidak ada yang mirip, kembalikan (keep) kata aslinya
        if not match_found:
            corrected_words.append(words[i])
            i += 1

    teks_hasil = " ".join(corrected_words)
    for token, phrase in _status_phrase_placeholders.items():
        teks_hasil = teks_hasil.replace(token, phrase)
    return teks_hasil
