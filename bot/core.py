"""
BOT TELEGRAM - Sistem Kasir & Tracking Hutang UMKM A&W Production
=================================================================
Entry Point — Lightweight (~120 baris)
Menginisialisasi bot, database, dan mendaftarkan semua handler dari modul.

Last Updated: May 9, 2026
"""

import logging
import os
from datetime import datetime
from pathlib import Path

os.environ.setdefault("FLAGS_use_mkldnn", "0")
os.environ.setdefault("FLAGS_use_onednn", "0")
os.environ.setdefault("FLAGS_use_oneDNN", "0")

import telebot
from dotenv import load_dotenv

load_dotenv()


# ==========================================
# SETUP LOGGING
# ==========================================
def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.DEBUG)

    # File Handler - Untuk persistensi lokal (jika ada)
    try:
        fh = logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")

    # Stream Handler - Utama untuk Hugging Face / Cloud Logs
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = setup_logging()

# ==========================================
# INISIALISASI BOT TELEGRAM DENGAN RETRY
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("[FATAL] TELEGRAM_BOT_TOKEN tidak ditemukan di file .env!")
    raise ValueError("TELEGRAM_BOT_TOKEN missing from .env")

from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import RequestException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


# Decorator untuk retry otomatis hanya pada kesalahan jaringan.
# Jangan retry ApiTelegramException generik karena banyak error Telegram
# bersifat final/non-retriable (mis. message is not modified, callback expired,
# message can't be edited) dan justru membuat semua respons terasa lambat.
def telegram_retry(func):
    @retry(
        stop=stop_after_attempt(5),  # Coba 5 kali
        wait=wait_exponential(multiplier=1, min=2, max=10),  # Tunggu 2, 4, 8, 10 detik
        retry=retry_if_exception_type((RequestException, RequestsConnectionError)),
        reraise=True,
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, num_threads=20)

# Hanya wrap method yang berhubungan dengan pengiriman/editan pesan (dan safe_send/safe_edit)
retry_methods = [
    "send_message",
    "send_photo",
    "send_document",
    "send_audio",
    "send_video",
    "send_sticker",
    "send_animation",
    "send_voice",
    "send_video_note",
    "send_location",
    "send_venue",
    "send_contact",
    "send_poll",
    "send_dice",
    "send_chat_action",
    "edit_message_text",
    "edit_message_caption",
    "edit_message_media",
    "edit_message_reply_markup",
    "delete_message",
    "answer_callback_query",
]
for method_name in retry_methods:
    if hasattr(bot, method_name):
        original_method = getattr(bot, method_name)
        setattr(bot, method_name, telegram_retry(original_method))

logger.info("[OK] Bot Telegram berhasil diinisialisasi dengan fitur retry otomatis")

from core.master_data import HEADERS_HISTORI_LUNAS, HEADERS_MASTER_BARANG, HEADERS_MASTER_METODE

# ==========================================
# INISIALISASI DATABASE SUPABASE
# ==========================================
from database import db_client
from database.gspread_mock import SupabaseWorksheet

try:
    logger.info("[INIT] Menghubungkan ke Supabase Database...")
    supabase = db_client.get_supabase()
    supabase.table("master_barang").select("id").limit(1).execute()
    IS_DB_CONNECTED = True

    db_transaksi = SupabaseWorksheet(
        "transaksi",
        [
            "Tanggal",
            "Nama",
            "Barang",
            "Jumlah",
            "Harga",
            "Total",
            "Status",
            "Metode",
            "Tagihan",
            "Uang Masuk",
        ],
    )
    db_barang = SupabaseWorksheet("master_barang", HEADERS_MASTER_BARANG)
    db_metode = SupabaseWorksheet("master_metode", HEADERS_MASTER_METODE)
    db_histori = SupabaseWorksheet("histori_pelunasan", HEADERS_HISTORI_LUNAS)
    logger.info("[OK] Berhasil terhubung ke Database!")
except Exception as e:
    IS_DB_CONNECTED = False
    db_transaksi = db_barang = db_metode = db_histori = None
    logger.warning(f"⚠️ Gagal terhubung ke Database. Mode Offline. Error: {e}")

# ==========================================
# INISIALISASI SHARED CONTEXT (DI)
# ==========================================
from core.bot_context import ctx
from services.cache_manager import GSpreadCache
from services.ocr_service import OCRService
from services.session_manager import UserSessions
from utils.security import RateLimiter

ADMIN_IDS_STR = os.getenv("TELEGRAM_BOT_ADMIN_IDS", "")
AUTHORIZED_ADMINS = [int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip().isdigit()]

# Inisialisasi Service Terpadu
ctx.bot = bot
ctx.user_sessions = UserSessions()
ctx.db_transaksi = db_transaksi
ctx.db_barang = db_barang
ctx.db_metode = db_metode
ctx.db_histori = db_histori
ctx.gs_cache = GSpreadCache(expiry_minutes=5)
ctx.IS_DB_CONNECTED = IS_DB_CONNECTED
ctx.rate_limiter = RateLimiter(max_requests=20, time_window=60)
ctx.ocr_service = OCRService()
ctx.AUTHORIZED_ADMINS = AUTHORIZED_ADMINS
ctx.BUILD_ID = os.getenv("BOT_BUILD_ID") or datetime.now().strftime("%Y%m%d-%H%M%S")
ctx.SHOW_BUILD = str(os.getenv("BOT_SHOW_BUILD", "1")).strip().lower() not in {
    "0",
    "false",
    "no",
    "off",
}

# ==========================================
# REGISTER SEMUA HANDLER DARI MODUL
# ==========================================
from handlers import register_all_handlers

register_all_handlers(bot)

logger.info("[OK] Semua handler terdaftar dari modul")

# ==========================================
# MAIN ENTRY POINT
