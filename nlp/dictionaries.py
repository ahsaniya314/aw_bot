import re
import logging

from nlp.embedded_data import NORMALIZATION_DICT

logger = logging.getLogger(__name__)

KAMUS_ALIAS = {
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

# Enrich KAMUS_ALIAS with known products from normalization dict
try:
    _known_products = NORMALIZATION_DICT.get("entity_patterns", {}).get("produk", {}).get("known_products", [])
    for prod in _known_products:
        if prod.lower() not in KAMUS_ALIAS:
            KAMUS_ALIAS[prod.lower()] = prod.title()
except Exception as e:
    logger.error(f"Error enriching KAMUS_ALIAS: {e}")

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

