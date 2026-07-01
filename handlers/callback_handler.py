"""
Callback Handler - Dispatcher (Router)
Mengalihkan callback ke handler yang sesuai (Transaksi, Pengaturan, Dashboard)
"""

import logging

# Import sub-handlers
from core.bot_context import ctx
from handlers.callback_pengaturan import handle_master_dan_pelunasan, handle_pengaturan_callbacks
from handlers.callback_transaksi import handle_transaksi_callbacks
from handlers.handler_dashboard import handle_dashboard_callbacks
from utils.security import authorized_only

logger = logging.getLogger("bot_logger")


@authorized_only
def handle_semua_tombol(call):
    """
    Router utama untuk semua callback query.
    """
    cmd = call.data
    chat_id = call.message.chat.id
    logger.info(f"[CALLBACK DEBUG] Received callback: cmd='{cmd}', chat_id={chat_id}")

    # Handle mb_batal and mb_do_update_price FIRST with handle_master_dan_pelunasan
    if cmd in ["mb_batal", "mb_do_update_price"]:
        logger.info(f"[CALLBACK DEBUG] DIRECT handling {cmd} with handle_master_dan_pelunasan")
        handle_master_dan_pelunasan(call)
        return

    # Logika Dispatching berdasarkan Prefix Callback
    if cmd.startswith(("mb_", "mm_", "ms_", "pick_metode")):
        # Master Barang, Master Metode, dan Master Satuan handlers
        logger.info("[CALLBACK DEBUG] Routing to handle_pengaturan_callbacks")
        handle_pengaturan_callbacks(call)
    elif cmd.startswith("dashboard_"):
        # Dashboard handlers
        logger.info("[CALLBACK DEBUG] Routing to handle_dashboard_callbacks")
        handle_dashboard_callbacks(ctx.bot, call, ctx.db_transaksi, ctx.user_sessions)
    else:
        # Default fallback untuk transaksi, pick_*, dan lainnya
        logger.info(f"[CALLBACK DEBUG] Routing to handle_transaksi_callbacks (cmd: {cmd[:20]}...)")
        handle_transaksi_callbacks(call)


def register_handlers(bot):
    """Register callback handlers with the bot."""
    bot.callback_query_handler(func=lambda call: True)(handle_semua_tombol)
