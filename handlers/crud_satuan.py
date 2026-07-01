"""
CRUD Master Satuan — Next-step handlers untuk Master Satuan
"""
import logging

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.bot_context import ctx
from core.master_data import get_all_satuan, tambah_satuan, update_satuan

logger = logging.getLogger("bot_logger")


def _ms_terima_nama(message):
    chat_id = message.chat.id
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    nama = message.text.strip()
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    try:
        # Simpan nama satuan yang akan ditambahkan ke session
        sess = user_sessions.ensure(chat_id)
        sess["ms_pending_nama"] = nama

        # Tampilkan konfirmasi
        teks_konfirmasi = f"⚠️ <b>KONFIRMASI TAMBAH SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\nAnda akan menambahkan satuan:\n\n📐 <b>{nama}</b>\n\nApakah Anda yakin?"
        markup_konfirmasi = InlineKeyboardMarkup(row_width=2)
        markup_konfirmasi.add(
            InlineKeyboardButton("✅ Ya, Simpan", callback_data="ms_confirm_add"),
            InlineKeyboardButton("❌ Batal", callback_data="ms_batal"),
        )

        # Edit pesan input (jika ada) atau kirim pesan baru
        msg_input_id = sess.get("ms_input_msg_id")
        if msg_input_id:
            from utils.security import safe_edit_message

            safe_edit_message(
                bot,
                teks_konfirmasi,
                chat_id,
                msg_input_id,
                parse_mode="HTML",
                reply_markup=markup_konfirmasi,
            )
        else:
            bot.send_message(
                chat_id, teks_konfirmasi, parse_mode="HTML", reply_markup=markup_konfirmasi
            )
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {e}")


def _ms_terima_nama_edit(message):
    chat_id = message.chat.id
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    id_satuan = user_sessions.get(chat_id, {}).get("ms_edit_id")
    nama_baru = message.text.strip()
    try:
        # Dapatkan nama satuan lama untuk konfirmasi
        semua_satuan = get_all_satuan()
        satuan_lama = next((s["nama_satuan"] for s in semua_satuan if s["id"] == id_satuan), None)

        # Simpan ke session
        sess = user_sessions.ensure(chat_id)
        sess["ms_pending_nama_edit"] = nama_baru

        # Tampilkan konfirmasi
        teks_konfirmasi = f"⚠️ <b>KONFIRMASI EDIT SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\nAnda akan mengubah satuan:\n\n📐 <b>{satuan_lama}</b> → <b>{nama_baru}</b>\n\nApakah Anda yakin?"
        markup_konfirmasi = InlineKeyboardMarkup(row_width=2)
        markup_konfirmasi.add(
            InlineKeyboardButton("✅ Ya, Update", callback_data="ms_confirm_edit"),
            InlineKeyboardButton("❌ Batal", callback_data="ms_batal"),
        )

        # Edit pesan input
        msg_input_id = sess.get("ms_input_msg_id")
        if msg_input_id:
            from utils.security import safe_edit_message

            safe_edit_message(
                bot,
                teks_konfirmasi,
                chat_id,
                msg_input_id,
                parse_mode="HTML",
                reply_markup=markup_konfirmasi,
            )
        else:
            bot.send_message(
                chat_id, teks_konfirmasi, parse_mode="HTML", reply_markup=markup_konfirmasi
            )
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {e}")
