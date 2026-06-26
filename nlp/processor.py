import re
from datetime import datetime, timedelta
from core.master_data import format_rupiah
from nlp.dictionaries import KAMUS_ALIAS, parse_price_shorthand
from nlp.normalizer import koreksi_teks
from nlp.extractor import ekstrak_entitas, tentukan_intent

def split_multi_entries(text):
    """
    Memisahkan teks panjang menjadi beberapa entri transaksi.
    Mendukung pemisah: koma, titik koma, baris baru, dan kata 'dan'.
    Peningkatan: Mendeteksi perubahan tanggal sebagai pemisah baris baru.
    """
    if not text: return []
    
    # 1. Normalisasi: Ganti ' dan ' dengan pemisah hanya jika diikuti oleh kata penunjuk waktu
    text_norm = re.sub(r'\s+dan\s+(?=hari ini|kemarin|besok|tgl|tanggal|\d{1,2}/\d{1,2})', ' | ', text, flags=re.IGNORECASE)

    # 1b. Normalisasi: Jika user menempelkan akhir segmen + kata perintah tanpa spasi/pemisah,
    # sisipkan pemisah agar bisa diproses multi-entry.
    # Contoh: "satuan kartontamhbahkan produk ..." -> "satuan karton | tamhbahkan produk ..."
    unit_words = r'(?:karton|pouch|toples|pack|bungkus|dus|pcs|pak|box|kg)'
    action_words = r'(?:tambah|tamhbahkan|tambahkan|input|daftarkan|buat)'
    text_norm = re.sub(rf'({unit_words})(?={action_words}\b)', r'\1 | ', text_norm, flags=re.IGNORECASE)
    text_norm = re.sub(rf'({unit_words})\s*(?={action_words}\b)', r'\1 | ', text_norm, flags=re.IGNORECASE)
    
    # 2. Peningkatan: Sisipkan pemisah (|) SEBELUM pola tanggal DD/MM
    # Contoh: "meses 55, 28/11/2025" -> "meses 55 | 28/11/2025"
    text_norm = re.sub(r'(?<=[\w\d])\s*,\s*(\d{1,2}/\d{1,2})', r' | \1', text_norm)
    
    # 3. Split berdasarkan pemisah umum
    segments = re.split(r'[,;\n|]+', text_norm)
    
    cleaned = []
    current_date = None
    
    for s in segments:
        s = s.strip()
        if not s: continue
        
        # Cek apakah segmen ini mengandung tanggal baru (DD/MM/YYYY atau DD/MM)
        # Jika ya, update current_date untuk segmen-segmen berikutnya yang tidak punya tanggal
        date_match = re.search(r'(\d{1,2}/\d{1,2}(?:/\d{2,4})?)', s)
        if date_match:
            current_date = date_match.group(1)
            cleaned.append(s)
        else:
            # Jika segmen tidak punya tanggal, tapi kita punya current_date dari segmen sebelumnya
            if current_date and len(s) >= 3:
                # Tempelkan tanggal ke segmen ini agar extractor bisa membacanya
                cleaned.append(f"{current_date} {s}")
            elif len(s) >= 3:
                cleaned.append(s)
            
    if len(cleaned) <= 1:
        return [text.strip()]
        
    return cleaned

# ═══════════════════════════════════════════════════════════
# POST-PROCESSOR: MULTI-ORDER / MULTI-ITEM OVERRIDES
# ═══════════════════════════════════════════════════════════

_ORDER_VERBS = ("pesan", "ambil", "order", "beli", "mesen", "pesen", "catat")
_MONTHS_ID = (
    "januari", "februari", "maret", "april", "mei", "juni",
    "juli", "agustus", "september", "oktober", "november", "desember"
)

_PROD_VARIANTS = {
    "willo": ["willo", "wiilo", "wilo", "will"],
    "bembeng": ["bemmbeng", "bembeng", "bengbeng", "beng-beng", "beng beng"],
    "cholatos": ["cholatos"],
    "adangrow": ["adangrow"],
    "miksu": ["miksu"],
    "getbory": ["getbory"],
}

def _detect_method_from_text(text_lower):
    if not text_lower:
        return None
    if any(k in text_lower for k in ["transfer", "tf", "trf"]):
        return "Transfer"
    if any(k in text_lower for k in ["tunai", "cash", "kontan"]):
        return "Tunai"
    return None

def _is_new_order_segment(original_text, entitas):
    t = (original_text or "").lower()
    if not any(v in t for v in _ORDER_VERBS):
        return False
    if entitas.get("TANGGAL") and entitas.get("NAMA"):
        return True
    if re.search(r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b", t):
        return True
    if re.search(rf"\b\d{{1,2}}\s+(?:{'|'.join(_MONTHS_ID)})\s+\d{{2,4}}\b", t):
        return True
    return False

def _item_variants(barang_name):
    if not barang_name:
        return []
    b = str(barang_name).strip().lower()
    if b in _PROD_VARIANTS:
        return _PROD_VARIANTS[b]
    return [b]

def _match_item_in_modifier(item_ent, text_lower):
    barang = item_ent.get("BARANG")
    if not barang:
        return False
    variants = _item_variants(barang)
    # Cocokkan by nama barang, dan jika ada angka yang menempel ke nama barang tersebut, cocokkan juga jumlahnya.
    matched_variant = None
    for v in variants:
        if v and v in text_lower:
            matched_variant = v
            break
    if not matched_variant:
        return False

    # Jika ada pola "<barang> <angka>", anggap angka itu milik barang tsb
    m_num_after = re.search(rf"\b{re.escape(matched_variant)}\b\s*(\d+)\b", text_lower)
    if m_num_after:
        target_num = m_num_after.group(1)
        jml = str(item_ent.get("JUMLAH") or "")
        m = re.search(r"\d+", jml)
        if not m:
            return True
        return m.group(0) == target_num

    # Tidak ada angka yang spesifik untuk barang ini → match by barang saja
    return True

def _apply_multi_overrides(results):
    """
    Menangani:
    - Global override: 'semua sudah lunas pembayaran transfer', 'semua hutang'
    - Per-item override: 'bembeng sudah lunas tf', 'willo 180 dan bembeng lunas'
    - Multi-order dalam 1 pesan (di-reset saat segmen baru berisi tanggal+pesan)
    """
    if not results or len(results) <= 1:
        return results

    # Grouping berdasar segmen order baru
    groups = []
    cur = []
    for r in results:
        if _is_new_order_segment(r.get("original_text"), r.get("entitas", {})) and cur:
            groups.append(cur)
            cur = [r]
        else:
            cur.append(r)
    if cur:
        groups.append(cur)

    final_results = []

    for group in groups:
        # Kandidat item transaksi: harus punya BARANG dan JUMLAH
        items = [r for r in group if r.get("entitas", {}).get("BARANG") and r.get("entitas", {}).get("JUMLAH")]
        if not items:
            continue

        # Inheritance konteks per group (tanpa menyeberang antar transaksi)
        ctx_tgl = None
        ctx_nama = None
        for r in group:
            e = r.get("entitas", {}) or {}
            if not ctx_tgl and e.get("TANGGAL"):
                ctx_tgl = e.get("TANGGAL")
            if not ctx_nama and e.get("NAMA"):
                ctx_nama = e.get("NAMA")
            if ctx_tgl and ctx_nama:
                break
        if ctx_tgl or ctx_nama:
            for it in items:
                e_it = it.get("entitas", {})
                if ctx_tgl and not e_it.get("TANGGAL"):
                    e_it["TANGGAL"] = ctx_tgl
                if ctx_nama and not e_it.get("NAMA"):
                    e_it["NAMA"] = ctx_nama

        # Pre-fill METODE dari slang (tf/trf/cash) jika belum diisi extractor
        for r in group:
            t = (r.get("original_text") or "").lower()
            e = r.get("entitas", {})
            if not e.get("METODE_PEMBAYARAN"):
                m = _detect_method_from_text(t)
                if m:
                    e["METODE_PEMBAYARAN"] = m

        unit_re = r"(dus|pcs|toples|pack|bks|buah|botol|karton|kg|bungkus|renceng|bal|box|lusin|roll|sachet|pouch|butir|kantong|koli|lembar|meter|ikat|can|kaleng|gelas|cup|tablet|kapsul)"

        def _status_from_text(t):
            tl = (t or "").lower()
            if any(k in tl for k in ["cicil", "dicicil", "nyicil", "dp", "uang muka"]):
                if any(k in tl for k in ["setengah", "separuh", "separo"]):
                    return "Dicicil", 0.5
                return "Dicicil", None
            if re.search(r"\bbelum\b", tl) and re.search(r"\blunas\b", tl):
                return "Hutang", None
            if any(k in tl for k in ["hutang", "utang", "kasbon", "kredit", "belum lunas", "belum bayar", "ngutang"]):
                return "Hutang", None
            if any(k in tl for k in ["lunas", "dibayar", "sudah bayar", "sudah lunas", "udah lunas", "udah bayar"]):
                return "Lunas", None
            return None, None

        # Global override dari frasa 'semua ...' (sering muncul di suffix item terakhir)
        global_status = None
        global_method = None
        global_frac = None
        for r in group:
            full_t = (r.get("original_text") or "").lower()
            e = r.get("entitas", {})
            # 1. Prioritas: Jika entitas sudah punya SEMUA: True dan STATUS, gunakan itu!
            if e.get("SEMUA") and e.get("STATUS"):
                global_status = e.get("STATUS")
                if e.get("METODE_PEMBAYARAN"):
                    global_method = e.get("METODE_PEMBAYARAN")
                if e.get("_CICIL_FRACTION"):
                    global_frac = e.get("_CICIL_FRACTION")
            elif "semua" not in full_t:
                continue
            else:
                # Fallback: cek dari teks asli
                st, frac = _status_from_text(full_t)
                if st:
                    global_status = st
                    global_frac = frac
                m = e.get("METODE_PEMBAYARAN") or _detect_method_from_text(full_t)
                if m:
                    global_method = m
        
        # 🆕 Logika tambahan: Jika entri terakhir memiliki status dan semua entri sebelumnya tanpa status, 
        # jadikan status dari entri terakhir sebagai global_status!
        if not global_status and len(items) > 1:
            last_item = items[-1] if items else None
            if last_item:
                st_last, frac_last = _status_from_text(last_item.get("original_text") or "")
                # Cek apakah semua item sebelum terakhir tidak memiliki status
                all_no_status = True
                for it in items[:-1]:
                    if it["entitas"].get("STATUS"):
                        all_no_status = False
                        break
                if st_last and all_no_status:
                    global_status = st_last
                    global_frac = frac_last
                    # Ambil juga metode pembayaran jika ada di entri terakhir
                    m_last = last_item["entitas"].get("METODE_PEMBAYARAN") or _detect_method_from_text(last_item.get("original_text") or "")
                    if m_last:
                        global_method = m_last

        # Terapkan global terlebih dulu
        if global_status or global_method:
            for it in items:
                e_it = it["entitas"]
                if global_status:
                    e_it["STATUS"] = global_status
                    if global_status == "Dicicil" and global_frac:
                        e_it["_CICIL_FRACTION"] = global_frac
                        e_it["NOMINAL_BAYAR"] = "SETENGAH" if float(global_frac) == 0.5 else e_it.get("NOMINAL_BAYAR")
                if global_method and not e_it.get("METODE_PEMBAYARAN"):
                    e_it["METODE_PEMBAYARAN"] = global_method

        # Per-item override:
        # - segmen murni: "bembeng sudah lunas tf"
        # - suffix di segmen item terakhir: "... karton bembeng sudah lunas tf"
        consumed_modifiers = set()
        any_partial_override = False

        def _apply_override_text(override_text, status_override, frac_override, metode_override):
            nonlocal any_partial_override
            if not override_text:
                return
            applied_any = False
            for it in items:
                if _match_item_in_modifier(it["entitas"], override_text):
                    if status_override:
                        it["entitas"]["STATUS"] = status_override
                        if status_override == "Dicicil" and frac_override:
                            it["entitas"]["_CICIL_FRACTION"] = frac_override
                            it["entitas"]["NOMINAL_BAYAR"] = "SETENGAH" if float(frac_override) == 0.5 else it["entitas"].get("NOMINAL_BAYAR")
                    if metode_override:
                        it["entitas"]["METODE_PEMBAYARAN"] = metode_override
                    applied_any = True
            if applied_any:
                any_partial_override = True

        # 1) Modifier segmen murni (tanpa JUMLAH) → apply & buang
        for r in group:
            if r in items:
                continue
            t = (r.get("original_text") or "").lower().strip()
            if not t:
                continue
            if "semua" in t:
                st, frac = _status_from_text(t)
                if st:
                    global_status = st
                    global_frac = frac
                mtd = r.get("entitas", {}).get("METODE_PEMBAYARAN") or _detect_method_from_text(t)
                if mtd:
                    global_method = mtd
                consumed_modifiers.add(id(r))
                continue
            st, frac = _status_from_text(t)
            mtd = r.get("entitas", {}).get("METODE_PEMBAYARAN") or _detect_method_from_text(t)
            if st or mtd:
                _apply_override_text(t, st, frac, mtd)
                consumed_modifiers.add(id(r))

        # 2) Embedded override pada suffix item segmen (setelah pola JUMLAH+SATUAN pertama)
        for it in items:
            full_t = (it.get("original_text") or "").lower()
            m_js = re.search(rf"\b\d+\s*{unit_re}\b", full_t)
            if not m_js:
                continue
            prefix = full_t[:m_js.end()].strip()
            suffix = full_t[m_js.end():].strip()
            if not suffix:
                continue

            # Global override via suffix 'semua ...'
            if "semua" in suffix:
                st, frac = _status_from_text(suffix)
                if st:
                    global_status = st
                    global_frac = frac
                mtd = it["entitas"].get("METODE_PEMBAYARAN") or _detect_method_from_text(suffix)
                if mtd:
                    global_method = mtd
                continue

            st, frac = _status_from_text(suffix)
            mtd = it["entitas"].get("METODE_PEMBAYARAN") or _detect_method_from_text(suffix)
            if not (st or mtd):
                continue

            # Jika status/metode berasal dari suffix (prefix tidak memuat indikator), 
            # JANGAN terapkan ke item utama (karena suffix untuk meng-override item lain)
            # tapi JANGAN hapus status/metode yang sudah ada di item utama!
            # Hanya skip _apply_override_text untuk item utama itu sendiri!

            _apply_override_text(suffix, st, frac, mtd)

        # Re-apply global override bila ditemukan di suffix
        if global_status or global_method:
            for it in items:
                e_it = it["entitas"]
                if global_status:
                    e_it["STATUS"] = global_status
                    if global_status == "Dicicil" and global_frac:
                        e_it["_CICIL_FRACTION"] = global_frac
                        e_it["NOMINAL_BAYAR"] = "SETENGAH" if float(global_frac) == 0.5 else e_it.get("NOMINAL_BAYAR")
                if global_method and not e_it.get("METODE_PEMBAYARAN"):
                    e_it["METODE_PEMBAYARAN"] = global_method

        # Jika ada override parsial (sebagian item lunas), defaultkan item tanpa status menjadi Hutang
        if any_partial_override and not global_status:
            has_any_status = any(it["entitas"].get("STATUS") for it in items)
            if has_any_status:
                for it in items:
                    if not it["entitas"].get("STATUS"):
                        it["entitas"]["STATUS"] = "Hutang"

        # Jika item Lunas tapi metode kosong, default Tunai (kecuali ada indikasi transfer)
        for it in items:
            e_it = it["entitas"]
            st = str(e_it.get("STATUS") or "").strip().lower()
            if st == "lunas" and not e_it.get("METODE_PEMBAYARAN"):
                t = (it.get("original_text") or "").lower()
                e_it["METODE_PEMBAYARAN"] = _detect_method_from_text(t) or "Tunai"
        
        # 🔴 Hitung ulang INTENT untuk setiap item setelah semua override diterapkan!
        for it in items:
            e_it = it["entitas"]
            t = (it.get("original_text") or "").lower()
            new_intent = tentukan_intent(e_it, t)
            it["intent"] = new_intent

        # Simpan hanya items (buang segmen modifier murni)
        for r in group:
            if id(r) in consumed_modifiers:
                continue
            if r in items:
                final_results.append(r)
            else:
                # Global-only segment seperti "semua hutang" dibuang (tidak jadi transaksi)
                pass

    return final_results if final_results else results

# ═══════════════════════════════════════════════════════════
# MULTI-ITEM WITH MIXED PAYMENT STATUS PARSER
# ═══════════════════════════════════════════════════════════

# Keyword patterns yang memisahkan daftar barang dari daftar status
_STATUS_SEPARATOR_PATTERNS = [
    r'yang\s+(?:sudah|udah|sdh|udh|dah)\s+(?:lunas|dibayar|bayar)',
    r'yang\s+(?:belum|blm|blom)\s+(?:lunas|dibayar|bayar)',
    r'yang\s+(?:sudah|udah|sdh|udh|dah)\s+(?:di)?cicil',
    r'status\s+(?:bayar|pembayaran)\s*:?\s*',
    r'(?:keterangan|ket)\s+(?:bayar|pembayaran)\s*:?\s*',
]

# Pola status per item di bagian status section
_ITEM_STATUS_KEYWORDS = {
    "lunas": ["lunas", "sudah lunas", "sudah bayar", "udah lunas", "udah bayar", "dah bayar", "dah lunas", "dibayar lunas"],
    "dicicil": ["dicicil", "cicil", "nyicil", "mencicil", "dp", "uang muka", "dicicil setengah", "dicicil separuh", "cicil setengah", "bayar setengah", "bayar separuh", "bayar sebagian"],
    "hutang": ["belum bayar", "blm bayar", "belum lunas", "blm lunas", "hutang", "utang", "ngutang", "kasbon", "bon dulu", "belum dibayar"],
}

def _detect_item_in_text(segment, daftar_barang=None):
    """
    Mendeteksi nama barang dan jumlah+satuan dari segmen teks pendek.
    Return: (barang_name, jumlah, satuan) atau (None, None, None)
    """
    seg_lower = segment.lower().strip()
    
    detected_barang = None
    detected_jumlah = None
    detected_satuan = None
    
    # 1. Cek dari Master Data (Daftar Barang resmi)
    if daftar_barang:
        sorted_barang = sorted(daftar_barang, key=len, reverse=True)
        for b_name in sorted_barang:
            if b_name.lower() in seg_lower:
                detected_barang = b_name
                break
    
    # 2. Fallback ke KAMUS_ALIAS
    if not detected_barang:
        # Sort by length descending to match longer names first
        sorted_keys = sorted(KAMUS_ALIAS.keys(), key=len, reverse=True)
        for kw in sorted_keys:
            if kw in seg_lower:
                detected_barang = KAMUS_ALIAS[kw]
                break
    
    # 3. Deteksi jumlah + satuan
    match_js = re.search(r'(\d+)\s*(dus|pcs|toples|pack|bks|buah|botol|karton|kg|bungkus|renceng|bal|box|lusin|roll|sachet|pouch|butir|kantong|koli|lembar|meter|ikat|can|kaleng|gelas|cup|tablet|kapsul)\b', seg_lower)
    if match_js:
        detected_jumlah = match_js.group(1)
        detected_satuan = match_js.group(2)
    else:
        # Angka saja tanpa satuan
        match_num = re.search(r'(\d+)', seg_lower)
        if match_num:
            detected_jumlah = match_num.group(1)
    
    return detected_barang, detected_jumlah, detected_satuan

def _detect_status_in_segment(segment):
    """
    Mendeteksi status pembayaran dari segmen teks.
    Return: (status_str, nominal_cicil_fraction) 
    """
    seg_lower = segment.lower().strip()
    
    # Cek dicicil dulu (prioritas tinggi karena ada nominal info)
    for kw in _ITEM_STATUS_KEYWORDS["dicicil"]:
        if kw in seg_lower:
            # Cek apakah ada info setengah/separuh
            if any(k in seg_lower for k in ["setengah", "separuh", "separo", "stengah", "stngah"]):
                return "Dicicil", 0.5
            # Cek apakah ada info sepertiga/seperempat
            if any(k in seg_lower for k in ["sepertiga", "1/3"]):
                return "Dicicil", 1/3
            if any(k in seg_lower for k in ["seperempat", "1/4"]):
                return "Dicicil", 0.25
            return "Dicicil", None
    
    # Cek hutang
    for kw in _ITEM_STATUS_KEYWORDS["hutang"]:
        if kw in seg_lower:
            return "Hutang", None
    
    # Cek lunas
    for kw in _ITEM_STATUS_KEYWORDS["lunas"]:
        if kw in seg_lower:
            return "Lunas", None
    
    return None, None

def parse_multi_item_with_status(teks_user, daftar_barang=None):
    """
    Parser khusus untuk kalimat order multi-item dengan mixed payment status.
    
    Contoh input:
    "hari ini pak rudi pesan permen 30 dus, permen 30 bungkus, meses 30 dus, bulus 100 pack, brownis 100 pcs 
     yang sudah lunas permen 30 dus, meses, brownis, permen 30 bungkus dicicil setengah, bulus belum bayar"
    
    Return: list of dict [{barang, jumlah, satuan, status, cicil_fraction}] atau None jika tidak cocok pola ini
    """
    teks_lower = teks_user.lower().strip()
    
    # Pre-normalization: ubah slang umum supaya separator patterns bisa match
    _pre_norm = [
        (r'\byg\b', 'yang'), (r'\bsdh\b', 'sudah'), (r'\budh\b', 'sudah'),
        (r'\budah\b', 'sudah'), (r'\bdah\b', 'sudah'), (r'\bblm\b', 'belum'),
        (r'\bblom\b', 'belum'), (r'\bstengah\b', 'setengah'), (r'\bstngah\b', 'setengah'),
        (r'\bseparo\b', 'setengah'), (r'\bbyar\b', 'bayar'), (r'\bbyr\b', 'bayar'),
        (r'\bhri\b', 'hari'), (r'\bhr\b', 'hari'), (r'\bpesen\b', 'pesan'),
        (r'\bprmen\b', 'permen'), (r'\bbronis\b', 'brownis'), (r'\bbngkus\b', 'bungkus'),
        (r'\bmses\b', 'meses'), (r'\bmeises\b', 'meses'), (r'\bmesis\b', 'meses'),
        (r'\btopls\b', 'toples'),
    ]
    for pat, repl in _pre_norm:
        teks_lower = re.sub(pat, repl, teks_lower)
    
    # Step 0: Deteksi apakah input mengandung pola separator status
    separator_match = None
    separator_pattern_used = None
    for pat in _STATUS_SEPARATOR_PATTERNS:
        m = re.search(pat, teks_lower)
        if m:
            separator_match = m
            separator_pattern_used = pat
            break
    
    if not separator_match:
        return None  # Bukan pola multi-item dengan mixed status
    
    # Step 1: Split menjadi ORDER_SECTION dan STATUS_SECTION
    split_pos = separator_match.start()
    order_section = teks_lower[:split_pos].strip()
    status_section = teks_lower[separator_match.end():].strip()
    
    # Tentukan default status dari separator pattern
    default_status = "Lunas"  # default
    sep_text = separator_match.group(0).lower()
    if "belum" in sep_text or "blm" in sep_text or "blom" in sep_text:
        default_status = "Hutang"
    elif "cicil" in sep_text:
        default_status = "Dicicil"
    
    # Step 2: Ekstrak konteks (tanggal, nama) dari order_section
    # Cari nama pelanggan — stop capture sebelum kata kerja
    _action_words = {"pesan", "ambil", "order", "beli", "mesen", "pesen", "bawa", "mau", "catat"}
    nama_match = re.search(r'(?:pak|bu|mas|mbak|kak|ibu|bapak)\s+([a-z]+(?:\s+[a-z]+)?)', order_section)
    if nama_match:
        raw_name = nama_match.group(0)
        # Filter out action words from name
        name_parts = raw_name.split()
        cleaned_parts = []
        for p in name_parts:
            if p.lower() in _action_words:
                break
            cleaned_parts.append(p)
        nama_pelanggan = " ".join(cleaned_parts).title() if len(cleaned_parts) > 1 else None
    else:
        nama_pelanggan = None
    
    # Cari tanggal
    tanggal = None
    if "hari ini" in order_section or "hari ni" in order_section:
        tanggal = datetime.now().strftime("%d-%m-%Y")
    elif "kemarin" in order_section:
        tanggal = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
    elif "besok" in order_section:
        tanggal = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    
    # Step 3: Parse daftar barang dari order_section
    # Hapus konteks (tanggal, nama, kata kerja) dari order_section untuk mendapat list barang
    order_clean = order_section
    # Hapus prefix konteks sampai kata kerja terakhir
    verb_match = re.search(r'\b(pesan|ambil|order|beli|mesen|pesen|bawa)\b', order_clean)
    if verb_match:
        order_clean = order_clean[verb_match.end():].strip()
    
    # Split order items by comma
    order_items_raw = re.split(r'[,;]+', order_clean)
    order_items = []
    for item_text in order_items_raw:
        item_text = item_text.strip()
        if len(item_text) < 2:
            continue
        barang, jumlah, satuan = _detect_item_in_text(item_text, daftar_barang)
        if barang:
            order_items.append({
                "barang": barang,
                "jumlah": jumlah,
                "satuan": satuan,
                "status": None,  # Will be filled from status section
                "cicil_fraction": None,
                "raw_text": item_text
            })
    
    if not order_items:
        return None  # Tidak ada barang terdeteksi
    
    # Step 4: Parse status section — assign status per item
    status_segments = re.split(r'[,;]+', status_section)
    
    # Track which order items have been assigned a status
    assigned = [False] * len(order_items)
    
    for seg in status_segments:
        seg = seg.strip()
        if len(seg) < 2:
            continue
        
        # Detect item name in this status segment
        seg_barang, seg_jumlah, seg_satuan = _detect_item_in_text(seg, daftar_barang)
        
        # Detect status in this segment
        seg_status, seg_fraction = _detect_status_in_segment(seg)
        
        if not seg_status:
            # Jika tidak ada status eksplisit di segmen ini, gunakan default dari separator
            seg_status = default_status
        
        if seg_barang:
            # Match segmen status ke order item berdasarkan nama barang (dan satuan jika ada)
            for i, oi in enumerate(order_items):
                if assigned[i]:
                    continue
                # Cocokkan: barang harus sama, satuan jika ada harus sama
                if oi["barang"].lower() == seg_barang.lower():
                    if seg_satuan and oi["satuan"] and seg_satuan != oi["satuan"]:
                        continue  # Satuan berbeda, skip
                    if seg_jumlah and oi["jumlah"] and seg_jumlah != oi["jumlah"]:
                        continue  # Jumlah berbeda, skip (beda varian)
                    oi["status"] = seg_status
                    oi["cicil_fraction"] = seg_fraction
                    assigned[i] = True
                    break
        else:
            # Jika tidak ada barang terdeteksi tapi ada status (misal segmen hanya "belum bayar")
            # Ini mungkin merupakan status lanjutan, skip
            pass
    
    # Step 5: Assign default status ke item yang belum di-assign
    for i, oi in enumerate(order_items):
        if not assigned[i] or oi["status"] is None:
            oi["status"] = default_status
    
    # Step 6: Return parsed items beserta konteks
    return {
        "nama": nama_pelanggan,
        "tanggal": tanggal,
        "items": order_items
    }

def _apply_generic_command_guards(text, entitas):
    text_lower = (text or "").lower().strip()
    if not text_lower or not entitas:
        return entitas

    price_lookup_match = re.search(
        r"\b(?:(?:cek|lihat|tampilkan|berapa)\s+)?harga\s+(barang|produk|item)\b(?:\s+(.*))?$",
        text_lower,
    ) or re.search(
        r"\b(?:cek|lihat|tampilkan|berapa)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        text_lower,
    )
    master_create_match = re.search(
        r"\b(?:tambah|input|masukkan|daftarkan|register|add)\s+(barang|produk|item)\b(?:\s+(.*))?$",
        text_lower,
    )
    master_delete_match = re.search(
        r"\bhapus(?:\s+data)?\s+(barang|produk|item)\b(?:\s+(.*))?$",
        text_lower,
    )
    master_edit_match = re.search(
        r"\b(?:set|ganti|update|ubah|edit|perbaharui|perbarui)\s+(?:harga\s+)?(barang|produk|item)\b(?:\s+(.*))?$",
        text_lower,
    )
    status_update_match = re.search(
        r"\b(?:ganti|update|ubah|edit|perbaharui|perbarui)\s+status(?:\s+(?:pesanan|transaksi|order|orderan))?\b",
        text_lower,
    )

    if status_update_match and not master_edit_match:
        entitas["AKSI"] = "Update Status"
        entitas["BARANG"] = None
        entitas["HARGA"] = None
        return entitas

    if master_edit_match and not (master_edit_match.group(2) or "").strip():
        entitas["AKSI"] = "Set Harga Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        entitas["HARGA"] = None
        entitas["SATUAN"] = None
        return entitas

    if master_create_match and not (master_create_match.group(2) or "").strip():
        entitas["AKSI"] = "Tambah Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        entitas["HARGA"] = None
        entitas["SATUAN"] = None
        return entitas

    if master_delete_match and not (master_delete_match.group(2) or "").strip():
        entitas["AKSI"] = "Hapus Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        return entitas

    if price_lookup_match and not (price_lookup_match.group(2) or "").strip():
        entitas["AKSI"] = "Cek Harga Barang"
        entitas["BARANG"] = None
        entitas["NAMA"] = None
        return entitas

    return entitas

def proses_nlp(teks_user, db_metode=None, daftar_barang=None, mapping_metode=None, already_normalized=False):
    """
    Proses teks user (bisa multi-entry) dan mengembalikan LIST of results.
    """
    # ═══ STEP 0: Cek pola multi-item dengan mixed payment status ═══
    multi_parsed = parse_multi_item_with_status(teks_user, daftar_barang=daftar_barang)
    if multi_parsed and multi_parsed.get("items"):
        results = []
        for item in multi_parsed["items"]:
            entitas = {
                "TANGGAL": multi_parsed.get("tanggal"),
                "NAMA": multi_parsed.get("nama"),
                "AKSI": "Tambah Penjualan",
                "BARANG": item["barang"],
                "JUMLAH": f"{item['jumlah']} {item['satuan']}" if item.get("jumlah") and item.get("satuan") else item.get("jumlah"),
                "HARGA": None,
                "SATUAN": item.get("satuan"),
                "TOTAL": None,
                "STATUS": item.get("status", "Lunas"),
                "NOMINAL_BAYAR": None,
                "METODE_PEMBAYARAN": None,
                "SEMUA": False,
                "KONTEKS_AGREGASI": None,
                "KONDISI": None
            }
            
            # Handle cicil fraction (setengah = 50%)
            if item.get("cicil_fraction"):
                entitas["_CICIL_FRACTION"] = item["cicil_fraction"]
            
            intent = "Catat_Penjualan_Lunas" if entitas["STATUS"] == "Lunas" else "Catat_Penjualan_Cicil"
            
            results.append({
                "intent": intent,
                "entitas": entitas,
                "original_text": teks_user
            })
        
        if results:
            return results
    
    # ═══ STEP 1: Normal flow — split dan proses per entry ═══
    entries = split_multi_entries(teks_user)
    results = []
    
    for entry in entries:
        teks_koreksi = entry if already_normalized else koreksi_teks(entry, daftar_barang=daftar_barang)
        hasil = ekstrak_entitas(teks_koreksi, teks_asli=entry, db_metode=db_metode, daftar_barang=daftar_barang, mapping_metode=mapping_metode)
        entitas = _apply_generic_command_guards(entry, hasil["entitas"])
        entry_lower = entry.lower()

        # Safeguard pelunasan: beberapa nama tanpa gelar masih bisa lolos
        # dengan NAMA + NOMINAL_BAYAR terisi tetapi AKSI kosong.
        if (
            not entitas.get("AKSI")
            and entitas.get("NAMA")
            and entitas.get("NOMINAL_BAYAR")
            and any(
                k in entry_lower
                for k in [
                    "bayar hutang", "bayar utang", "bayar tagihan", "bayar sisa",
                    "bayar cicilan", "bayar angsuran",
                    "pelunasan", "lunasi", "lunasin", "tambahan bayar", "bayar lagi",
                    "cicilan", "angsuran", "cicil", "dicicil", "nyicil", "mencicil",
                ]
            )
        ):
            entitas["AKSI"] = "Catat Pelunasan"
            if not entitas.get("STATUS"):
                entitas["STATUS"] = "Dicicil"
        intent = tentukan_intent(entitas, entry_lower)
        
        # Validasi minimal untuk multi-entry agar tidak sampah
        if len(entries) > 1:
            # Jika aksi tidak terdeteksi dan tidak ada nama/barang, abaikan segmen ini
            if not entitas.get("AKSI") and not entitas.get("NAMA") and not entitas.get("BARANG") and not entitas.get("STATUS") and not entitas.get("METODE_PEMBAYARAN") and not entitas.get("SEMUA"):
                continue
                
        results.append({
            "intent": intent,
            "entitas": entitas,
            "original_text": entry
        })
    
    # Fallback jika pemisahan menghasilkan nol hasil yang valid
    if not results and teks_user.strip():
        teks_koreksi = teks_user if already_normalized else koreksi_teks(teks_user, daftar_barang=daftar_barang)
        hasil = ekstrak_entitas(teks_koreksi, teks_asli=teks_user, db_metode=db_metode, daftar_barang=daftar_barang)
        entitas = _apply_generic_command_guards(teks_user, hasil["entitas"])
        intent = tentukan_intent(entitas, teks_user.lower())
        results.append({
            "intent": intent,
            "entitas": entitas,
            "original_text": teks_user
        })
        
    # Post-process overrides untuk kasus kalimat panjang (semua lunas/hutang, override per-item)
    results = _apply_multi_overrides(results)
    return results

