import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client
from supabase.lib.client_options import ClientOptions

load_dotenv()

logger = logging.getLogger("bot_logger")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_supabase_client: Client = None


def get_supabase() -> Client:
    """Menginisialisasi dan mengembalikan instance Supabase client (Singleton)."""
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.error("SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di environment.")
            raise ValueError("Supabase credentials missing.")
        try:
            try:
                timeout_pg = int(os.getenv("SUPABASE_POSTGREST_TIMEOUT", "30"))
            except Exception:
                timeout_pg = 30
            try:
                timeout_storage = int(os.getenv("SUPABASE_STORAGE_TIMEOUT", "20"))
            except Exception:
                timeout_storage = 20

            options = ClientOptions(
                postgrest_client_timeout=max(5, min(timeout_pg, 180)),
                storage_client_timeout=max(5, min(timeout_storage, 180)),
            )
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
            logger.info("[OK] Berhasil terhubung ke Supabase!")
        except Exception as e:
            logger.error(f"[ERROR] Gagal inisialisasi Supabase: {e}")
            raise
    return _supabase_client


# =====================================================
# OPERASI MASTER BARANG
# =====================================================
def get_all_barang_db():
    supabase = get_supabase()
    response = supabase.table("master_barang").select("*").order("id").execute()
    return response.data


def insert_barang_db(nama, harga, satuan="pcs"):
    supabase = get_supabase()
    data = {"nama_barang": nama, "harga": harga, "satuan": satuan}
    try:
        response = (
            supabase.table("master_barang").upsert(data, on_conflict="nama_barang,satuan").execute()
        )
        return response.data
    except Exception:
        response = supabase.table("master_barang").insert(data).execute()
        return response.data


def update_barang_db(id_barang, nama=None, harga=None, satuan=None):
    supabase = get_supabase()
    data = {}
    if nama is not None:
        data["nama_barang"] = nama
    if harga is not None:
        data["harga"] = harga
    if satuan is not None:
        data["satuan"] = satuan
    response = supabase.table("master_barang").update(data).eq("id", id_barang).execute()
    return response.data


def delete_barang_db(id_barang):
    supabase = get_supabase()
    response = supabase.table("master_barang").delete().eq("id", id_barang).execute()
    return response.data


def delete_all_barang_db():
    supabase = get_supabase()
    response = supabase.table("master_barang").delete().neq("id", 0).execute()
    return response.data


# =====================================================
# OPERASI MASTER SATUAN
# =====================================================
def get_all_satuan_db():
    supabase = get_supabase()
    response = supabase.table("master_satuan").select("*").order("nama_satuan").execute()
    return response.data


def insert_satuan_db(nama_satuan):
    supabase = get_supabase()
    data = {"nama_satuan": nama_satuan}
    try:
        response = supabase.table("master_satuan").upsert(data, on_conflict="nama_satuan").execute()
    except Exception:
        response = supabase.table("master_satuan").insert(data).execute()
    return response.data


def update_satuan_db(id_satuan, nama_satuan=None):
    supabase = get_supabase()
    data = {}
    if nama_satuan is not None:
        data["nama_satuan"] = nama_satuan
    response = supabase.table("master_satuan").update(data).eq("id", id_satuan).execute()
    return response.data


def delete_satuan_db(id_satuan):
    supabase = get_supabase()
    response = supabase.table("master_satuan").delete().eq("id", id_satuan).execute()
    return response.data


# =====================================================
# OPERASI MASTER METODE
# =====================================================
def get_all_metode_db():
    supabase = get_supabase()
    response = supabase.table("master_metode").select("*").order("id").execute()
    return response.data


def insert_metode_db(nama, keyword):
    supabase = get_supabase()
    data = {"nama_metode": nama, "kata_kunci": keyword}
    response = supabase.table("master_metode").insert(data).execute()
    return response.data


def update_metode_db(id_metode, nama=None, keyword=None):
    supabase = get_supabase()
    data = {}
    if nama is not None:
        data["nama_metode"] = nama
    if keyword is not None:
        data["kata_kunci"] = keyword
    response = supabase.table("master_metode").update(data).eq("id", id_metode).execute()
    return response.data


def delete_metode_db(id_metode):
    supabase = get_supabase()
    response = supabase.table("master_metode").delete().eq("id", id_metode).execute()
    return response.data


# =====================================================
# OPERASI TRANSAKSI
# =====================================================
def insert_transaksi_db(data_transaksi):
    supabase = get_supabase()
    response = supabase.table("transaksi").insert(data_transaksi).execute()
    data = getattr(response, "data", None)
    err = getattr(response, "error", None)
    if err:
        raise RuntimeError(str(err))
    if data:
        return data
    dup_id = find_duplicate_transaksi_flat(data_transaksi)
    if dup_id:
        cek = supabase.table("transaksi").select("*").eq("id", dup_id).limit(1).execute()
        if getattr(cek, "data", None):
            return cek.data
    raise RuntimeError("Insert transaksi tidak terkonfirmasi (response kosong).")


def update_transaksi_db(id_transaksi, data_update):
    supabase = get_supabase()
    response = supabase.table("transaksi").update(data_update).eq("id", id_transaksi).execute()
    return response.data


def delete_transaksi_db(id_transaksi):
    supabase = get_supabase()
    response = supabase.table("transaksi").delete().eq("id", id_transaksi).execute()
    return response.data


def get_semua_transaksi_db(columns="*"):
    supabase = get_supabase()
    response = supabase.table("transaksi").select(columns).order("id").execute()
    return response.data


def get_transaksi_by_filter(kolom, nilai, operator="eq", columns="*"):
    """
    Fungsi native Supabase untuk mengambil transaksi dengan filter (eq, like, ilike, gte, lte).
    Mencegah pengambilan seluruh data ke RAM.
    """
    supabase = get_supabase()
    query = supabase.table("transaksi").select(columns)

    if operator == "eq":
        query = query.eq(kolom, nilai)
    elif operator == "ilike":
        query = query.ilike(kolom, f"%{nilai}%")
    elif operator == "like":
        query = query.like(kolom, f"%{nilai}%")
    elif operator == "gte":
        query = query.gte(kolom, nilai)
    elif operator == "lte":
        query = query.lte(kolom, nilai)
    elif operator == "gt":
        query = query.gt(kolom, nilai)

    response = query.order("id").execute()
    return response.data


def get_transaksi_multi_filter(filters, columns="*"):
    """
    Mengambil transaksi dengan banyak filter dinamis secara native (Supabase).
    filters: list of dict [{"kolom": "nama_pelanggan", "nilai": "x", "operator": "ilike"}, ...]
    """
    supabase = get_supabase()
    query = supabase.table("transaksi").select(columns)

    for f in filters:
        k = f["kolom"]
        v = f["nilai"]
        op = f.get("operator", "eq")

        if op == "eq":
            query = query.eq(k, v)
        elif op == "ilike":
            query = query.ilike(k, f"%{v}%")
        elif op == "like":
            query = query.like(k, f"%{v}%")
        elif op == "gte":
            query = query.gte(k, v)
        elif op == "lte":
            query = query.lte(k, v)
        elif op == "gt":
            query = query.gt(k, v)

    response = query.order("id").execute()
    return response.data


def find_duplicate_transaksi_flat(data_flat):
    """
    Cek transaksi duplikat berdasarkan field inti pada tabel 'transaksi'.
    Return id transaksi jika ada, else None.
    """
    try:
        supabase = get_supabase()
        q = supabase.table("transaksi").select("id")
        for k in [
            "tanggal",
            "nama_pelanggan",
            "barang",
            "jumlah_satuan",
            "total",
            "status",
            "metode_pembayaran",
        ]:
            if k in data_flat:
                q = q.eq(k, data_flat[k])
        res = q.order("id", desc=True).limit(1).execute()
        if res.data:
            return res.data[0]["id"]
    except Exception as e:
        logger.error(f"Gagal cek duplikat transaksi: {e}")
    return None


def find_adjacent_duplicate_transaksi_ids(rows=None):
    if rows is None:
        rows = get_semua_transaksi_db()
    rows_sorted = sorted(rows or [], key=lambda r: int(r.get("id") or 0))
    dup_ids = []
    prev_sig = None
    for r in rows_sorted:
        sig = (
            str(r.get("tanggal") or "").strip(),
            str(r.get("nama_pelanggan") or "").strip().lower(),
            str(r.get("barang") or "").strip().lower(),
            str(r.get("jumlah_satuan") or "").strip().lower(),
            str(r.get("harga") or "").strip(),
            str(r.get("total") or "").strip(),
            str(r.get("status") or "").strip().lower(),
            str(r.get("metode_pembayaran") or "").strip().lower(),
            str(r.get("tagihan") or "").strip(),
            str(r.get("uang_masuk") or "").strip(),
        )
        if prev_sig is not None and sig == prev_sig:
            rid = r.get("id")
            if rid is not None:
                dup_ids.append(rid)
        else:
            prev_sig = sig
    return dup_ids


def delete_transaksi_ids(ids):
    if not ids:
        return 0
    supabase = get_supabase()
    ok = 0
    for rid in ids:
        try:
            supabase.table("transaksi").delete().eq("id", rid).execute()
            ok += 1
        except Exception as e:
            logger.error(f"Gagal hapus transaksi id={rid}: {e}")
    return ok


# =====================================================
# OPERASI HISTORI PELUNASAN
# =====================================================
def insert_histori_pelunasan_db(data_histori):
    supabase = get_supabase()
    response = supabase.table("histori_pelunasan").insert(data_histori).execute()
    return response.data


# =====================================================
# OPERASI RELASIONAL (FASE 2)
# =====================================================
def get_or_create_pelanggan(nama):
    """Mencari pelanggan berdasarkan nama, jika tidak ada, buat baru dan kembalikan ID-nya."""
    supabase = get_supabase()
    res = supabase.table("pelanggan").select("id").ilike("nama", nama).execute()
    if res.data:
        return res.data[0]["id"]
    # Jika tidak ada, insert baru
    ins = supabase.table("pelanggan").insert({"nama": nama}).execute()
    return ins.data[0]["id"] if ins.data else None


def insert_pesanan(data_pesanan):
    """Menyimpan data pesanan induk."""
    supabase = get_supabase()
    response = supabase.table("pesanan").insert(data_pesanan).execute()
    return response.data


def insert_pesanan_item(data_item):
    """Menyimpan rincian item ke dalam suatu pesanan."""
    supabase = get_supabase()
    response = supabase.table("pesanan_item").insert(data_item).execute()
    return response.data


# =====================================================
# UTILS & KEEP ALIVE
# =====================================================
def get_pesanan_by_filter(kolom, nilai, operator="eq"):
    """Query pesanan beserta pelanggan dan item-nya (menggunakan join/relasi)."""
    supabase = get_supabase()
    # supabase-py mendukung relasi, misal pesanan(..., pelanggan(nama), pesanan_item(...))
    query = supabase.table("pesanan").select("*, pelanggan(*), pesanan_item(*)")

    if operator == "eq":
        query = query.eq(kolom, nilai)
    elif operator == "ilike":
        query = query.ilike(kolom, f"%{nilai}%")
    elif operator == "gt":
        query = query.gt(kolom, nilai)

    response = query.order("id").execute()
    return response.data


# =====================================================
# OPERASI BOT SESSIONS (PERSISTENSI STATUS SESI)
# =====================================================
def load_session_db(chat_id):
    """Mengambil data sesi dari tabel bot_sessions di database."""
    try:
        supabase = get_supabase()
        res = supabase.table("bot_sessions").select("session_data").eq("chat_id", chat_id).execute()
        if res.data:
            return res.data[0]["session_data"]
    except Exception as e:
        if "bot_sessions" in str(e):
            logger.warning(
                "[NOTICE] Menggunakan sesi RAM lokal karena tabel 'bot_sessions' belum dibuat di Supabase."
            )
        else:
            logger.error(f"Gagal memuat sesi chat {chat_id}: {e}")
    return {}


def save_session_db(chat_id, data):
    """Menyimpan data sesi (upsert) ke tabel bot_sessions di database."""
    try:
        supabase = get_supabase()
        payload = {"chat_id": chat_id, "session_data": data}
        res = supabase.table("bot_sessions").upsert(payload, on_conflict="chat_id").execute()
        return res.data
    except Exception as e:
        if "bot_sessions" not in str(e):
            logger.error(f"Gagal menyimpan sesi chat {chat_id}: {e}")
        return None


# =====================================================
# KEEP-ALIVE (ANTI-PAUSE)
# =====================================================
def ping_supabase_keep_alive():
    """
    Melakukan operasi baca ringan untuk mencegah Supabase menjeda proyek (Inactivity Pause).
    Supabase Free Tier menjeda proyek setelah 1 minggu tidak ada aktivitas.
    """
    try:
        supabase = get_supabase()
        # Query ringan: cek koneksi dengan mengambil 1 ID dari master_barang
        supabase.table("master_barang").select("id").limit(1).execute()
        logger.info("[KEEP-ALIVE] Supabase heartbeat dikirim sukses.")
        return True
    except Exception as e:
        logger.error(f"[KEEP-ALIVE] Gagal ping Supabase: {e}")
        return False
