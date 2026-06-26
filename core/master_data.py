"""
master_data.py
Module untuk mengelola Master Data Barang dan Master Metode Pembayaran.
Menggunakan tab/worksheet terpisah dalam satu Google Database "AW PRODUCTION".
"""
import re
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz
from database import db_client

def _invalidate_cache(key):
    """Invalidasikan cache agar update database langsung tercermin di bot."""
    try:
        from core.bot_context import ctx
        if ctx.gs_cache:
            ctx.gs_cache.invalidate(key)
    except Exception:
        pass

# Header standar tidak diperlukan lagi karena menggunakan Supabase, namun tetap ada untuk referensi
HEADERS_MASTER_BARANG   = ["ID Barang", "Nama Barang", "Harga Satuan", "Satuan"]
HEADERS_MASTER_METODE   = ["ID Metode", "Nama Metode", "Keyword/Alias"]
HEADERS_HISTORI_LUNAS   = ["Tanggal Bayar", "Nama Pelanggan", "Nominal Bayar", "Sisa Setelah", "Catatan"]

def get_or_create_sheet(database, db_name, headers):
    """
    Deprecated: GSpread sheet builder. Dipertahankan sebagai stub agar main.py tidak error
    sebelum di-refactor.
    """
    return None


def parse_rupiah(teks):
    """Parse string Rupiah ('Rp 15.000') atau angka biasa ke integer."""
    try:
        bersih = str(teks).replace("Rp", "").replace(".", "").replace(",", "").strip()
        return int(bersih) if bersih else 0
    except Exception:
        return 0


def format_rupiah(angka):
    """Format integer ke string Rupiah (mis: 15000 → 'Rp 15.000')."""
    try:
        return f"Rp {int(angka):,}".replace(",", ".")
    except Exception:
        return "Rp 0"


MASTER_BARANG_CATALOG = [
    {
        "kategori": "Permen",
        "items": [
            {"nama": "Willo", "units": ["karton", "toples", "pouch"]},
            {"nama": "Bembeng", "units": ["karton", "toples", "pouch"]},
            {"nama": "Cholatos", "units": ["karton", "toples", "pouch"]},
            {"nama": "Adangrow", "units": ["karton", "toples", "pouch"]},
            {"nama": "Miksu", "units": ["karton", "toples", "pouch"]},
            {"nama": "Getbory", "units": ["karton", "toples", "pouch"]},
        ],
    },
    {
        "kategori": "Roti/Pia",
        "items": [
            {"nama": "Bulus", "units": ["pack", "bungkus"]},
            {"nama": "Roda", "units": ["pack", "bungkus"]},
            {"nama": "Potong", "units": ["pack", "bungkus"]},
        ],
    },
    {
        "kategori": "Serbuk",
        "items": [
            {"nama": "Serbuk Biasa", "units": ["karton"]},
            {"nama": "Serbuk Jelly", "units": ["karton"]},
        ],
    },
    {
        "kategori": "Lainnya",
        "items": [
            {"nama": "Meses", "units": ["karton", "bungkus"]},
            {"nama": "Brownis", "units": ["keranjang"]},
        ],
    },
]


def format_daftar_master_barang_grouped(semua_barang):
    rows = semua_barang or []

    def _norm_name(s):
        return re.sub(r"\s+", " ", str(s or "").strip().lower())

    def _kategori_fallback(nm):
        t = nm or ""
        if any(k in t for k in ["permen", "lolipop", "lollipop"]):
            return "Permen"
        if any(k in t for k in ["roti", "pia", "bakpia"]):
            return "Roti/Pia"
        if "serbuk" in t:
            return "Serbuk"
        if any(k in t for k in ["meses", "brownis", "brownies"]):
            return "Lainnya"
        return "Tambahan"

    def _title_unit(u):
        u = str(u or "").strip().lower()
        if not u:
            return ""
        return u[:1].upper() + u[1:]

    kategori_by_norm = {}
    units_order_by_norm = {}
    for group in MASTER_BARANG_CATALOG:
        kategori = group.get("kategori")
        for item in group.get("items") or []:
            nm = item.get("nama")
            if kategori and nm:
                nm_norm = _norm_name(nm)
                kategori_by_norm[nm_norm] = kategori
                units_order_by_norm[nm_norm] = [str(u).strip().lower() for u in (item.get("units") or []) if u]

    grouped = {}
    for b in rows:
        nama_raw = str(b.get("nama", "")).strip()
        satuan_raw = str(b.get("satuan", "")).strip()
        try:
            harga = int(b.get("harga") or 0)
        except Exception:
            harga = 0

        if not nama_raw or not satuan_raw or harga <= 0:
            continue

        nm = _norm_name(nama_raw)
        kategori = kategori_by_norm.get(nm) or _kategori_fallback(nm)
        by_name = grouped.setdefault(kategori, {})
        by_unit = by_name.setdefault(nm, {"nama_display": nama_raw.strip().title(), "units": {}})
        unit = satuan_raw.strip().lower()
        by_unit["units"][unit] = harga

    if not grouped:
        return (
            "<b>DAFTAR MASTER BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "(Belum ada data barang)\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )

    ordered_kategori = [g["kategori"] for g in MASTER_BARANG_CATALOG]
    if "Tambahan" not in ordered_kategori:
        ordered_kategori.append("Tambahan")

    divider = "━━━━━━━━━━━━━━━━━━━━━━"
    teks = f"<b>DAFTAR MASTER BARANG</b>\n{divider}\n"

    for kategori in ordered_kategori:
        by_name = grouped.get(kategori) or {}
        if not by_name:
            continue

        teks += f"\n<b>{kategori}</b>\n"
        for nm in sorted(by_name.keys()):
            info = by_name[nm]
            nama_disp = info["nama_display"]
            units_map = info.get("units") or {}

            ordered_units = units_order_by_norm.get(nm)
            if ordered_units:
                units_sorted = [u for u in ordered_units if u in units_map] + [u for u in sorted(units_map.keys()) if u not in ordered_units]
            else:
                units_sorted = sorted(units_map.keys())

            parts = []
            for u in units_sorted:
                harga_disp = format_rupiah(units_map[u])
                parts.append(f"<code>{harga_disp}</code> / {_title_unit(u)}")

            if parts:
                teks += f"• <b>{nama_disp}</b> — " + " | ".join(parts) + "\n"

    teks += f"\n{divider}"
    return teks


def normalisasi_tanggal_gs(tgl_str):
    """
    Normalisasi tanggal dari berbagai format (teks, slash, titik) ke format standar DD-MM-YYYY.
    Mendukung input: '21 april 2026', '21/04/2026', '21.04.26', 'kemarin', 'besok', dll.
    """
    if not tgl_str:
        return ""
    tgl_norm = str(tgl_str).lower().strip()
    if not tgl_norm:
        return ""

    hari_ini = datetime.now()

    teks_clean = re.sub(r"\s+", " ", tgl_norm).strip()
    if any(k in teks_clean for k in ["hari ini", "hariini", "hr ini", "hri ini", "today"]):
        return hari_ini.strftime("%d-%m-%Y")

    if any(k in teks_clean for k in ["kemarin", "kmrin", "kmarin", "yesterday"]):
        return (hari_ini - timedelta(days=1)).strftime("%d-%m-%Y")
    if any(k in teks_clean for k in ["besok", "bsok", "tomorrow"]):
        return (hari_ini + timedelta(days=1)).strftime("%d-%m-%Y")
    if "lusa" in teks_clean:
        return (hari_ini + timedelta(days=2)).strftime("%d-%m-%Y")

    m = re.search(r"\b(\d+)\s*(hari|hri)\s*(lalu|yang lalu)\b", teks_clean)
    if m:
        days = int(m.group(1))
        return (hari_ini - timedelta(days=days)).strftime("%d-%m-%Y")
    m = re.search(r"\b(\d+)\s*(hari|hri)\s*(lagi|ke depan)\b", teks_clean)
    if m:
        days = int(m.group(1))
        return (hari_ini + timedelta(days=days)).strftime("%d-%m-%Y")
    m = re.search(r"\b(\d+)?\s*(minggu|mgg)\s*(lalu|yang lalu)\b", teks_clean)
    if m:
        n = int(m.group(1) or 1)
        return (hari_ini - timedelta(days=7 * n)).strftime("%d-%m-%Y")
    m = re.search(r"\b(\d+)?\s*(minggu|mgg)\s*(lagi|ke depan)\b", teks_clean)
    if m:
        n = int(m.group(1) or 1)
        return (hari_ini + timedelta(days=7 * n)).strftime("%d-%m-%Y")
    m = re.search(r"\b(\d+)?\s*(bulan|bln)\s*(lalu|yang lalu)\b", teks_clean)
    if m:
        n = int(m.group(1) or 1)
        return (hari_ini - timedelta(days=30 * n)).strftime("%d-%m-%Y")
    m = re.search(r"\b(\d+)?\s*(bulan|bln)\s*(lagi|ke depan)\b", teks_clean)
    if m:
        n = int(m.group(1) or 1)
        return (hari_ini + timedelta(days=30 * n)).strftime("%d-%m-%Y")

    # Hapus nama hari (opsional) agar parsing tanggal lebih stabil
    for nama_hari in [
        "senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu", "ahad",
        "sen", "sel", "rab", "kam", "jum", "jmt", "sab", "min", "ahd",
    ]:
        tgl_norm = re.sub(rf"\b{nama_hari}\b", " ", tgl_norm)
    
    # 1. Cek apakah ada nama bulan teks di dalamnya (misal "21 april 2026")
    bulan_dict = {
        "januari": "01", "jan": "01", "februari": "02", "feb": "02",
        "maret": "03", "mar": "03", "april": "04", "apr": "04",
        "mei": "05", "juni": "06", "jun": "06", "juli": "07", "jul": "07",
        "agustus": "08", "agu": "08", "agus": "08", "agt": "08",
        "september": "09", "sep": "09", "sept": "09",
        "oktober": "10", "okt": "10",
        "november": "11", "nov": "11", "nop": "11", "nopember": "11",
        "desember": "12", "des": "12"
    }
    
    for nama_bln, angka_bln in bulan_dict.items():
        tgl_norm = re.sub(rf"\b{re.escape(nama_bln)}\b", angka_bln, tgl_norm)
            
    # Ganti sembarang spasi, titik, slash dengan strip
    tgl_norm = re.sub(r'[-/\.\s]+', '-', tgl_norm).strip()
    # Hilangkan strip di awal atau akhir jika ada
    tgl_norm = tgl_norm.strip('-')
    
    parts = tgl_norm.split('-')
    
    # Ambil blok numerik saja (membuang bagian jam seperti 00:00:00 jika ada)
    angka_parts = [p for p in parts if p.isdigit()]
    
    try:
        def _to_year(y_raw: int):
            if y_raw < 100:
                return 2000 + y_raw
            return y_raw

        def _valid_date(d: int, m: int, y: int):
            try:
                datetime(year=y, month=m, day=d)
                return True
            except Exception:
                return False

        if len(angka_parts) >= 3:
            # Coba deteksi mana yang Tahun (4 digit)
            p1, p2, p3 = angka_parts[0], angka_parts[1], angka_parts[2]
            
            if len(p1) == 4: # YYYY-MM-DD
                y, m, d = int(p1), int(p2), int(p3)
            elif len(p3) == 4: # DD-MM-YYYY
                a, b, y_raw = int(p1), int(p2), int(p3)
                y = _to_year(y_raw)
                if a <= 12 and b > 12:
                    m, d = a, b
                else:
                    d, m = a, b
            else: # DD-MM-YY atau MM-DD-YY
                a, b, y_raw = int(p1), int(p2), int(p3)
                y = _to_year(y_raw)
                if a <= 12 and b > 12:
                    m, d = a, b
                else:
                    d, m = a, b

            if not (1 <= m <= 12 and 1 <= d <= 31) or not _valid_date(d, m, y):
                return ""
            return f"{d:02d}-{m:02d}-{y}"
                
        elif len(angka_parts) == 2:
            a = int(angka_parts[0])
            b = int(angka_parts[1])
            # MM-YYYY atau YYYY-MM
            if len(angka_parts[0]) == 4 and 1 <= b <= 12:
                return f"{b:02d}-{a}"
            if len(angka_parts[1]) == 4 and 1 <= a <= 12:
                return f"{a:02d}-{b}"

            # User hanya memasukkan DD-MM (contoh: 12-04) atau MM-DD (contoh: 04-12)
            if a <= 12 and b > 12:
                m, d = a, b
            else:
                d, m = a, b
            y = hari_ini.year
            if not (1 <= m <= 12 and 1 <= d <= 31) or not _valid_date(d, m, y):
                return ""
            return f"{d:02d}-{m:02d}-{y}"
            
        elif len(angka_parts) == 1:
            # User HANYA memasukkan angka hari (contoh: 12)
            d = int(angka_parts[0])
            m = hari_ini.month
            y = hari_ini.year
            if not (1 <= d <= 31) or not _valid_date(d, m, y):
                return ""
            return f"{d:02d}-{m:02d}-{y}"
    except Exception:
        return ""
        
    return ""


# =====================================================
# MASTER BARANG
# =====================================================
def get_all_barang(db_barang=None):
    """Kembalikan semua barang sebagai list of dict."""
    try:
        rows = db_client.get_all_barang_db()
        result = []
        for r in rows:
            result.append({
                "id":      r["id"],
                "nama":    r["nama_barang"],
                "harga":   r["harga"],
                "satuan":  r["satuan"] or "pcs",
                "row_idx": r["id"] # Menggunakan ID DB sebagai row_idx
            })
        return result
    except Exception as e:
        print(f"Error get_all_barang: {e}")
        return []

def tambah_barang(db_barang, nama, harga, satuan="pcs"):
    """Insert barang baru, return ID."""
    try:
        res = db_client.insert_barang_db(nama, int(harga), satuan)
        if res:
            _invalidate_cache("barang")
            return res[0]["id"]
    except Exception as e:
        e_str = str(e)
        if "23505" in e_str:
            try:
                semua = get_all_barang(db_barang)
                key_n = str(nama or "").strip().lower()
                key_u = str(satuan or "").strip().lower()
                row_idx = next(
                    (
                        b.get("row_idx")
                        for b in semua
                        if str(b.get("nama", "")).strip().lower() == key_n
                        and str(b.get("satuan", "")).strip().lower() == key_u
                    ),
                    None,
                )
                if row_idx:
                    update_barang(db_barang, row_idx, harga=int(harga), satuan=satuan)
                    return row_idx
            except Exception:
                pass
        print(f"Error tambah_barang: {e}")
        raise e
    return None

def update_barang(db_barang, row_idx, nama=None, harga=None, satuan=None):
    """Update field barang berdasarkan ID (row_idx mapping)."""
    try:
        db_client.update_barang_db(row_idx, nama=nama, harga=int(harga) if harga else None, satuan=satuan)
        _invalidate_cache("barang")
    except Exception as e:
        print(f"Error update_barang: {e}")
        raise e

def hapus_barang(db_barang, row_idx):
    """Hapus baris barang berdasarkan ID."""
    try:
        db_client.delete_barang_db(row_idx)
        _invalidate_cache("barang")
    except Exception as e:
        print(f"Error hapus_barang: {e}")
        raise e


def hapus_semua_barang(db_barang=None):
    try:
        db_client.delete_all_barang_db()
        _invalidate_cache("barang")
    except Exception as e:
        print(f"Error hapus_semua_barang: {e}")
        raise e


def cari_harga_default(db_barang, nama_barang, satuan_cari=None, semua_barang=None):
    """
    Cari harga default berdasarkan nama barang (exact → partial → fuzzy).
    Mendukung multi-match dan filter Satuan: Return list of dict [{nama, harga, satuan}, ...]
    If satuan_cari is provided but no matches found, return first match regardless of satuan
    Skip barang with harga <= 0
    """
    semua = semua_barang if semua_barang is not None else get_all_barang(db_barang)
    if not semua:
        return []

    nama_cari = nama_barang.strip().lower()
    nama_cari_clean = re.sub(r'[^\w\s]', '', nama_cari)
    
    if satuan_cari:
        satuan_cari = str(satuan_cari).strip().lower()

    matches = []

    # 1. Exact match (case-insensitive)
    for b in semua:
        if b["harga"] <= 0:
            continue
        nama_db = b["nama"].strip().lower()
        if nama_cari == nama_db or nama_cari_clean == re.sub(r'[^\w\s]', '', nama_db):
            matches.append({"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]})
    
    # Filter berdasarkan satuan jika ada exact match nama
    if matches and satuan_cari:
        filtered = [m for m in matches if m["satuan"].strip().lower() == satuan_cari]
        if filtered:
            return filtered
    elif matches:
        return matches

    matches = []

    # 2. Partial match
    for b in semua:
        if b["harga"] <= 0:
            continue
        nama_db = b["nama"].strip().lower()
        nama_db_clean = re.sub(r'[^\w\s]', '', nama_db)
        if nama_cari in nama_db or nama_db in nama_cari or \
           nama_cari_clean in nama_db_clean or nama_db_clean in nama_cari_clean:
            matches.append({"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]})
    
    if matches and satuan_cari:
        filtered = [m for m in matches if m["satuan"].strip().lower() == satuan_cari]
        if filtered:
            return filtered
    elif matches:
        return matches

    matches = []

    # 3. Fuzzy match (skor >= 70)
    daftar_nama = [b["nama"] for b in semua if b["harga"] > 0]
    hasil_list = process.extract(nama_cari, daftar_nama, scorer=fuzz.token_sort_ratio, limit=10)
    for res in hasil_list:
        if res[1] >= 70:
            for b in semua:
                if b["nama"] == res[0] and b["harga"] > 0:
                    matches.append({"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]})
    
    if matches:
        if satuan_cari:
            filtered = [m for m in matches if m["satuan"].strip().lower() == satuan_cari]
            if filtered:
                return filtered
        # If satuan not found or not provided, return all matches
        return matches

    return []


# =====================================================
# MASTER SATUAN
# =====================================================
def get_all_satuan():
    try:
        rows = db_client.get_all_satuan_db()
        return rows
    except Exception as e:
        print(f"Error get_all_satuan: {e}")
        return []


def tambah_satuan(nama_satuan):
    try:
        # First check if satuan already exists
        all_satuan = get_all_satuan()
        for s in all_satuan:
            if s["nama_satuan"].lower() == nama_satuan.lower():
                return s["id"]
        
        # If not, insert new one
        res = db_client.insert_satuan_db(nama_satuan)
        return res[0]["id"] if res else None
    except Exception as e:
        print(f"Error tambah_satuan: {e}")
        raise e


def update_satuan(id_satuan, nama_satuan=None):
    try:
        db_client.update_satuan_db(id_satuan, nama_satuan=nama_satuan)
    except Exception as e:
        print(f"Error update_satuan: {e}")
        raise e


def hapus_satuan(id_satuan):
    try:
        db_client.delete_satuan_db(id_satuan)
    except Exception as e:
        print(f"Error hapus_satuan: {e}")
        raise e


# =====================================================
# MASTER METODE PEMBAYARAN
# =====================================================
def get_all_metode(db_metode=None):
    """Kembalikan semua metode sebagai list of dict."""
    try:
        rows = db_client.get_all_metode_db()
        result = []
        for r in rows:
            result.append({
                "id":      r["id"],
                "nama":    r["nama_metode"],
                "keyword": r["kata_kunci"],
                "row_idx": r["id"]
            })
        return result
    except Exception as e:
        print(f"Error get_all_metode: {e}")
        return []

def tambah_metode(db_metode, nama, keyword_alias=""):
    try:
        res = db_client.insert_metode_db(nama, keyword_alias)
        if res:
            _invalidate_cache("metode_mapping")
            return res[0]["id"]
    except Exception as e:
        print(f"Error tambah_metode: {e}")
    return None

def update_metode(db_metode, row_idx, nama=None, keyword=None):
    try:
        db_client.update_metode_db(row_idx, nama=nama, keyword=keyword)
        _invalidate_cache("metode_mapping")
    except Exception as e:
        print(f"Error update_metode: {e}")

def hapus_metode(db_metode, row_idx):
    try:
        db_client.delete_metode_db(row_idx)
        _invalidate_cache("metode_mapping")
    except Exception as e:
        print(f"Error hapus_metode: {e}")

def muat_metode_keywords(db_metode=None):
    """
    Build dict {keyword_lower: nama_metode} dari tabel Master Metode.
    Digunakan oleh NLP processor untuk deteksi metode pembayaran dinamis.
    """
    mapping = {}
    for m in get_all_metode(db_metode):
        if not m["keyword"]: continue
        for kw in m["keyword"].split(","):
            kw = kw.strip().lower()
            if kw:
                mapping[kw] = m["nama"]
    return mapping
