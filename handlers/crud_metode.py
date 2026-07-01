"""
CRUD Metode Pembayaran — Next-step handlers untuk Master Metode
"""
import logging

from core.bot_context import ctx
from core.master_data import tambah_metode, update_metode

logger = logging.getLogger("bot_logger")


def _mm_terima_nama(message):
    chat_id = message.chat.id
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    nama = message.text.strip()
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    user_sessions.setdefault(chat_id, {})["mm_nama_baru"] = nama
    msg = bot.send_message(
        chat_id,
        f"✅ Nama: <b>{nama}</b>\n\nKetik <b>keyword/alias</b> (pisah koma):\n<i>Contoh: <code>bni, tf bni, transfer bni</code></i>",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(msg, _mm_terima_keyword)


def _mm_terima_keyword(message):
    chat_id = message.chat.id
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    keyword = message.text.strip()
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    sess = user_sessions.get(chat_id, {})
    nama = sess.get("mm_nama_baru", "-")
    try:
        id_baru = tambah_metode(ctx.db_metode, nama, keyword)
        bot.send_message(
            chat_id,
            f"✅ <b>Metode berhasil ditambahkan!</b>\nID: <code>{id_baru}</code> | Nama: <b>{nama}</b>",
            parse_mode="HTML",
        )
    except Exception as e:
        bot.send_message(chat_id, f"❌ Gagal simpan: {e}")
    user_sessions.pop(chat_id, None)


def _mm_terima_keyword_edit(message):
    chat_id = message.chat.id
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    row_idx = user_sessions.get(chat_id, {}).get("mm_edit_row")
    try:
        update_metode(ctx.db_metode, row_idx, keyword=message.text.strip())
        bot.send_message(chat_id, "✅ Keyword metode berhasil diperbarui.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Gagal update: {e}")
    user_sessions.pop(chat_id, None)
