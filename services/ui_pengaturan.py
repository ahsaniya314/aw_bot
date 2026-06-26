"""
UI Pengaturan - Fungsi render untuk menu pengaturan master data (barang, metode)
"""
import logging
import math
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.bot_context import ctx
from utils.security import safe_edit_message
from core.master_data import format_rupiah, get_all_barang

logger = logging.getLogger("bot_logger")


def render_daftar_master_barang(barang_list):
    """
    Render daftar master barang dengan keyboard
    """
    teks = "📋 <b>DAFTAR MASTER BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
    
    if not barang_list:
        teks += "Tidak ada barang di master data."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("➕ Tambah Barang", callback_data="mb_tambah"))
        return teks, markup
    
    # Kelompokkan barang
    grouped = {}
    for b in barang_list:
        nama = b["nama"].lower()
        if nama not in grouped:
            grouped[nama] = []
        grouped[nama].append(b)
    
    # Urutkan dan render
    for nama in sorted(grouped.keys()):
        items = grouped[nama]
        teks += f"\n📦 <b>{nama.capitalize()}</b>\n"
        for b in items:
            teks += f"• {format_rupiah(b['harga'])} / {b['satuan']}\n"
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ Tambah Barang", callback_data="mb_tambah"),
        InlineKeyboardButton("✏️ Edit Harga", callback_data="mb_edit"),
    )
    markup.add(
        InlineKeyboardButton("🗑️ Hapus Barang", callback_data="mb_hapus"),
        InlineKeyboardButton("🔄 Refresh", callback_data="mb_list"),
    )
    markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
    return teks, markup


def tampilkan_pilihan_barang(chat_id, message_id_target, barang_list, callback_prefix):
    """
    Tampilkan pilihan barang dengan keyboard
    """
    bot = ctx.bot
    
    if len(barang_list) == 0:
        safe_edit_message(bot, "❌ Tidak ada barang yang sesuai.", chat_id, message_id_target)
        return
    
    teks = f"🔍 Ditemukan <b>{len(barang_list)}</b> barang:\n\n"
    markup = InlineKeyboardMarkup(row_width=1)
    
    for i, b in enumerate(barang_list):
        teks += f"{i+1}. <b>{b['nama']}</b> - {format_rupiah(b['harga'])} / {b['satuan']}\n"
        markup.add(InlineKeyboardButton(
            f"✓ Pilih: {b['nama']} ({b['satuan']})", 
            callback_data=f"{callback_prefix}_{i}"
        ))
    
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    safe_edit_message(bot, teks, chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)


def susun_tombol_konfirmasi():
    """
    Susun tombol konfirmasi untuk OCR
    """
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Simpan", callback_data="btn_kirim"),
        InlineKeyboardButton("✏️ Edit", callback_data="btn_masuk_edit"),
    )
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="btn_buang"))
    return markup
