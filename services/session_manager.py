"""
Session Manager — Persistent User Sessions via Supabase
"""
import logging
import threading

from database import db_client

logger = logging.getLogger("bot_logger")


class UserSessions:
    """Class wrapper untuk mensimulasikan dict tetapi menyimpan data secara persisten ke database Supabase."""

    def __init__(self):
        self.local_cache = {}
        self.lock = threading.Lock()

    def keys(self):
        return self.local_cache.keys()

    def __iter__(self):
        return iter(self.local_cache)

    def __len__(self):
        return len(self.local_cache)

    def _get_session(self, chat_id):
        try:
            chat_id_int = int(chat_id)
            with self.lock:
                if chat_id_int not in self.local_cache:
                    # Load dari database
                    session_data = db_client.load_session_db(chat_id_int)
                    if not session_data:
                        session_data = {"state": "standby", "ui_keyboard_shown": False}
                    else:
                        session_data.setdefault("state", "standby")
                        session_data.setdefault("ui_keyboard_shown", False)
                    self.local_cache[chat_id_int] = session_data
                return self.local_cache[chat_id_int]
        except Exception as e:
            logger.error(f"Error getting session for {chat_id}: {e}")
            return {"state": "standby", "ui_keyboard_shown": False}

    def __getitem__(self, chat_id):
        return self._get_session(chat_id)

    def create_session(self, chat_id):
        session = {"state": "standby", "ui_keyboard_shown": False}
        self[chat_id] = session
        return session

    def clear_session(self, chat_id):
        try:
            chat_id_int = int(chat_id)
            with self.lock:
                self.local_cache.pop(chat_id_int, None)
            db_client.save_session_db(chat_id_int, {})
        except Exception as e:
            logger.error(f"Gagal menghapus sesi untuk {chat_id}: {e}")

    def get_session(self, chat_id):
        try:
            chat_id_int = int(chat_id)
            with self.lock:
                if chat_id_int in self.local_cache:
                    return self.local_cache[chat_id_int]

            session_data = db_client.load_session_db(chat_id_int)
            if session_data:
                with self.lock:
                    self.local_cache[chat_id_int] = session_data
                return session_data
        except Exception:
            pass
        return None

    def __setitem__(self, chat_id, value):
        try:
            chat_id_int = int(chat_id)
            with self.lock:
                self.local_cache[chat_id_int] = value
            # Save ke database (diluar lock agar tidak blocking operasi cache lain)
            db_client.save_session_db(chat_id_int, value)
        except Exception as e:
            logger.error(f"Gagal menset sesi untuk {chat_id}: {e}")

    def __delitem__(self, chat_id):
        try:
            chat_id_int = int(chat_id)
            self.local_cache.pop(chat_id_int, None)
            # Kosongkan di database
            db_client.save_session_db(chat_id_int, {})
        except Exception as e:
            logger.error(f"Gagal menghapus sesi untuk {chat_id}: {e}")

    def __contains__(self, chat_id):
        try:
            chat_id_int = int(chat_id)
            session = self._get_session(chat_id_int)
            if not session:
                return False
            # Anggap "ada sesi" jika sedang berada di state selain standby atau memiliki payload penting.
            if session.get("state") and session.get("state") != "standby":
                return True
            for k in ("entitas", "pending_price_update", "multi_results", "ocr_text", "ringkas"):
                if k in session:
                    return True
            return False
        except Exception:
            return False

    def get(self, chat_id, default=None):
        try:
            chat_id_int = int(chat_id)
            return self._get_session(chat_id_int)
        except Exception:
            return default

    def setdefault(self, chat_id, default=None):
        try:
            chat_id_int = int(chat_id)
            session = self._get_session(chat_id_int)
            if not session:
                session = default or {"state": "standby", "ui_keyboard_shown": False}
                self[chat_id_int] = session
                return self[chat_id_int]
            session.setdefault("state", "standby")
            session.setdefault("ui_keyboard_shown", False)
            return session
        except Exception:
            return default or {"state": "standby", "ui_keyboard_shown": False}

    def ensure(self, chat_id):
        return self.setdefault(chat_id, {"state": "standby", "ui_keyboard_shown": False})

    def pop(self, chat_id, default=None):
        try:
            chat_id_int = int(chat_id)
            val = self.local_cache.pop(chat_id_int, default)
            # Kosongkan di database
            db_client.save_session_db(chat_id_int, {})
            return val
        except Exception:
            return default
