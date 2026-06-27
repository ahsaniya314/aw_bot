"""
handler_dashboard.py
Handler untuk fitur dashboard harian di Telegram Bot
"""
import os
import logging
import ipaddress
from urllib.parse import urlparse
from core.bot_context import ctx
from services.daily_dashboard import get_dashboard_harian, get_dashboard_custom_date, render_dashboard_text
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.visualizer import generate_dashboard_chart
import io

logger = logging.getLogger("bot_logger")


def _normalize_url_maybe(url: str):
    teks = (url or "").strip()
    if not teks:
        return ""
    if "://" not in teks:
        teks = f"https://{teks}"
    return teks


def _is_public_http_url(url: str):
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False
        host = p.hostname
        if not host:
            return False
        if host.lower() in {"localhost", "127.0.0.1", "0.0.0.0"}:
            return False
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
        except ValueError:
            pass
        return True
    except Exception:
        return False


def get_dashboard_web_url():
    explicit = _normalize_url_maybe(os.getenv("DASHBOARD_WEB_URL") or os.getenv("DASHBOARD_PUBLIC_URL") or "")
    if explicit:
        url = explicit.rstrip("/")
        if not url.endswith("/dashboard"):
            url = f"{url}/dashboard"
        return url if _is_public_http_url(url) else None

    space_host = (os.getenv("SPACE_HOST") or "").strip()
    if space_host:
        url = f"https://{space_host}/dashboard"
        return url if _is_public_http_url(url) else None

    public_base = _normalize_url_maybe(os.getenv("PUBLIC_BASE_URL") or os.getenv("APP_BASE_URL") or os.getenv("BASE_URL") or "")
    if public_base:
        url = f"{public_base.rstrip('/')}/dashboard"
        return url if _is_public_http_url(url) else None

    return "https://aw-bot-backend.onrender.com/dashboard/"


def build_dashboard_web_button():
    url = get_dashboard_web_url()
    if not url:
        return None
    return InlineKeyboardButton("Dashboard Website", url=url)


def tangani_dashboard_harian(bot, chat_id, message_id_target, db_transaksi):
    """
    Handler untuk menampilkan dashboard harian.
    """
    try:
        # Ambil data dashboard
        dashboard_data = get_dashboard_harian(db_transaksi)
        dashboard_text = render_dashboard_text(dashboard_data)
        chart_buf = generate_dashboard_chart(dashboard_data)
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔄 Refresh", callback_data="dashboard_refresh"),
            InlineKeyboardButton("📅 Pilih Tanggal", callback_data="dashboard_custom_date")
        )
        dashboard_web_btn = build_dashboard_web_button()
        if dashboard_web_btn:
            markup.add(dashboard_web_btn)
        markup.row(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        
        # Selalu coba hapus pesan lama agar UI bersih
        try:
            bot.delete_message(chat_id, message_id_target)
        except:
            pass
            
        if chart_buf:
            bot.send_photo(chat_id, chart_buf, caption=dashboard_text, parse_mode="HTML", reply_markup=markup)
        else:
            bot.send_message(chat_id, dashboard_text, parse_mode="HTML", reply_markup=markup)
            
    except Exception as e:
        logger.error(f"Error dashboard harian: {e}")
        bot.send_message(chat_id, f"❌ <b>Gagal memuat dashboard:</b>\n{e}", parse_mode="HTML")


def tangani_dashboard_custom_date(bot, chat_id, message_id_target, db_transaksi, target_date):
    """
    Handler untuk menampilkan dashboard tanggal tertentu.
    """
    try:
        # Ambil data dashboard
        dashboard_data = get_dashboard_custom_date(db_transaksi, target_date)
        dashboard_text = render_dashboard_text(dashboard_data)
        chart_buf = generate_dashboard_chart(dashboard_data)
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🏠 Hari Ini", callback_data="dashboard_refresh"),
            InlineKeyboardButton("📅 Tanggal Lain", callback_data="dashboard_custom_date")
        )
        dashboard_web_btn = build_dashboard_web_button()
        if dashboard_web_btn:
            markup.add(dashboard_web_btn)
        markup.row(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        
        # Selalu coba hapus pesan lama
        try:
            bot.delete_message(chat_id, message_id_target)
        except:
            pass
            
        if chart_buf:
            bot.send_photo(chat_id, chart_buf, caption=dashboard_text, parse_mode="HTML", reply_markup=markup)
        else:
            bot.send_message(chat_id, dashboard_text, parse_mode="HTML", reply_markup=markup)
            
    except Exception as e:
        logger.error(f"Error dashboard custom date: {e}")
        bot.send_message(chat_id, f"❌ <b>Gagal memuat data tanggal {target_date}:</b>\n{e}", parse_mode="HTML")


def handle_dashboard_callbacks(bot, call, db_transaksi, user_sessions):
    """
    Handler untuk callback button dashboard.
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "dashboard_refresh":
        # Refresh dashboard hari ini
        tangani_dashboard_harian(bot, chat_id, message_id, db_transaksi)
        bot.answer_callback_query(call.id, "✅ Dashboard diperbarui!")
    
    elif call.data == "dashboard_detail":
        # Tampilkan detail lengkap semua transaksi
        dashboard_data = get_dashboard_harian(db_transaksi)
        
        if dashboard_data.get("error"):
            bot.answer_callback_query(call.id, "❌ Gagal memuat detail")
            return
        
        # Render detail transaksi
        detail_text = f"📝 <b>DETAIL TRANSAKSI HARI INI</b>\n"
        detail_text += f"📅 {dashboard_data['tanggal_display']}\n"
        detail_text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if not dashboard_data["transaksi_list"]:
            detail_text += "<i>(Belum ada transaksi hari ini)</i>"
        else:
            for i, trx in enumerate(dashboard_data["transaksi_list"], 1):
                status_emoji = (
                    "✅" if "lunas" in trx["status"].lower() else
                    "⏳" if any(k in trx["status"].lower() for k in ["cicil", "dicicil", "dp"]) else
                    "🔴"
                )
                detail_text += f"{i}. {status_emoji} <b>{trx['nama']}</b>\n"
                detail_text += f"   📦 {trx['jumlah']} {trx['barang']}\n"
                detail_text += f"   💵 Total: <code>{trx['total']}</code>\n"
                detail_text += f"   🏦 Metode: {trx['metode']}\n"
                if trx["tagihan"] != "Rp 0":
                    detail_text += f"   ⚠️ Tagihan: <code>{trx['tagihan']}</code>\n"
                if trx["uang_masuk"] != "Rp 0":
                    detail_text += f"   💰 Uang Masuk: <code>{trx['uang_masuk']}</code>\n"
                detail_text += "\n"
        
        # Kirim sebagai pesan baru (karena bisa panjang)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="dashboard_refresh"))
        
        # Hapus pesan lama (bisa jadi photo dashboard)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
            
        bot.send_message(
            chat_id,
            detail_text,
            parse_mode="HTML",
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, "✅ Detail ditampilkan")
    
    elif call.data == "dashboard_custom_date":
        # Minta user input tanggal
        text_pilih = (
            "📅 <b>Pilih Tanggal</b>\n\n"
            "Ketik tanggal yang ingin Anda lihat dalam format:\n"
            "<code>DD-MM-YYYY</code>\n\n"
            "Contoh: <code>30-04-2026</code>\n"
            "Atau: <code>kemarin</code>, <code>3 hari lalu</code>"
        )
        
        # Hapus pesan lama (dashboard/photo)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        # Hindari konflik dengan flow lain yang memakai next-step handler.
        try:
            bot.clear_step_handler_by_chat_id(chat_id)
        except Exception as e:
            logger.debug(f"Gagal clear step handler dashboard untuk {chat_id}: {e}")
            
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Batal", callback_data="dashboard_cancel_date_input"))
        msg_prompt = bot.send_message(chat_id, text_pilih, parse_mode="HTML", reply_markup=markup)
        
        # Set state untuk menunggu input tanggal
        sess = user_sessions.ensure(chat_id) if hasattr(user_sessions, "ensure") else user_sessions.setdefault(chat_id, {})
        sess["state"] = "awaiting_dashboard_date"
        sess["message_id"] = msg_prompt.message_id
        bot.register_next_step_handler_by_chat_id(
            chat_id,
            lambda message: handle_dashboard_date_input(bot, message, db_transaksi, user_sessions)
        )
        
        bot.answer_callback_query(call.id, "Ketik tanggal yang diinginkan")
    elif call.data == "dashboard_cancel_date_input":
        sess = user_sessions.get(chat_id) if hasattr(user_sessions, "get") else None
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        try:
            bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        if sess:
            sess.pop("state", None)
            sess.pop("message_id", None)
        bot.send_message(chat_id, "❌ Pencarian tanggal dibatalkan.")
        bot.answer_callback_query(call.id, "Dibatalkan")


def handle_dashboard_date_input(bot, message, db_transaksi, user_sessions):
    """
    Handler untuk menerima input tanggal dari user.
    """
    chat_id = message.chat.id
    sess_now = user_sessions.get(chat_id) if hasattr(user_sessions, "get") else None
    
    if chat_id not in user_sessions or user_sessions[chat_id].get("state") != "awaiting_dashboard_date":
        return False
    
    message_id_target = user_sessions[chat_id].get("message_id")
    tanggal_input = message.text.strip()
    
    # Jika user ingin membatalkan
    if tanggal_input.lower() in ["batal", "cancel", "stop", "exit"]:
        try:
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, message_id_target)
        except:
            pass
        try:
            bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        bot.send_message(chat_id, "❌ Pencarian tanggal dibatalkan.")
        del user_sessions[chat_id]
        return True

    from core.master_data import normalisasi_tanggal_gs

    target_date = normalisasi_tanggal_gs(tanggal_input)
    if not target_date:
        bot.reply_to(
            message,
            "⚠️ <b>Format tanggal tidak dikenali.</b>\n"
            "Contoh:\n"
            "• <code>30-04-2026</code>\n"
            "• <code>20 mei</code>\n"
            "• <code>30 nop</code>\n"
            "• <code>12/23/25</code>\n"
            "• <code>kemarin</code> / <code>3 hari lalu</code>",
            parse_mode="HTML",
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id,
            lambda next_message: handle_dashboard_date_input(bot, next_message, db_transaksi, user_sessions)
        )
        return True

    # Hapus pesan user
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    # Tampilkan dashboard (tangani_dashboard_custom_date sudah handle delete message_id_target)
    tangani_dashboard_custom_date(bot, chat_id, message_id_target, db_transaksi, target_date)
    
    # Clear state
    try:
        bot.clear_step_handler_by_chat_id(chat_id)
    except Exception:
        pass
    del user_sessions[chat_id]
    
    return True
