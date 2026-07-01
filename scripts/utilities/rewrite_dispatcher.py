import os

dispatcher_code = """
\"\"\"
Callback Handler - Dispatcher (Router)
Mengalihkan callback ke handler yang sesuai (Transaksi, Pengaturan, Dashboard)
\"\"\"
import logging
from utils.security import authorized_only

# Import sub-handlers
from handlers.callback_transaksi import handle_transaksi_callbacks
from handlers.callback_pengaturan import handle_pengaturan_callbacks
from handlers.handler_dashboard import handle_dashboard_callbacks

logger = logging.getLogger("bot_logger")

@authorized_only
def handle_semua_tombol(call):
    \"\"\"
    Router utama untuk semua callback query.
    \"\"\"
    cmd = call.data

    # Logika Dispatching Sederhana berdasarkan Prefix
    if cmd.startswith("mb_") or cmd.startswith("mm_") or cmd.startswith("pick_metode") or cmd.startswith("btn_batal_edit") or cmd.startswith("pick_del"):
        handle_pengaturan_callbacks(call)
    elif cmd.startswith("dashboard_"):
        # Misal dashboard memiliki handler tersendiri di handler_dashboard.py
        # Jika handler_dashboard.py sudah meregistrasikan callbacknya sendiri, 
        # kita mungkin tidak perlu memanggilnya secara manual, tapi jika butuh:
        handle_dashboard_callbacks(call)
    else:
        # Default fallback untuk transaksi dan lainnya
        handle_transaksi_callbacks(call)
"""

with open("handlers/callback_handler.py", "w", encoding="utf-8") as f:
    f.write(dispatcher_code)
