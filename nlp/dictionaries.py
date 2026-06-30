import re
import logging

from nlp.embedded_data import NORMALIZATION_DICT
from core.master_data import get_all_barang, MASTER_BARANG_CATALOG, get_all_satuan

logger = logging.getLogger(__name__)

# Data statis KAMUS_ALIAS (fallback jika database kosong)
KAMUS_ALIAS_STATIS = {
    # === PERMEN COKLAT ===
    "permen coklat": "Permen Coklat",
    "coklat": "Permen Coklat",
    "millo": "Permen Coklat",
    "permen millo": "Permen Coklat",
    "prmen coklat": "Permen Coklat",
    "permen cokelat": "Permen Coklat",
    "prmen": "Permen Coklat",
    "willo": "Willo",
    "permen willo": "Willo",
    "wilo": "Willo",
    "wiilo": "Willo",
    "ewillo": "Willo",
    "bemmbeng": "Bembeng",
    "bembeng": "Bembeng",
    "bengbeng": "Bembeng",
    "beng-beng": "Bembeng",
    "beng beng": "Bembeng",
    "permen bemmbeng": "Bembeng",
    "permen bembeng": "Bembeng",
    "permen bengbeng": "Bembeng",
    "beem-beeng": "Bembeng",
    "adangrow": "Adangrow",
    "chocholetus": "Cholatos",
    "cholatos": "Cholatos",
    "miksu": "Miksu",
    "getbory": "Getbory",
    "siiperquuen": "Getbory",
    
    # === PERMEN GENERIK ===
    "permen": "Lolipop",
    "permen toples": "Lolipop",
    "permen dus": "Lolipop",
    
    # === PERMEN LOLIPOP ===
    "permen lolipop": "Lolipop",
    "lolipop": "Lolipop",
    "lalipop": "Lolipop",
    "permen loli": "Lolipop",
    "lolipop": "Lolipop",
    "l0lipop": "Lolipop",
    "loli pop": "Lolipop",
    "lolli pop": "Lolipop",
    "lolipop": "Lolipop",
    "lolypop": "Lolipop",
    "lolypopp": "Lolipop",
    "lollippop": "Lolipop",
    "lollipop": "Lolipop",
    "lollipop": "Lolipop",
    "lolopop": "Lolipop",
    "l0llip0p": "Lolipop",
    "l0lipop": "Lolipop",
    "permen l0lipop": "Lolipop",
    
    # === ROTI PIA ===
    "pia potong": "Roti Pia (Potong)",
    "pia roda": "Roti Pia (Roda)",
    "pia bulus": "Roti Pia (Bulus)",
    "roti pia potong": "Roti Pia (Potong)",
    "roti pia roda": "Roti Pia (Roda)",
    "bulus": "Roti Pia (Bulus)",
    "bulu": "Roti Pia (Bulus)",
    "roti pia bulus": "Roti Pia (Bulus)",
    "roti pia": "Roti Pia (Generik)",
    "pia": "Roti Pia (Generik)",
    "bakpia": "Roti Pia (Generik)",
    "rti pia": "Roti Pia (Generik)",
    "pia roti": "Roti Pia (Generik)",
    "pita": "Roti Pia (Generik)",
    
    # === BROWNIS ===
    "roti brownis": "Brownis",
    "brownis": "Brownis",
    "bronis": "Brownis",
    "roti bronis": "Brownis",
    "brownies": "Brownis",
    "brownis bungkus": "Brownis",
    
    # === SERBUK ===
    "makanan serbuk": "Serbuk",
    "serbuk": "Serbuk",
    "mknan serbuk": "Serbuk",
    "makanan srbk": "Serbuk",
    "hanya serbuk": "Serbuk",
    "salju": "Salju",
    
    # === JELLY / JELI ===
    "serbuk jelly": "Serbuk Jelly",
    "serbuk jelli": "Serbuk Jelly",
    "serbuk jeli": "Serbuk Jelly",
    "jelly": "Serbuk Jelly",
    "jeli": "Serbuk Jelly",
    "jelli": "Serbuk Jelly",
    "serbuk yeli": "Serbuk Jelly",
    "yelli": "Serbuk Jelly",

    # === COKLAT VARIAN ===
    "coklat kubus": "Coklat Kubus",
    "kubus": "Coklat Kubus",
    "piramide": "Coklat Piramide",
    "piramid": "Coklat Piramide",

    # === MESES ===
    "meses": "Meses",
    "meises": "Meses",
    "messes": "Meses",
    "messis": "Meses",
    "messej": "Meses",
    "mses": "Meses",
    "mesis": "Meses",
    "meses coklat": "Meses",
    "coklat meses": "Meses",
    "meses warna": "Meses",
    "meses campur": "Meses",

    # === TAMBAHAN ITEM UMKM (Lengkap) ===
    "keripik": "Keripik",
    "kripik": "Keripik",
    "krupuk": "Kerupuk",
    "kerupuk": "Kerupuk",
    "krpuk": "Kerupuk",
    
    "mie instan": "Mie Instan",
    "mie": "Mie",
    "mi": "Mie",
    "indomie": "Indomie",
    "sarimi": "Sarimi",
    
    "snack": "Snack",
    "makanan ringan": "Snack",
    "jajanan": "Snack",
    "ciki": "Snack",
    
    "minuman": "Minuman",
    "minuman dingin": "Minuman",
    "aer": "Air Mineral",
    "air mineral": "Air Mineral",
    "aqua": "Air Mineral",
    
    "kopi": "Kopi",
    "kopi sachet": "Kopi",
    "teh": "Teh",
    "susu": "Susu",
    
    "roti": "Roti",
    "kue": "Kue",
    "bolu": "Bolu",
    "biskuit": "Biskuit",
    "biskuat": "Biskuit",
    "biskuwit": "Biskuit",
    
    "kecap": "Kecap",
    "saus": "Saus",
    "saos": "Saus",
    "sambal": "Sambal",
    "sambel": "Sambal",
    
    "minyak": "Minyak Goreng",
    "minyak goreng": "Minyak Goreng",
    "mentega": "Mentega",
    "margarin": "Mentega",
    
    "gula": "Gula",
    "garem": "Garam",
    "garam": "Garam",
    "terigu": "Tepung Terigu",
    "tepung": "Tepung",
}

VALID_UNITS_STATIS = frozenset([
    "dus", "karton", "pcs", "bungkus", "bal", "renceng", "box",
    "kg", "toples", "pack", "buah", "botol", "sachet", "lusin", "paket"
])

def muat_kamus_alias():
    """
    Build KAMUS_ALIAS secara dinamis:
    1. Load nama barang dari database
    2. Tambahkan variasi nama (lowercase, tanpa spasi, dll.)
    3. Gabung dengan KAMUS_ALIAS_STATIS (fallback)
    """
    # Mulai dengan data statis
    kamus = KAMUS_ALIAS_STATIS.copy()
    
    try:
        # Load semua barang dari database
        semua_barang = get_all_barang()
        
        for barang in semua_barang:
            nama_barang = barang["nama"].strip()
            nama_lower = nama_barang.lower()
            
            # Tambahkan mapping dasar (nama_lower → nama_barang)
            if nama_lower not in kamus:
                kamus[nama_lower] = nama_barang
            
            # Tambahkan variasi nama (contoh: tanpa spasi, singkatan umum)
            nama_tanpa_spasi = nama_lower.replace(" ", "")
            if nama_tanpa_spasi not in kamus and nama_tanpa_spasi != nama_lower:
                kamus[nama_tanpa_spasi] = nama_barang
        
        # Tambahkan juga dari MASTER_BARANG_CATALOG
        for group in MASTER_BARANG_CATALOG:
            for item in group.get("items", []):
                nama_item = item["nama"].strip()
                nama_item_lower = nama_item.lower()
                if nama_item_lower not in kamus:
                    kamus[nama_item_lower] = nama_item
        
    except Exception as e:
        logger.error(f"Error loading KAMUS_ALIAS from database: {e}")
    
    return kamus

def muat_valid_units():
    """
    Build VALID_UNITS secara dinamis:
    1. Load satuan dari database
    2. Gabung dengan VALID_UNITS_STATIS (fallback)
    """
    # Mulai dengan data statis
    units = set(VALID_UNITS_STATIS)
    
    try:
        # Load semua satuan dari database
        semua_satuan = get_all_satuan()
        
        for satuan in semua_satuan:
            nama_satuan = satuan["nama_satuan"].strip().lower()
            if nama_satuan:
                units.add(nama_satuan)
        
    except Exception as e:
        logger.error(f"Error loading VALID_UNITS from database: {e}")
    
    return frozenset(units)

# Load KAMUS_ALIAS dan VALID_UNITS secara dinamis saat modul diimpor
KAMUS_ALIAS = muat_kamus_alias()
VALID_UNITS = muat_valid_units()

DAFTAR_KATA_KUNCI = list(KAMUS_ALIAS.keys())

def parse_price_shorthand(text):
    """
    Mengonversi variasi teks harga seperti '10k', '5 jt', '2 jutaan', '1.5jt', '200 rts' menjadi integer.
    """
    if not text: return None
    # Bersihkan spasi dan konversi koma ke titik untuk desimal
    text = text.lower().replace(" ", "").replace(",", ".")
    
    # Deteksi Juta / JT
    match_jt = re.search(r'(\d+(?:\.\d+)?)\s*(?:juta|jt|jutaan)', text)
    if match_jt:
        return int(float(match_jt.group(1)) * 1_000_000)
        
    # Deteksi Ribu / RB / K
    match_rb = re.search(r'(\d+(?:\.\d+)?)\s*(?:ribu|rb|ribuan|k)', text)
    if match_rb:
        return int(float(match_rb.group(1)) * 1_000)

    # Deteksi Ratus / RTS
    match_rt = re.search(r'(\d+(?:\.\d+)?)\s*(?:ratus|rt|rts|ratusan)', text)
    if match_rt:
        return int(float(match_rt.group(1)) * 100)

    # Bersihkan Rp dan titik/koma untuk angka murni
    clean_num = re.sub(r"[^\d]", "", text)
    if clean_num:
        return int(clean_num)
    return None

