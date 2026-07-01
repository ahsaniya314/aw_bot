"""
Bot Context — Dependency Injection Container
=============================================
Menyimpan semua shared state yang dibutuhkan oleh handler dan service modules.
Diinisialisasi sekali di main.py, lalu diakses oleh semua modul via:
    from core.bot_context import ctx
"""

from typing import Any, List


class BotContext:
    """Container untuk semua dependency global bot."""

    bot: Any = None
    user_sessions: Any = None
    db_transaksi: Any = None
    db_barang: Any = None
    db_metode: Any = None
    db_histori: Any = None
    gs_cache: Any = None
    IS_DB_CONNECTED: bool = False
    rate_limiter: Any = None
    ocr_service: Any = None
    AUTHORIZED_ADMINS: List[int] = []
    ITEM_PER_PAGE: int = 5
    BUILD_ID: str = ""
    SHOW_BUILD: bool = True


ctx = BotContext()
