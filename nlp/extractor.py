import logging
import re
from datetime import datetime, timedelta

from rapidfuzz import fuzz, process

from core.master_data import MASTER_BARANG_CATALOG, format_rupiah
from nlp.dictionaries import (
    DAFTAR_KATA_KUNCI,
    KAMUS_ALIAS,
    NORMALIZATION_DICT,
    VALID_UNITS,
    parse_price_shorthand,
)
from nlp.intent_matcher import (
    DATASET_TO_SYSTEM_INTENT,
    fuzzy_intent_fallback,
    match_intent_from_dataset,
    tentukan_intent_manual,
)

logger = logging.getLogger(__name__)

_MASTER_BARANG_UNITS = {
    "karton",
    "toples",
    "pouch",
    "pack",
    "bungkus",
    "keranjang",
    "pcs",
    "dus",
    "pak",
    "box",
    "buah",
    "botol",
    "kg",
    "lusin",
    "sachet",
    "kantong",
}
_TRANSAKSI_HINT_WORDS = {
    "ambil",
    "pesan",
    "beli",
    "order",
    "orderan",
    "catat",
    "pak",
    "bu",
    "mas",
    "mbak",
    "kak",
    "a.n",
    "atas nama",
    "lunas",
    "hutang",
    "utang",
    "dicicil",
    "cicil",
    "dp",
    "uang muka",
    "bayar",
    "tunai",
    "transfer",
    "qris",
}


def _clean_text_for_match(s):
    return re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())


def _detect_short_set_harga(teks_lower, daftar_barang):
    if not teks_lower:
        return None
    if any(
        w in teks_lower
        for w in ["tambah", "tambahkan", "tamhbahkan", "input", "bikin", "baru", "add"]
    ):
        return None
    if any(w in teks_lower for w in _TRANSAKSI_HINT_WORDS):
        return None

    known_products = []
    for b in daftar_barang or []:
        if b and isinstance(b, str):
            known_products.append(b)
    try:
        for g in MASTER_BARANG_CATALOG or []:
            for it in g.get("items") or []:
                nm = it.get("nama")
                if nm and isinstance(nm, str):
                    known_products.append(nm)
    except Exception:
        pass
    if not known_products:
        return None

    clean_text = _clean_text_for_match(teks_lower)
    barang_match = None
    for b in sorted(set(known_products), key=len, reverse=True):
        b_clean = _clean_text_for_match(b).strip()
        if b_clean and re.search(rf"\b{re.escape(b_clean)}\b", clean_text):
            barang_match = b
            break
        if b_clean and b_clean in clean_text:
            barang_match = b
            break

    if not barang_match:
        return None

    unit_match = None
    m_unit = re.search(
        r"\b(" + "|".join(sorted(_MASTER_BARANG_UNITS, key=len, reverse=True)) + r")\b", teks_lower
    )
    if m_unit:
        unit_match = m_unit.group(1).lower()
        if unit_match == "bks":
            unit_match = "bungkus"

    harga_candidates = []
    for m in re.finditer(
        r"(rp\.?\s*)?(\d[\d\.,]*)\s*(juta|jt|jutaan|ribu|rb|ribuan|k)?\b", teks_lower
    ):
        raw_full = (m.group(0) or "").strip()
        if not raw_full:
            continue
        raw_num = (m.group(2) or "").strip()
        suffix = (m.group(3) or "").strip()
        has_rp = bool(m.group(1))
        if not raw_num:
            continue
        val = parse_price_shorthand(raw_full)
        if val is None:
            continue
        digits_only = re.sub(r"[^\d]", "", raw_num)
        is_price_like = (
            has_rp
            or bool(suffix)
            or (digits_only and len(digits_only) >= 4)
            or ("=" in teks_lower)
            or ("harga" in teks_lower)
        )
        if is_price_like:
            harga_candidates.append((val, has_rp, bool(suffix), len(digits_only)))

    if not harga_candidates:
        return None

    harga_candidates.sort(key=lambda x: (x[1], x[2], x[3], x[0]), reverse=True)
    harga_val = harga_candidates[0][0]
    if harga_val <= 0:
        return None

    exists_in_master = False
    if daftar_barang:
        exists_in_master = any(
            str(x).strip().lower() == str(barang_match).strip().lower() for x in daftar_barang
        )

    return {
        "barang": barang_match.title() if isinstance(barang_match, str) else barang_match,
        "satuan": unit_match,
        "harga": str(harga_val),
        "exists_in_master": exists_in_master,
    }


def fuzzy_match_satuan(satuan_input):
    """
    Mencari satuan yang cocok secara fuzzy dari VALID_UNITS.
    Return satuan yang cocok atau None jika tidak ada yang cocok.
    """
    if not satuan_input:
        return None

    satuan_input_lower = satuan_input.lower()

    # Cari fuzzy match dengan skor minimal 80
    best_match = process.extractOne(
        satuan_input_lower, list(VALID_UNITS), scorer=fuzz.token_sort_ratio
    )

    if best_match and best_match[1] >= 80:
        return best_match[0]

    return None


# TODO: Ganti dengan HuggingFace Pipeline IndoBERT nanti di bagian ini.
def ekstrak_entitas(
    teks_koreksi, teks_asli="", db_metode=None, daftar_barang=None, mapping_metode=None
):
    """
    Mendeteksi entitas dari kalimat pengguna menggunakan rule-based dan Regex.
    Nantinya direplace oleh indobert token-classification.
    """
    hari_ini = datetime.now()

    # TAHAP 0: Slang Preprocessor — Normalisasi singkatan gaul SEBELUM analisis apapun
    bulan_dict = {
        "januari": "01",
        "jan": "01",
        "februari": "02",
        "feb": "02",
        "maret": "03",
        "mar": "03",
        "april": "04",
        "apr": "04",
        "mei": "05",
        "juni": "06",
        "jun": "06",
        "juli": "07",
        "jul": "07",
        "agustus": "08",
        "agu": "08",
        "agus": "08",
        "september": "09",
        "sep": "09",
        "oktober": "10",
        "okt": "10",
        "november": "11",
        "nov": "11",
        "nop": "11",
        "nopember": "11",
        "desember": "12",
        "des": "12",
    }
    slang_map = {
        r"\bdel\b": "hapus",
        r"\bilangin\b": "hapus",
        r"\bbuang\b": "hapus",
        r"\bbatalin\b": "hapus",
        r"\bapush\b": "hapus",
        r"\bkmn\b": "kemarin",
        r"\bkmarin\b": "kemarin",
        r"\bkmrin\b": "kemarin",
        r"\bkmaren\b": "kemarin",
        r"\bhri\b": "hari",
        r"\bhri ini\b": "hari ini",
        r"\bhari inj\b": "hari ini",
        r"\bh4ri\b": "hari",
        r"\bhr ini\b": "hari ini",
        r"\bhr ni\b": "hari ini",
        r"\bbsk\b": "besok",
        r"\bbsok\b": "besok",
        r"\bpk\b": "pak",
        r"\bbpk\b": "pak",
        r"\bp4k\b": "pak",
        r"\bdy\b": "dia",
        r"\bdya\b": "dia",
        r"\budh\b": "sudah",
        r"\bsdh\b": "sudah",
        r"\budah\b": "sudah",
        r"\bbyr\b": "bayar",
        r"\bbyar\b": "bayar",
        r"\bbyarnya\b": "bayar",
        r"\bnitip\b": "bayar",
        r"\bstngh\b": "setengah",
        r"\bstngah\b": "setengah",
        r"\bseparo\b": "setengah",
        r"\bpke\b": "pakai",
        r"\bpkai\b": "pakai",
        r"\btrnsfer\b": "transfer",
        r"\btrnsfr\b": "transfer",
        r"\btf\b": "transfer",
        r"\btranfer\b": "transfer",
        r"\btrf\b": "transfer",
        r"\bbln\b": "bulan",
        r"\bthn\b": "tahun",
        r"\btgl\b": "tanggal",
        r"\btmpilin\b": "tampilkan",
        r"\btampilin\b": "tampilkan",
        r"\btampilan\b": "tampilkan",
        r"\btampil\b": "tampilkan",
        r"\btmmpilin\b": "tampilkan",
        r"\bliat\b": "tampilkan",
        r"\bliatin\b": "tampilkan",
        r"\brincian\b": "tampilkan",
        r"\bksih tau\b": "tampilkan",
        r"\bkasih tau\b": "tampilkan",
        r"\bksih\b": "kasih",
        r"\bpesenan\b": "pesanan",
        r"\bpesnan\b": "pesanan",
        r"\bpesanannya\b": "pesanan",
        r"\bpsnn\b": "pesanan",
        r"\bpsnan\b": "pesanan",
        r"\bpesenane\b": "pesanan",
        r"\blunasin\b": "lunasi",
        r"\blunaskan\b": "lunasi",
        r"\bngelunasin\b": "lunasi",
        r"\blns\b": "lunas",
        r"\blnas\b": "lunas",
        r"\bnutup\b": "lunasi",
        r"\bkurangin tagihane\b": "lunasi",
        r"\byg\b": "yang",
        r"\bdgn\b": "dengan",
        r"\bsm\b": "sama",
        r"\bgk\b": "tidak",
        r"\bgak\b": "tidak",
        r"\bga\b": "tidak",
        r"\brb\b": "ribu",
        r"\bjt\b": "juta",
        r"\bbrg\b": "barang",
        r"\bprng\b": "barang",
        r"\bparang\b": "barang",
        r"\bitm\b": "item",
        r"\bprod\b": "produk",
        r"\bspa\b": "siapa",
        r"\bsapa\b": "siapa",
        r"\bsiapa aja\b": "siapa",
        r"\bsiapa saja\b": "siapa",
        r"\bbrp\b": "berapa",
        r"\bjml\b": "jumlah",
        r"\btotalan\b": "total",
        r"\bttal\b": "total",
        r"\bmasih nyicil\b": "nyicil",
        r"\bblom\b": "belum",
        r"\bblm\b": "belum",
        # --- Tambahan slang baru ---
        r"\bdicil\b": "dicicil",
        r"\bdicill\b": "dicicil",
        r"\bdicl\b": "dicicil",
        r"\bkasbon\b": "hutang dulu",
        r"\bkasbon2\b": "hutang dulu",
        r"\bbon dulu\b": "hutang dulu",
        r"\butang\b": "hutang",
        r"\butang dulu\b": "hutang dulu",
        r"\bhutan\b": "hutang",
        r"\bngutang\b": "hutang",
        r"\bnanti bayar\b": "bayarnya nanti",
        r"\bbayar nanti\b": "bayarnya nanti",
        r"\bum\b": "uang muka",
        r"\bpelunasan\b": "pelunasan",
        r"\btambah bayar\b": "tambahan bayar",
        r"\bbayar lagi\b": "tambahan bayar",
        r"\bbayar kekurangan\b": "tambahan bayar",
        r"\bkredit\b": "hutang",
        r"\bgopay\b": "go pay",
        r"\bspay\b": "shopeepay",
        # --- Mapping Karton & Shorthand ---
        r"\bctn\b": "karton",
        r"\betn\b": "karton",
        r"\bcrn\b": "karton",
        r"\bkrtn\b": "karton",
        r"\bkartun\b": "karton",
        r"\bkraton\b": "karton",
        r"\bkaton\b": "karton",
        r"\bkatron\b": "karton",
        r"\bkrton\b": "karton",
        r"\bkerton\b": "karton",
        r"\bkartom\b": "karton",
        r"\bbks\b": "bungkus",
        r"\btunai\b": "tunai",
        r"\bcash\b": "tunai",
        r"\bkontan\b": "tunai",
        r"\bcsh\b": "tunai",
        r"\b(?:di)?bayar langsung\b": "tunai",
        r"\blangsung\s+(?:di)?bayar\b": "tunai",
        r"\bganti harga\b": "update harga",
        r"\bubah harga\b": "update harga",
        r"\bedti\b": "edit",
        r"\bupdet\b": "update",
        r"\bupdt\b": "update",
        r"\bralat\b": "update",
        r"\btmbhin\b": "tambah",
        r"\bmasukin\b": "tambah",
        r"\bbikin\b": "tambah",
        r"\btmb\b": "tambah",
        r"\badd\b": "tambah",
        r"\btamhbahkan\b": "tambah",
        r"\btamhahkan\b": "tambah",
        r"\btambahin\b": "tambah",
        r"\bhr ini\b": "hari ini",
        r"\bhr ni\b": "hari ini",
        r"\blaproan\b": "laporan",
        r"\blapuran\b": "laporan",
        r"\blaporan\b": "laporan",
        r"\bmnggu ini\b": "minggu ini",
        r"\bplg gede\b": "paling banyak",
    }
    # Enrich slang_map with synonyms from normalization dict
    try:
        _synonyms = NORMALIZATION_DICT.get("synonyms", {})
        _existing_replacements = set(slang_map.values())
        # Map synonym group names to their normalized replacement word
        _group_to_replacement = {
            "aksi_tambah": "tambah",
            "aksi_tampilkan": "tampilkan",
            "aksi_hapus": "hapus",
            "aksi_edit": "edit",
            "aksi_cek": "cek",
            "status_lunas": "lunas",
            "status_belum_lunas": "belum lunas",
            "metode_cash": "tunai",
            "metode_transfer": "transfer",
        }
        for group_name, words_list in _synonyms.items():
            if isinstance(words_list, list):
                replacement = _group_to_replacement.get(group_name)
                if replacement:
                    for word in words_list:
                        pattern = rf"\b{re.escape(word)}\b"
                        if pattern not in slang_map:
                            slang_map[pattern] = replacement
    except Exception as e:
        logger.error(f"Error enriching slang_map: {e}")
    teks_prenorm = teks_koreksi.lower()
    # Handle leet speak angka yang sering jadi huruf
    teks_prenorm = (
        teks_prenorm.replace("5o", "50")
        .replace("4gus", "agus")
        .replace("0rder", "order")
        .replace("1lo", "110")
        .replace("3o", "30")
        .replace("10o", "100")
        .replace("t0t0k", "totok")
    )

    for pattern, replacement in slang_map.items():
        teks_prenorm = re.sub(pattern, replacement, teks_prenorm)

    hari_ini = datetime.now()
    teks_lower = teks_prenorm  # Untuk deteksi BARANG (sudah dikoreksi typo + slang)
    teks_asli_lower = (
        teks_asli or teks_koreksi
    ).lower()  # Untuk deteksi JUMLAH/HARGA (angka dari teks asli)

    # --- STEP 0: FUZZY FALLBACK CHECK ---
    # Jika input sangat mirip dengan contoh di dataset, ambil inspirasi dari situ
    dataset_hint = fuzzy_intent_fallback(teks_lower)

    entitas = {
        "TANGGAL": None,
        "NAMA": None,
        "AKSI": None,
        "BARANG": None,
        "JUMLAH": None,
        "HARGA": None,
        "SATUAN": None,
        "TOTAL": None,
        "STATUS": None,
        "NOMINAL_BAYAR": None,
        "METODE_PEMBAYARAN": None,
        "SEMUA": False,
        "KONTEKS_AGREGASI": None,
        "KONDISI": None,
    }

    # Jika ada hint dari dataset, kita bisa prioritaskan AKSI-nya
    if dataset_hint:
        intent = dataset_hint.get("intent", "")
        # Map dataset intent tags to system actions
        _mapped = DATASET_TO_SYSTEM_INTENT.get(intent, "")
        if _mapped in ("Catat_Penjualan_Lunas", "Catat_Penjualan_Cicil"):
            entitas["AKSI"] = "Tambah Penjualan"
        elif _mapped == "Pelunasan_Hutang":
            entitas["AKSI"] = "Catat Pelunasan"
        elif _mapped in (
            "Read_Analitik_Penjualan",
            "Read_Analitik_Hutang",
            "Read_Transaksi_Spesifik",
        ):
            entitas["AKSI"] = "Read Data"
        elif _mapped == "CRUD_Barang":
            if "tambah" in intent:
                entitas["AKSI"] = "Tambah Barang"
            elif "edit" in intent:
                entitas["AKSI"] = "Set Harga Barang"
            elif "hapus" in intent:
                entitas["AKSI"] = "Hapus Barang"
            else:
                entitas["AKSI"] = "Cek Harga Barang"
        elif _mapped == "Update_Delete_Transaksi":
            if "hapus" in intent:
                entitas["AKSI"] = "Delete Data"
            else:
                entitas["AKSI"] = "Update Status"
        elif _mapped == "Chit_Chat":
            entitas["AKSI"] = "Chit Chat"
        # Also handle legacy intent name format (backward compat)
        elif "Catat_Penjualan" in intent:
            entitas["AKSI"] = "Tambah Penjualan"
        elif "Pelunasan" in intent:
            entitas["AKSI"] = "Catat Pelunasan"
        elif "Read_Transaksi_Analitik" in intent:
            entitas["AKSI"] = "Read Data"
        elif "Read_Transaksi_Spesifik" in intent:
            entitas["AKSI"] = "Read Data"
        elif "Create_Barang" in intent:
            entitas["AKSI"] = "Tambah Barang"
        elif "Update_Barang" in intent:
            entitas["AKSI"] = "Set Harga Barang"
        elif "Delete_Barang" in intent:
            entitas["AKSI"] = "Hapus Barang"

        # Ekstrak entitas dari hint jika ada
        hint_entities = dataset_hint.get("entities", {})
        if hint_entities.get("nama_pelanggan"):
            entitas["NAMA"] = hint_entities["nama_pelanggan"].title()
        elif hint_entities.get("pelanggan"):
            entitas["NAMA"] = hint_entities["pelanggan"].title()
        if hint_entities.get("barang"):
            barang_hint = hint_entities["barang"].lower()
            if barang_hint in KAMUS_ALIAS:
                entitas["BARANG"] = KAMUS_ALIAS[barang_hint]
            else:
                entitas["BARANG"] = hint_entities["barang"].title()
        elif hint_entities.get("produk"):
            produk_hint = hint_entities["produk"].lower()
            if produk_hint in KAMUS_ALIAS:
                entitas["BARANG"] = KAMUS_ALIAS[produk_hint]
            else:
                entitas["BARANG"] = hint_entities["produk"].title()

    if "semua" in teks_lower or "seluruh" in teks_lower:
        entitas["SEMUA"] = True

    short_set = _detect_short_set_harga(teks_lower, daftar_barang)
    if (
        short_set
        and (not entitas.get("AKSI") or entitas.get("AKSI") == "Tambah Penjualan")
        and not entitas.get("NAMA")
    ):
        entitas["AKSI"] = (
            "Set Harga Barang" if short_set.get("exists_in_master") else "Tambah Barang"
        )
        entitas["BARANG"] = short_set["barang"]
        entitas["HARGA"] = short_set["harga"]
        if short_set.get("satuan"):
            entitas["SATUAN"] = short_set["satuan"]

    # A. Cari TANGGAL (Relative & Realtime Parse Mode)

    # 1. Deteksi X hari/minggu lalu / besok
    match_hari_lagi = re.search(
        r"(\d+)(?:\s*-\s*(\d+))?\s+(hari|minggu)\s+(yang\s+)?(besok|lagi|kedepan|ke depan)",
        teks_lower,
    )
    match_hari_lalu = re.search(
        r"(\d+)(?:\s*-\s*(\d+))?\s+(hari|minggu)\s+(yang\s+)?(kemarin|lalu)", teks_lower
    )

    # 2. Deteksi Nama Hari relatif
    match_nama_hari = re.search(
        r"(kemarin|besok|lalu|depan)\s+(?:hari\s+)?(senin|selasa|rabu|kamis|jumat|sabtu|minggu)|(?:hari\s+)?(senin|selasa|rabu|kamis|jumat|sabtu|minggu)\s+(kemarin|lalu|depan|besok)",
        teks_lower,
    )

    # 3. Prioritas (Kemarin > Hari Ini > Spesifik)
    if "kemarin" in teks_lower or "semalam" in teks_lower:
        entitas["TANGGAL"] = (hari_ini - timedelta(days=1)).strftime("%d-%m-%Y")
    elif match_hari_lalu:
        delta_val = int(
            match_hari_lalu.group(2) if match_hari_lalu.group(2) else match_hari_lalu.group(1)
        )
        unit = match_hari_lalu.group(3)
        if "minggu" in unit:
            delta_val *= 7
        entitas["TANGGAL"] = (hari_ini - timedelta(days=delta_val)).strftime("%d-%m-%Y")
    elif "hari ini" in teks_lower or "hari ni" in teks_lower or "tadi pagi" in teks_lower:
        entitas["TANGGAL"] = hari_ini.strftime("%d-%m-%Y")
    elif "besok" in teks_lower:
        entitas["TANGGAL"] = (hari_ini + timedelta(days=1)).strftime("%d-%m-%Y")
    elif match_hari_lagi:
        delta_val = int(
            match_hari_lagi.group(2) if match_hari_lagi.group(2) else match_hari_lagi.group(1)
        )
        unit = match_hari_lagi.group(3)
        if "minggu" in unit:
            delta_val *= 7
        entitas["TANGGAL"] = (hari_ini + timedelta(days=delta_val)).strftime("%d-%m-%Y")
    elif match_nama_hari:
        hari_dict = {
            "senin": 0,
            "selasa": 1,
            "rabu": 2,
            "kamis": 3,
            "jumat": 4,
            "sabtu": 5,
            "minggu": 6,
        }
        hari_terdeteksi = match_nama_hari.group(2) or match_nama_hari.group(3)
        modifier = match_nama_hari.group(1) or match_nama_hari.group(4)
        target_day = hari_dict[hari_terdeteksi]
        today_idx = hari_ini.weekday()

        if modifier in ["kemarin", "lalu"]:
            delta_days = (today_idx - target_day) % 7
            if delta_days == 0:
                delta_days = 7
            entitas["TANGGAL"] = (hari_ini - timedelta(days=delta_days)).strftime("%d-%m-%Y")
        elif modifier in ["besok", "depan"]:
            delta_days = (target_day - today_idx) % 7
            if delta_days == 0:
                delta_days = 7
            entitas["TANGGAL"] = (hari_ini + timedelta(days=delta_days)).strftime("%d-%m-%Y")
    elif "besok lusa" in teks_lower or "lusa" in teks_lower:
        entitas["TANGGAL"] = (hari_ini + timedelta(days=2)).strftime("%d-%m-%Y")
    elif "bulan lalu" in teks_lower:
        entitas["TANGGAL"] = (hari_ini - timedelta(days=30)).strftime("%d-%m-%Y")
    elif "bulan ini" in teks_lower:
        entitas["TANGGAL"] = hari_ini.strftime("%m-%Y")
    else:
        # Peningkatan Ekstraksi Tanggal Multi-Format
        bulan_pattern = "|".join(bulan_dict.keys())
        match_bulan_teks = re.search(
            rf"(\d{{1,2}})\s+({bulan_pattern})(?:\s+(\d{{2,4}}))?", teks_lower
        )
        match_tgl_full = re.search(r"\b(\d{1,2})[-/\s\.](\d{1,2})[-/\s\.](\d{2,4})\b", teks_lower)
        match_tgl_rapat = re.search(r"\b(\d{2})(\d{2})(20\d{2})\b", teks_lower)
        match_tgl_saja = re.search(r"\b(?:tanggal|tgl|tgl\.)\s+(\d{1,2})\b", teks_lower)

        if match_bulan_teks:
            d = int(match_bulan_teks.group(1))
            m = bulan_dict[match_bulan_teks.group(2)]
            y_str = match_bulan_teks.group(3)
            y = int(y_str) if y_str else hari_ini.year
            if y < 100:
                y += 2000
            entitas["TANGGAL"] = f"{d:02d}-{m}-{y}"
        elif match_tgl_full:
            d, m, y = (
                int(match_tgl_full.group(1)),
                int(match_tgl_full.group(2)),
                int(match_tgl_full.group(3)),
            )
            if y < 100:
                y += 2000
            entitas["TANGGAL"] = f"{d:02d}-{m:02d}-{y}"
        elif match_tgl_rapat:
            d, m, y = (
                int(match_tgl_rapat.group(1)),
                int(match_tgl_rapat.group(2)),
                int(match_tgl_rapat.group(3)),
            )
            entitas["TANGGAL"] = f"{d:02d}-{m:02d}-{y}"
        elif match_tgl_saja:
            d = int(match_tgl_saja.group(1))
            m, y = hari_ini.month, hari_ini.year
            if d > hari_ini.day:
                m -= 1
                if m == 0:
                    m = 12
                    y -= 1
            entitas["TANGGAL"] = f"{d:02d}-{m:02d}-{y}"

    if entitas.get("TANGGAL"):
        try:
            from core.master_data import normalisasi_tanggal_gs

            tgl_norm = normalisasi_tanggal_gs(entitas["TANGGAL"])
            if tgl_norm:
                entitas["TANGGAL"] = tgl_norm
        except Exception:
            pass

    # TAHAP 1: DETEKSI KONTEKS & AKSI (PRIORITAS TERTINGGI)
    # ═══════════════════════════════════════════════════════════

    # 1. Dashboard & Agregasi
    if any(
        k in teks_lower for k in ["dashboard", "laporan harian", "rekap harian", "ringkasan harian"]
    ):
        entitas["KONTEKS_AGREGASI"] = "Dashboard Harian"
        entitas["AKSI"] = "Read Data"
        entitas["SEMUA"] = True
        if not entitas["TANGGAL"]:
            entitas["TANGGAL"] = hari_ini.strftime("%d-%m-%Y")

    elif any(
        k in teks_lower
        for k in ["terbanyak", "paling banyak", "plg gede", "terbangak", "paking banyak"]
    ):
        if any(k in teks_lower for k in ["pembeli", "nama", "orang", "pelanggan"]):
            entitas["KONTEKS_AGREGASI"] = "Pembeli Terbanyak"
        elif any(k in teks_lower for k in ["tunggakan", "hutang", "nyicil", "debitur", "tagihan"]):
            entitas["KONTEKS_AGREGASI"] = "Tunggakan Terbanyak"
        else:
            entitas["KONTEKS_AGREGASI"] = "Total Transaksi"
        entitas["AKSI"] = "Read Data"
        entitas["SEMUA"] = True

    elif any(
        k in teks_lower
        for k in [
            "tagihan",
            "piutang",
            "tunggakan",
            "belum bayar",
            "sisa bayar",
            "kekurangan",
            "sisa tagihan",
            "total hutang",
            "berapa utang",
            "berapa tagihan",
        ]
    ):
        entitas["KONTEKS_AGREGASI"] = "Total Tunggakan"
        entitas["AKSI"] = "Read Data"
        # Jika kueri mengandung "pak/bu/mas" atau nama terdeteksi, biarkan SEMUA=False agar filter nama bekerja
        if "semua" in teks_lower or "siapa" in teks_lower:
            entitas["SEMUA"] = True
        elif entitas["NAMA"]:
            entitas["SEMUA"] = False

    elif any(k in teks_lower for k in ["omzet", "pendapatan", "pemasukan", "uang masuk"]):
        entitas["KONTEKS_AGREGASI"] = "Uang Masuk"
        entitas["AKSI"] = "Read Data"
        entitas["SEMUA"] = True

    elif "semua" in teks_lower and any(
        k in teks_lower for k in ["transaksi", "penjualan", "pesanan", "order", "data"]
    ):
        entitas["SEMUA"] = True
        entitas["AKSI"] = "Read Data"
        if "penjualan" in teks_lower or "transaksi" in teks_lower:
            entitas["KONTEKS_AGREGASI"] = "Total Transaksi"

    # 2. CRUD Master Data & Pelunasan & Analitik
    if any(
        k in teks_lower
        for k in ["set harga", "ubah harga", "ganti harga", "edit harga", "naikin jd"]
    ):
        entitas["AKSI"] = "Set Harga Barang"
    elif any(
        k in teks_lower
        for k in [
            "tambah barang",
            "barang baru",
            "tambah parang",
            "input barang",
            "input produk",
            "tambah produk",
            "tambah item",
            "add",
            "bikin master",
        ]
    ):
        entitas["AKSI"] = "Tambah Barang"
    elif any(
        k in teks_lower
        for k in [
            "hapus barang",
            "hapus data barang",
            "hapus produk",
            "buang barang",
            "delete barang",
            "hapus item",
            "delete item",
        ]
    ):
        entitas["AKSI"] = "Hapus Barang"
    elif any(
        k in teks_lower
        for k in [
            "cek harga",
            "lihat harga",
            "daftar harga",
            "cek hrg",
            "cek brg",
            "list barang",
            "daftar produk",
            "prc list",
            "brapaan",
        ]
    ):
        entitas["AKSI"] = "Cek Harga Barang"
    elif any(
        k in teks_koreksi.lower()
        for k in [
            "bayar hutang",
            "bayar utang",
            "bayar tagihan",
            "bayar sisa",
            "pelunasan",
            "lunasi",
            "bayar lunas tagihan",
            "sudah bayar lunas",
            "nutup utang",
            "lunasin",
        ]
    ):
        entitas["AKSI"] = "Catat Pelunasan"
    elif any(
        k in teks_lower
        for k in ["update", "edit", "perbaharui", "perbarui", "ubah", "revisi", "ganti", "ralat"]
    ):
        # Jika ada kata 'barang' atau 'produk', arahkan ke CRUD Master
        if any(k in teks_lower for k in ["barang", "produk", "item"]):
            entitas["AKSI"] = "Set Harga Barang"
        else:
            entitas["AKSI"] = "Update Status"
    elif any(
        k in teks_lower
        for k in [
            "tampilkan",
            "lihat",
            "baca",
            "cari",
            "cek",
            "rekap",
            "riwayat",
            "laporan",
            "tampilan",
            "tampil",
            "info",
            "kasih tau",
            "siapa",
            "sapa",
            "berapa",
        ]
    ):
        entitas["AKSI"] = "Read Data"

    # Jika sudah terdeteksi sebagai laporan/pelunasan, kita lanjut ke tahap ekstraksi pendukung
    # Jika BELUM, maka kemungkinan ini adalah input penjualan baru
    if not entitas["AKSI"]:
        if any(
            k in teks_lower
            for k in [
                "tambah",
                "input",
                "catat",
                "order",
                "orderan",
                "ordran",
                "beli",
                "pembelian",
                "ambil",
                "pesan",
                "pesanan",
            ]
        ):
            entitas["AKSI"] = "Tambah Penjualan"
        else:
            # Fallback jika ada nama barang + nama orang, asumsikan penjualan
            if any(k in teks_lower for k in DAFTAR_KATA_KUNCI) and len(teks_lower.split()) >= 2:
                entitas["AKSI"] = "Tambah Penjualan"

    # B. Cari NAMA Pintar
    ignore_for_name = {
        "siapa",
        "apa",
        "mana",
        "kapan",
        "berapa",
        "bagaimana",
        "kenapa",
        "saja",
        "aja",
        "ambil",
        "order",
        "pesan",
        "beli",
        "tambah",
        "masukkan",
        "catat",
        "baru",
        "bikin",
        "mesen",
        "pesen",
        "hapus",
        "delete",
        "buang",
        "remove",
        "menghapus",
        "batalkan",
        "cancel",
        "update",
        "edit",
        "ubah",
        "revisi",
        "ganti",
        "perbaharui",
        "perbarui",
        "mengatur",
        "setel",
        "setting",
        "pengaturan",
        "set",
        "atur",
        "bayar",
        "bayarnya",
        "dibayar",
        "dibayarkan",
        "membayar",
        "lunasi",
        "melunasi",
        "dilunasi",
        "lunasin",
        "lunasinnya",
        "lunas",
        "cicil",
        "dicicil",
        "nyicil",
        "nyicilnya",
        "mencicil",
        "mencicilnya",
        "cicilan",
        "dp",
        "ngutang",
        "hutang",
        "utang",
        "kasbon",
        "kredit",
        "hutan",
        "tagihan",
        "tagihannya",
        "belum",
        "sudah",
        "telah",
        "lunas",
        "lunasin",
        "sudah bayar",
        "tampilkan",
        "berikan",
        "lihat",
        "baca",
        "cari",
        "cek",
        "riwayat",
        "laporan",
        "rekap",
        "tampilan",
        "tampil",
        "data",
        "transaksi",
        "semua",
        "kasih",
        "info",
        "pesanan",
        "orderan",
        "nota",
        "bon",
        "struk",
        "pembayaran",
        "pelunasan",
        "cicilan",
        "piutang",
        "tunggakan",
        "tunggakannya",
        "sisa",
        "sisanya",
        "kekurangan",
        "kekurangannya",
        "uang",
        "muka",
        "separuh",
        "setengah",
        "setengahnya",
        "permen",
        "coklat",
        "millo",
        "cokelat",
        "prmen",
        "lolipop",
        "lalipop",
        "loli",
        "roti",
        "pia",
        "potong",
        "roda",
        "bulus",
        "bakpia",
        "pita",
        "brownis",
        "bronis",
        "brownies",
        "makanan",
        "serbuk",
        "mknan",
        "srbk",
        "meses",
        "meises",
        "mses",
        "mesis",
        "dus",
        "pcs",
        "kg",
        "pack",
        "bks",
        "buah",
        "botol",
        "karton",
        "bungkus",
        "toples",
        "renceng",
        "harga",
        "harganya",
        "rp",
        "rupiah",
        "total",
        "jadi",
        "jumlah",
        "satuan",
        "sebanyak",
        "sejumlah",
        "senilai",
        "sebesar",
        "sejumlah",
        "atas",
        "nama",
        "an",
        "hari",
        "ini",
        "besok",
        "kemarin",
        "lusa",
        "minggu",
        "bulan",
        "tahun",
        "tanggal",
        "tgl",
        "pagi",
        "siang",
        "sore",
        "malam",
        "sekarang",
        "kemudian",
        "nanti",
        "yang",
        "di",
        "ke",
        "dari",
        "buat",
        "untuk",
        "sama",
        "dengan",
        "dan",
        "atau",
        "tolong",
        "mohon",
        "coba",
        "dong",
        "ya",
        "lah",
        "pun",
        "naha",
        "secara",
        "langsung",
        "segera",
        "sebagian",
        "sepenuhnya",
        "seluruhnya",
        "otomatis",
        "manual",
        "via",
        "pakai",
        "pake",
        "ada",
        "tidak",
        "gak",
        "enggak",
        "nya",
        "punya",
        "kalo",
        "kalau",
        "bisa",
        "mau",
        "juga",
        "lagi",
        "saja",
        "aja",
        "sih",
        "kok",
        "deh",
        "kan",
        "pas",
        "tunai",
        "transfer",
        "cash",
        "qris",
        "bca",
        "bri",
        "mandiri",
        "gopay",
        "dana",
        "ovo",
        "shopeepay",
        "dia",
        "sedang",
        "diambil",
        "dipesan",
        "pre",
        "penjualan",
        "pembelian",
        "pengiriman",
        "catatan",
        "daftar",
        "list",
        "record",
        "toko",
        "barang",
        "produk",
        "item",
        "stok",
        "stock",
        "dashboard",
        "laporan",
        "ringkasan",
        "summary",
        "rekap",
        "paling",
        "banyak",
        "terbanyak",
        "teratas",
        "tertinggi",
        "pembeli",
        "pelanggan",
        "masih",
        "masuk",
        "pemasukan",
        "keluar",
        "omzet",
        "terbangak",
        "paking",
        "berpa",
        "brapaan",
        "siapa",
        "sapa",
        "laproan",
        "lapuran",
        "penjualan",
        "inj",
        "inih",
        "ini",
        "itu",
        "ituu",
        "tadi",
        "tadih",
        "pesan",
        "psn",
    }

    entitas["NAMA"] = None

    # 1. Deteksi Nama dengan Prefix (Prioritas Tinggi)
    match_prefix = re.search(
        r"(pak|bu|mas|mbak|kak|atas nama|a\.n\.?)\s+([a-z]+)(?:\s+([a-z]+))?", teks_lower
    )
    if match_prefix:
        gelar = match_prefix.group(1)
        kata1 = match_prefix.group(2)
        kata2 = match_prefix.group(3)
        nama_parts = [gelar]
        if kata1 and kata1 not in ignore_for_name:
            nama_parts.append(kata1)
            if kata2 and kata2 not in ignore_for_name:
                nama_parts.append(kata2)
        if len(nama_parts) > 1:
            entitas["NAMA"] = " ".join(nama_parts).title()

    # 2. Deteksi Nama Tanpa Prefix (Fallback)
    # Pengecualian diperluas: JANGAN cari nama jika intent adalah Laporan Global (tanpa nama orang)
    # Tapi TETAP cari nama jika intent adalah 'Read Data' untuk orang tertentu (misal: "tampilkan transaksi zio")
    if not entitas["NAMA"] and entitas["AKSI"] not in ["Cek Harga Barang"]:
        # Cek apakah ada kata kunci laporan global
        is_global_report = any(
            k in teks_lower
            for k in [
                "dashboard",
                "rekap harian",
                "ringkasan harian",
                "pembeli terbanyak",
                "tunggakan terbanyak",
                "siapa yang",
                "total",
                "berapa",
                "berpa",
                "semua data",
                "data penjualan",
                "semua penjualan",
            ]
        )

        if not is_global_report:
            # Hilangkan tanda baca agar tidak mengganggu ignore_for_name
            teks_bersih_nama = re.sub(r"[^\w\s]", "", teks_lower)
            words = teks_bersih_nama.split()
            nama_kandidat = []
            for w in words:
                # Cari kata pertama/kedua yang memenuhi kriteria nama:
                # - Bukan ignore word
                # - Bukan angka murni
                # - Panjang > 2
                # - Bukan bagian dari bulan
                # - Bukan shorthand harga (misal '100k', '5jt')
                # - Bukan bagian dari KAMUS_ALIAS (barang)
                if (
                    w not in ignore_for_name
                    and not w.isdigit()
                    and len(w) >= 3
                    and w not in bulan_dict
                    and not re.search(r"\d+[kjt]", w)
                    and not any(w.lower() == k.lower() for k in DAFTAR_KATA_KUNCI)
                ):
                    nama_kandidat.append(w)
                    if len(nama_kandidat) >= 2:
                        break

            if nama_kandidat:
                # Pastikan nama tidak mengandung kata status atau kuantitas yang mungkin lolos
                forbidden_name_words = [
                    "lunas",
                    "cicil",
                    "hutang",
                    "tunai",
                    "transfer",
                    "nyicil",
                    "mencicil",
                    "juta",
                    "jtan",
                    "jt",
                    "ribu",
                    "rb",
                    "rban",
                    "ratus",
                    "puluh",
                    "dus",
                    "pcs",
                    "toples",
                    "pack",
                    "bks",
                    "buah",
                    "botol",
                    "karton",
                    "ctn",
                    "etn",
                    "crn",
                    "krtn",
                    "kg",
                    "bal",
                    "butir",
                    "kantong",
                    "lusin",
                    "koli",
                    "roll",
                    "meter",
                    "lembar",
                    "box",
                    "bungkus",
                    "ambil",
                    "beli",
                    "order",
                    "pesan",
                    "catat",
                    "bayar",
                    "nominal",
                    "total",
                    "satuan",
                    "hari",
                    "ini",
                    "besok",
                    "kemarin",
                    "lusa",
                    "tanggal",
                    "tgl",
                ]
                nama_final = [n for n in nama_kandidat if n.lower() not in forbidden_name_words]
                if nama_final:
                    entitas["NAMA"] = " ".join(nama_final).title()

    # D. BARANG & SATUAN
    barang_posisi = -1

    def _is_generic_barang(nama_barang):
        nb = str(nama_barang or "").strip().lower()
        if "generik" in nb:
            return True
        return nb in {"permen", "serbuk", "roti pia", "roti/pia", "roti", "pia"}

    def _is_generic_barang_keyword(keyword):
        kk = str(keyword or "").strip().lower()
        return kk in {"permen", "roti", "pia", "serbuk"}

    # 1. PRIORITAS: Cek dari Master Data (Daftar Barang resmi)
    if daftar_barang:
        # Jika lebih dari satu barang muncul, pilih yang paling awal disebut (posisi terkecil),
        # lalu tie-break dengan panjang nama (lebih panjang menang).
        kandidat_master = []
        for b_name in set(daftar_barang):
            b_l = str(b_name).lower()
            pos = teks_lower.find(b_l)
            if pos != -1:
                kandidat_master.append((_is_generic_barang(b_name), pos, -len(b_l), b_name))

        # Jika tidak ada exact match, coba fuzzy match!
        if not kandidat_master:
            # Ambil semua kata dari teks yang mungkin nama barang
            kata_teks = [
                w
                for w in teks_lower.split()
                if len(w) >= 3 and w not in _MASTER_BARANG_UNITS and w not in _TRANSAKSI_HINT_WORDS
            ]
            if kata_teks:
                # Fuzzy match dengan daftar barang
                daftar_nama_barang = [b.lower() for b in set(daftar_barang)]
                for kata in kata_teks:
                    match = process.extractOne(
                        kata, daftar_nama_barang, scorer=fuzz.token_sort_ratio
                    )
                    if match and match[1] >= 80:  # Skor minimal 80
                        # Cari nama barang asli dari daftar_barang
                        nama_barang_asli = next(
                            (b for b in set(daftar_barang) if b.lower() == match[0]), None
                        )
                        if nama_barang_asli:
                            # Cari posisi kata di teks
                            pos = teks_lower.find(kata)
                            if pos != -1:
                                kandidat_master.append(
                                    (
                                        _is_generic_barang(nama_barang_asli),
                                        pos,
                                        -len(nama_barang_asli),
                                        nama_barang_asli,
                                    )
                                )

        if kandidat_master:
            kandidat_master.sort(key=lambda x: (x[0], x[1], x[2]))
            entitas["BARANG"] = kandidat_master[0][3]
            barang_posisi = kandidat_master[0][1]

        if entitas["BARANG"] and _is_generic_barang(entitas["BARANG"]):
            kandidat = []
            for kata_kunci in DAFTAR_KATA_KUNCI:
                if kata_kunci in teks_lower:
                    mapped = KAMUS_ALIAS.get(kata_kunci)
                    kandidat.append((kata_kunci, mapped))
            if kandidat:
                kandidat.sort(
                    key=lambda x: (
                        _is_generic_barang(x[1]),
                        teks_lower.find(x[0]),
                        -len(x[0]),
                    )
                )
                chosen_kw, chosen_val = kandidat[0]
                if chosen_val and not _is_generic_barang(chosen_val):
                    entitas["BARANG"] = chosen_val
                    barang_posisi = teks_lower.find(chosen_kw)

    # 2. FALLBACK: Cek dari Kamus Alias
    kandidat = []
    for kata_kunci in DAFTAR_KATA_KUNCI:
        if kata_kunci in teks_lower:
            mapped = KAMUS_ALIAS.get(kata_kunci)
            kandidat.append((kata_kunci, mapped))

    # Jika tidak ada exact match di KAMUS_ALIAS, coba fuzzy match dengan KAMUS_ALIAS!
    if not kandidat:
        # Ambil semua kata dari teks yang mungkin nama barang
        kata_teks = [
            w
            for w in teks_lower.split()
            if len(w) >= 3 and w not in _MASTER_BARANG_UNITS and w not in _TRANSAKSI_HINT_WORDS
        ]
        if kata_teks:
            daftar_kata_kunci = list(KAMUS_ALIAS.keys())
            for kata in kata_teks:
                match = process.extractOne(kata, daftar_kata_kunci, scorer=fuzz.token_sort_ratio)
                if match and match[1] >= 80:  # Skor minimal 80
                    kata_kunci = match[0]
                    mapped = KAMUS_ALIAS.get(kata_kunci)
                    if mapped:
                        pos = teks_lower.find(kata)
                        if pos != -1:
                            kandidat.append((kata_kunci, mapped))

    if kandidat:
        kandidat.sort(
            key=lambda x: (
                _is_generic_barang_keyword(x[0]),
                _is_generic_barang(x[1]),
                teks_lower.find(x[0]),
                -len(x[0]),
            )
        )
        chosen_kw, chosen_val = kandidat[0]
        if chosen_val:
            if (not entitas["BARANG"]) or (
                entitas["BARANG"]
                and _is_generic_barang(entitas["BARANG"])
                and not _is_generic_barang(chosen_val)
            ):
                entitas["BARANG"] = chosen_val
                barang_posisi = teks_lower.find(chosen_kw)

    teks_qty = teks_lower
    teks_qty = re.sub(r"\b(19\d{2}|20\d{2})\s+(pak|bu|mas|mbak|kak|ibu|bapak)\b", r"\2", teks_qty)

    # Cari angka + kata apapun (kemudian kita cek fuzzy match satuan)
    match_jumlah_satuan = re.search(
        r"(\d+)\s*([a-zA-Z]+)\b",
        teks_qty,
    )
    if match_jumlah_satuan:
        jumlah = match_jumlah_satuan.group(1)
        satuan_candidate = match_jumlah_satuan.group(2)

        # Coba fuzzy match satuan candidate dengan VALID_UNITS
        satuan_fuzzy = fuzzy_match_satuan(satuan_candidate)

        if satuan_fuzzy:
            satuan_detected = satuan_fuzzy
        else:
            satuan_detected = satuan_candidate

        # Standardize units for consistency
        if satuan_detected == "bks":
            satuan_detected = "bungkus"

        entitas["JUMLAH"] = f"{jumlah} {satuan_detected}"
        entitas["SATUAN"] = satuan_detected
    else:
        # Deteksi satuan tanpa angka di depannya (hanya untuk CRUD barang/aksi set harga/tambah barang)
        if entitas["AKSI"] in ["Tambah Barang", "Set Harga Barang"]:
            match_satuan_murni = re.search(r"\bsatuan\s*([a-zA-Z]+)\b", teks_lower)
            if match_satuan_murni:
                satuan_candidate = match_satuan_murni.group(1)

                # Coba fuzzy match satuan candidate dengan VALID_UNITS
                satuan_fuzzy = fuzzy_match_satuan(satuan_candidate)

                if satuan_fuzzy:
                    satuan_detected = satuan_fuzzy
                else:
                    satuan_detected = satuan_candidate

                if satuan_detected == "bks":
                    satuan_detected = "bungkus"

                entitas["SATUAN"] = satuan_detected

        # 2. Deteksi Jumlah dengan Awalan (misal: jumlah 10)
        match_jml_prefix = re.search(r"(?:sebanyak|jumlah|jml)\s*(\d+)", teks_qty)
        if match_jml_prefix:
            entitas["JUMLAH"] = match_jml_prefix.group(1)
        else:
            # 3. Deteksi Angka Murni setelah Nama Barang (misal: serbuk 100)
            if entitas["BARANG"]:
                # Cari angka yang muncul setelah posisi barang, maksimal terpaut 1-2 kata
                teks_setelah_barang = teks_lower[barang_posisi:].split()
                # teks_setelah_barang[0] adalah kata kunci barang itu sendiri
                for word in teks_setelah_barang[1:4]:  # Cek 3 kata setelahnya
                    if word.isdigit() and int(word) < 1000:
                        entitas["JUMLAH"] = word
                        break

            # 4. Fallback: Cari angka pertama yang bukan bagian dari tanggal/harga/tahun
            if not entitas["JUMLAH"]:
                # Ambil semua angka murni (bisa leet speak 5O -> 50)
                teks_jml = (
                    teks_qty.replace("5o", "50")
                    .replace("1lo", "110")
                    .replace("3o", "30")
                    .replace("10o", "100")
                )
                angka_murni = re.findall(r"\b\d+\b", teks_jml)
                for num in angka_murni:
                    # Abaikan jika itu tahun sekarang atau tahun depan/lalu
                    if num in [str(hari_ini.year), str(hari_ini.year - 1), str(hari_ini.year + 1)]:
                        continue
                    # Abaikan jika angka tersebut sudah terdeteksi di tanggal (DD-MM-YYYY)
                    if entitas["TANGGAL"] and num in entitas["TANGGAL"]:
                        continue
                    # Abaikan jika angka >= 1000 tanpa satuan karena kemungkinan besar itu adalah nominal uang/harga
                    if int(num) >= 1000:
                        continue
                    # Abaikan jika di depan angka tersebut ada kata "harga", "rp", "senilai", "sebesar", "nominal", "per"
                    pos = teks_jml.find(num)
                    pre_text = teks_jml[:pos].strip().split()
                    if pre_text and pre_text[-1] in [
                        "harga",
                        "rp",
                        "senilai",
                        "sebesar",
                        "nominal",
                        "per",
                        "satuan",
                    ]:
                        continue
                    entitas["JUMLAH"] = num
                    break

    # E. HARGA & TOTAL
    # Lebih fleksibel: Cari angka setelah kata kunci harga/total, meskipun ada kata barang di antaranya
    match_harga = re.search(
        r"(?:harga|satuan|per)\b.*?\b(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu|jutaan))?)\b",
        teks_asli_lower,
    )
    if match_harga:
        val = parse_price_shorthand(match_harga.group(1))
        if val:
            entitas["HARGA"] = format_rupiah(val)

    match_total = re.search(
        r"(?:total|jadi|bayar)\b.*?\b(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu|jutaan))?)\b",
        teks_asli_lower,
    )
    if match_total:
        val = parse_price_shorthand(match_total.group(1))
        if val:
            entitas["TOTAL"] = format_rupiah(val)

    # F. NOMINAL BAYAR (Extract first to help determine status)
    # Mendukung variasi 'cicil', 'mencicil', 'nyicil', 'dp', 'bayar', dll
    match_nom = re.search(
        r"(?:bayar|dp|cicil|dicil|mencicil|nyicil|nominal|sejumlah|sebesar|nominalnya|bayarnya|pembayaran)\b.*?\b(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu|jutaan))?)\b",
        teks_asli_lower,
    )
    if match_nom:
        val = parse_price_shorthand(match_nom.group(1))
        if val:
            entitas["NOMINAL_BAYAR"] = format_rupiah(val)

    # Deteksi kata kunci 'setengah' atau 'separuh' untuk nominal bayar (special logic)
    if any(k in teks_lower for k in ["setengah", "separuh"]):
        entitas["NOMINAL_BAYAR"] = "SETENGAH"  # Marker untuk kalkulasi nanti

    # G. STATUS — prioritaskan Hutang/Belum Lunas sebelum Lunas
    if any(
        k in teks_lower
        for k in [
            "cicil",
            "dicil",
            "nyicil",
            "dp",
            "uang muka",
            "separuh",
            "bayar dulu",
            "bayar tagihan",
            "bayar hutang",
            "pelunasan",
        ]
    ):
        entitas["STATUS"] = "Dicicil"
        match_nom = re.search(
            r"(?:bayar|dp|cicil|dicil|nominal|sejumlah|sebesar|pelunasan)\b.*?\b(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu|jutaan))?)\b",
            teks_asli_lower,
        )
        if match_nom:
            val = parse_price_shorthand(match_nom.group(1))
            if val:
                entitas["NOMINAL_BAYAR"] = format_rupiah(val)
    elif re.search(r"\bbelum\b", teks_lower) and re.search(r"\blunas\b", teks_lower):
        entitas["STATUS"] = "Hutang"
    elif any(
        k in teks_lower
        for k in [
            "hutang",
            "utang",
            "kasbon",
            "kredit",
            "bon dulu",
            "nanti bayar",
            "belum bayar",
            "belum lunas",
            "ngutang",
            "tunggakan",
            "piutang",
        ]
    ):
        entitas["STATUS"] = "Hutang"
    elif any(
        k in teks_lower
        for k in [
            "lunas",
            "dibayar lunas",
            "sudah bayar",
            "sudah lunas",
            "udah lunas",
            "udah bayar",
            "bayar penuh",
        ]
    ):
        entitas["STATUS"] = "Lunas"

    # Logic Fallback: Jika ada nominal bayar tapi status belum terdeteksi/Hutang, set ke Dicicil
    if entitas["NOMINAL_BAYAR"] and (not entitas["STATUS"] or entitas["STATUS"] == "Hutang"):
        entitas["STATUS"] = "Dicicil"

    # G. METODE PEMBAYARAN
    # 1. Cek dari mapping yang diberikan (Dinamis - Cache)
    if mapping_metode:
        for kw, nama_metode in mapping_metode.items():
            if kw in teks_lower:
                entitas["METODE_PEMBAYARAN"] = nama_metode
                break

    # 2. Jika tidak ada mapping tapi ada sheet (Legacy Support - Slow)
    elif db_metode:
        try:
            # Note: Sebaiknya gunakan mapping_metode untuk performa
            from core.master_data import muat_metode_keywords

            mapping_metode_tmp = muat_metode_keywords(db_metode)
            for kw, nama_metode in mapping_metode_tmp.items():
                if kw in teks_lower:
                    entitas["METODE_PEMBAYARAN"] = nama_metode
                    break
        except Exception:
            pass

    # 2. Fallback ke list standar (Statik) jika belum terdeteksi
    if not entitas["METODE_PEMBAYARAN"]:
        metode_list = [
            "tunai",
            "cash",
            "kontan",
            "transfer",
            "tf",
            "trf",
            "qris",
            "bca",
            "bri",
            "mandiri",
            "gopay",
            "dana",
            "ovo",
            "shopeepay",
        ]
        for m in metode_list:
            if m in teks_lower:
                # Normalisasi: "cash" dan "tunai" keduanya menjadi "Tunai"
                if m in ("tunai", "cash", "kontan"):
                    entitas["METODE_PEMBAYARAN"] = "Tunai"
                elif m in ("tf", "trf"):
                    entitas["METODE_PEMBAYARAN"] = "Transfer"
                else:
                    entitas["METODE_PEMBAYARAN"] = m.title()
                break

    # H. DETEKSI AKSI & KONTEKS (Berdasarkan Dataset & Rules)
    generic_price_lookup_match = re.search(
        r"\b(?:(?:cek|lihat|tampilkan|berapa)\s+)?harga\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    ) or re.search(
        r"\b(?:cek|lihat|tampilkan|berapa)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    generic_master_create_match = re.search(
        r"\b(?:tambah|input|masukkan|daftarkan|register|add)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    generic_master_delete_match = re.search(
        r"\bhapus(?:\s+data)?\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    generic_master_edit_match = re.search(
        r"\b(?:set|ganti|update|ubah|edit|perbaharui|perbarui)\s+(?:harga\s+)?(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    generic_status_update_match = re.search(
        r"\b(?:ganti|update|ubah|edit|perbaharui|perbarui)\s+status(?:\s+(?:pesanan|transaksi|order|orderan))?\b",
        teks_lower,
    )

    greetings = [
        r"\bhallo\b",
        r"\bhalo\b",
        r"\bassalamualaikum\b",
        r"\bwuy\b",
        r"\bpagi\b",
        r"\bsiang\b",
        r"\bsore\b",
        r"\bmalam\b",
        r"\bp\b",
        r"\bbot\b",
    ]
    if any(re.search(g, teks_lower) for g in greetings):
        entitas["AKSI"] = "Chit Chat"

    if generic_status_update_match and not generic_master_edit_match:
        entitas["AKSI"] = "Update Status"

    # Deteksi Read Data / Analitik
    if any(
        k in teks_lower
        for k in [
            "cek",
            "tampilkan",
            "tampilan",
            "berapa",
            "berpa",
            "brapaan",
            "siapa",
            "sapa",
            "lihat",
            "laporan",
            "laproan",
            "rekap",
            "dashboard",
            "dasbor",
        ]
    ):
        if any(k in teks_lower for k in ["harga", "barang", "produk"]):
            entitas["AKSI"] = "Cek Harga Barang"
            if (
                generic_price_lookup_match
                and not (generic_price_lookup_match.group(2) or "").strip()
            ):
                entitas["BARANG"] = None
                entitas["NAMA"] = None
        else:
            entitas["AKSI"] = "Read Data"

        # Selalu jalankan deteksi konteks jika AKSI adalah Read Data
        if entitas["AKSI"] == "Read Data":
            if any(k in teks_lower for k in ["nyicil", "cicil", "cicilan", "dp"]):
                entitas["STATUS"] = "Dicicil"
            elif any(
                k in teks_lower
                for k in ["hutang", "utang", "ngutang", "belum lunas", "tunggakan", "tagihan"]
            ):
                entitas["STATUS"] = "Hutang"

            if any(
                k in teks_lower for k in ["total", "jumlah", "ttal", "akumulasi", "berpa", "berapa"]
            ):
                if any(k in teks_lower for k in ["uang masuk", "pemasukan"]):
                    entitas["KONTEKS_AGREGASI"] = "Uang Masuk"
                elif any(
                    k in teks_lower
                    for k in ["tunggakan", "tagihan", "hutang", "piutang", "belum lunas"]
                ):
                    entitas["KONTEKS_AGREGASI"] = "Total Tunggakan"
                elif "cicilan" in teks_lower:
                    entitas["KONTEKS_AGREGASI"] = "Total Cicilan"
                else:
                    entitas["KONTEKS_AGREGASI"] = "Total Transaksi"
            elif any(
                k in teks_lower
                for k in [
                    "terbanyak",
                    "paling banyak",
                    "terbangak",
                    "paking banyak",
                    "paling gede",
                    "plg gede",
                ]
            ):
                if any(k in teks_lower for k in ["pembeli", "nama", "orang"]):
                    entitas["KONTEKS_AGREGASI"] = "Pembeli Terbanyak"
                elif any(
                    k in teks_lower for k in ["tunggakan", "hutang", "nyicil", "debitur", "tagihan"]
                ):
                    entitas["KONTEKS_AGREGASI"] = "Tunggakan Terbanyak"
                else:
                    entitas["KONTEKS_AGREGASI"] = "Total Transaksi"
            elif any(k in teks_lower for k in ["siapa", "sapa", "siapakah"]) and any(
                k in teks_lower
                for k in ["tunggakan", "hutang", "belum lunas", "ngutang", "piutang"]
            ):
                # Jika tanya "siapa yang ngutang", tampilkan daftar penunggak terbanyak/rekap debitur
                entitas["KONTEKS_AGREGASI"] = "Tunggakan Terbanyak"
                entitas["STATUS"] = "Hutang"
            elif any(k in teks_lower for k in ["siapa", "sapa", "siapakah"]) and any(
                k in teks_lower for k in ["lunas", "lunasin", "sudah bayar"]
            ):
                entitas["KONTEKS_AGREGASI"] = "Summary Lunas"
                entitas["STATUS"] = "Lunas"
            elif any(
                k in teks_lower
                for k in ["tunggakan", "tagihan", "piutang", "hutang", "belum lunas"]
            ):
                entitas["KONTEKS_AGREGASI"] = "Total Tunggakan"
                entitas["STATUS"] = "Hutang"
            elif "cash" in teks_lower or "tunai" in teks_lower or "langsung" in teks_lower:
                entitas["KONTEKS_AGREGASI"] = "Filter Cash"
            elif "transfer" in teks_lower or "tf" in teks_lower or "trf" in teks_lower:
                entitas["KONTEKS_AGREGASI"] = "Filter Transfer"

            # ✨ DASHBOARD CHECK: Jika user eksplisit minta dashboard atau laporan harian
            if any(
                k in teks_lower for k in ["dashboard", "dasbor", "laporan harian", "rekap hari ini"]
            ):
                entitas["KONTEKS_AGREGASI"] = "Dashboard Harian"

            # Hapus fallback rakus ke 'Dashboard Harian' di sini agar pencarian berdasarkan tanggal murni tetap menampilkan list data rinci
            pass

    elif "tambah" in teks_lower:
        if any(k in teks_lower for k in ["barang", "produk"]):
            entitas["AKSI"] = "Tambah Barang"
            if (
                generic_master_create_match
                and not (generic_master_create_match.group(2) or "").strip()
            ):
                entitas["BARANG"] = None
                entitas["NAMA"] = None
                entitas["HARGA"] = None
                entitas["SATUAN"] = None
    elif any(k in teks_lower for k in ["hapus", "delete", "batalin", "apush"]):
        explicit_master_tail = (
            (generic_master_delete_match.group(2) or "").strip()
            if generic_master_delete_match
            else ""
        )
        if entitas.get("NAMA") and str(entitas["NAMA"]).strip().lower() in {
            "saya",
            "aku",
            "kami",
            "kita",
            "gue",
            "gua",
        }:
            entitas["NAMA"] = None
        is_transaksi_ctx = (
            any(
                k in teks_lower
                for k in ["transaksi", "pesanan", "order", "orderan", "penjualan", "pembelian"]
            )
            or bool(entitas.get("TANGGAL"))
            or bool(entitas.get("NAMA"))
        )
        is_master_phrase = (
            bool(generic_master_delete_match)
            or (" master" in f" {teks_lower}")
            or (" daftar barang" in f" {teks_lower}")
            or (" list barang" in f" {teks_lower}")
        )
        if is_master_phrase and not is_transaksi_ctx:
            entitas["AKSI"] = "Hapus Barang"
            # Jangan pakai hint barang dari fuzzy dataset jika user hanya menulis
            # frasa generik seperti "hapus barang" tanpa menyebut produk spesifik.
            if not explicit_master_tail:
                entitas["BARANG"] = None
                entitas["NAMA"] = None
        else:
            entitas["AKSI"] = "Delete Data"
    elif any(k in teks_lower for k in ["ganti", "update", "ubah", "edit", "perbaharui"]):
        explicit_master_tail = (
            (generic_master_edit_match.group(2) or "").strip() if generic_master_edit_match else ""
        )
        is_transaksi_ctx = (
            any(
                k in teks_lower
                for k in ["transaksi", "pesanan", "order", "orderan", "penjualan", "pembelian"]
            )
            or any(k in teks_lower for k in ["lunas", "hutang", "dicicil", "cicil", "status"])
            or bool(entitas.get("TANGGAL"))
            or bool(entitas.get("NAMA"))
        )
        has_price_number = bool(re.search(r"\b\d{3,}\b", teks_lower))
        is_master_phrase = (
            ("harga" in teks_lower)
            or bool(generic_master_edit_match)
            or (bool(entitas.get("BARANG")) and has_price_number and not entitas.get("NAMA"))
        )
        if is_master_phrase and not is_transaksi_ctx:
            entitas["AKSI"] = "Set Harga Barang"
            if generic_master_edit_match and not explicit_master_tail:
                entitas["BARANG"] = None
                entitas["NAMA"] = None
                entitas["HARGA"] = None
        else:
            entitas["AKSI"] = "Update Status"

    elif any(
        k in teks_koreksi.lower()
        for k in [
            "bayar hutang",
            "bayar tagihan",
            "bayar cicilan",
            "bayar angsuran",
            "pelunasan",
            "nutup utang",
            "lunasin",
            "lunasi",
            "cicilan",
            "angsuran",
            "cicil",
            "dicicil",
            "mencicil",
            "nyicil",
        ]
    ):
        if not (
            entitas.get("BARANG")
            and entitas.get("JUMLAH")
            and "bayar" not in teks_koreksi.lower()
            and "pelunasan" not in teks_koreksi.lower()
        ):
            entitas["AKSI"] = "Catat Pelunasan"

    if entitas.get("AKSI") == "Read Data":
        has_transaksi_verb = any(
            k in teks_lower for k in ["ambil", "order", "pesan", "beli", "catat", "input"]
        )
        has_qty = bool(entitas.get("JUMLAH")) or bool(re.search(r"\b\d+\b", teks_lower))
        if has_transaksi_verb and entitas.get("BARANG") and has_qty:
            entitas["AKSI"] = "Tambah Penjualan"

    # Safeguard: frasa eksplisit update status transaksi jangan dibiarkan
    # tertimpa menjadi Read Data oleh hint/rule lain.
    if generic_status_update_match and not any(
        m
        for m in (
            generic_master_edit_match,
            generic_master_create_match,
            generic_master_delete_match,
            generic_price_lookup_match,
        )
    ):
        entitas["AKSI"] = "Update Status"

    if entitas.get("AKSI") == "Set Harga Barang" and not entitas.get("HARGA"):
        if entitas.get("TOTAL") and not entitas.get("JUMLAH"):
            entitas["HARGA"] = entitas["TOTAL"]
            entitas["TOTAL"] = None

    # Final guard untuk perintah generik agar hint dataset/rule lama
    # tidak mengisi entitas yang seharusnya kosong.
    final_price_lookup_match = re.search(
        r"\b(?:(?:cek|lihat|tampilkan|berapa)\s+)?harga\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    ) or re.search(
        r"\b(?:cek|lihat|tampilkan|berapa)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    final_master_create_match = re.search(
        r"\b(?:tambah|input|masukkan|daftarkan|register|add)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    final_master_delete_match = re.search(
        r"\bhapus(?:\s+data)?\s+(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    final_master_edit_match = re.search(
        r"\b(?:set|ganti|update|ubah|edit|perbaharui|perbarui)\s+(?:harga\s+)?(barang|produk|item)\b(?:\s+(.*))?$",
        teks_lower,
    )
    final_status_update_match = re.search(
        r"\b(?:ganti|update|ubah|edit|perbaharui|perbarui)\s+status(?:\s+(?:pesanan|transaksi|order|orderan))?\b",
        teks_lower,
    )

    if final_status_update_match and not final_master_edit_match:
        entitas["AKSI"] = "Update Status"
        entitas["BARANG"] = None
        entitas["HARGA"] = None
    elif final_master_edit_match and not (final_master_edit_match.group(2) or "").strip():
        entitas["AKSI"] = "Set Harga Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        entitas["HARGA"] = None
        entitas["SATUAN"] = None
    elif final_master_create_match and not (final_master_create_match.group(2) or "").strip():
        entitas["AKSI"] = "Tambah Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        entitas["HARGA"] = None
        entitas["SATUAN"] = None
    elif final_master_delete_match and not (final_master_delete_match.group(2) or "").strip():
        entitas["AKSI"] = "Hapus Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
    elif final_price_lookup_match and not (final_price_lookup_match.group(2) or "").strip():
        entitas["AKSI"] = "Cek Harga Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None

    # Safeguard pelunasan: jika nama + nominal bayar sudah terbaca dan
    # kalimat jelas berbunyi bayar hutang/tagihan, jangan biarkan AKSI kosong.
    has_pelunasan_phrase = any(
        k in teks_koreksi.lower()
        for k in [
            "bayar hutang",
            "bayar utang",
            "bayar tagihan",
            "bayar sisa",
            "pelunasan",
            "lunasi",
            "lunasin",
            "tambahan bayar",
            "bayar lagi",
        ]
    )
    if has_pelunasan_phrase and entitas.get("NAMA") and entitas.get("NOMINAL_BAYAR"):
        entitas["AKSI"] = "Catat Pelunasan"
        if not entitas.get("STATUS"):
            entitas["STATUS"] = "Dicicil"

    return {"entitas": entitas}


def tentukan_intent(entitas, teks_lower):
    """
    Menentukan intent berdasarkan entitas yang diekstrak dan teks input.
    Mencocokkan dengan kategori intent di dataset.json.
    """
    aksi = entitas.get("AKSI")
    konteks = entitas.get("KONTEKS_AGREGASI")

    ds_intent, ds_score = match_intent_from_dataset(teks_lower)
    if ds_intent and ds_score >= 85:
        allow = True
        if ds_intent in {
            "Read_Analitik_Penjualan",
            "Read_Analitik_Hutang",
            "Read_Transaksi_Spesifik",
        }:
            allow = aksi == "Read Data"
        elif ds_intent == "Chit_Chat":
            allow = aksi == "Chit Chat"
        elif ds_intent == "CRUD_Barang":
            allow = aksi in {
                "Tambah Barang",
                "Cek Harga Barang",
                "Set Harga Barang",
                "Hapus Barang",
            }
        elif ds_intent == "Pelunasan_Hutang":
            allow = aksi == "Catat Pelunasan"
        elif ds_intent == "Update_Delete_Transaksi":
            allow = aksi in {"Update Status", "Delete Data"}
        elif ds_intent in {"Catat_Penjualan_Lunas", "Catat_Penjualan_Cicil"}:
            allow = aksi == "Tambah Penjualan" or (entitas.get("BARANG") and entitas.get("NAMA"))
            # 🆕 Sesuaikan intent dengan STATUS yang ada (jika sudah di-override)
            if allow and entitas.get("STATUS"):
                if entitas["STATUS"] in ["Dicicil", "Hutang"]:
                    ds_intent = "Catat_Penjualan_Cicil"
                else:
                    ds_intent = "Catat_Penjualan_Lunas"

        if allow:
            return ds_intent

    if aksi == "Chit Chat":
        return "Chit_Chat"

    if aksi == "Tambah Barang":
        return "CRUD_Barang"

    if aksi == "Cek Harga Barang":
        return "CRUD_Barang"

    if aksi == "Set Harga Barang":
        return "CRUD_Barang"

    if aksi == "Hapus Barang":
        return "CRUD_Barang"

    if aksi == "Catat Pelunasan":
        return "Pelunasan_Hutang"

    if aksi == "Read Data":
        if konteks in ["Total Transaksi", "Uang Masuk", "Pembeli Terbanyak"]:
            return "Read_Analitik_Penjualan"
        if konteks in ["Total Tunggakan", "Total Cicilan", "Tunggakan Terbanyak"]:
            return "Read_Analitik_Hutang"
        return "Read_Transaksi_Spesifik"

    if aksi == "Update Status" or aksi == "Delete Data":
        return "Update_Delete_Transaksi"

    # Default: Catat Penjualan
    if entitas.get("BARANG") and entitas.get("NAMA"):
        if entitas.get("STATUS") in ["Dicicil", "Hutang"]:
            return "Catat_Penjualan_Cicil"
        return "Catat_Penjualan_Lunas"

    return "Unknown"
