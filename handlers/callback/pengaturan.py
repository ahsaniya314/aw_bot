"""
Callback Handler - Settings (Pengaturan)
"""

import logging

from telebot.types import CallbackQuery

from core.bot_context import ctx
from core.master_data import get_all_barang
from services.ui_pengaturan import render_daftar_master_barang
from utils.security import safe_edit_message

logger = logging.getLogger("bot_logger")


def register(bot):
    """Register all settings-related callbacks."""

    @bot.callback_query_handler(func=lambda call: call.data == "mb_kembali")
    def handle_kembali(call: CallbackQuery):
        """Kembali ke menu pengaturan utama."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            # Show main settings menu
            barang_list = get_all_barang(ctx.db_barang)
            teks, markup = render_daftar_master_barang(barang_list)

            safe_edit_message(
                bot, teks, chat_id, message_id, parse_mode="HTML", reply_markup=markup
            )
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_KEMBALI] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)


__all__ = ["register"]
