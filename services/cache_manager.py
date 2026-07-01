"""
Cache Manager — GSpread Cache & Cached Data Accessors
"""
import logging
import threading
from datetime import datetime

from core.bot_context import ctx
from core.master_data import get_all_barang, muat_metode_keywords

logger = logging.getLogger("bot_logger")


# ✨ CACHE SYSTEM: Mengurangi API Call ke Database Supabase untuk performa & stabilitas
class GSpreadCache:
    def __init__(self, expiry_minutes=5):
        self.expiry_minutes = expiry_minutes
        self.cache = {}  # {key: {"data": value, "time": timestamp}}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            entry = self.cache.get(key)
            if entry is None:
                return None

            ttl_seconds = entry.get("ttl")
            if ttl_seconds is None:
                ttl_seconds = self.expiry_minutes * 60

            if (datetime.now() - entry["time"]).total_seconds() < ttl_seconds:
                return entry["data"]

            self.cache.pop(key, None)
        return None

    def set(self, key, value, ttl=None):
        with self.lock:
            self.cache[key] = {"data": value, "time": datetime.now(), "ttl": ttl}

    def invalidate(self, key=None):
        with self.lock:
            if key:
                self.cache.pop(key, None)
            else:
                self.cache = {}


def get_cached_barang():
    data = ctx.gs_cache.get("barang")
    if data is None and ctx.IS_DB_CONNECTED:
        try:
            data = get_all_barang(ctx.db_barang)
            ctx.gs_cache.set("barang", data)
        except Exception as e:
            logger.error(f"Error caching barang: {e}")
            return []
    return data or []


def get_cached_metode():
    data = ctx.gs_cache.get("metode_mapping")
    if data is None and ctx.IS_DB_CONNECTED:
        try:
            data = muat_metode_keywords(ctx.db_metode)
            ctx.gs_cache.set("metode_mapping", data)
        except Exception as e:
            logger.error(f"Error caching metode: {e}")
            return {}
    return data or {}
