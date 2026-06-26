"""
CRUD Master Barang — Handler untuk tambah, cek harga, set harga, hapus barang via chat
"""
import re
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.bot_context import ctx
from utils.security import safe_edit_message
from services.cache_manager import get_cached_barang
from services.ui_pengaturan import render_daftar_master_barang, tampilkan_pilihan_barang
from core.master_data import (
    format_rupiah, parse_rupiah, get_all_barang, tambah_barang,
    update_barang, cari_harga_default, format_daftar_master_barang_grouped
)

logger = logging.getLogger("bot_logger")


def tangani_tambah_barang_chat(chat_id, message_id_target):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    if chat_id not in user_sessions: return
    entitas = user_sessions[chat_id]["entitas"]
    nama = entitas.get("BARANG")
    harga_raw = entitas.get("HARGA")
    satuan_raw = entitas.get("SATUAN")
    original_text = ""
    try:
        original_text = (user_sessions[chat_id].get("hasil_nlp") or {}).get("original_text") or ""
    except Exception:
        original_text = ""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    markup_selesai = InlineKeyboardMarkup(row_width=2)
    markup_selesai.add(
        InlineKeyboardButton("📋 Lihat Daftar", callback_data="mb_list"),
        InlineKeyboardButton("➕ Tambah Lagi", callback_data="mb_tambah"),
        InlineKeyboardButton("✏️ Edit Harga", callback_data="mb_edit"),
        InlineKeyboardButton("🗑️ Hapus Barang", callback_data="mb_hapus"),
    )
    markup_selesai.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))

    if nama and str(nama).strip().lower() in {"permen", "serbuk", "roti", "pia", "roti pia", "roti/pia"}:
        t = original_text.lower()
        mapping = [
            (["wiilo", "wilo", "willo"], "Willo"),
            (["bemmbeng", "bembeng", "bengbeng", "beng-beng", "beng beng", "beem-beeng"], "Bembeng"),
            (["cholatos", "chocholetus"], "Cholatos"),
            (["adangrow"], "Adangrow"),
            (["miksu"], "Miksu"),
            (["getbory", "siiperquuen"], "Getbory"),
            (["lolipop", "lalipop", "lollipop"], "Lolipop"),
        ]
        picked = None
        for keys, val in mapping:
            if any(k in t for k in keys):
                picked = val
                break
        if picked:
            nama = picked

    if nama and harga_raw and satuan_raw:
        try:
            harga = parse_rupiah(harga_raw)
            semua = get_all_barang(ctx.db_barang)
            exists = any(b["nama"].lower() == nama.lower() and b["satuan"].lower() == satuan_raw.lower() for b in semua)
            if exists:
                safe_edit_message(bot, f"⚠️ Barang <b>{nama}</b> dengan satuan <b>{satuan_raw}</b> sudah ada. Gunakan menu 'Set Harga' untuk mengubahnya.", chat_id, message_id_target, parse_mode="HTML")
            else:
                tambah_barang(ctx.db_barang, nama, harga, satuan_raw)
                safe_edit_message(
                    bot,
                    f"✨ <b>BERHASIL MENAMBAHKAN BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📦 <b>Nama:</b> {nama}\n"
                    f"💰 <b>Harga Default:</b> {format_rupiah(harga)}\n"
                    f"📐 <b>Satuan:</b> {satuan_raw}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"<i>Barang telah disimpan di database master data.</i>",
                    chat_id,
                    message_id_target,
                    parse_mode="HTML",
                    reply_markup=markup_selesai,
                )
            if chat_id in user_sessions: del user_sessions[chat_id]
            return
        except Exception as e:
            logger.error(f"Gagal tambah barang instan: {e}")
            err_str = str(e)
            if "23505" in err_str or "duplicate key" in err_str.lower():
                msg_fail = (
                    "⚠️ <b>DITOLAK DATABASE SUPABASE</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Bot <b>BERHASIL</b> mengenali input Anda:\n"
                    f"📦 Barang: <code>{nama}</code>\n"
                    f"📐 Satuan: <b>{satuan_raw}</b>\n"
                    f"💰 Harga: <code>{format_rupiah(harga)}</code>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    "🚫 <b>PENYEBAB GAGAL:</b>\n"
                    f"Database Supabase Anda menolak pendaftaran karena nama <b>{nama}</b> dianggap duplikat.\n\n"
                    "💡 <b>SOLUSI MUTLAK:</b>\nJalankan perintah SQL di dashboard Supabase yang saya berikan sebelumnya untuk membuka kunci pembatasan nama ini."
                )
                safe_edit_message(bot, msg_fail, chat_id, message_id_target, parse_mode="HTML")
            else:
                safe_edit_message(bot, f"❌ <b>Gagal menyimpan barang</b>\n\nDetail error: <code>{err_str}</code>", chat_id, message_id_target, parse_mode="HTML")
            
            if chat_id in user_sessions: del user_sessions[chat_id]
            return


    if not nama:
        user_sessions[chat_id]["state"] = "mb_awaiting_name"
        user_sessions[chat_id]["mb_msg_id"] = message_id_target
        safe_edit_message(bot, "➕ <b>Barang apa yang ingin Anda tambahkan?</b>\nContoh: <code>Permen Coklat</code>", chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, _mb_terima_nama)
        return

    user_sessions[chat_id]["mb_nama_baru"] = nama
    user_sessions[chat_id]["mb_msg_id"] = message_id_target
    msg = safe_edit_message(bot, f"💰 Berapa harga default untuk <b>{nama}</b>?\n(Ketik angka saja, mis: <code>15000</code>)", chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)
    bot.register_next_step_handler(msg, _mb_terima_harga)


def _mb_terima_nama(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    if chat_id not in user_sessions or user_sessions[chat_id].get("state") == "cancelled": return
    if message.text.startswith('/'): return
    nama = message.text.strip()
    user_sessions[chat_id]["mb_nama_baru"] = nama
    msg_id = user_sessions[chat_id].get("mb_msg_id")
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    msg = safe_edit_message(bot, f"✅ Nama: <b>{nama}</b>\n\n💰 Berapa harga defaultnya?\n(Ketik angka saja, mis: <code>15000</code>)", chat_id, msg_id, parse_mode="HTML", reply_markup=markup)
    bot.register_next_step_handler(msg, _mb_terima_harga)


def _mb_terima_harga(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    if chat_id not in user_sessions or "mb_nama_baru" not in user_sessions[chat_id]: return
    if user_sessions[chat_id].get("state") == "cancelled": return
    if message.text.startswith('/'): return
    harga = parse_rupiah(message.text)
    nama = user_sessions[chat_id]["mb_nama_baru"]
    msg_id = user_sessions[chat_id].get("mb_msg_id")
    user_sessions[chat_id]["mb_harga_baru"] = harga

    # ✨ DYNAMIC SMART UNIT KEYBOARD: Gunakan daftar satuan dari MASTER SATUAN
    from core.master_data import get_all_satuan
    semua_satuan = get_all_satuan()
    satuan_list = [s["nama_satuan"].lower() for s in semua_satuan]
    
    # Urutkan satuan alphabetically
    satuan_list_sorted = sorted(satuan_list)
    
    # Buat tombol secara adaptif/cerdas
    markup = InlineKeyboardMarkup(row_width=3)
    btn_list = [InlineKeyboardButton(unit.capitalize(), callback_data=f"mb_unit_{unit}") for unit in satuan_list_sorted]
    
    # Masukkan ke Grid Keyboard per 3 kolom
    for i in range(0, len(btn_list), 3):
        markup.add(*btn_list[i:i+3])
        
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    safe_edit_message(bot,
        f"✅ Nama: <b>{nama}</b>\n💰 Harga: <code>{format_rupiah(harga)}</code>\n\n📐 Apa <b>satuan</b> barang ini? (mis: <code>pcs</code>, <code>dus</code>, <code>pak</code>, <code>karton</code>)\n<i>Silakan pilih tombol di bawah atau <b>ketik langsung nama satuan kustom Anda</b> (misal: <code>bungkus</code>, <code>pouch</code>, <code>lusin</code>):</i> ",
        chat_id, msg_id, parse_mode="HTML", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(chat_id, _mb_terima_satuan)


def _mb_terima_satuan(message, chat_id=None, message_id_target=None):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    if not chat_id: chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if not message_id_target: message_id_target = user_sessions[chat_id].get("mb_msg_id")
    satuan = ""
    if message:
        if message.text.startswith('/'): return
        satuan = message.text.lower().strip()
        try: bot.delete_message(chat_id, message.message_id)
        except: pass
    elif chat_id in user_sessions and "mb_satuan_baru" in user_sessions[chat_id]:
        satuan = user_sessions[chat_id]["mb_satuan_baru"]

    nama = user_sessions[chat_id]["mb_nama_baru"]
    harga = user_sessions[chat_id]["mb_harga_baru"]
    markup_selesai = InlineKeyboardMarkup(row_width=2)
    markup_selesai.add(
        InlineKeyboardButton("📋 Lihat Daftar", callback_data="mb_list"),
        InlineKeyboardButton("➕ Tambah Lagi", callback_data="mb_tambah"),
        InlineKeyboardButton("✏️ Edit Harga", callback_data="mb_edit"),
        InlineKeyboardButton("🗑️ Hapus Barang", callback_data="mb_hapus"),
    )
    markup_selesai.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
    try:
        semua = get_all_barang(ctx.db_barang)
        exists = any(b["nama"].lower() == nama.lower() and b["satuan"].lower() == satuan.lower() for b in semua)
        if exists:
            safe_edit_message(bot, f"⚠️ Barang <b>{nama}</b> dengan satuan <b>{satuan}</b> sudah ada. Gunakan menu 'Set Harga' untuk mengubahnya.", chat_id, message_id_target, parse_mode="HTML")
        else:
            tambah_barang(ctx.db_barang, nama, harga, satuan)
            safe_edit_message(
                bot,
                f"✨ <b>BERHASIL MENAMBAHKAN BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Nama:</b> {nama}\n"
                f"💰 <b>Harga:</b> <code>{format_rupiah(harga)}</code>\n"
                f"📐 <b>Satuan:</b> {satuan}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ Data telah tersimpan di Master Data.",
                chat_id,
                message_id_target,
                parse_mode="HTML",
                reply_markup=markup_selesai,
            )
        if chat_id in user_sessions: del user_sessions[chat_id]
    except Exception as e:
        err_str = str(e)
        if "23505" in err_str or "duplicate key" in err_str.lower():
            safe_edit_message(bot, f"⚠️ <b>GAGAL MENYIMPAN BARANG</b>\n\nNama barang <b>{nama}</b> sudah ada di database.\n\nSilakan ikuti petunjuk fix database atau tambahkan pembeda di nama produk.", chat_id, message_id_target, parse_mode="HTML")
        else:
            safe_edit_message(bot, f"❌ Gagal menyimpan barang: {e}", chat_id, message_id_target)


def _mb_terima_harga_edit(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    logger.info(f"[HARGA DEBUG] _mb_terima_harga_edit called for chat_id={chat_id}")
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    
    # Ensure session exists
    if chat_id not in user_sessions:
        logger.error(f"[HARGA DEBUG] Session not found for chat_id={chat_id}")
        bot.send_message(chat_id, "❌ Sesi kedaluwarsa. Silakan ulangi perintah.")
        return
    
    sess = user_sessions[chat_id]
    row_idx = sess.get("mb_edit_row")
    msg_id = sess.get("mb_msg_id")
    logger.info(f"[HARGA DEBUG] row_idx={row_idx}, msg_id={msg_id}")
    
    if not row_idx or not msg_id:
        logger.error(f"[HARGA DEBUG] Missing row_idx or msg_id. row_idx={row_idx}, msg_id={msg_id}")
        bot.send_message(chat_id, "❌ Terjadi kesalahan sesi (baris atau msg_id tidak ditemukan).")
        return
    try:
        harga_baru = int(re.sub(r"[^\d]", "", message.text))
        sess["mb_pending_harga"] = harga_baru  # Ini sekarang edit session yang benar
        logger.info(f"[HARGA DEBUG] Set mb_pending_harga={harga_baru}")
        
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if not target:
            logger.error(f"[HARGA DEBUG] Barang with row_idx={row_idx} not found in DB")
            bot.send_message(chat_id, "❌ Data barang tidak ditemukan di Database.")
            return
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Ya, Update Harga", callback_data="mb_do_update_price"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal")
        )
        logger.info(f"[HARGA DEBUG] About to edit message {msg_id} with confirmation dialog")
        safe_edit_message(bot,
            f"⚠️ <b>PERINGATAN PERGANTIAN HARGA</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Apakah Anda yakin ingin mengubah harga barang ini?\n\n"
            f"📦 <b>Barang:</b> <b>{target['nama']}</b>\n📐 <b>Satuan:</b> <b>{target['satuan']}</b>\n"
            f"💰 <b>Harga Lama:</b> <code>{format_rupiah(target['harga'])}</code>\n"
            f"✨ <b>Harga Baru:</b> <b>{format_rupiah(harga_baru)}</b>",
            chat_id, msg_id, parse_mode="HTML", reply_markup=markup)
        logger.info(f"[HARGA DEBUG] Confirmation dialog sent")
    except Exception as e:
        logger.error(f"[HARGA DEBUG] Exception: {e}", exc_info=True)
        bot.send_message(chat_id, f"❌ Input tidak valid: {e}")


def tangani_cek_harga_chat(chat_id, message_id_target):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    entitas = user_sessions[chat_id]["entitas"]
    nama_cari = entitas.get("BARANG")
    satuan_cari = entitas.get("SATUAN")
    semua = get_cached_barang() if ctx.IS_DB_CONNECTED else []
    if not semua:
        safe_edit_message(bot, "📭 Master barang masih kosong.", chat_id, message_id_target)
        return
    if not nama_cari:
        teks, markup = render_daftar_master_barang(semua)
        safe_edit_message(bot, teks, chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)
    else:
        hasil_list = cari_harga_default(ctx.db_barang, nama_cari, satuan_cari=satuan_cari, semua_barang=semua)
        if hasil_list:
            if len(hasil_list) == 1:
                hasil = hasil_list[0]
                teks = (f"🔍 <b>Informasi Harga Barang</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📦 Nama   : <b>{hasil['nama']}</b>\n💰 Harga  : <code>{format_rupiah(hasil['harga'])}</code>\n"
                        f"📐 Satuan : {hasil['satuan']}\n")
                safe_edit_message(bot, teks, chat_id, message_id_target, parse_mode="HTML")
            else:
                teks = f"🔍 Ditemukan <b>{len(hasil_list)}</b> barang yang mirip:\n\n"
                for h in hasil_list:
                    teks += f"• <b>{h['nama']}</b> — <code>{format_rupiah(h['harga'])}</code> / {h['satuan']}\n"
                safe_edit_message(bot, teks, chat_id, message_id_target, parse_mode="HTML")
        else:
            safe_edit_message(bot, f"❌ Barang <b>{nama_cari}</b> tidak ditemukan di Master Barang.", chat_id, message_id_target, parse_mode="HTML")


def tangani_set_harga_chat(chat_id, message_id_target):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    
    # Ensure session dan entitas ada
    if chat_id not in user_sessions or "entitas" not in user_sessions[chat_id]:
        safe_edit_message(bot, "❌ Sesi kedaluwarsa. Silakan unggah foto barang kembali.", chat_id, message_id_target)
        return
    
    entitas = user_sessions[chat_id]["entitas"]
    nama = entitas.get("BARANG")
    harga_raw = entitas.get("HARGA")
    satuan_cari = entitas.get("SATUAN")

    if not nama:
        semua = get_all_barang(ctx.db_barang)
        if not semua:
            safe_edit_message(bot, "📭 Tidak ada barang untuk diedit.", chat_id, message_id_target)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        for b in semua:
            markup.add(InlineKeyboardButton(f"✏️ {b['nama']} ({format_rupiah(b['harga'])})", callback_data=f"mb_edit_{b['row_idx']}"))
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
        safe_edit_message(bot, "Pilih barang yang ingin diatur harganya:", chat_id, message_id_target, reply_markup=markup)
        return

    if not harga_raw:
        hasil_list = cari_harga_default(ctx.db_barang, nama, satuan_cari=satuan_cari)
        if not hasil_list:
            safe_edit_message(bot, f"❌ Barang <b>{nama}</b> tidak ditemukan.", chat_id, message_id_target, parse_mode="HTML")
            return
        user_sessions[chat_id]["temp_matches"] = hasil_list
        user_sessions[chat_id]["mb_msg_id"] = message_id_target
        if len(hasil_list) > 1:
            from services.ui_pengaturan import tampilkan_pilihan_barang
            tampilkan_pilihan_barang(chat_id, message_id_target, hasil_list, "pick_edit_row")
        else:
            h = hasil_list[0]
            semua = get_all_barang(ctx.db_barang)
            row_idx = next((b["row_idx"] for b in semua if b["nama"] == h["nama"] and b["satuan"] == h["satuan"]), None)
            user_sessions[chat_id]["mb_edit_row"] = row_idx
            user_sessions[chat_id]["mb_msg_id"] = message_id_target  # Setup msg_id untuk callback nanti
            teks = f"💰 Berapa harga baru untuk <b>{h['nama']}</b> ({h['satuan']})?\n(Harga saat ini: <code>{format_rupiah(h['harga'])}</code>)"
            msg = safe_edit_message(bot, teks, chat_id, message_id_target, parse_mode="HTML")
            bot.register_next_step_handler(msg, _mb_terima_harga_edit)
        return

    hasil_list = cari_harga_default(ctx.db_barang, nama, satuan_cari=satuan_cari)
    if not hasil_list:
        safe_edit_message(bot, f"❌ Barang <b>{nama}</b> tidak ditemukan.", chat_id, message_id_target, parse_mode="HTML")
        return
    harga_baru = parse_rupiah(harga_raw)
    user_sessions[chat_id]["mb_pending_harga"] = harga_baru
    user_sessions[chat_id]["temp_matches"] = hasil_list
    user_sessions[chat_id]["mb_msg_id"] = message_id_target

    if len(hasil_list) == 1:
        h = hasil_list[0]
        semua = get_all_barang(ctx.db_barang)
        row_idx = next((b["row_idx"] for b in semua if b["nama"] == h["nama"] and b["satuan"] == h["satuan"]), None)
        user_sessions[chat_id]["mb_edit_row"] = row_idx
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Ya, Update Harga", callback_data="mb_do_update_price"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal")
        )
        safe_edit_message(bot,
            f"⚠️ <b>PERINGATAN PERGANTIAN HARGA</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Apakah Anda yakin ingin mengubah harga barang ini?\n\n"
            f"📦 <b>Barang:</b> {h['nama']}\n📐 <b>Satuan:</b> {h['satuan']}\n"
            f"💰 <b>Harga Lama:</b> <code>{format_rupiah(h['harga'])}</code>\n"
            f"✨ <b>Harga Baru:</b> <code>{format_rupiah(harga_baru)}</code>",
            chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(hasil_list):
            markup.add(InlineKeyboardButton(f"✏️ Update {m['nama']} ({m['satuan']})", callback_data=f"mb_apply_price_{i}"))
        markup.add(InlineKeyboardButton("✅ Terapkan ke SEMUA", callback_data="mb_apply_price_all"))
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
        safe_edit_message(bot,
            f"💰 <b>HARGA BARU:</b> <code>{format_rupiah(harga_baru)}</code>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Ditemukan {len(hasil_list)} barang yang mirip. Pilih mana yang ingin diupdate harganya:",
            chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)


def tangani_hapus_barang_chat(chat_id, message_id_target):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    entitas = user_sessions[chat_id]["entitas"]
    nama = entitas.get("BARANG")
    satuan_cari = entitas.get("SATUAN")

    if not nama:
        semua = get_cached_barang() if ctx.IS_DB_CONNECTED else []
        if not semua:
            safe_edit_message(bot, "📭 Master barang masih kosong.", chat_id, message_id_target)
            return
        
        if hasattr(user_sessions, "ensure"):
            sess = user_sessions.ensure(chat_id)
        else:
            sess = user_sessions.setdefault(chat_id, {})
        sess["mb_hapus_msg_id"] = message_id_target
        sess["mb_msg_id"] = message_id_target
        
        # Display barang list for deletion
        markup = InlineKeyboardMarkup(row_width=1)
        for b in semua:
            markup.add(InlineKeyboardButton(f"🗑️ {b['nama']} ({format_rupiah(b['harga'])})", callback_data=f"mb_hapus_prep_{b['row_idx']}"))
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
        safe_edit_message(bot, "Pilih barang yang ingin dihapus:", chat_id, message_id_target, reply_markup=markup)
        return

    semua = get_cached_barang() if ctx.IS_DB_CONNECTED else []
    hasil_list = cari_harga_default(ctx.db_barang, nama, satuan_cari=satuan_cari, semua_barang=semua)
    if not hasil_list:
        safe_edit_message(bot, f"❌ Barang <b>{nama}</b> tidak ditemukan di Master Data.", chat_id, message_id_target, parse_mode="HTML")
        return
    if len(hasil_list) > 1:
        user_sessions[chat_id]["temp_matches"] = hasil_list
        from services.ui_pengaturan import tampilkan_pilihan_barang
        tampilkan_pilihan_barang(chat_id, message_id_target, hasil_list, "pick_del_row")
        return
    hasil = hasil_list[0]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_hapus_{hasil['row_idx']}"),
        InlineKeyboardButton("❌ Batal", callback_data="mb_batal")
    )
    safe_edit_message(bot,
        f"🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Apakah Anda yakin ingin menghapus barang ini dari Master Data?\n\n"
        f"📦 <b>Nama:</b> {hasil['nama']}\n💰 <b>Harga:</b> <code>{format_rupiah(hasil['harga'])}</code>\n"
        f"📐 <b>Satuan:</b> {hasil['satuan']}\n",
        chat_id, message_id_target, parse_mode="HTML", reply_markup=markup)


# =================================================================
# HANDLERS UNTUK UPGRADE EDIT PRODUK (SINGLE & WIZARD FLOWS)
# =================================================================

def _mb_terima_nama_edit_single(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    row_idx = user_sessions[chat_id]["mb_edit_row"]
    msg_id = user_sessions[chat_id]["mb_msg_id"]
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    nama_baru = message.text.strip()
    try:
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if target:
            update_barang(ctx.db_barang, row_idx, nama=nama_baru)
            bot.send_message(chat_id,
                f"✅ <b>Nama barang berhasil diperbarui!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Nama Lama:</b> {target['nama']}\n"
                f"✨ <b>Nama Baru:</b> <b>{nama_baru}</b>", parse_mode="HTML")
            try: bot.delete_message(chat_id, msg_id)
            except: pass
        if chat_id in user_sessions: del user_sessions[chat_id]
    except Exception as e:
        bot.send_message(chat_id, f"❌ Gagal update nama: {e}")


def _mb_terima_harga_edit_single(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    row_idx = user_sessions[chat_id]["mb_edit_row"]
    msg_id = user_sessions[chat_id]["mb_msg_id"]
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    try:
        harga_baru = parse_rupiah(message.text)
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if target:
            update_barang(ctx.db_barang, row_idx, harga=harga_baru)
            bot.send_message(chat_id,
                f"✅ <b>Harga barang berhasil diperbarui!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Barang:</b> {target['nama']}\n"
                f"💰 <b>Harga Lama:</b> <code>{format_rupiah(target['harga'])}</code>\n"
                f"✨ <b>Harga Baru:</b> <b>{format_rupiah(harga_baru)}</b>", parse_mode="HTML")
            try: bot.delete_message(chat_id, msg_id)
            except: pass
        if chat_id in user_sessions: del user_sessions[chat_id]
    except Exception as e:
        bot.send_message(chat_id, f"❌ Input tidak valid atau gagal update harga: {e}")


def _mb_terima_satuan_edit_single(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    row_idx = user_sessions[chat_id]["mb_edit_row"]
    msg_id = user_sessions[chat_id]["mb_msg_id"]
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    unit_baru = message.text.lower().strip()
    try:
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if target:
            update_barang(ctx.db_barang, row_idx, satuan=unit_baru)
            bot.send_message(chat_id,
                f"✅ <b>Satuan barang berhasil diperbarui!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Barang:</b> {target['nama']}\n"
                f"📐 <b>Satuan Lama:</b> {target['satuan']}\n"
                f"✨ <b>Satuan Baru:</b> <b>{unit_baru}</b>", parse_mode="HTML")
            try: bot.delete_message(chat_id, msg_id)
            except: pass
        if chat_id in user_sessions: del user_sessions[chat_id]
    except Exception as e:
        bot.send_message(chat_id, f"❌ Gagal update satuan: {e}")


def _mb_terima_nama_edit_wizard(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    msg_id = user_sessions[chat_id]["mb_msg_id"]
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    nama_baru = message.text.strip()
    user_sessions[chat_id]["mb_pending_nama"] = nama_baru
    msg = safe_edit_message(bot,
        f"🔄 <b>EDIT SEMUA FIELD</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Nama Baru: <b>{nama_baru}</b>\n\n"
        f"💰 Langkah 2: Ketik <b>harga baru</b> (angka saja, mis: <code>15000</code>):",
        chat_id, msg_id, parse_mode="HTML"
    )
    bot.register_next_step_handler(msg, _mb_terima_harga_edit_wizard)


def _mb_terima_harga_edit_wizard(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    msg_id = user_sessions[chat_id]["mb_msg_id"]
    nama_baru = user_sessions[chat_id]["mb_pending_nama"]
    try: bot.delete_message(chat_id, message.message_id)
    except: pass
    try:
        harga_baru = parse_rupiah(message.text)
        user_sessions[chat_id]["mb_pending_harga"] = harga_baru
        # Gunakan daftar satuan dari Master Satuan untuk wizard edit
        from core.master_data import get_all_satuan
        semua_satuan_wizard = get_all_satuan()
        satuan_list_wizard = sorted([s["nama_satuan"].lower() for s in semua_satuan_wizard])
        
        markup = InlineKeyboardMarkup(row_width=3)
        btn_list_wizard = [InlineKeyboardButton(unit.capitalize(), callback_data=f"mb_wizard_unit_{unit}") for unit in satuan_list_wizard]
        for i in range(0, len(btn_list_wizard), 3):
            markup.add(*btn_list_wizard[i:i+3])
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
        safe_edit_message(bot,
            f"🔄 <b>EDIT SEMUA FIELD</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Nama Baru: <b>{nama_baru}</b>\n"
            f"✅ Harga Baru: <code>{format_rupiah(harga_baru)}</code>\n\n"
            f"📐 Langkah 3: Pilih atau ketik <b>satuan baru</b>:",
            chat_id, msg_id, parse_mode="HTML", reply_markup=markup
        )
        bot.register_next_step_handler_by_chat_id(chat_id, _mb_terima_satuan_edit_wizard)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Input tidak valid: {e}")


def _mb_terima_satuan_edit_wizard(message, chat_id=None, message_id_target=None):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    if not chat_id: chat_id = message.chat.id
    try: bot.clear_step_handler_by_chat_id(chat_id)
    except: pass
    if not message_id_target: message_id_target = user_sessions[chat_id].get("mb_msg_id")
    if chat_id not in user_sessions or "mb_edit_row" not in user_sessions[chat_id]: return
    row_idx = user_sessions[chat_id]["mb_edit_row"]
    nama_baru = user_sessions[chat_id]["mb_pending_nama"]
    harga_baru = user_sessions[chat_id]["mb_pending_harga"]
    unit_baru = ""
    if message:
        unit_baru = message.text.lower().strip()
        try: bot.delete_message(chat_id, message.message_id)
        except: pass
    elif "mb_pending_satuan" in user_sessions[chat_id]:
        unit_baru = user_sessions[chat_id]["mb_pending_satuan"]
    try:
        update_barang(ctx.db_barang, row_idx, nama=nama_baru, harga=harga_baru, satuan=unit_baru)
        bot.send_message(chat_id,
            f"✨ <b>PRODUK BERHASIL DIPERBARUI SECARA MENYELURUH</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Nama:</b> <b>{nama_baru}</b>\n"
            f"💰 <b>Harga:</b> <code>{format_rupiah(harga_baru)}</code>\n"
            f"📐 <b>Satuan:</b> {unit_baru}\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Semua data telah diperbarui.", parse_mode="HTML")
        try: bot.delete_message(chat_id, message_id_target)
        except: pass
        if chat_id in user_sessions: del user_sessions[chat_id]
    except Exception as e:
        bot.send_message(chat_id, f"❌ Gagal memperbarui produk: {e}")
