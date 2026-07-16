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


import os
import telebot

@authorized_only
def handle_semua_tombol(call):
    """
    Router utama untuk semua callback query.
    """
    cmd = call.data
    chat_id = call.message.chat.id
    logger.info(f"[CALLBACK DEBUG] Received callback: cmd='{cmd}', chat_id={chat_id}")

    # Handle request access, approve, and reject callbacks
    if cmd.startswith(("request_access_", "approve_", "reject_")):
        handle_auth_callbacks(call)
        return

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


def handle_auth_callbacks(call):
    """Menangani proses pengajuan akses, persetujuan, dan penolakan admin."""
    cmd = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if cmd.startswith("request_access_"):
        user_id = int(cmd.split("_")[2])
        username = call.from_user.username or "Tanpa Username"
        first_name = call.from_user.first_name or "User"
        
        # Ambil Owner ID
        OWNER_ID_STR = os.getenv("TELEGRAM_BOT_OWNER_ID", "")
        if not OWNER_ID_STR.strip().isdigit():
            if ctx.AUTHORIZED_ADMINS:
                OWNER_ID = ctx.AUTHORIZED_ADMINS[0]
            else:
                ctx.bot.answer_callback_query(call.id, text="Gagal: Owner ID tidak terkonfigurasi.", show_alert=True)
                return
        else:
            OWNER_ID = int(OWNER_ID_STR.strip())
            
        markup = telebot.types.InlineKeyboardMarkup()
        btn_approve = telebot.types.InlineKeyboardButton(
            text="✅ Setujui", 
            callback_data=f"approve_{user_id}_{username}_{first_name}"
        )
        btn_reject = telebot.types.InlineKeyboardButton(
            text="❌ Tolak", 
            callback_data=f"reject_{user_id}_{first_name}"
        )
        markup.add(btn_approve, btn_reject)
        
        try:
            ctx.bot.send_message(
                OWNER_ID,
                f"🔔 <b>Permintaan Akses Baru!</b>\n\n"
                f"👤 Nama: {first_name}\n"
                f"🏷 Username: @{username}\n"
                f"🆔 ID Telegram: <code>{user_id}</code>",
                parse_mode="HTML",
                reply_markup=markup
            )
            
            # Beri tahu user bahwa permintaan telah dikirim
            ctx.bot.edit_message_text(
                text="⌛ <b>Permintaan Terkirim!</b>\nHarap tunggu konfirmasi dari owner utama.",
                chat_id=chat_id,
                message_id=message_id,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"[AUTH_CALLBACK] Gagal mengirim pesan request ke owner: {e}")
            ctx.bot.answer_callback_query(call.id, text="Gagal mengajukan izin. Pastikan Owner sudah start bot.", show_alert=True)
            
    elif cmd.startswith("approve_"):
        parts = cmd.split("_")
        user_id = int(parts[1])
        username = parts[2]
        first_name = parts[3]
        
        try:
            from database.db_client import add_authorized_admin_db
            add_authorized_admin_db(user_id, username, first_name)
            
            if user_id not in ctx.AUTHORIZED_ADMINS:
                ctx.AUTHORIZED_ADMINS.append(user_id)
                
            ctx.bot.edit_message_text(
                text=f"✅ Akses untuk <b>{first_name}</b> (<code>{user_id}</code>) telah <b>DISETUJUI</b>.",
                chat_id=chat_id,
                message_id=message_id,
                parse_mode="HTML"
            )
            
            ctx.bot.send_message(
                user_id,
                "🎉 <b>Akses Disetujui!</b>\nAnda sekarang telah menjadi admin terdaftar dan bisa menggunakan bot. Silakan ketik /start.",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"[AUTH_CALLBACK] Gagal menyetujui user: {e}")
            ctx.bot.answer_callback_query(call.id, text="Error saat menyetujui user.", show_alert=True)
            
    elif cmd.startswith("reject_"):
        parts = cmd.split("_")
        user_id = int(parts[1])
        first_name = parts[2] if len(parts) > 2 else "User"
        
        try:
            ctx.bot.edit_message_text(
                text=f"❌ Akses untuk <b>{first_name}</b> (<code>{user_id}</code>) telah <b>DITOLAK</b>.",
                chat_id=chat_id,
                message_id=message_id,
                parse_mode="HTML"
            )
            
            ctx.bot.send_message(
                user_id,
                "🚫 Maaf, permintaan akses Anda ditolak oleh Owner.",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"[AUTH_CALLBACK] Gagal menolak user: {e}")
            ctx.bot.answer_callback_query(call.id, text="Error saat menolak user.", show_alert=True)


def register_handlers(bot):
    """Register callback handlers with the bot."""
    bot.callback_query_handler(func=lambda call: True)(handle_semua_tombol)
