"""
Security Utilities — Rate Limiting, RBAC, Input Sanitization, Safe Edit
"""

import json
import logging
import os
import re
import traceback
import urllib.request
from datetime import datetime
from functools import wraps

from core.bot_context import ctx

logger = logging.getLogger("bot_logger")


# ==========================================
# SECURITY: Rate Limiting Helper
# ==========================================
class RateLimiter:
    """Simple rate limiter untuk mencegah spam"""

    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window  # dalam detik
        self.user_requests = {}

    def is_allowed(self, user_id):
        """Check apakah user boleh melakukan request"""
        now = datetime.now()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        # Hapus request lama (> time_window)
        self.user_requests[user_id] = [
            req_time
            for req_time in self.user_requests[user_id]
            if (now - req_time).total_seconds() < self.time_window
        ]

        # Check apakah sudah exceed limit
        if len(self.user_requests[user_id]) >= self.max_requests:
            return False

        # Add current request
        self.user_requests[user_id].append(now)
        return True


# ==========================================
# SECURITY: Role-Based Access Control (RBAC)
# ==========================================
def authorized_only(func):
    """Decorator untuk membatasi akses bot hanya untuk admin terdaftar."""

    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        try:
            # Handle both message and callback_query objects
            user_id = obj.from_user.id
            func_name = func.__name__
            obj_type = type(obj).__name__

            logger.debug(
                f"[AUTH] Checking access for user {user_id} → {func_name} (type: {obj_type})"
            )

            # Jika AUTHORIZED_ADMINS kosong, izinkan semua (mode pengembangan/transisi)
            # Jika sudah diisi, blokir user asing.
            if ctx.AUTHORIZED_ADMINS and user_id not in ctx.AUTHORIZED_ADMINS:
                logger.warning(
                    f"[AUTH] BLOCKED: Akses tidak sah dari User ID {user_id} → {func_name}"
                )
                try:
                    ctx.bot.reply_to(
                        obj,
                        f"🚫 <b>Akses Ditolak.</b>\nID Telegram Anda (<code>{user_id}</code>) belum terdaftar sebagai pengelola sistem kasir ini.\n\n"
                        f"💡 <i>Silakan salin ID di atas dan masukkan ke variabel <code>TELEGRAM_BOT_ADMIN_IDS</code> di dalam file <code>.env</code> Anda!</i>",
                        parse_mode="HTML",
                    )
                except Exception:
                    pass  # For callback queries, reply_to doesn't work anyway
                return

            logger.debug(f"[AUTH] ALLOWED: User {user_id} → {func_name}")
            return func(obj, *args, **kwargs)
        except Exception as e:
            logger.error(f"[AUTH] Decorator error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            # Fallback: allow the function to proceed if decorator fails
            return func(obj, *args, **kwargs)

    return wrapper


# ==========================================
# SECURITY: Safe Edit Message
# ==========================================
def safe_edit_message(bot, text, chat_id, message_id, reply_markup=None, parse_mode=None):
    """
    Mengedit pesan dengan aman. Jika pesan tidak ditemukan (error 400),
    akan mengirim pesan baru sebagai fallback.
    """
    try:
        kwargs = {"text": text, "chat_id": chat_id, "message_id": message_id}
        if parse_mode is not None:
            kwargs["parse_mode"] = parse_mode

        if reply_markup is False:
            kwargs["reply_markup"] = None
        elif reply_markup is not None:
            kwargs["reply_markup"] = reply_markup

        return bot.edit_message_text(**kwargs)
    except Exception as e:
        err = str(e).lower()
        if any(
            x in err
            for x in [
                "message to edit not found",
                "message is not modified",
                "message can't be edited",
                "message can`t be edited",
                "can't be edited",
                "message is too old",
                "message_id_invalid",
                "message_too_long",
                "too long",
            ]
        ):
            try:
                send_kwargs = {"chat_id": chat_id, "text": text}
                if parse_mode is not None:
                    send_kwargs["parse_mode"] = parse_mode
                if reply_markup is not False and reply_markup is not None:
                    send_kwargs["reply_markup"] = reply_markup
                return bot.send_message(**send_kwargs)
            except Exception as e2:
                logger.error(f"Error fallback send_message: {e2}")
                return None
        logger.error(f"Error in safe_edit_message: {e}")
        return None


# ==========================================
# SECURITY: Input Sanitization
# ==========================================
def sanitize_input(text):
    """
    Membersihkan input user dari karakter yang berpotensi merusak struktur query atau tampilan.
    Lebih lunak dari sebelumnya agar tidak merusak nama atau bahasa natural.
    """
    if not text:
        return ""

    # Karakter yang benar-benar berisiko tinggi untuk SQL/Script injection
    # Namun tetap izinkan karakter umum seperti ' (kutip) untuk nama seperti "Pak Ma'ruf"
    # dan | (pipe) karena digunakan internal oleh nlp_processor.

    # Kita fokus menghapus karakter kontrol dan script tag
    sanitized = text
    # Hapus tag HTML sederhana
    sanitized = re.sub(r"<[^>]*?>", "", sanitized)

    # Hapus karakter yang jarang digunakan tapi berisiko
    dangerous_chars = [";", "$", "`", "{", "}", "\\"]
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    return sanitized.strip()


def notify_admins(text, parse_mode="HTML"):
    bot = ctx.bot
    if not bot:
        return
    admin_ids = ctx.AUTHORIZED_ADMINS or []
    for admin_id in admin_ids:
        try:
            bot.send_message(admin_id, text, parse_mode=parse_mode)
        except Exception:
            pass


def log_exception(prefix, e):
    try:
        logger.error(f"{prefix}: {e}")
        logger.error(traceback.format_exc())
    except Exception:
        pass


def safe_debug_event(
    payload, env_path=".dbg/save-dashboard-mismatch.env", default_url="http://127.0.0.1:7777/event"
):
    """
    Kirim event debug ke local debug server jika tersedia.
    Jangan pernah memutus flow utama bila file env hilang atau koneksi ditolak.
    """
    url = default_url
    session_id = "save-dashboard-mismatch"

    try:
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                content = f.read()
            for line in content.splitlines():
                if line.startswith("DEBUG_SERVER_URL="):
                    url = line.split("=", 1)[1].strip() or url
                elif line.startswith("DEBUG_SESSION_ID="):
                    session_id = line.split("=", 1)[1].strip() or session_id

        body = dict(payload or {})
        body.setdefault("sessionId", session_id)
        req = urllib.request.Request(
            url,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            resp.read()
        return True
    except Exception as e:
        logger.debug(f"Debug event skipped: {e}")
        return False


# ==========================================
# SECURITY: Safe Delete Message
# ==========================================
def safe_delete_message(bot, chat_id, message_id):
    """Menghapus pesan dengan aman. Jangan lempar error jika pesan tidak ditemukan."""
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        logger.debug(f"Tidak bisa menghapus pesan {message_id} di chat {chat_id}: {e}")
        pass


# ==========================================
# SECURITY: Safe Answer Callback Query
# ==========================================
def safe_answer_callback_query(bot, call, text=None, show_alert=False):
    """Jawab callback query dengan aman, handle semua error Telegram."""
    try:
        bot.answer_callback_query(call.id, text=text, show_alert=show_alert)
    except Exception as e:
        logger.debug(f"Tidak bisa menjawab callback query {call.id}: {e}")
        pass
