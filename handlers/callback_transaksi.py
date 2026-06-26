"""
Callback Handler — handle_semua_tombol (mega-callback router)
Handles all inline keyboard button presses.
"""
import re
import os
import html
import logging
import math
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.bot_context import ctx
from utils.security import safe_edit_message, authorized_only, log_exception, notify_admins, safe_answer_callback_query, safe_debug_event
from utils.helpers import hitung_ulang_total_dinamis
from services.ui_transaksi import susun_balasan_resume, susun_balasan_update, tampilkan_menu_kriteria_edit, susun_balasan_conversational, susun_balasan_multi_resume, tampilkan_menu_kriteria_edit_multi
from services.ui_pengaturan import tampilkan_pilihan_barang, render_daftar_master_barang
from services.cache_manager import get_cached_barang
from core.master_data import (
    format_rupiah, parse_rupiah,
    get_all_barang, tambah_barang, update_barang, hapus_barang, hapus_semua_barang,
    get_all_metode, tambah_metode, update_metode, hapus_metode,
    cari_harga_default, normalisasi_tanggal_gs, format_daftar_master_barang_grouped
)
from services.debt_tracker import hitung_sisa_tagihan, proses_bayar_tambahan
from handlers.handler_dashboard import handle_dashboard_callbacks
from handlers.crud_metode import _mm_terima_nama, _mm_terima_keyword_edit
from database import db_client
from handlers.crud_transaksi import (
    tangani_simpan_transaksi, tangani_simpan_multi, tangani_read_data, tangani_delete_data,
    tangani_update_status, tangani_revisi_manual, tangani_revisi_manual_multi,
    siapkan_konfirmasi_delete, siapkan_konfirmasi_delete_masal,
    siapkan_konfirmasi_update, tangani_catat_pelunasan,
    _tampilkan_konfirmasi_pelunasan, kirim_halaman_read
)
from handlers.crud_barang import (
    _mb_terima_nama, _mb_terima_harga_edit, _mb_terima_satuan,
    _mb_terima_nama_edit_single, _mb_terima_harga_edit_single, _mb_terima_satuan_edit_single,
    _mb_terima_nama_edit_wizard, _mb_terima_harga_edit_wizard, _mb_terima_satuan_edit_wizard
)

logger = logging.getLogger("bot_logger")

def _render_mb_hapus_picker(chat_id, msg_id, semua_barang, query=None, page=1, page_size=8):
    bot = ctx.bot
    sess = ctx.user_sessions.ensure(chat_id) if hasattr(ctx.user_sessions, "ensure") else ctx.user_sessions.setdefault(chat_id, {})
    items = sorted(semua_barang, key=lambda x: (str(x.get("nama") or "").lower(), str(x.get("satuan") or "").lower()))

    q = (query or "").strip().lower()
    if q:
        items = [b for b in items if q in str(b.get("nama") or "").lower() or q in str(b.get("satuan") or "").lower()]

    matches = [{"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]} for b in items]
    sess["temp_matches"] = matches
    sess["mb_hapus_query"] = q
    sess["mb_hapus_page"] = int(page) if str(page).isdigit() else 1
    sess["state"] = "mb_hapus_browse"

    total = len(items)
    if total == 0:
        teks = (
            "🗑️ <b>HAPUS BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Tidak ada barang yang cocok.\n"
            f"Kata kunci: <code>{q or '-'}</code>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔎 Cari Lagi", callback_data="mb_hapus_search"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(bot, teks, chat_id, msg_id, parse_mode="HTML", reply_markup=markup)
        return

    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(int(page), total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    slice_items = items[start:end]
    slice_indices = list(range(start, min(end, total)))

    info_line = []
    if q:
        info_line.append(f"Pencarian: <code>{q}</code>")
    if total_pages > 1:
        info_line.append(f"Halaman: <b>{page}</b>/<b>{total_pages}</b>")
    teks = (
        "🗑️ <b>HAPUS BARANG</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Pilih barang yang ingin dihapus dari Master Data:"
        + (f"\n{ ' | '.join(info_line) }" if info_line else "")
    )

    markup = InlineKeyboardMarkup(row_width=1)
    for idx, b in zip(slice_indices, slice_items):
        label = f"🗑️ {b['nama']} ({format_rupiah(b['harga'])} / {b['satuan']})"
        if len(label) > 60:
            label = label[:57].rstrip() + "…"
        markup.add(InlineKeyboardButton(label, callback_data=f"pick_del_row_{idx}"))

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"mb_hapus_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"mb_hapus_page_{page+1}"))
    if nav:
        markup.row(*nav)

    markup.row(
        InlineKeyboardButton("🔎 Cari Barang", callback_data="mb_hapus_search"),
        InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"),
    )
    markup.row(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    safe_edit_message(bot, teks, chat_id, msg_id, parse_mode="HTML", reply_markup=markup)


def _mb_hapus_search_input(message):
    chat_id = message.chat.id
    text = (message.text or "").strip()
    sess = ctx.user_sessions.ensure(chat_id) if hasattr(ctx.user_sessions, "ensure") else ctx.user_sessions.setdefault(chat_id, {})
    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    if text.lower() in {"batal", "cancel", "stop", "exit"}:
        q = ""
    else:
        q = text

    semua = get_all_barang(ctx.db_barang)
    _render_mb_hapus_picker(chat_id, sess.get("mb_msg_id") or sess.get("mb_hapus_msg_id") or sess.get("mb_msg_id_last") or message.message_id, semua, query=q, page=1)

def _render_mb_edit_picker(chat_id, msg_id, semua_barang, query=None, page=1, page_size=8):
    bot = ctx.bot
    sess = ctx.user_sessions.ensure(chat_id) if hasattr(ctx.user_sessions, "ensure") else ctx.user_sessions.setdefault(chat_id, {})
    items = sorted(semua_barang, key=lambda x: (str(x.get("nama") or "").lower(), str(x.get("satuan") or "").lower()))
    
    q = (query or "").strip().lower()
    if q:
        items = [b for b in items if q in str(b.get("nama") or "").lower() or q in str(b.get("satuan") or "").lower()]

    matches = [{"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]} for b in items]
    sess["temp_matches"] = matches
    sess["mb_edit_query"] = q
    sess["mb_edit_page"] = int(page) if str(page).isdigit() else 1
    sess["state"] = "mb_edit_browse"

    total = len(items)
    if total == 0:
        teks = (
            "✏️ <b>EDIT BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Tidak ada barang yang cocok.\n"
            f"Kata kunci: <code>{q or '-'}</code>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔎 Cari Lagi", callback_data="mb_edit_search"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(bot, teks, chat_id, msg_id, parse_mode="HTML", reply_markup=markup)
        return

    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(int(page), total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    slice_items = items[start:end]
    slice_indices = list(range(start, min(end, total)))

    info_line = []
    if q:
        info_line.append(f"Pencarian: <code>{q}</code>")
    if total_pages > 1:
        info_line.append(f"Halaman: <b>{page}</b>/<b>{total_pages}</b>")
    teks = (
        "✏️ <b>EDIT BARANG</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Pilih barang yang ingin diedit:"
        + (f"\n{ ' | '.join(info_line) }" if info_line else "")
    )

    markup = InlineKeyboardMarkup(row_width=1)
    for idx, b in zip(slice_indices, slice_items):
        label = f"✏️ {b['nama']} ({format_rupiah(b['harga'])} / {b['satuan']})"
        if len(label) > 60:
            label = label[:57].rstrip() + "…"
        markup.add(InlineKeyboardButton(label, callback_data=f"mb_edit_{b['row_idx']}"))

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"mb_edit_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"mb_edit_page_{page+1}"))
    if nav:
        markup.row(*nav)

    markup.row(InlineKeyboardButton("🔎 Cari Barang", callback_data="mb_edit_search"))
    markup.row(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
    safe_edit_message(bot, teks, chat_id, msg_id, parse_mode="HTML", reply_markup=markup)

def _mb_edit_search_input(message):
    chat_id = message.chat.id
    text = (message.text or "").strip()
    sess = ctx.user_sessions.ensure(chat_id) if hasattr(ctx.user_sessions, "ensure") else ctx.user_sessions.setdefault(chat_id, {})
    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    if text.lower() in {"batal", "cancel", "stop", "exit"}:
        q = ""
    else:
        q = text

    semua = get_all_barang(ctx.db_barang)
    _render_mb_edit_picker(chat_id, sess.get("mb_msg_id") or sess.get("mb_edit_msg_id") or sess.get("mb_msg_id_last") or message.message_id, semua, query=q, page=1)

def _quick_clean_text(text):
    teks = (text or "").strip()
    teks = re.sub(r"\s+", " ", teks).strip()
    return teks


def _quick_read_by_name(message):
    chat_id = message.chat.id
    user_text = (message.text or "").strip()
    
    # Check for cancel first
    if user_text.lower() in {"batal", "cancel", "stop", "exit"}:
        ctx.bot.send_message(chat_id, "❌ Pencarian dibatalkan.")
        return
        
    nama = _quick_clean_text(message.text)
    if not nama:
        ctx.bot.reply_to(message, "❌ Nama kosong. Coba ketik nama pelanggan.")
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "NAMA": nama.title()}  # CLEAN ENTIRE ENTITAS
    msg_loading = ctx.bot.reply_to(message, "⏳ Mencari riwayat transaksi...")
    tangani_read_data(chat_id, msg_loading.message_id)


def _quick_read_by_date(message):
    chat_id = message.chat.id
    user_text = (message.text or "").strip()
    
    # Check for cancel first
    if user_text.lower() in {"batal", "cancel", "stop", "exit"}:
        ctx.bot.send_message(chat_id, "❌ Pencarian dibatalkan.")
        return
        
    raw = _quick_clean_text(message.text)
    if not raw:
        ctx.bot.reply_to(message, "❌ Tanggal kosong. Contoh: 07-11-2024")
        return
    from core.master_data import normalisasi_tanggal_gs
    tgl = normalisasi_tanggal_gs(raw)
    if not tgl:
        ctx.bot.reply_to(
            message,
            "❌ Format tanggal tidak dikenali.\n"
            "Contoh: 20 mei / 30 nop / 12 des 2025 / 12/23/25 / kemarin / 3 hari lalu"
        )
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "TANGGAL": tgl}  # CLEAN ENTIRE ENTITAS
    msg_loading = ctx.bot.reply_to(message, f"⏳ Mencari transaksi tanggal {tgl}...")
    tangani_read_data(chat_id, msg_loading.message_id)


def _quick_read_by_barang(message):
    chat_id = message.chat.id
    user_text = (message.text or "").strip()
    
    # Check for cancel first
    if user_text.lower() in {"batal", "cancel", "stop", "exit"}:
        ctx.bot.send_message(chat_id, "❌ Pencarian dibatalkan.")
        return
        
    brg = _quick_clean_text(message.text)
    if not brg:
        ctx.bot.reply_to(message, "❌ Nama barang kosong. Coba ketik nama barang.")
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "BARANG": brg}  # CLEAN ENTIRE ENTITAS
    msg_loading = ctx.bot.reply_to(message, "⏳ Mencari transaksi berdasarkan barang...")
    tangani_read_data(chat_id, msg_loading.message_id)







def _handle_riwayat_search_input(message):
    """Handle input pencarian riwayat transaksi dari callback riwayat_cari_lain (hanya nama pelanggan)."""
    chat_id = message.chat.id
    user_text = (message.text or "").strip()

    if user_text.lower() in {"batal", "cancel", "stop", "exit"}:
        sess = ctx.user_sessions.ensure(chat_id)
        sess.pop("action", None)
        sess.pop("riwayat_prompt_msg_id", None)
        sess.pop("state", None)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🏠 Menu Utama", callback_data="menu_main"),
            InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"),
        )
        safe_edit_message(
            ctx.bot,
            "❌ <b>Pencarian dibatalkan.</b>",
            chat_id,
            sess.get("riwayat_prompt_msg_id") or message.message_id,
            parse_mode="HTML",
            reply_markup=markup,
        )
        return
    
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.send_message(chat_id, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    
    sess = ctx.user_sessions.ensure(chat_id)
    prompt_msg_id = sess.get("riwayat_prompt_msg_id") or message.message_id
    sess["riwayat_prompt_msg_id"] = prompt_msg_id
    sess["state"] = "awaiting_riwayat_search"

    nama = re.sub(r"\s+", " ", user_text).strip()
    if not nama:
        safe_edit_message(
            ctx.bot,
            "❌ Nama kosong. Coba ketik nama pelanggan.\nContoh: <code>pak andi</code>",
            chat_id,
            prompt_msg_id,
            parse_mode="HTML",
        )
        ctx.bot.register_next_step_handler_by_chat_id(chat_id, _handle_riwayat_search_input)
        return
    
    # Cari berdasarkan nama pelanggan - CLEAR ALL OLD ENTITAS FIELDS FIRST!
    sess["entitas"] = {"AKSI": "Read Data", "NAMA": nama}
    safe_edit_message(
        ctx.bot,
        f"⏳ Mencari transaksi untuk <code>{html.escape(nama)}</code>...",
        chat_id,
        prompt_msg_id,
        parse_mode="HTML",
    )
    tangani_read_data(chat_id, prompt_msg_id)


def _handle_input_cicilan(message):
    """Handle input cicilan dari mode tambah cicilan"""
    chat_id = message.chat.id
    user_text = (message.text or "").strip()
    
    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    if chat_id not in ctx.user_sessions:
        ctx.bot.send_message(chat_id, "❌ Sesi kedaluwarsa")
        return
    
    sess = ctx.user_sessions[chat_id]
    
    if user_text.lower() in {"batal", "cancel", "stop", "exit"}:
        ctx.bot.send_message(chat_id, "❌ Dibatalkan")
        return
    
    # Parse nominal cicilan
    try:
        cicilan_nominal = parse_rupiah(user_text)
        if cicilan_nominal <= 0:
            raise ValueError("Nominal harus lebih dari 0")
    except Exception as e:
        ctx.bot.send_message(chat_id, f"❌ Format nominal tidak valid: {str(e)}")
        return
    
    # Simpan cicilan ke sesi untuk diproses
    sess["nominal_cicilan"] = cicilan_nominal
    sess["update_mode"] = "tambah_cicilan"
    
    # Tampilkan konfirmasi
    safe_edit_message(
        ctx.bot,
        f"✅ <b>KONFIRMASI CICILAN</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Nominal: <code>{format_rupiah(cicilan_nominal)}</code>\n\n"
        f"Apakah sudah benar?",
        chat_id,
        sess.get("msg_idx", 0),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✅ Benar", callback_data="btn_update_kirim"),
            InlineKeyboardButton("❌ Ubah", callback_data="upd_mode_tambah"),
            InlineKeyboardButton("🔙 Batal", callback_data="btn_batal_edit")
        )
    )


def handle_transaksi_callbacks(call):
    chat_id = call.message.chat.id
    msg_idx = call.message.message_id
    cmd = call.data

    if cmd in {"ocr_apply_cicilan", "ocr_cancel_cicilan"}:
        safe_answer_callback_query(ctx.bot, call)
        sess = ctx.user_sessions.ensure(chat_id) if hasattr(ctx.user_sessions, "ensure") else ctx.user_sessions.setdefault(chat_id, {})
        plan = sess.get("ocr_payment_apply_plan") or []

        if cmd == "ocr_cancel_cicilan":
            sess.pop("ocr_payment_apply_plan", None)
            safe_edit_message(
                ctx.bot,
                "❌ <b>Apply cicilan OCR dibatalkan.</b>\nRingkasan hanya ditampilkan tanpa mengubah database.",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            return

        if not plan:
            safe_edit_message(
                ctx.bot,
                "⚠️ <b>Tidak ada alokasi cicilan OCR yang siap di-apply.</b>",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            return

        hasil_lines = ["✅ <b>APPLY CICILAN OCR BERHASIL</b>", "━━━━━━━━━━━━━━━━━━━━━━"]
        total_applied = 0
        gagal = 0

        for item in plan:
            try:
                bayar = int(item.get("bayar") or 0)
                if bayar <= 0:
                    continue
                row_idx = item.get("row_index")
                nama = item.get("name") or "-"
                barang = item.get("barang") or "-"
                tanggal = item.get("tanggal") or "-"
                res = proses_bayar_tambahan(
                    ctx.db_transaksi,
                    ctx.db_histori,
                    row_idx,
                    bayar,
                    nama,
                    f"Apply cicilan OCR {tanggal}",
                )
                if not res.get("sukses"):
                    gagal += 1
                    hasil_lines.append(
                        f"• ❌ {nama} | {barang} | <code>{format_rupiah(bayar)}</code> gagal: <i>{res.get('error') or 'unknown'}</i>"
                    )
                    continue
                total_applied += bayar
                hasil_lines.append(
                    f"• ✅ {nama} | {barang}\n"
                    f"  Bayar: <code>{format_rupiah(bayar)}</code>\n"
                    f"  Sisa Baru: <code>{format_rupiah(res.get('tagihan_baru') or 0)}</code>"
                )
            except Exception as e:
                gagal += 1
                hasil_lines.append(f"• ❌ Gagal apply item: <i>{str(e)[:120]}</i>")

        hasil_lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        hasil_lines.append(f"💰 <b>Total Cicilan Terpakai:</b> <code>{format_rupiah(total_applied)}</code>")
        if gagal:
            hasil_lines.append(f"⚠️ <b>Item gagal:</b> <b>{gagal}</b>")

        sess.pop("ocr_payment_apply_plan", None)
        safe_edit_message(
            ctx.bot,
            "\n".join(hasil_lines),
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        return
    
    # Handle session-less callbacks first
    sessionless_callbacks = [
        "quick_input_text", "quick_input_ocr", "quick_search_menu",
        "read_all_transaksi", "read_filter_hutang", "help_guide",
        "quick_help", "menu_main", "btn_buang", "quick_search_name",
        "quick_search_date", "quick_search_barang", "quick_search_status",
        "quick_search_status_lunas", "quick_search_status_hutang"
    ]
    
    if cmd in sessionless_callbacks or cmd.startswith("guide_"):
        safe_answer_callback_query(ctx.bot, call)
        
        # Handle menu_main: show main menu
        if cmd == "menu_main":
            from handlers.command_handler import build_main_menu_markup, build_menu_text
            safe_edit_message(
                ctx.bot,
                build_menu_text(),
                chat_id,
                msg_idx,
                parse_mode="HTML",
                reply_markup=build_main_menu_markup()
            )
            return
            
        # Handle quick_input_text: start text input mode
        if cmd == "quick_input_text":
            ctx.bot.send_message(
                chat_id,
                "✍️ Silakan ketik detail transaksi Anda (misal: \"Pak Andi beli willo 3 karton lunas tunai\")"
            )
            return
            
        # Handle quick_input_ocr: start photo input mode
        if cmd == "quick_input_ocr":
            teks = (
                "📸 <b>INPUT TRANSAKSI VIA FOTO (OCR)</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Silakan kirimkan foto nota/struk/list pesanan Anda.\n\n"
                "✨ <b>Tips Hasil Terbaik:</b>\n"
                "1. Pastikan foto cukup terang & tulisan terbaca jelas.\n"
                "2. Ambil foto secara tegak lurus (tidak miring).\n\n"
                "<i>Asisten AI akan memproses & mengekstrak data pesanan otomatis.</i>"
            )
            safe_edit_message(
                ctx.bot,
                teks,
                chat_id,
                msg_idx,
                parse_mode="HTML"
            )
            ctx.bot.send_message(chat_id, "📸 Silakan kirim foto nota Anda")
            return
            
        # Handle quick_search_menu: show search menu
        if cmd == "quick_search_menu":
            teks = (
                "🔍 <b>PENCARIAN TRANSAKSI</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Pilih kriteria pencarian transaksi di bawah ini untuk mempermudah menemukan data:"
            )
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("👤 Cari Nama", callback_data="quick_search_name"),
                InlineKeyboardButton("📅 Cari Tanggal", callback_data="quick_search_date")
            )
            markup.add(
                InlineKeyboardButton("📦 Cari Barang", callback_data="quick_search_barang"),
                InlineKeyboardButton("💳 Cari Status Bayar", callback_data="quick_search_status")
            )
            markup.add(
                InlineKeyboardButton("📑 Riwayat Lengkap", callback_data="read_all_transaksi"),
                InlineKeyboardButton("💰 Khusus Hutang", callback_data="read_filter_hutang")
            )
            markup.add(
                InlineKeyboardButton("🏠 Menu Utama", callback_data="menu_main"),
                InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
            )
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            return
            
        # Handle quick_search_name: ask for name
        if cmd == "quick_search_name":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data"}  # CLEAR ALL OLD FIELDS
            teks = "👤 <b>CARI BERDASARKAN NAMA</b>\n━━━━━━━━━━━━━━━━━━━━━━\nKetik nama pelanggan yang ingin Anda cari:"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🔙 Kembali", callback_data="quick_search_menu"),
                InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
            )
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            ctx.bot.register_next_step_handler_by_chat_id(chat_id, _quick_read_by_name)
            return
            
        # Handle quick_search_date: ask for date
        if cmd == "quick_search_date":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data"}  # CLEAR ALL OLD FIELDS
            teks = "📅 <b>CARI BERDASARKAN TANGGAL</b>\n━━━━━━━━━━━━━━━━━━━━━━\nKetik tanggal yang ingin Anda cari (contoh: 20-12-2024 atau kemarin):"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🔙 Kembali", callback_data="quick_search_menu"),
                InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
            )
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            ctx.bot.register_next_step_handler_by_chat_id(chat_id, _quick_read_by_date)
            return
            
        # Handle quick_search_barang: ask for barang
        if cmd == "quick_search_barang":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data"}  # CLEAR ALL OLD FIELDS
            teks = "📦 <b>CARI BERDASARKAN BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\nKetik nama barang yang ingin Anda cari:"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🔙 Kembali", callback_data="quick_search_menu"),
                InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
            )
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            ctx.bot.register_next_step_handler_by_chat_id(chat_id, _quick_read_by_barang)
            return
            
        # Handle quick_search_status: ask for status
        if cmd == "quick_search_status":
            teks = (
                "💳 <b>CARI BERDASARKAN STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                "Pilih status yang ingin Anda cari:"
            )
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("✅ Lunas", callback_data="quick_search_status_lunas"),
                InlineKeyboardButton("⏳ Hutang", callback_data="quick_search_status_hutang")
            )
            markup.add(
                InlineKeyboardButton("🔙 Kembali", callback_data="quick_search_menu"),
                InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
            )
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            return
            
        # Handle quick_search_status_lunas: search for lunas
        if cmd == "quick_search_status_lunas":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data", "STATUS": "Lunas"}
            from handlers.crud_transaksi import tangani_read_data
            tangani_read_data(chat_id, msg_idx)
            return
            
        # Handle quick_search_status_hutang: search for hutang
        if cmd == "quick_search_status_hutang":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data", "STATUS": "Hutang"}
            from handlers.crud_transaksi import tangani_read_data
            tangani_read_data(chat_id, msg_idx)
            return
            
        # Handle read_all_transaksi: show all transactions
        if cmd == "read_all_transaksi":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data", "SEMUA": True}
            from handlers.crud_transaksi import tangani_read_data
            tangani_read_data(chat_id, msg_idx)
            return
            
        # Handle read_filter_hutang: show hutang only
        if cmd == "read_filter_hutang":
            sess = ctx.user_sessions.ensure(chat_id)
            sess["entitas"] = {"AKSI": "Read Data", "STATUS": "Hutang"}
            from handlers.crud_transaksi import tangani_read_data
            tangani_read_data(chat_id, msg_idx)
            return
            
        # Handle help_guide: show guide menu
        if cmd == "help_guide":
            from handlers.command_handler import GUIDE_PAGES, build_guide_markup
            safe_edit_message(
                ctx.bot,
                GUIDE_PAGES["guide_home"],
                chat_id,
                msg_idx,
                parse_mode="HTML",
                reply_markup=build_guide_markup("guide_home")
            )
            return
            
        # Handle guide_* callbacks: show specific guide page
        if cmd.startswith("guide_"):
            from handlers.command_handler import GUIDE_PAGES, build_guide_markup
            page_key = cmd
            if page_key not in GUIDE_PAGES:
                page_key = "guide_home"
            safe_edit_message(
                ctx.bot,
                GUIDE_PAGES[page_key],
                chat_id,
                msg_idx,
                parse_mode="HTML",
                reply_markup=build_guide_markup(page_key)
            )
            return
            
        # Handle quick_help: show welcome message
        if cmd == "quick_help":
            from handlers.command_handler import build_main_menu_markup
            first_name = "User"
            teks = f"""👋 <b>Halo, {first_name}!</b>

Selamat datang di <b>Sistem Kasir Pintar AW Production</b>. Asisten bot pintar untuk mengelola transaksi bisnis & UMKM Anda secara instan.

🚀 <b>FITUR UTAMA:</b>
━━━━━━━━━━━━━━━━━━━━━━
📝 <b>Pencatatan Penjualan Cepat</b>
Ketik penjualan Anda dalam format bebas.
<i>Contoh: "Budi beli roti tawar 2 bungkus lunas cash"</i>

📷 <b>Pencatatan Berbasis Foto (OCR)</b>
Cukup kirim foto nota/kertas coretan transaksi, AI kami akan memproses detailnya secara otomatis.

📊 <b>Dashboard & Laporan Real-time</b>
Kelola database barang, metode pembayaran, serta lacak hutang dengan menekan tombol menu di bawah.
━━━━━━━━━━━━━━━━━━━━━━
"""
            ctx.bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=build_main_menu_markup())
            return
            
        # Handle btn_buang: delete message AND clear session!
        if cmd == "btn_buang":
            try:
                ctx.bot.delete_message(chat_id, msg_idx)
            except:
                safe_edit_message(ctx.bot, "❌ <b>Sesi Ditutup.</b>", chat_id, msg_idx, parse_mode="HTML", reply_markup=None)
            # Clear the session completely so the user can send a new command!
            try:
                if chat_id in ctx.user_sessions:
                    del ctx.user_sessions[chat_id]
            except:
                pass  # Ignore if we can't delete the session!
            return
            
    # Now handle session-required callbacks
    if chat_id not in ctx.user_sessions:
        ctx.bot.answer_callback_query(call.id, "❌ Sesi kedaluwarsa atau bot telah di-restart.\nSilakan ketik ulang perintah Anda.", show_alert=True)
        return
        
    sess = ctx.user_sessions[chat_id]
    
    # ─ Handle pick_* callbacks (pemilihan barang dari tampilan master barang)
    if cmd.startswith(("pick_brg_", "multi_pick_brg_", "pick_edit_row_", "pick_edit_row_full_", "pick_del_row_")):
        handle_pick_barang_callback(call)
        return
    
    # ─ Handle deletion callbacks
    if cmd.startswith("delres_"):
        safe_answer_callback_query(ctx.bot, call)
        try:
            row_idx = int(cmd.replace("delres_", ""))
            match_list = sess.get("hapus_data", [])
            info_row = next((ml for ml in match_list if ml["row_index"] == row_idx), None)
            if info_row:
                from handlers.crud_transaksi import siapkan_konfirmasi_delete
                siapkan_konfirmasi_delete(chat_id, msg_idx, info_row)
            else:
                safe_edit_message(ctx.bot, "❌ Data tidak ditemukan.", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling delres_: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memproses permintaan.", show_alert=True)
        return

    # ─ Handle edit callbacks (resolve_)
    if cmd.startswith("resolve_"):
        safe_answer_callback_query(ctx.bot, call)
        try:
            row_idx = int(cmd.replace("resolve_", ""))
            match_list = sess.get("konflik_data", [])
            info_row = next((ml for ml in match_list if ml["row_index"] == row_idx), None)
            if info_row:
                from handlers.crud_transaksi import siapkan_konfirmasi_update
                siapkan_konfirmasi_update(chat_id, msg_idx, info_row)
            else:
                safe_edit_message(ctx.bot, "❌ Data tidak ditemukan.", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling resolve_: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memproses permintaan.", show_alert=True)
        return
    
    if cmd == "btn_delete_bulk_trigger":
        safe_answer_callback_query(ctx.bot, call)
        try:
            match_list = sess.get("hapus_data", [])
            if match_list:
                from handlers.crud_transaksi import siapkan_konfirmasi_delete_masal
                siapkan_konfirmasi_delete_masal(chat_id, msg_idx, match_list)
            else:
                safe_edit_message(ctx.bot, "❌ Data tidak ditemukan.", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling btn_delete_bulk_trigger: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memproses permintaan.", show_alert=True)
        return
    
    if cmd == "btn_delete_yes":
        safe_answer_callback_query(ctx.bot, call)
        try:
            target_row = sess.get("delete_target_row")
            if target_row is not None:
                removed = db_client.delete_transaksi_ids([target_row])
                safe_edit_message(
                    ctx.bot,
                    f"✅ <b>DATA BERHASIL DIHAPUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nTerhapus: <b>{removed}</b>",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
                if chat_id in ctx.user_sessions:
                    del ctx.user_sessions[chat_id]
            else:
                safe_edit_message(ctx.bot, "❌ Sesi kedaluwarsa.", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling btn_delete_yes: {e}")
            safe_edit_message(ctx.bot, f"❌ Gagal menghapus data: {e}", chat_id, msg_idx)
        return
    
    if cmd == "btn_delete_masal_yes":
        safe_answer_callback_query(ctx.bot, call)
        try:
            row_indices = sess.get("delete_masal_rows", [])
            if row_indices:
                removed = db_client.delete_transaksi_ids(row_indices)
                safe_edit_message(
                    ctx.bot,
                    f"✅ <b>DATA BERHASIL DIHAPUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nTerhapus: <b>{removed}</b>",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
                if chat_id in ctx.user_sessions:
                    del ctx.user_sessions[chat_id]
            else:
                safe_edit_message(ctx.bot, "❌ Sesi kedaluwarsa.", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling btn_delete_masal_yes: {e}")
            safe_edit_message(ctx.bot, f"❌ Gagal menghapus data: {e}", chat_id, msg_idx)
        return
    
    if cmd == "btn_delete_no":
        safe_answer_callback_query(ctx.bot, call)
        safe_edit_message(ctx.bot, "❌ Dibatalkan.", chat_id, msg_idx)
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]
        return
    
    if cmd == "trx_dedup_no":
        safe_edit_message(ctx.bot, "❌ Dibatalkan.", chat_id, msg_idx)
        sess.pop("dedup_transaksi_ids", None)
        return

    if cmd == "trx_dedup_yes":
        ids = sess.get("dedup_transaksi_ids") or []
        if not ids:
            safe_edit_message(ctx.bot, "⚠️ Tidak ada data duplikat di sesi.", chat_id, msg_idx)
            return
        try:
            safe_edit_message(ctx.bot, "⏳ Menghapus duplikat...", chat_id, msg_idx)
            removed = db_client.delete_transaksi_ids(ids)
            sess.pop("dedup_transaksi_ids", None)
            safe_edit_message(
                ctx.bot,
                "✅ <b>DUPLIKAT DIBERSIHKAN</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Terhapus: <b>{removed}</b>",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
        except Exception:
            pass
        return

    # Batch processing
    if cmd == "btn_multi_kirim":
        safe_debug_event({
            "runId": "pre-fix",
            "hypothesisId": "A",
            "location": "handlers/callback_transaksi.py:845",
            "msg": "[DEBUG] btn_multi_kirim clicked",
            "data": {"chat_id": chat_id, "msg_idx": msg_idx, "has_session": bool(sess), "multi_count": len(sess.get("multi_results") or []) if sess else 0},
        })
        tangani_simpan_multi(chat_id, msg_idx)
        return

    if cmd == "btn_multi_lengkapi":
        results = sess.get("multi_results") or []
        if not results:
            ctx.bot.answer_callback_query(call.id, "Data batch tidak ditemukan.")
            return
        sess["multi_edit_mode"] = "missing_only"
        teks = (
            "🧩 <b>LENGKAPI BATCH</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Pilih item yang masih kurang untuk dilengkapi:\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        shown = 0
        for i, r in enumerate(results[:50], 1):
            miss = r.get("missing_fields") or []
            if not miss:
                continue
            e = r.get("entitas", {}) or {}
            brg = e.get("BARANG") or "-"
            jml = e.get("JUMLAH") or "-"
            teks += f"• <b>[{i}]</b> {jml} {brg}\n"
            markup.add(InlineKeyboardButton(f"🧩 Lengkapi [{i}] {brg}", callback_data=f"multi_pick_{i-1}"))
            shown += 1
        if shown == 0:
            safe_edit_message(
                ctx.bot,
                "✅ <b>DATA BATCH SUDAH LENGKAP</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Tidak ada item yang perlu dilengkapi.",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            return
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
        markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
        return

    if cmd == "btn_lengkapi":
        entitas = sess.get("entitas", {}) or {}
        field_wajib = ["TANGGAL", "NAMA", "BARANG", "JUMLAH", "TOTAL", "STATUS", "METODE_PEMBAYARAN"]
        missing = [f for f in field_wajib if not entitas.get(f)]
        sess["missing_fields"] = missing
        tampilkan_menu_kriteria_edit(chat_id, msg_idx, mode="missing_only")
        return

    if cmd == "btn_multi_edit":
        results = sess.get("multi_results") or []
        if not results:
            ctx.bot.answer_callback_query(call.id, "Data batch tidak ditemukan.")
            return
        sess["multi_edit_mode"] = "all"
        teks = (
            "🛠️ <b>EDIT BATCH</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Pilih item yang ingin diubah:\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        for i, r in enumerate(results[:20], 1):
            e = r.get("entitas", {}) or {}
            brg = e.get("BARANG") or "-"
            jml = e.get("JUMLAH") or "-"
            teks += f"• <b>[{i}]</b> {jml} {brg}\n"
            markup.add(InlineKeyboardButton(f"✏️ Edit [{i}] {brg}", callback_data=f"multi_pick_{i-1}"))
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
        markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
        return

    if cmd == "btn_buang":
        ctx.bot.answer_callback_query(call.id, "✅ Ditutup")
        try:
            ctx.bot.delete_message(chat_id, msg_idx)
        except:
            safe_edit_message(ctx.bot, "❌ <b>Sesi Ditutup.</b>", chat_id, msg_idx, parse_mode="HTML", reply_markup=None)
        if chat_id in ctx.user_sessions:
            sess = ctx.user_sessions[chat_id]
            if sess.get("action") == "reading_pagination":
                sess["action"] = "standby"
            sess.pop("entitas", None)
            sess.pop("data_list", None)
            sess.pop("ringkasan_teks", None)
            sess.pop("action", None)
        return

    if cmd == "riwayat_cari_lain":
        # Reset sesi dan mulai pencarian ulang
        if chat_id in ctx.user_sessions:
            sess = ctx.user_sessions[chat_id]
            sess.pop("action", None)
            sess.pop("data_list", None)
            sess.pop("ringkasan_teks", None)
            sess.pop("current_page", None)
            sess.pop("total_pages", None)
            sess.pop("entitas", None)  # CLEAR OLD ENTITAS
            sess.pop("state", None)
            sess.pop("riwayat_prompt_msg_id", None)
        
        # Tampilkan menu pencarian ulang
        sess = ctx.user_sessions.ensure(chat_id)
        # Initialize clean entitas with no leftover fields
        sess["entitas"] = {"AKSI": "Read Data"}
        sess["state"] = "awaiting_riwayat_search"
        sess["riwayat_prompt_msg_id"] = msg_idx
        teks = (
            "🔍 <b>CARI RIWAYAT TRANSAKSI</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Ketik nama pelanggan yang ingin dicari:\n\n"
            "Contoh:\n"
            "• <code>pak andi</code>\n"
            "• <code>bu siti</code>\n"
            "• <i>Atau klik tombol Batal</i>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="riwayat_cancel"))
        safe_edit_message(
            ctx.bot,
            teks,
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup
        )
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        ctx.bot.register_next_step_handler_by_chat_id(chat_id, _handle_riwayat_search_input)
        return

    if cmd == "riwayat_cancel":
        safe_answer_callback_query(ctx.bot, call)
        sess = ctx.user_sessions.ensure(chat_id)
        sess.pop("action", None)
        sess.pop("data_list", None)
        sess.pop("ringkasan_teks", None)
        sess.pop("current_page", None)
        sess.pop("total_pages", None)
        sess.pop("entitas", None)
        sess.pop("state", None)
        sess.pop("riwayat_prompt_msg_id", None)
        safe_edit_message(
            ctx.bot,
            "❌ <b>Pencarian dibatalkan.</b>",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=None,
        )
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        return

    if cmd.startswith("read_page_"):
        try:
            page = int(cmd.replace("read_page_", ""))
            kirim_halaman_read(chat_id, page, msg_idx, call.id)
        except Exception as e:
            logger.error(f"Error handling read_page callback: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memuat halaman", show_alert=True)
        return

    if cmd.startswith("read_date_"):
        try:
            tgl = cmd.replace("read_date_", "")
            if chat_id in ctx.user_sessions:
                sess = ctx.user_sessions[chat_id]
                sess["entitas"] = sess.get("entitas", {})
                sess["entitas"]["TANGGAL"] = tgl
            tangani_read_data(chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error handling read_date callback: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memproses tanggal", show_alert=True)
        return

    if cmd == "btn_multi_edit_back":
        susun_balasan_multi_resume(chat_id, msg_idx)
        return

    if cmd == "btn_multi_pick_back":
        if sess.get("multi_edit_mode") == "missing_only":
            cmd = "btn_multi_lengkapi"
        else:
            cmd = "btn_multi_edit"
        safe_answer_callback_query(ctx.bot, call)
        if cmd == "btn_multi_lengkapi":
            results = sess.get("multi_results") or []
            if not results:
                safe_edit_message(ctx.bot, "❌ Data batch tidak ditemukan.", chat_id, msg_idx)
                return
            sess["multi_edit_mode"] = "missing_only"
            teks = (
                "🧩 <b>LENGKAPI BATCH</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Pilih item yang masih kurang untuk dilengkapi:\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            markup = InlineKeyboardMarkup(row_width=1)
            shown = 0
            for i, r in enumerate(results[:50], 1):
                miss = r.get("missing_fields") or []
                if not miss:
                    continue
                e = r.get("entitas", {}) or {}
                brg = e.get("BARANG") or "-"
                jml = e.get("JUMLAH") or "-"
                teks += f"• <b>[{i}]</b> {jml} {brg}\n"
                markup.add(InlineKeyboardButton(f"🧩 Lengkapi [{i}] {brg}", callback_data=f"multi_pick_{i-1}"))
                shown += 1
            if shown == 0:
                safe_edit_message(
                    ctx.bot,
                    "✅ <b>DATA BATCH SUDAH LENGKAP</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    "Tidak ada item yang perlu dilengkapi.",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
                return
            markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
            markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            return
        else:
            results = sess.get("multi_results") or []
            if not results:
                safe_edit_message(ctx.bot, "❌ Data batch tidak ditemukan.", chat_id, msg_idx)
                return
            sess["multi_edit_mode"] = "all"
            teks = (
                "🛠️ <b>EDIT BATCH</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Pilih item yang ingin diubah:\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            markup = InlineKeyboardMarkup(row_width=1)
            for i, r in enumerate(results[:20], 1):
                e = r.get("entitas", {}) or {}
                brg = e.get("BARANG") or "-"
                jml = e.get("JUMLAH") or "-"
                teks += f"• <b>[{i}]</b> {jml} {brg}\n"
                markup.add(InlineKeyboardButton(f"✏️ Edit [{i}] {brg}", callback_data=f"multi_pick_{i-1}"))
            markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
            markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
            safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
            return

    # Handler untuk tombol-tombol yang sebelumnya tidak ditangani
    if cmd == "btn_masuk_pelunasan":
        safe_answer_callback_query(ctx.bot, call)
        tangani_catat_pelunasan(chat_id, msg_idx)
        return

    if cmd == "btn_masuk_edit":
        safe_answer_callback_query(ctx.bot, call)
        tampilkan_menu_kriteria_edit(chat_id, msg_idx, mode="all")
        return

    if cmd == "upd_mode_tambah":
        safe_answer_callback_query(ctx.bot, call)
        sess["update_mode"] = "tambah_cicilan"
        sess["action"] = "update_data"
        from services.ui_transaksi import susun_balasan_update
        susun_balasan_update(chat_id, msg_idx)
        return

    if cmd == "upd_mode_koreksi":
        safe_answer_callback_query(ctx.bot, call)
        sess["update_mode"] = "koreksi_data"
        sess["action"] = "update_data"
        from services.ui_transaksi import susun_balasan_update
        susun_balasan_update(chat_id, msg_idx)
        return

    if cmd == "btn_update_kirim":
        safe_answer_callback_query(ctx.bot, call)
        update_mode = sess.get("update_mode", "koreksi_data")
        
        row_idx = sess.get("update_target_row")
        ent = sess.get("entitas", {})
        update_info = sess.get("update_info", {})
        
        if not row_idx:
            safe_edit_message(ctx.bot, "❌ Data tidak ditemukan. Silakan mulai edit kembali.", chat_id, msg_idx)
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            return
        
        try:
            if update_mode == "tambah_cicilan" and update_info.get("nominal_baru") is not None:
                new_metode = ent.get("METODE_PEMBAYARAN") or "-"
                nama_pelanggan = ent.get("NAMA", "")
                proses_bayar_tambahan(ctx.db_transaksi, None, row_idx, update_info["nominal_baru"], nama_pelanggan, new_metode)
                msg_final = f"✅ <b>Update Berhasil!</b>\n\nCicilan ditambahkan sebesar <code>{format_rupiah(update_info['nominal_baru'])}</code>."
            else:
                data_update = {}
                if ent.get("TANGGAL"):
                    data_update["tanggal"] = ent["TANGGAL"]
                if ent.get("NAMA"):
                    data_update["nama_pelanggan"] = ent["NAMA"]
                if ent.get("BARANG"):
                    data_update["barang"] = ent["BARANG"]
                if ent.get("JUMLAH"):
                    data_update["jumlah_satuan"] = ent["JUMLAH"]
                if ent.get("HARGA"):
                    data_update["harga"] = parse_rupiah(ent["HARGA"])
                if ent.get("TOTAL"):
                    data_update["total"] = parse_rupiah(ent["TOTAL"])
                if ent.get("STATUS"):
                    status = ent["STATUS"].title()
                    data_update["status"] = status
                    if status.lower() == "lunas":
                        data_update["uang_masuk"] = parse_rupiah(ent["TOTAL"])
                        data_update["tagihan"] = 0
                if ent.get("METODE_PEMBAYARAN"):
                    data_update["metode_pembayaran"] = ent["METODE_PEMBAYARAN"].title()
                if update_info.get("nominal_baru") is not None:
                    if update_mode == "koreksi_data":
                        uang_masuk = update_info["nominal_baru"]
                    else:
                        uang_masuk = update_info.get("uang_masuk_lama", 0) + update_info["nominal_baru"]
                    data_update["uang_masuk"] = uang_masuk
                    total = parse_rupiah(ent.get("TOTAL", "0"))
                    data_update["tagihan"] = max(0, total - uang_masuk)
                
                if data_update:
                    db_client.update_transaksi_db(row_idx, data_update)
                msg_final = f"✅ <b>Data Diperbarui!</b>\n\nPerubahan berhasil disimpan ke database."
            
            safe_edit_message(ctx.bot, msg_final, chat_id, msg_idx, parse_mode="HTML")
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
                
        except Exception as e:
            logger.error(f"Error handling btn_update_kirim: {e}")
            safe_edit_message(ctx.bot, f"❌ Gagal memperbarui data: {e}", chat_id, msg_idx)
        
        return

    if cmd == "btn_kirim":
        safe_debug_event({
            "runId": "pre-fix",
            "hypothesisId": "A",
            "location": "handlers/callback_transaksi.py:1168",
            "msg": "[DEBUG] btn_kirim clicked",
            "data": {"chat_id": chat_id, "msg_idx": msg_idx, "missing_fields": sess.get("missing_fields") if sess else None, "entitas_keys": sorted(list((sess.get("entitas") or {}).keys())) if sess else []},
        })
        safe_answer_callback_query(ctx.bot, call)
        missing = sess.get("missing_fields")
        if missing:
            susun_balasan_resume(chat_id, msg_idx, confirm_force=True)
        else:
            tangani_simpan_transaksi(chat_id, msg_idx)
        return

    if cmd == "btn_kirim_force":
        safe_debug_event({
            "runId": "pre-fix",
            "hypothesisId": "A",
            "location": "handlers/callback_transaksi.py:1177",
            "msg": "[DEBUG] btn_kirim_force clicked",
            "data": {"chat_id": chat_id, "msg_idx": msg_idx, "entitas_keys": sorted(list((sess.get("entitas") or {}).keys())) if sess else []},
        })
        safe_answer_callback_query(ctx.bot, call)
        tangani_simpan_transaksi(chat_id, msg_idx)
        return

    if cmd == "btn_batal_edit":
        safe_answer_callback_query(ctx.bot, call)
        safe_edit_message(
            ctx.bot,
            "✅ Edit dibatalkan. Kembali ke menu utama.",
            chat_id,
            msg_idx
        )
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]
        return

    # Handle single edit callbacks (edit_TANGGAL, edit_NAMA, etc.)
    if cmd.startswith("edit_"):
        safe_answer_callback_query(ctx.bot, call)
        field = cmd.replace("edit_", "")
        # Map to user-friendly prompts
        prompts = {
            "TANGGAL": "📅 Masukkan tanggal baru (contoh: 21-06-2026 atau hari ini):",
            "NAMA": "👤 Masukkan nama pelanggan baru:",
            "BARANG": "📦 Masukkan nama barang baru:",
            "JUMLAH": "🔢 Masukkan jumlah baru (contoh: 10 dus):",
            "SATUAN": "📐 Masukkan satuan baru (contoh: dus, bungkus):",
            "HARGA": "💰 Masukkan harga satuan baru:",
            "TOTAL": "💵 Masukkan total harga baru:",
            "STATUS": "💳 Masukkan status baru (Lunas/Hutang):",
            "METODE_PEMBAYARAN": "🏦 Masukkan metode pembayaran baru:",
            "NOMINAL_BAYAR": "💸 Masukkan nominal cicilan/DP baru:"
        }
        prompt = prompts.get(field, f"✏️ Masukkan nilai baru untuk {field}:")
        sess["state"] = "awaiting_edit_teks"
        sess["field_target"] = field
        sess["summary_msg_id"] = msg_idx
        safe_edit_message(ctx.bot, prompt, chat_id, msg_idx, parse_mode="HTML")
        return

    # Handle multi edit callbacks (multi_edit_TANGGAL, etc.)
    if cmd.startswith("multi_edit_"):
        safe_answer_callback_query(ctx.bot, call)
        field = cmd.replace("multi_edit_", "")
        # Map to user-friendly prompts
        prompts = {
            "TANGGAL": "📅 Masukkan tanggal baru untuk item ini:",
            "NAMA": "👤 Masukkan nama pelanggan baru untuk item ini:",
            "BARANG": "📦 Masukkan nama barang baru untuk item ini:",
            "JUMLAH": "🔢 Masukkan jumlah baru untuk item ini:",
            "SATUAN": "📐 Masukkan satuan baru untuk item ini:",
            "HARGA": "💰 Masukkan harga satuan baru untuk item ini:",
            "TOTAL": "💵 Masukkan total harga baru untuk item ini:",
            "STATUS": "💳 Masukkan status baru untuk item ini:",
            "METODE_PEMBAYARAN": "🏦 Masukkan metode pembayaran baru untuk item ini:",
            "NOMINAL_BAYAR": "💸 Masukkan nominal cicilan/DP baru untuk item ini:"
        }
        prompt = prompts.get(field, f"✏️ Masukkan nilai baru untuk {field}:")
        sess["state"] = "awaiting_edit_teks_multi"
        sess["field_target"] = field
        sess["summary_msg_id"] = msg_idx
        safe_edit_message(ctx.bot, prompt, chat_id, msg_idx, parse_mode="HTML")
        return

    # Handle selecting which transaction to pay
    if cmd.startswith("pel_pilih_"):
        safe_answer_callback_query(ctx.bot, call)
        try:
            row_idx = int(cmd.replace("pel_pilih_", ""))
            hutang_list = sess.get("hutang_list", [])
            info_hutang = next((h for h in hutang_list if h["row_index"] == row_idx), None)
            if not info_hutang:
                safe_edit_message(ctx.bot, "❌ Data hutang tidak ditemukan", chat_id, msg_idx)
                return
            
            from handlers.crud_transaksi import _tampilkan_konfirmasi_pelunasan
            _tampilkan_konfirmasi_pelunasan(chat_id, msg_idx, info_hutang, sess.get("nominal_bayar"))
        except Exception as e:
            logger.error(f"Error handling pel_pilih: {e}")
            safe_edit_message(ctx.bot, f"❌ Error: {str(e)}", chat_id, msg_idx)
        return
        
    if cmd == "pel_konfirm_ya":
        safe_answer_callback_query(ctx.bot, call)
        # Lanjutkan catat pelunasan yang sudah dikonfirmasi
        row_idx = sess.get("pel_row_idx")
        nominal_bayar = sess.get("pel_nominal")
        nama = sess.get("pel_nama")
        
        if row_idx is None or nominal_bayar is None:
            safe_edit_message(ctx.bot, "❌ Data pelunasan tidak ditemukan", chat_id, msg_idx)
            return
            
        # Update histori pelunasan di database
        try:
            from services.debt_tracker import proses_bayar_tambahan
            from core.master_data import format_rupiah
            
            result = proses_bayar_tambahan(ctx.db_transaksi, None, row_idx, nominal_bayar, nama)
            if result.get("sukses"):
                safe_edit_message(
                    ctx.bot,
                    f"✅ <b>PELUNASAN TERCATAT</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"Nominal: <code>{format_rupiah(nominal_bayar)}</code>\n"
                    f"Status: <b>TERCATAT</b>",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
            else:
                safe_edit_message(ctx.bot, f"❌ Gagal mencatat pelunasan: {result.get('error', 'Unknown error')}", chat_id, msg_idx)
        except Exception as e:
            logger.error(f"Error processing pelunasan: {e}")
            safe_edit_message(ctx.bot, f"❌ Error: {str(e)}", chat_id, msg_idx)
        finally:
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
        return

    # Fallback untuk callback yang tidak ditangani di atas
    from handlers.callback_pengaturan import handle_master_dan_pelunasan as handle_master_fallback
    handle_master_fallback(call)


def handle_pick_barang_callback(call):
    """
    Handler untuk callbacks pick_brg_*, multi_pick_brg_*, pick_edit_row_*, 
    pick_edit_row_full_*, pick_del_row_* dari tampilan pemilihan barang.
    """
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    
    if chat_id not in ctx.user_sessions or "temp_matches" not in ctx.user_sessions[chat_id]:
        ctx.bot.answer_callback_query(call.id, "❌ Sesi kedaluwarsa. Silakan ulangi perintah.")
        return
        
    matches = ctx.user_sessions[chat_id]["temp_matches"]
    safe_answer_callback_query(ctx.bot, call)
    
    try:
        if data.startswith("multi_pick_brg_"):
            parts = data.split("_")
            if len(parts) < 5:
                ctx.bot.answer_callback_query(call.id, "Format tidak valid.")
                return
            item_idx = int(parts[3])
            choice_idx = int(parts[4])
            m = matches[choice_idx]

            sess = ctx.user_sessions[chat_id]
            results = sess.get("multi_results") or []
            if item_idx < 0 or item_idx >= len(results):
                safe_edit_message(ctx.bot, "❌ Item batch tidak ditemukan.", chat_id, msg_id)
                return

            entitas = results[item_idx].get("entitas", {}) or {}
            entitas["BARANG"] = m["nama"]
            entitas["HARGA"] = format_rupiah(m["harga"])
            entitas["SATUAN"] = m["satuan"]
            hitung_ulang_total_dinamis(entitas)
            results[item_idx]["entitas"] = entitas
            sess["multi_results"] = results
            sess["edit_notice"] = f"Item #{item_idx+1}: barang dipilih <b>{m['nama']}</b>"

            susun_balasan_multi_resume(chat_id, msg_id)

        elif data.startswith("pick_brg_"):
            idx = int(data.replace("pick_brg_", ""))
            m = matches[idx]
            if "entitas" not in ctx.user_sessions[chat_id]:
                safe_edit_message(ctx.bot, "❌ Sesi data hilang, silakan ulangi.", chat_id, msg_id)
                return

            entitas = ctx.user_sessions[chat_id]["entitas"]
            entitas["BARANG"] = m["nama"]
            entitas["HARGA"] = format_rupiah(m["harga"])
            entitas["SATUAN"] = m["satuan"]
            hitung_ulang_total_dinamis(entitas)
            ctx.user_sessions[chat_id]["edit_notice"] = f"Barang dipilih: <b>{m['nama']}</b>"
            
            if ctx.user_sessions[chat_id].get("is_update_mode"):
                susun_balasan_update(chat_id, msg_id)
            else:
                susun_balasan_resume(chat_id, msg_id)
                
        elif data.startswith("pick_edit_row_full_"):
            idx = int(data.replace("pick_edit_row_full_", ""))
            m = matches[idx]
            entitas = ctx.user_sessions[chat_id].get("entitas", {})
            row_idx = m["row_idx"]
            
            harga_baru = parse_rupiah(entitas.get("HARGA") or "0")
            satuan_baru = entitas.get("SATUAN")
            
            ctx.user_sessions[chat_id]["pending_price_update"] = {
                "row": row_idx,
                "barang": m["nama"],
                "harga": harga_baru,
                "satuan": satuan_baru
            }
            
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("✅ Ya, Terapkan ke Semua", callback_data="btn_bulk_price_yes"),
                InlineKeyboardButton("❌ Tidak, Barang Ini Saja", callback_data="btn_bulk_price_no")
            )
            safe_edit_message(ctx.bot, 
                f"🔄 <b>UPDATE HARGA: {m['nama']}</b>\n\n"
                f"Ditemukan transaksi lain dengan barang yang sama.\n"
                f"Apakah Anda ingin menerapkan harga <code>{format_rupiah(harga_baru)}</code> ke <b>SEMUA</b> transaksi <code>{m['nama']}</code> yang belum lunas?",
                chat_id, msg_id, parse_mode="HTML", reply_markup=markup
            )
            
        elif data.startswith("pick_edit_row_"):
            idx = int(data.replace("pick_edit_row_", ""))
            m = matches[idx]
            row_idx = m["row_idx"]
            ctx.user_sessions[chat_id]["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_id
            msg = safe_edit_message(ctx.bot, f"💸 Berapa harga baru untuk <b>{m['nama']}</b> ({m['satuan']})?\n(Harga saat ini: {format_rupiah(m['harga'])})", chat_id, msg_id, parse_mode="HTML")
            ctx.bot.register_next_step_handler(msg, _mb_terima_harga_edit)

        elif data.startswith("pick_del_row_"):
            idx = int(data.replace("pick_del_row_", ""))
            logger.info(f"[PICK DEL DEBUG] idx={idx}, matches={matches}")
            m = matches[idx]
            logger.info(f"[PICK DEL DEBUG] m={m}, m['row_idx']={m.get('row_idx')}")
            row_idx = m["row_idx"]
            
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_hapus_{row_idx}"),
                InlineKeyboardButton("❌ Batal", callback_data="mb_batal")
            )
            safe_edit_message(ctx.bot, 
                f"🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Apakah Anda yakin ingin menghapus barang ini dari Master Data?\n\n"
                f"📦 <b>Nama:</b> {m['nama']}\n"
                f"💸 <b>Harga:</b> <code>{format_rupiah(m['harga'])}</code>\n"
                f"📏 <b>Satuan:</b> {m['satuan']}\n",
                chat_id, msg_id, parse_mode="HTML", reply_markup=markup
            )
        else:
            safe_answer_callback_query(ctx.bot, call, "❌ Aksi tidak dikenali")
            
    except Exception as e:
        logger.error(f"Error in handle_pick_barang_callback: {e}")
        safe_answer_callback_query(ctx.bot, call, "❌ Terjadi kesalahan")
        notify_admins(f"Error handling pick callback: {e}")
