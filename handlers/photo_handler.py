"""
Photo Handler — OCR processing (simplified: only show extracted text)
"""
import os
import logging
import html
import re
from datetime import datetime
from time import perf_counter

from rapidfuzz import process, fuzz

from core.bot_context import ctx
from utils.security import authorized_only, safe_edit_message, sanitize_input, log_exception, notify_admins
from utils.helpers import cocokkan_nama
from handlers.command_handler import build_reply_keyboard
from services.cache_manager import get_cached_barang, get_cached_metode
from nlp.normalizer import koreksi_teks
from nlp.processor import proses_nlp
from core.master_data import cari_harga_default, format_rupiah, parse_rupiah
from services.debt_tracker import cari_hutang_aktif
from services.ui_transaksi import susun_balasan_multi_resume, susun_balasan_resume

logger = logging.getLogger("bot_logger")

_DATE_RE = re.compile(r"\b(\d{1,2})\s*[-/]\s*(\d{1,2})\s*[-/]\s*(\d{2,4})\b")
_OCR_DATE_CHARS = str.maketrans({
    "o": "0",
    "O": "0",
    "i": "1",
    "I": "1",
    "l": "1",
    "L": "1",
    "g": "9",
    "G": "9",
    "z": "2",
    "Z": "2",
    "s": "5",
    "S": "5",
    "b": "8",
    "B": "8",
})
_OCR_DATE_TOKEN_RE = re.compile(
    r"\b([0-9A-Za-z]{1,4})\s*([-/])\s*([0-9A-Za-z]{1,4})\s*([-/])\s*([0-9A-Za-z]{2,4})\b"
)
_OCR_QTY_CHARS = str.maketrans({
    "o": "0",
    "O": "0",
    "i": "1",
    "I": "1",
    "l": "1",
    "L": "1",
    "t": "1",
    "T": "1",
    "z": "2",
    "Z": "2",
    "s": "5",
    "S": "5",
    "b": "8",
    "B": "8",
    "g": "9",
    "G": "9",
})
_UNIT_RE = r"(?:dus|pcs|toples|pack|bungkus|karton|bks|buah|botol|kg|bal|kantong|lusin|koli|roll|meter|lembar|box|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul|gelas|cup|can|sachet|pak|ctn|cen|cth)"
_IGNORE_LINE_RE = re.compile(
    r"\b(?:total|subtotal|grand\s*total|jumlah\s*total|sisa|sisa\s*tagihan|tagihan|saldo|keterangan|ket\.?)\b",
    flags=re.IGNORECASE,
)
_BOT_UI_NOISE_RE = re.compile(
    r"(?:"
    r"hasil\s*ekstraksi\s*ocr"
    r"|rangkuman\s*ekstraksi\s*mesin"
    r"|data\s*belum\s*lengkap"
    r"|lengkapi\s*data"
    r"|kirim\s*data"
    r"|edit\s*kembali"
    r"|data\s*belum\s*masuk\s*database"
    r")",
    flags=re.IGNORECASE,
)
_BOT_UI_LABEL_LINE_RE = re.compile(
    r"^(?:📅|👤|⚙️|📦|🔢|📋|💵|💳|🏦|💸|⚠️)\s*",
    flags=re.IGNORECASE,
)


def _normalize_ocr_line(text):
    line = (text or "").strip()
    line = re.sub(r"^[\s👤📅📦🔢💳🏦💵⚠️✅🤖]+", "", line).strip()
    line = re.sub(r"^\[\d+\]\s*", "", line).strip()
    line = re.sub(r"^[\s~•*\-–—]+", "", line).strip()
    line = re.sub(r"\s+", " ", line).strip()
    return line


def _normalize_ocr_date_text(text):
    raw = (text or "").strip()

    def _replace_date_tokens(match):
        day = re.sub(r"\D", "", match.group(1).translate(_OCR_DATE_CHARS))
        month = re.sub(r"\D", "", match.group(3).translate(_OCR_DATE_CHARS))
        year = re.sub(r"\D", "", match.group(5).translate(_OCR_DATE_CHARS))
        if not day or not month or len(year) not in {2, 4}:
            return match.group(0)
        return f"{day}{match.group(2)}{month}{match.group(4)}{year}"

    return _OCR_DATE_TOKEN_RE.sub(_replace_date_tokens, raw)


def _to_iso_date(text):
    raw = (text or "").strip()
    cleaned = _normalize_ocr_date_text(raw)

    m = _DATE_RE.search(cleaned)
    if not m:
        digits = re.sub(r"\D", "", cleaned)
        if len(digits) == 8:
            day = int(digits[:2])
            month = int(digits[2:4])
            year = int(digits[4:])
        else:
            return None
    else:
        day = int(m.group(1))
        month = int(m.group(2))
        year = int(m.group(3))
    if year < 100:
        year += 2000
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def _to_display_date(iso_date):
    if not iso_date:
        return None
    try:
        parts = iso_date.split("-")
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except Exception:
        return iso_date


def _extract_date_and_remainder(text):
    raw = (text or "").strip()
    cleaned = _normalize_ocr_date_text(raw)

    digit_groups = re.findall(r"\d{1,4}", cleaned)
    if len(digit_groups) >= 4 and len(digit_groups[-1]) == 4:
        try:
            dd = int(digit_groups[-3])
            mm = int(digit_groups[-2])
            yy = int(digit_groups[-1])
            if 1 <= dd <= 31 and 1 <= mm <= 12 and 2000 <= yy <= 2100:
                date_iso = f"{yy:04d}-{mm:02d}-{dd:02d}"
                date_pat = re.compile(
                    rf"{re.escape(digit_groups[-3])}\s*[-/]\s*{re.escape(digit_groups[-2])}\s*[-/]\s*{re.escape(digit_groups[-1])}"
                )
                remainder = date_pat.sub("", cleaned, count=1).strip()
                remainder = _normalize_ocr_line(remainder)
                return date_iso, remainder
        except Exception:
            pass

    m = _DATE_RE.search(cleaned)
    if m:
        date_iso = _to_iso_date(m.group(0))
        remainder = (cleaned[:m.start()] + " " + cleaned[m.end():]).strip()
        remainder = _normalize_ocr_line(remainder)
        return date_iso, remainder

    # Fallback tanggal padat (tanpa separator), contoh: "28112029"
    # Jangan aktif untuk baris item/price yang biasanya mengandung "x", "=", "rp", ".", ","
    raw_compact = re.sub(r"\s+", "", cleaned)
    if re.fullmatch(r"\d{8}", raw_compact):
        date_iso = _to_iso_date(raw_compact)
        if date_iso:
            return date_iso, ""

    return None, _normalize_ocr_line(cleaned)


def _split_ocr_blocks(ocr_text):
    blocks = []
    current = {"date": None, "lines": []}
    for raw in (ocr_text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = _normalize_ocr_line(raw)
        if not line:
            continue
        date_iso, remainder = _extract_date_and_remainder(line)
        if date_iso:
            if current["date"] or current["lines"]:
                blocks.append(current)
            current = {"date": date_iso, "lines": []}
            if remainder:
                current["lines"].append(remainder)
            continue
        current["lines"].append(remainder or line)
    if current["date"] or current["lines"]:
        blocks.append(current)
    return blocks


def _remove_bot_ui_noise(text):
    if not text:
        return text
    out_lines = []
    for raw in str(text).replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = _normalize_ocr_line(raw)
        if not line:
            continue
        if _BOT_UI_NOISE_RE.search(line):
            continue
        if _BOT_UI_LABEL_LINE_RE.match(line) and ":" in line:
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def _extract_first_date_display(text):
    for raw in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = _normalize_ocr_line(raw)
        if not line:
            continue
        date_iso, _ = _extract_date_and_remainder(line)
        if date_iso:
            return _to_display_date(date_iso)
    return None

def _is_placeholder_name(name):
    raw = re.sub(r"\s+", " ", str(name or "")).strip(" .,:;-").lower()
    if not raw:
        return True
    return raw in {"nama", "nama sales", "pelanggan", "customer", "pembeli", "-"}


def _extract_first_name_fallback(text, daftar_b=None):
    lines = []
    for raw in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = _normalize_ocr_line(raw)
        if line:
            lines.append(line)
    name = _extract_block_name(lines, daftar_b=daftar_b)
    if name and not _is_placeholder_name(name):
        return name
    for line in lines:
        m = re.search(r"\bnama(?:\s+sales)?\s+(.+)$", line, flags=re.IGNORECASE)
        if m:
            cand = re.sub(r"\s+", " ", m.group(1)).strip(" .,:;-")
            if cand and not _is_placeholder_name(cand):
                return cand
    return None


def _get_known_customer_names():
    if not ctx.IS_DB_CONNECTED:
        return []

    names = set()
    try:
        from database import db_client

        try:
            res = db_client.get_supabase().table("pelanggan").select("nama").order("id", desc=True).limit(300).execute()
            for row in res.data or []:
                nama = re.sub(r"\s+", " ", str(row.get("nama") or "")).strip(" .,:;-")
                if nama:
                    names.add(nama)
        except Exception:
            pass

        try:
            rows = db_client.get_semua_transaksi_db(columns="nama_pelanggan")
            for row in rows or []:
                nama = re.sub(r"\s+", " ", str(row.get("nama_pelanggan") or "")).strip(" .,:;-")
                if nama:
                    names.add(nama)
        except Exception:
            pass
    except Exception:
        return []

    return sorted(names)


def _normalize_customer_name(name, known_names=None):
    raw_name = re.sub(r"\s+", " ", str(name or "")).strip(" .,:;-")
    if not raw_name:
        return raw_name

    candidates = known_names if known_names is not None else _get_known_customer_names()
    if not candidates:
        return raw_name

    raw_words = re.findall(r"[a-z0-9]+", raw_name.lower())
    if not raw_words:
        return raw_name

    filtered = []
    for candidate in candidates:
        cand_words = re.findall(r"[a-z0-9]+", str(candidate).lower())
        if not cand_words:
            continue
        if cand_words[0] == raw_words[0]:
            filtered.append(candidate)

    search_pool = filtered or candidates
    best = process.extractOne(raw_name, search_pool, scorer=fuzz.token_sort_ratio)
    if not best:
        return raw_name

    best_name, score = best[0], best[1]
    if score >= 86:
        return best_name
    return raw_name


def _match_product_phrase(tokens, start_idx, daftar_b=None):
    if not daftar_b:
        return None, None
    max_len = min(4, len(tokens) - start_idx)
    for phrase_len in range(max_len, 0, -1):
        phrase_tokens = tokens[start_idx:start_idx + phrase_len]
        if any(re.fullmatch(_UNIT_RE, tok, flags=re.IGNORECASE) for tok in phrase_tokens):
            continue
        if any(_is_ocr_number_like_token(tok) for tok in phrase_tokens[1:]):
            continue
        candidate = " ".join(phrase_tokens).strip(" .,:;-")
        if not candidate:
            continue
        normalized = _normalize_product_name(candidate, daftar_b)
        if any(str(normalized).lower() == str(barang).lower() for barang in daftar_b):
            return normalized, start_idx + phrase_len
    return None, None


def _find_product_start(tokens, daftar_b=None):
    if not tokens or not daftar_b:
        return None, None, None
    for start_idx in range(len(tokens)):
        matched_name, end_idx = _match_product_phrase(tokens, start_idx, daftar_b)
        if matched_name:
            return start_idx, end_idx, matched_name
    return None, None, None


def _is_ocr_number_like_token(token):
    raw = str(token or "").strip()
    if not raw or not re.fullmatch(r"[0-9A-Za-z]+", raw):
        return False
    translated = raw.translate(_OCR_QTY_CHARS)
    digits = re.sub(r"\D", "", translated)
    return bool(digits) and len(digits) == len(translated)


def _split_inline_name_and_items(line, daftar_b=None):
    teks = re.sub(r"\s+", " ", str(line or "")).strip(" .,:;-")
    if not teks:
        return None, None

    m_nama = re.search(r"\bnama(?:\s+sales)?\s*[:=]\s*(.+)$", teks, flags=re.IGNORECASE)
    if not m_nama:
        return None, None

    after_name = re.sub(r"\s+", " ", m_nama.group(1)).strip(" .,:;-")
    if not after_name:
        return None, None

    tokens_all = after_name.split()
    product_start_idx, _, _ = _find_product_start(tokens_all, daftar_b)
    if product_start_idx is not None and product_start_idx > 0:
        customer_name = " ".join(tokens_all[:product_start_idx]).strip(" .,:;-")
        item_blob = " ".join(tokens_all[product_start_idx:]).strip(" .,:;-")
        return customer_name or None, item_blob or None

    qty_unit_pattern = re.compile(
        rf"(?P<qty>[0-9lIoO]{{1,6}})\s*(?P<unit>{_UNIT_RE})\b",
        flags=re.IGNORECASE,
    )
    first_qty = qty_unit_pattern.search(after_name)
    if not first_qty:
        return after_name, None

    before_first_qty = after_name[:first_qty.start()].strip(" .,:;-")
    if not before_first_qty:
        return None, after_name

    tokens = before_first_qty.split()
    if not tokens:
        return None, after_name

    product_start_idx = None
    if daftar_b:
        for start_idx in range(len(tokens)):
            candidate = " ".join(tokens[start_idx:]).strip()
            if not candidate:
                continue
            normalized = _normalize_product_name(candidate, daftar_b)
            if any(str(normalized).lower() == str(barang).lower() for barang in (daftar_b or [])):
                product_start_idx = start_idx
                break

    if product_start_idx is None:
        return before_first_qty, None

    customer_name = " ".join(tokens[:product_start_idx]).strip(" .,:;-")
    first_product = " ".join(tokens[product_start_idx:]).strip(" .,:;-")
    item_blob = f"{first_product} {after_name[first_qty.start():]}".strip()
    return customer_name or None, item_blob or None


def _split_unlabeled_name_and_items(line, daftar_b=None):
    teks = re.sub(r"\s+", " ", str(line or "")).strip(" .,:;-")
    teks = re.sub(r"^\[\d+\]\s*", "", teks).strip()
    if not teks or not daftar_b:
        return None, None

    qty_unit_pattern = re.compile(
        rf"(?P<qty>[0-9lIoO]{{1,6}})\s*(?P<unit>{_UNIT_RE})\b",
        flags=re.IGNORECASE,
    )
    first_qty = qty_unit_pattern.search(teks)
    if not first_qty:
        return None, None

    before_first_qty = teks[:first_qty.start()]
    before_first_qty = re.sub(r"\s*:\s*$", "", before_first_qty).strip(" .,:;-")
    if not before_first_qty:
        return None, None

    tokens = before_first_qty.split()
    if not tokens:
        return None, None

    all_tokens = teks.split()
    product_start_idx_all, _, _ = _find_product_start(all_tokens, daftar_b)
    if product_start_idx_all is not None and product_start_idx_all > 0:
        customer_name = " ".join(all_tokens[:product_start_idx_all]).strip(" .,:;-")
        item_blob = " ".join(all_tokens[product_start_idx_all:]).strip(" .,:;-")
        return customer_name or None, item_blob or None

    product_start_idx = None
    for start_idx in range(len(tokens)):
        candidate = " ".join(tokens[start_idx:]).strip(" .,:;-")
        if not candidate:
            continue
        normalized = _normalize_product_name(candidate, daftar_b)
        if any(str(normalized).lower() == str(barang).lower() for barang in daftar_b):
            product_start_idx = start_idx
            break

    if product_start_idx is None:
        return None, None

    customer_name = " ".join(tokens[:product_start_idx]).strip(" .,:;-")
    first_product = " ".join(tokens[product_start_idx:]).strip(" .,:;-")
    item_blob = f"{first_product} {teks[first_qty.start():]}".strip()
    return customer_name or None, item_blob or None


def _extract_block_name(lines, daftar_b=None):
    for line in lines or []:
        inline_name, _ = _split_inline_name_and_items(line, daftar_b)
        if inline_name:
            return _normalize_customer_name(inline_name)
        inline_name2, _ = _split_unlabeled_name_and_items(line, daftar_b)
        if inline_name2:
            return _normalize_customer_name(inline_name2)
        m = re.search(r"\bnama(?:\s+sales)?\s*[:=]\s*(.+)$", line, flags=re.IGNORECASE)
        if m:
            return _normalize_customer_name(re.sub(r"\s+", " ", m.group(1)).strip(" .,:;-"))
    return None


def _extract_block_method(lines):
    text = " ".join(str(line or "") for line in (lines or []))
    low = text.lower()
    if re.search(r"\b(tf|trf|transfer)\b", low):
        return "Transfer"
    if re.search(r"\b(tunai|cash|kontan)\b", low):
        return "Tunai"
    if re.search(r"\bqris\b", low):
        return "QRIS"
    return None


def _normalize_unit_for_nlp(unit):
    unit_l = str(unit or "").strip().lower()
    return "karton" if unit_l in {"ctn", "cen", "cth"} else unit_l


def _normalize_qty_token(token):
    s = str(token or "").strip()
    if not s:
        return None
    s = re.sub(r"\s+", "", s)
    s = s.translate(_OCR_QTY_CHARS)
    digits = re.sub(r"\D", "", s)
    if not digits:
        return None
    try:
        return str(int(digits))
    except Exception:
        return None


def _strip_pricing_extras(line):
    s = str(line or "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*(?:x|\*)\s*[\d\.,]+\s*(?:=\s*[\d\.,]+)?\s*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*=\s*[\d\.,]+\s*$", "", s, flags=re.IGNORECASE)
    return s.strip(" .,:;-")


def _normalize_product_name(name, daftar_b):
    raw_name = re.sub(r"\s+", " ", str(name or "")).strip(" .,:;-")
    if not raw_name:
        return raw_name

    # Koreksi typo ringan lebih dulu dengan kamus/fuzzy NLP.
    corrected = koreksi_teks(raw_name, daftar_barang=daftar_b)
    corrected = re.sub(r"\s+", " ", str(corrected or "")).strip(" .,:;-") or raw_name

    # Jika ada master barang, pakai nama kanonik dari hasil lookup fuzzy master.
    if ctx.IS_DB_CONNECTED:
        cached_barang = get_cached_barang()
        matches = cari_harga_default(ctx.db_barang, corrected, semua_barang=cached_barang)
        if not matches and corrected.lower() != raw_name.lower():
            matches = cari_harga_default(ctx.db_barang, raw_name, semua_barang=cached_barang)
        if matches:
            return matches[0]["nama"]

    for barang in daftar_b or []:
        if corrected.lower() == str(barang).lower():
            return barang

    fuzzy_match = process.extractOne(corrected, daftar_b or [], scorer=fuzz.token_sort_ratio)
    if fuzzy_match and fuzzy_match[1] >= 80:
        return fuzzy_match[0]

    return corrected


def _extract_item_lines_from_block(lines, daftar_b=None):
    extracted = []
    anchored_pattern = re.compile(
        rf"^(?P<name>[a-zA-Z][a-zA-Z0-9\s\-/]{{1,60}}?)\s+(?P<qty>[0-9lIoO]{{1,6}})\s*(?P<unit>{_UNIT_RE})\b$",
        flags=re.IGNORECASE,
    )
    qty_unit_pattern = re.compile(
        rf"(?P<qty>[0-9lIoO]{{1,6}})\s*(?P<unit>{_UNIT_RE})\b",
        flags=re.IGNORECASE,
    )

    def _extract_segmented_items(text):
        teks = re.sub(r"\s+", " ", str(text or "")).strip(" .,:;-")
        tokens = teks.split()
        if not tokens or not daftar_b:
            return []

        items = []
        idx = 0
        while idx < len(tokens):
            product_name, product_end_idx = _match_product_phrase(tokens, idx, daftar_b)
            if not product_name:
                idx += 1
                continue

            next_idx = product_end_idx
            next_product_idx = len(tokens)
            while next_idx < len(tokens):
                next_name, _ = _match_product_phrase(tokens, next_idx, daftar_b)
                if next_name:
                    next_product_idx = next_idx
                    break
                next_idx += 1

            tail_tokens = tokens[product_end_idx:next_product_idx]
            unit = None
            qty_raw = None
            for unit_idx in range(len(tail_tokens) - 1, -1, -1):
                if re.fullmatch(_UNIT_RE, tail_tokens[unit_idx], flags=re.IGNORECASE):
                    unit = _normalize_unit_for_nlp(tail_tokens[unit_idx])
                    raw_tokens = [tok for tok in tail_tokens[:unit_idx] if _is_ocr_number_like_token(tok)]
                    if raw_tokens:
                        qty_raw = " ".join(raw_tokens)
                    break

            qty = _normalize_qty_token(qty_raw) if qty_raw else None
            if product_name and qty and int(qty) > 0 and unit:
                items.append(f"{product_name} {qty} {unit}")
            idx = product_end_idx

        return items

    for raw_line in lines or []:
        low = raw_line.lower()
        if _IGNORE_LINE_RE.search(low):
            continue
        if any(k in low for k in ["bayar cicilan", "bayar angsuran", "cicilan", "angsuran"]):
            continue

        working = str(raw_line or "")
        if re.search(r"\bnama(?:\s+sales)?\b", low):
            _, item_blob = _split_inline_name_and_items(raw_line, daftar_b)
            if not item_blob:
                continue
            working = item_blob
        elif daftar_b:
            _, item_blob = _split_unlabeled_name_and_items(raw_line, daftar_b)
            if item_blob:
                working = item_blob

        working = re.sub(r"^\s*nama\s+produk\s*[:=-]?\s*", "", working, flags=re.IGNORECASE)
        working = re.sub(r"^\s*ambil\s+barang\s*[:=-]?\s*", "", working, flags=re.IGNORECASE)
        working = re.sub(r"^\s*(produk|barang)\s*[:=-]?\s*", "", working, flags=re.IGNORECASE)
        working = re.sub(r"\s*:\s*(?=[0-9lIoO])", " ", working)
        working = re.sub(r"\s+", " ", working).strip(" .,:;-")
        working = _strip_pricing_extras(working)
        if not working:
            continue

        segmented_items = _extract_segmented_items(working)
        if segmented_items:
            extracted.extend(segmented_items)
            continue

        qty_matches = list(qty_unit_pattern.finditer(working))

        full = anchored_pattern.match(working)
        if full and len(qty_matches) <= 1:
            name = re.sub(r"\s+", " ", full.group("name")).strip(" .,:;-")
            name = re.sub(r"^(produk|barang)\s+", "", name, flags=re.IGNORECASE).strip(" .,:;-")
            qty = _normalize_qty_token(full.group("qty"))
            unit = _normalize_unit_for_nlp(full.group("unit"))
            if name and qty and int(qty) > 0:
                extracted.append(f"{name} {qty} {unit}")
            continue

        # Fallback untuk OCR yang menggabungkan beberapa item dalam satu baris.
        last_end = 0
        for match in qty_matches:
            name = working[last_end:match.start()].strip(" .,:;-")
            name = re.sub(r"^(dan|,)\s*", "", name, flags=re.IGNORECASE).strip(" .,:;-")
            name = re.sub(r"^(produk|barang)\s+", "", name, flags=re.IGNORECASE).strip(" .,:;-")
            qty = _normalize_qty_token(match.group("qty"))
            unit = _normalize_unit_for_nlp(match.group("unit"))
            if name and qty and int(qty) > 0:
                extracted.append(f"{name} {qty} {unit}")
            last_end = match.end()

    return extracted


def _extract_payment_entries(blocks, daftar_b=None):
    entries = []
    for block in blocks:
        date_iso = block.get("date")
        date_disp = _to_display_date(date_iso)
        name = _extract_block_name(block.get("lines") or [], daftar_b=daftar_b)
        metode = _extract_block_method(block.get("lines") or [])
        if not name:
            continue
        for line in block.get("lines") or []:
            low = line.lower()
            if "cicilan" not in low and "angsuran" not in low:
                continue
            match = re.search(
                r"(?:bayar\s+)?(?:cicilan|angsuran)\s*[:=]?\s*(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu))?)",
                line,
                flags=re.IGNORECASE,
            )
            nominal_src = match.group(1) if match else None
            amount = parse_rupiah(nominal_src) if nominal_src else 0
            if amount <= 0:
                continue
            entries.append({
                "date": date_disp or datetime.now().strftime("%d-%m-%Y"),
                "name": name,
                "amount": amount,
                "method": metode,
                "raw_line": line,
            })
    return entries


def _build_structured_nlp_input(ocr_text, daftar_b=None):
    blocks = _split_ocr_blocks(ocr_text)
    if not blocks:
        return ocr_text, [], [], []

    generated_lines = []
    payment_entries = _extract_payment_entries(blocks, daftar_b=daftar_b)
    sales_contexts = []
    sales_entries = []

    for block in blocks:
        date_disp = _to_display_date(block.get("date")) or datetime.now().strftime("%d-%m-%Y")
        lines = block.get("lines") or []
        name = _extract_block_name(lines, daftar_b=daftar_b)
        metode = _extract_block_method(lines)
        if not name:
            continue
        item_lines = _extract_item_lines_from_block(lines, daftar_b=daftar_b)
        for item_line in item_lines:
            generated_lines.append(f"tanggal {date_disp} nama {name} {item_line} belum lunas")
            sales_contexts.append({"TANGGAL": date_disp, "NAMA": name})
            sales_entries.append({
                "TANGGAL": date_disp,
                "NAMA": name,
                "ITEM_TEXT": item_line,
                "METODE_PEMBAYARAN": metode,
            })

    if not generated_lines:
        return ocr_text, payment_entries, [], []
    return ", ".join(generated_lines), payment_entries, sales_contexts, sales_entries


def _build_sales_results_from_ocr_entries(sales_entries, daftar_b, mapping_m):
    results = []
    for entry in sales_entries or []:
        item_text = str(entry.get("ITEM_TEXT") or "").strip()
        if not item_text:
            continue

        m = re.match(rf"^(?P<name>.+?)\s+(?P<qty>[0-9lIoO]{{1,6}})\s+(?P<unit>{_UNIT_RE})$", item_text, flags=re.IGNORECASE)
        if m:
            normalized_name = _normalize_product_name(m.group("name"), daftar_b)
            qty = _normalize_qty_token(m.group("qty"))
            ent = {
                "TANGGAL": entry.get("TANGGAL"),
                "NAMA": entry.get("NAMA"),
                "AKSI": "Tambah Penjualan",
                "STATUS": "Hutang",
                "NOMINAL_BAYAR": None,
                "METODE_PEMBAYARAN": entry.get("METODE_PEMBAYARAN"),
                "BARANG": normalized_name,
                "JUMLAH": f"{qty or m.group('qty')} {_normalize_unit_for_nlp(m.group('unit'))}",
                "SATUAN": _normalize_unit_for_nlp(m.group("unit")),
            }
        else:
            parsed = proses_nlp(
                koreksi_teks(item_text, daftar_barang=daftar_b),
                daftar_barang=daftar_b,
                mapping_metode=mapping_m,
                already_normalized=True,
            )
            base = (parsed[0] if parsed else {"intent": "Unknown", "entitas": {}})
            ent = base.get("entitas", {}) or {}

            # Paksa field penting dari parser blok OCR, bukan tebakan NLP kalimat panjang.
            ent["TANGGAL"] = entry.get("TANGGAL") or ent.get("TANGGAL")
            ent["NAMA"] = entry.get("NAMA") or ent.get("NAMA")
            ent["AKSI"] = "Tambah Penjualan"
            ent["STATUS"] = "Hutang"
            ent["NOMINAL_BAYAR"] = None
            ent["METODE_PEMBAYARAN"] = entry.get("METODE_PEMBAYARAN") or ent.get("METODE_PEMBAYARAN") or None

            if ent.get("BARANG"):
                ent["BARANG"] = _normalize_product_name(ent.get("BARANG"), daftar_b)

            if not ent.get("BARANG") or not ent.get("JUMLAH"):
                if not ent.get("BARANG") and m:
                    ent["BARANG"] = _normalize_product_name(m.group("name"), daftar_b)
                if not ent.get("JUMLAH") and m:
                    ent["JUMLAH"] = f"{m.group('qty')} {_normalize_unit_for_nlp(m.group('unit'))}"
                if not ent.get("SATUAN") and m:
                    ent["SATUAN"] = _normalize_unit_for_nlp(m.group("unit"))

        if not ent.get("SATUAN") and ent.get("JUMLAH"):
            m_sat = re.search(rf"\d+\s*({_UNIT_RE})\b", str(ent["JUMLAH"]), re.IGNORECASE)
            if m_sat:
                ent["SATUAN"] = _normalize_unit_for_nlp(m_sat.group(1))

        results.append({"intent": "Catat_Penjualan_Cicil", "entitas": ent, "original_text": item_text})

    return results


def _render_payment_summary(payment_entries):
    if not payment_entries:
        return None, []

    grouped = {}
    for entry in payment_entries:
        name = str(entry.get("name") or "-").strip()
        payload = grouped.setdefault(name, {"total": 0, "items": []})
        payload["total"] += int(entry.get("amount") or 0)
        payload["items"].append(entry)

    parts = ["💳 <b>RINGKASAN CICILAN OCR</b>", "━━━━━━━━━━━━━━━━━━━━━━"]
    apply_plan = []
    for name, payload in grouped.items():
        parts.append(f"👤 <b>{html.escape(name)}</b>")
        for item in payload["items"]:
            parts.append(
                f"• {html.escape(item['date'])}: <code>{format_rupiah(item['amount'])}</code>"
            )
        parts.append(f"💰 <b>Total Cicilan Akhir:</b> <code>{format_rupiah(payload['total'])}</code>")

        if ctx.IS_DB_CONNECTED:
            try:
                hutang_list = cari_hutang_aktif(ctx.db_transaksi, name, cocokkan_nama)
                outstanding = int(sum(float(h.get("tagihan", 0) or 0) for h in hutang_list))
                if hutang_list and outstanding > 0:
                    remaining_payment = int(payload["total"])
                    parts.append(f"⚠️ <b>Total Tagihan Aktif:</b> <code>{format_rupiah(outstanding)}</code>")
                    parts.append("🧾 <b>Alokasi Cicilan ke Tagihan Aktif:</b>")

                    for idx, hutang in enumerate(hutang_list, start=1):
                        tagihan_awal = int(float(hutang.get("tagihan", 0) or 0))
                        terpakai = min(tagihan_awal, remaining_payment)
                        sisa = max(0, tagihan_awal - terpakai)
                        remaining_payment = max(0, remaining_payment - terpakai)
                        barang = html.escape(str(hutang.get("barang") or "-"))
                        tanggal = html.escape(str(hutang.get("tanggal") or "-"))
                        if terpakai > 0:
                            apply_plan.append({
                                "name": name,
                                "row_index": hutang.get("row_index"),
                                "barang": hutang.get("barang") or "-",
                                "tanggal": hutang.get("tanggal") or "-",
                                "tagihan_awal": tagihan_awal,
                                "bayar": terpakai,
                                "sisa": sisa,
                            })
                        parts.append(
                            f"{idx}. {tanggal} | {barang}\n"
                            f"   Tagihan awal: <code>{format_rupiah(tagihan_awal)}</code>\n"
                            f"   Cicilan masuk: <code>{format_rupiah(terpakai)}</code>\n"
                            f"   Sisa akhir: <code>{format_rupiah(sisa)}</code>"
                        )

                    sisa_total = max(0, outstanding - payload["total"])
                    parts.append(f"📉 <b>Total Sisa Akhir:</b> <code>{format_rupiah(sisa_total)}</code>")
                    if remaining_payment > 0:
                        parts.append(f"💚 <b>Kelebihan Cicilan:</b> <code>{format_rupiah(remaining_payment)}</code>")
                elif outstanding <= 0:
                    parts.append("✅ <b>Tidak ada tagihan aktif yang cocok di database.</b>")
            except Exception:
                pass
        parts.append("━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(parts), apply_plan


def _payment_total_from_entries(payment_entries):
    return int(sum(int(entry.get("amount") or 0) for entry in (payment_entries or [])))


def _build_pelunasan_results_from_payment_entries(payment_entries):
    grouped = {}
    for entry in payment_entries or []:
        name = str(entry.get("name") or "").strip()
        if not name:
            continue
        payload = grouped.setdefault(name, {"date": None, "method": None, "amount": 0})
        payload["amount"] += int(entry.get("amount") or 0)
        if not payload["date"]:
            payload["date"] = entry.get("date")
        if not payload["method"]:
            payload["method"] = entry.get("method")

    results = []
    for name, payload in grouped.items():
        amount = int(payload.get("amount") or 0)
        if amount <= 0:
            continue
        ent = {
            "TANGGAL": payload.get("date") or datetime.now().strftime("%d-%m-%Y"),
            "NAMA": name,
            "AKSI": "Catat Pelunasan",
            "STATUS": "Dicicil",
            "NOMINAL_BAYAR": format_rupiah(amount),
            "METODE_PEMBAYARAN": payload.get("method") or None,
        }
        original_text = f"{name} bayar cicilan {format_rupiah(amount)}"
        results.append({"intent": "Pelunasan_Hutang", "entitas": ent, "original_text": original_text})
    return results


def _proses_hasil_ocr_ke_nlp(chat_id, message_id_target, ocr_text):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    sess = user_sessions.ensure(chat_id)
    perf_total_start = perf_counter()

    all_b = get_cached_barang()
    daftar_b = [b["nama"] for b in all_b]
    mapping_m = get_cached_metode()

    nlp_stage_start = perf_counter()
    clean_ocr_text = _remove_bot_ui_noise(ocr_text)
    nlp_input_text, payment_entries, sales_contexts, sales_entries = _build_structured_nlp_input(clean_ocr_text, daftar_b=daftar_b)
    fallback_name = _extract_first_name_fallback(clean_ocr_text, daftar_b=daftar_b)

    if (not sales_entries) and payment_entries:
        pelunasan_results = _build_pelunasan_results_from_payment_entries(payment_entries)
        if pelunasan_results:
            hasil_nlp = pelunasan_results[0]
            entitas = hasil_nlp.get("entitas", {}) or {}
            if _is_placeholder_name(entitas.get("NAMA")) and fallback_name:
                entitas["NAMA"] = fallback_name
            sess["hasil_nlp"] = hasil_nlp
            sess["entitas"] = {k: v for k, v in entitas.items() if v is not None and str(v).strip() != ""}
            sess["state"] = "pending_confirmation"
            render_start = perf_counter()
            susun_balasan_resume(chat_id, message_id_target)
            logger.info(
                "[Perf][ocr] chat_id=%s render_pelunasan_ms=%.1f total_ms=%.1f",
                chat_id,
                (perf_counter() - render_start) * 1000,
                (perf_counter() - perf_total_start) * 1000,
            )
            return

    if sales_entries:
        results_nlp = _build_sales_results_from_ocr_entries(sales_entries, daftar_b, mapping_m)
    else:
        user_text_norm = koreksi_teks(nlp_input_text, daftar_barang=daftar_b)
        results_nlp = proses_nlp(
            user_text_norm,
            db_metode=ctx.db_metode,
            daftar_barang=daftar_b,
            mapping_metode=mapping_m,
            already_normalized=True,
        )
    logger.info(
        "[Perf][ocr] chat_id=%s nlp_ms=%.1f results=%s",
        chat_id,
        (perf_counter() - nlp_stage_start) * 1000,
        len(results_nlp or []),
    )

    if not results_nlp:
        safe_edit_message(
            bot,
            "🔍 <b>HASIL OCR SUDAH DITAMPILKAN</b>\n\n"
            "Teks OCR berhasil dibaca, tetapi belum berhasil dipahami sebagai transaksi oleh NLP.",
            chat_id,
            message_id_target,
            parse_mode="HTML",
        )
        return

    valid_results = [
        r for r in results_nlp
        if r.get("entitas", {}).get("AKSI")
        or r.get("entitas", {}).get("NAMA")
        or r.get("entitas", {}).get("BARANG")
    ]
    if valid_results:
        results_nlp = valid_results

    if sales_contexts and results_nlp:
        for idx, result in enumerate(results_nlp):
            if idx >= len(sales_contexts):
                break
            ctx_item = sales_contexts[idx]
            ent = result.get("entitas", {}) or {}
            ent["TANGGAL"] = ctx_item.get("TANGGAL") or ent.get("TANGGAL")
            if _is_placeholder_name(ent.get("NAMA")):
                ent["NAMA"] = None
            ent["NAMA"] = ctx_item.get("NAMA") or ent.get("NAMA") or fallback_name
            result["entitas"] = ent

    sales_results = []
    for result in results_nlp:
        aksi = (result.get("entitas", {}) or {}).get("AKSI")
        if aksi == "Catat Pelunasan":
            continue
        else:
            sales_results.append(result)
    if sales_results:
        results_nlp = sales_results

    if len(results_nlp) > 1:
        base_aksi = None
        for r in results_nlp:
            if r.get("entitas", {}).get("AKSI"):
                base_aksi = r["entitas"]["AKSI"]
                break

        context_pesan = {}
        if results_nlp and isinstance(results_nlp[0], dict):
            ent0 = results_nlp[0].get("entitas", {}) or {}
            for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN"]:
                if ent0.get(k):
                    context_pesan[k] = ent0.get(k)

        lookup_total_ms = 0.0
        for item in results_nlp:
            gabungan = {}
            for k, v in context_pesan.items():
                if v and not gabungan.get(k):
                    gabungan[k] = v
            for k, v in item.get("entitas", {}).items():
                if v:
                    gabungan[k] = v

            if base_aksi == "Tambah Penjualan":
                gabungan["AKSI"] = "Tambah Penjualan"
            elif not gabungan.get("AKSI"):
                gabungan["AKSI"] = "Tambah Penjualan"

            if not gabungan.get("SATUAN") and gabungan.get("JUMLAH"):
                m_sat = re.search(
                    r"\d+\s*(dus|pcs|toples|pack|bungkus|karton|bks|buah|botol|kg|bal|kantong|lusin|koli|roll|meter|lembar|box|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul|gelas|cup|can|sachet|pak)\b",
                    str(gabungan["JUMLAH"]),
                    re.IGNORECASE,
                )
                if m_sat:
                    gabungan["SATUAN"] = m_sat.group(1).lower()

            if ctx.IS_DB_CONNECTED and gabungan.get("BARANG") and not gabungan.get("HARGA"):
                lookup_start = perf_counter()
                matches = cari_harga_default(
                    ctx.db_barang,
                    gabungan["BARANG"],
                    satuan_cari=gabungan.get("SATUAN"),
                    semua_barang=all_b,
                )
                lookup_total_ms += (perf_counter() - lookup_start) * 1000
                if matches:
                    info_h = matches[0]
                    gabungan["HARGA"] = format_rupiah(info_h["harga"])
                    gabungan["SATUAN"] = info_h["satuan"]
                    if gabungan.get("JUMLAH"):
                        try:
                            _m = re.search(r"\d+", str(gabungan["JUMLAH"]))
                            if _m:
                                jml_n = int(_m.group())
                                gabungan["TOTAL"] = format_rupiah(jml_n * info_h["harga"])
                        except Exception:
                            pass

            if not gabungan.get("TANGGAL") and not gabungan.get("SEMUA"):
                gabungan["TANGGAL"] = datetime.now().strftime("%d-%m-%Y")
            if _is_placeholder_name(gabungan.get("NAMA")):
                gabungan["NAMA"] = fallback_name

            item["entitas"] = gabungan

        sess["multi_results"] = results_nlp
        sess["state"] = "pending_multi_insert"
        total_payment = _payment_total_from_entries(payment_entries)
        if total_payment > 0:
            sess["multi_batch_payment_total"] = total_payment
            sess["multi_batch_context"] = {
                "STATUS": "Dicicil",
                "NOMINAL_BAYAR": format_rupiah(total_payment),
            }
            for item in results_nlp:
                ent = item.get("entitas", {}) or {}
                ent["STATUS"] = "Dicicil"
                item["entitas"] = ent
        else:
            sess.pop("multi_batch_payment_total", None)
            sess.pop("multi_batch_context", None)
        sess.pop("ocr_payment_apply_plan", None)
        logger.info(
            "[Perf][ocr] chat_id=%s lookup_harga_multi_ms=%.1f items=%s",
            chat_id,
            lookup_total_ms,
            len(results_nlp),
        )
        render_start = perf_counter()
        susun_balasan_multi_resume(chat_id, message_id_target)
        logger.info(
            "[Perf][ocr] chat_id=%s render_rekap_ms=%.1f total_ms=%.1f",
            chat_id,
            (perf_counter() - render_start) * 1000,
            (perf_counter() - perf_total_start) * 1000,
        )
        return

    if results_nlp:
        hasil_nlp = results_nlp[0]
        entitas = hasil_nlp.get("entitas", {}) or {}
        if ctx.IS_DB_CONNECTED and entitas.get("BARANG") and not entitas.get("HARGA"):
            lookup_start = perf_counter()
            matches = cari_harga_default(
                ctx.db_barang,
                entitas["BARANG"],
                satuan_cari=entitas.get("SATUAN"),
                semua_barang=all_b,
            )
            logger.info(
                "[Perf][ocr] chat_id=%s lookup_harga_single_ms=%.1f",
                chat_id,
                (perf_counter() - lookup_start) * 1000,
            )
            if matches:
                info_harga = matches[0]
                entitas["HARGA"] = format_rupiah(info_harga["harga"])
                entitas["SATUAN"] = info_harga["satuan"]
                if entitas.get("JUMLAH"):
                    try:
                        _m = re.search(r"\d+", str(entitas["JUMLAH"]))
                        if _m:
                            jml_num = int(_m.group())
                            entitas["TOTAL"] = format_rupiah(jml_num * info_harga["harga"])
                    except Exception:
                        pass
        elif entitas.get("HARGA") and entitas.get("JUMLAH") and not entitas.get("TOTAL"):
            try:
                _m = re.search(r"\d+", str(entitas["JUMLAH"]))
                if _m:
                    jml_num = int(_m.group())
                    hrg_num = parse_rupiah(entitas["HARGA"])
                    entitas["TOTAL"] = format_rupiah(jml_num * hrg_num)
            except Exception:
                pass

        nama_now = str(entitas.get("NAMA") or "").strip()
        if nama_now and _BOT_UI_NOISE_RE.search(nama_now):
            entitas.pop("NAMA", None)
        if _is_placeholder_name(entitas.get("NAMA")):
            entitas.pop("NAMA", None)
        if not entitas.get("NAMA") and fallback_name:
            entitas["NAMA"] = fallback_name
        if not entitas.get("TANGGAL") and not entitas.get("SEMUA"):
            date_fb = _extract_first_date_display(clean_ocr_text)
            if date_fb:
                entitas["TANGGAL"] = date_fb
        if not entitas.get("STATUS"):
            entitas["STATUS"] = "Hutang"

        sess["hasil_nlp"] = hasil_nlp
        sess["entitas"] = {k: v for k, v in entitas.items() if v is not None and str(v).strip() != ""}
        sess["state"] = "pending_confirmation"
        render_start = perf_counter()
        susun_balasan_resume(chat_id, message_id_target)
        logger.info(
            "[Perf][ocr] chat_id=%s render_resume_ms=%.1f total_ms=%.1f",
            chat_id,
            (perf_counter() - render_start) * 1000,
            (perf_counter() - perf_total_start) * 1000,
        )
    else:
        safe_edit_message(
            bot,
            "🔍 <b>HASIL OCR SUDAH DITAMPILKAN</b>\n\n"
            "Blok cicilan berhasil dikenali, tetapi tidak ada item penjualan baru yang perlu diringkas.",
            chat_id,
            message_id_target,
            parse_mode="HTML",
        )

def handle_docs_photo(message):
    """Handle unggahan foto - tampilkan hasil OCR lalu teruskan ke NLP transaksi"""
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg_proses = None
    temp_image_path = f"temp_photo_{chat_id}.jpg"

    if not ctx.rate_limiter.is_allowed(user_id):
        logger.warning(f"Rate limit exceeded untuk user {user_id} pada OCR photo")
        bot.reply_to(message, "⏱️ Terlalu banyak request. Tunggu sebentar...")
        return

    logger.info(f"User {user_id} unggah photo untuk OCR")

    try:
        perf_request_start = perf_counter()
        sess = user_sessions.ensure(chat_id)
        need_keyboard = not bool(sess.get("ui_keyboard_shown"))
        if need_keyboard:
            sess["ui_keyboard_shown"] = True

        msg_proses = bot.reply_to(
            message,
            "Sedang diproses...",
            reply_markup=(build_reply_keyboard() if need_keyboard else None)
        )
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(temp_image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        logger.debug(f"Foto OCR untuk chat {chat_id} mulai diproses via ctx.ocr_service")

        # Use OCR Service
        ocr_start = perf_counter()
        hasil_akhir = ctx.ocr_service.extract_text(temp_image_path)
        logger.info(
            "[Perf][ocr] chat_id=%s ocr_ms=%.1f",
            chat_id,
            (perf_counter() - ocr_start) * 1000,
        )

        if not hasil_akhir or hasil_akhir.strip() == "":
            logger.warning(f"Tidak ada teks terdeteksi di foto.")
            safe_edit_message(bot, "❌ Tidak ada teks terdeteksi di foto. Coba foto lagi dengan kualitas lebih baik.",
                                 chat_id, msg_proses.message_id)
            return

        if str(hasil_akhir).strip().startswith("Error OCR:"):
            error_message = str(hasil_akhir).strip()
            logger.warning("OCR service returned error text instead of extracted text: %s", error_message)
            safe_edit_message(
                bot,
                f"❌ Gagal memproses foto dengan OCR:\n{error_message}\n\nCoba kirim ulang foto yang sama 1x. Jika masih gagal, coba foto yang lebih jelas.",
                chat_id,
                msg_proses.message_id,
            )
            return

        hasil_akhir = sanitize_input(hasil_akhir)
        logger.debug(f"Teks terextract: {hasil_akhir[:100]}...")

        # Send the OCR result
        chunk_size = 3200
        chunks = [hasil_akhir[i:i + chunk_size] for i in range(0, len(hasil_akhir), chunk_size)]
        total = len(chunks)
        for idx, chunk in enumerate(chunks[:10], start=1):
            header = "🔍 <b>HASIL EKSTRAKSI OCR</b>"
            if total > 1:
                header = f"{header} <i>({idx}/{total})</i>"
            payload = f"{header}\n<pre>{html.escape(chunk)}</pre>"
            if idx == 1:
                safe_edit_message(bot, payload, chat_id, msg_proses.message_id, parse_mode="HTML")
            else:
                bot.send_message(chat_id, payload, parse_mode="HTML")

        msg_nlp = bot.send_message(chat_id, "🤖 Memproses hasil OCR ke NLP...")
        _proses_hasil_ocr_ke_nlp(chat_id, msg_nlp.message_id, hasil_akhir)
        logger.info(
            "[Perf][ocr] chat_id=%s total_request_ms=%.1f",
            chat_id,
            (perf_counter() - perf_request_start) * 1000,
        )

        return
    except Exception as e:
        log_exception(f"Error processing photo user {user_id}", e)
        notify_admins(f"❌ <b>Error OCR</b>\nUser: <code>{user_id}</code>\nChat: <code>{chat_id}</code>\nPesan: <code>{str(e)[:200]}</code>")
        bot.reply_to(message, "❌ Terjadi kesalahan pemrosesan gambar. Coba ulangi 1x, jika masih gagal kirim foto yang lebih jelas.")
    finally:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)


def register_handlers(bot):
    """Register photo handler ke bot instance."""
    bot.message_handler(content_types=['photo'])(authorized_only(handle_docs_photo))
