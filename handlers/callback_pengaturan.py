"""
Callback Handler — handle_semua_tombol (mega-callback router)
Handles all inline keyboard button presses.
"""
import logging
import math
import os
import re
import traceback

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.bot_context import ctx
from core.master_data import (
    cari_harga_default,
    format_daftar_master_barang_grouped,
    format_rupiah,
    get_all_barang,
    get_all_metode,
    get_all_satuan,
    hapus_barang,
    hapus_metode,
    hapus_satuan,
    hapus_semua_barang,
    normalisasi_tanggal_gs,
    parse_rupiah,
    tambah_barang,
    tambah_metode,
    tambah_satuan,
    update_barang,
    update_metode,
    update_satuan,
)
from database import db_client
from handlers.crud_barang import (
    _mb_terima_harga_edit,
    _mb_terima_harga_edit_single,
    _mb_terima_harga_edit_wizard,
    _mb_terima_nama,
    _mb_terima_nama_edit_single,
    _mb_terima_nama_edit_wizard,
    _mb_terima_satuan,
    _mb_terima_satuan_edit_single,
    _mb_terima_satuan_edit_wizard,
)
from handlers.crud_metode import _mm_terima_keyword_edit, _mm_terima_nama
from handlers.crud_satuan import _ms_terima_nama, _ms_terima_nama_edit
from handlers.crud_transaksi import (
    _tampilkan_konfirmasi_pelunasan,
    kirim_halaman_read,
    siapkan_konfirmasi_delete,
    siapkan_konfirmasi_delete_masal,
    siapkan_konfirmasi_update,
    tangani_catat_pelunasan,
    tangani_delete_data,
    tangani_read_data,
    tangani_revisi_manual,
    tangani_revisi_manual_multi,
    tangani_simpan_multi,
    tangani_update_status,
)
from handlers.handler_dashboard import handle_dashboard_callbacks
from services.cache_manager import get_cached_barang
from services.debt_tracker import hitung_sisa_tagihan, proses_bayar_tambahan
from services.ui_pengaturan import render_daftar_master_barang, tampilkan_pilihan_barang
from services.ui_transaksi import (
    susun_balasan_conversational,
    susun_balasan_multi_resume,
    susun_balasan_resume,
    susun_balasan_update,
    tampilkan_menu_kriteria_edit,
    tampilkan_menu_kriteria_edit_multi,
)
from utils.helpers import hitung_ulang_total_dinamis
from utils.security import (
    authorized_only,
    log_exception,
    notify_admins,
    safe_answer_callback_query,
    safe_edit_message,
)

logger = logging.getLogger("bot_logger")


def _render_mb_hapus_picker(chat_id, msg_id, semua_barang, query=None, page=1, page_size=8):
    bot = ctx.bot
    sess = (
        ctx.user_sessions.ensure(chat_id)
        if hasattr(ctx.user_sessions, "ensure")
        else ctx.user_sessions.setdefault(chat_id, {})
    )
    items = sorted(
        semua_barang,
        key=lambda x: (str(x.get("nama") or "").lower(), str(x.get("satuan") or "").lower()),
    )

    q = (query or "").strip().lower()
    if q:
        items = [
            b
            for b in items
            if q in str(b.get("nama") or "").lower() or q in str(b.get("satuan") or "").lower()
        ]

    matches = [
        {"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]}
        for b in items
    ]
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
    sess = (
        ctx.user_sessions.ensure(chat_id)
        if hasattr(ctx.user_sessions, "ensure")
        else ctx.user_sessions.setdefault(chat_id, {})
    )
    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    if text.lower() in {"batal", "cancel", "stop", "exit"}:
        q = ""
    else:
        q = text

    semua = get_all_barang(ctx.db_barang)
    _render_mb_hapus_picker(
        chat_id,
        sess.get("mb_msg_id")
        or sess.get("mb_hapus_msg_id")
        or sess.get("mb_msg_id_last")
        or message.message_id,
        semua,
        query=q,
        page=1,
    )


def _render_mb_edit_picker(chat_id, msg_id, semua_barang, query=None, page=1, page_size=8):
    bot = ctx.bot
    sess = (
        ctx.user_sessions.ensure(chat_id)
        if hasattr(ctx.user_sessions, "ensure")
        else ctx.user_sessions.setdefault(chat_id, {})
    )
    items = sorted(
        semua_barang,
        key=lambda x: (str(x.get("nama") or "").lower(), str(x.get("satuan") or "").lower()),
    )

    q = (query or "").strip().lower()
    if q:
        items = [
            b
            for b in items
            if q in str(b.get("nama") or "").lower() or q in str(b.get("satuan") or "").lower()
        ]

    matches = [
        {"nama": b["nama"], "harga": b["harga"], "satuan": b["satuan"], "row_idx": b["row_idx"]}
        for b in items
    ]
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
        "Pilih barang yang ingin diedit:" + (f"\n{ ' | '.join(info_line) }" if info_line else "")
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
    sess = (
        ctx.user_sessions.ensure(chat_id)
        if hasattr(ctx.user_sessions, "ensure")
        else ctx.user_sessions.setdefault(chat_id, {})
    )
    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    if text.lower() in {"batal", "cancel", "stop", "exit"}:
        q = ""
    else:
        q = text

    semua = get_all_barang(ctx.db_barang)
    _render_mb_edit_picker(
        chat_id,
        sess.get("mb_msg_id")
        or sess.get("mb_edit_msg_id")
        or sess.get("mb_msg_id_last")
        or message.message_id,
        semua,
        query=q,
        page=1,
    )


def _quick_clean_text(text):
    teks = (text or "").strip()
    teks = re.sub(r"\s+", " ", teks).strip()
    return teks


def _quick_read_by_name(message):
    chat_id = message.chat.id
    nama = _quick_clean_text(message.text)
    if not nama:
        ctx.bot.reply_to(message, "❌ Nama kosong. Coba ketik nama pelanggan.")
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "NAMA": nama.title()}
    msg_loading = ctx.bot.reply_to(message, "⏳ Mencari riwayat transaksi...")
    tangani_read_data(chat_id, msg_loading.message_id)


def _quick_read_by_date(message):
    chat_id = message.chat.id
    raw = _quick_clean_text(message.text)
    if not raw:
        ctx.bot.reply_to(message, "❌ Tanggal kosong. Contoh: 07-11-2024")
        return
    tgl = normalisasi_tanggal_gs(raw)
    if not tgl:
        ctx.bot.reply_to(
            message,
            "❌ Format tanggal tidak dikenali.\n"
            "Contoh: 20 mei | 30 nop | 12 des 2025 | 12/23/25 | kemarin | 3 hari lalu",
        )
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "TANGGAL": tgl}
    msg_loading = ctx.bot.reply_to(message, f"⏳ Mencari transaksi tanggal {tgl}...")
    tangani_read_data(chat_id, msg_loading.message_id)


def _quick_read_by_barang(message):
    chat_id = message.chat.id
    brg = _quick_clean_text(message.text)
    if not brg:
        ctx.bot.reply_to(message, "❌ Nama barang kosong. Coba ketik nama barang.")
        return
    if not ctx.IS_DB_CONNECTED:
        ctx.bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "BARANG": brg}
    msg_loading = ctx.bot.reply_to(message, "⏳ Mencari transaksi berdasarkan barang...")
    tangani_read_data(chat_id, msg_loading.message_id)


def handle_bulk_price_callback(call):
    chat_id = call.message.chat.id
    if chat_id not in ctx.user_sessions or "pending_price_update" not in ctx.user_sessions[chat_id]:
        ctx.bot.answer_callback_query(call.id, "Sesi kedaluwarsa.")
        return

    info = ctx.user_sessions[chat_id]["pending_price_update"]
    is_bulk = "yes" in call.data

    try:
        # 1. Update di Master Barang (Selalu dilakukan)
        update_barang(ctx.db_barang, info["row"], harga=info["harga"], satuan=info["satuan"])

        msg = f"✅ Harga <b>{info['barang']}</b> berhasil diubah menjadi <code>{format_rupiah(info['harga'])}</code> di Master Data."

        # 2. Jika bulk, update semua transaksi di ctx.db_transaksi yang barangnya sama dan belum lunas
        if is_bulk:
            safe_edit_message(
                ctx.bot,
                f"⏳ Sedang memperbarui semua transaksi {info['barang']}...",
                chat_id=chat_id,
                message_id=call.message.message_id,
            )
            filters = [{"kolom": "barang", "nilai": info["barang"], "operator": "ilike"}]
            semua_trx = db_client.get_transaksi_multi_filter(filters)
            count = 0
            for row in semua_trx:
                # Cek status bukan lunas
                if "lunas" not in row.get("status", "").lower():
                    row_idx = row["id"]
                    data_update = {"harga": info["harga"]}
                    # Hitung ulang total
                    try:
                        jml_match = re.search(r"\d+", str(row.get("jumlah_satuan", "")))
                        if jml_match:
                            jml = int(jml_match.group())
                            data_update["total"] = jml * info["harga"]
                    except:
                        pass
                    db_client.update_transaksi_db(row_idx, data_update)
                    count += 1
            msg += f"\n\n🔄 Berhasil memperbarui <b>{count} transaksi</b> lama yang belum lunas."

        safe_edit_message(
            ctx.bot, msg, chat_id=chat_id, message_id=call.message.message_id, parse_mode="HTML"
        )
        del ctx.user_sessions[chat_id]

    except Exception:
        pass


def handle_pengaturan_callbacks(call):
    chat_id = call.message.chat.id
    msg_idx = call.message.message_id
    cmd = call.data
    logger.info(
        f"[PENGATURAN DEBUG] handle_pengaturan_callbacks called: cmd='{cmd}', chat_id={chat_id}, msg_idx={msg_idx}"
    )

    # Handle master barang, metode, satuan callbacks FIRST (mb_batal, mb_do_update_price, etc.)
    if (
        cmd in ["mb_batal", "mb_do_update_price"]
        or cmd.startswith("mb_")
        or cmd.startswith("mm_")
        or cmd.startswith("ms_")
    ):
        logger.info(f"[PENGATURAN DEBUG] Calling handle_master_dan_pelunasan for cmd='{cmd}'")
        try:
            handle_master_dan_pelunasan(call)
        except Exception as e:
            logger.error(f"[PENGATURAN ERROR] Exception in handle_master_dan_pelunasan: {e}")
            logger.error(traceback.format_exc())
            try:
                safe_edit_message(
                    ctx.bot,
                    f"❌ Terjadi kesalahan: {str(e)[:100]}",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
            except Exception as e2:
                logger.error(f"[PENGATURAN ERROR] Could not send error message: {e2}")
        return

    # Callbacks yang bisa berjalan tanpa session
    no_session_needed = {"btn_buang"}

    if chat_id not in ctx.user_sessions:
        # Jika tombolnya adalah tombol 'Tutup' atau 'Buang', biarkan saja tanpa butuh sesi
        if cmd in no_session_needed:
            logger.info(f"[PENGATURAN DEBUG] Handling {cmd} without session")
            ctx.bot.answer_callback_query(call.id, "✅ Ditutup")
            try:
                ctx.bot.delete_message(chat_id, msg_idx)
            except Exception as e:
                logger.error(f"[PENGATURAN DEBUG] Error deleting message: {e}")
                safe_edit_message(
                    ctx.bot,
                    "❌ <b>Sesi Ditutup.</b>",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                    reply_markup=None,
                )
            # Clear the user session!
            try:
                if chat_id in ctx.user_sessions:
                    del ctx.user_sessions[chat_id]
            except:
                pass
            return

        # Untuk callback lainnya yang BUTUH session, show error
        logger.warning(f"[PENGATURAN DEBUG] Session not found for callback: {cmd}")
        ctx.bot.answer_callback_query(
            call.id, "❌ Sesi kedaluwarsa. Silakan ulangi perintah.", show_alert=True
        )
        return

    cmd = call.data
    sess = ctx.user_sessions[chat_id]
    logger.info(f"[PENGATURAN DEBUG] Session found. Keys in session: {list(sess.keys())}")
    # Handle btn_buang first!
    if cmd == "btn_buang":
        ctx.bot.answer_callback_query(call.id, "✅ Ditutup")
        try:
            ctx.bot.delete_message(chat_id, msg_idx)
        except Exception as e:
            logger.error(f"[PENGATURAN DEBUG] Error deleting message: {e}")
            safe_edit_message(
                ctx.bot,
                "❌ <b>Sesi Ditutup.</b>",
                chat_id,
                msg_idx,
                parse_mode="HTML",
                reply_markup=None,
            )
        # Clear the user session completely!
        try:
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
        except:
            pass
        return

    # Handle bulk price confirmation buttons
    if cmd.startswith("btn_bulk_price_"):
        handle_bulk_price_callback(call)
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
            markup.add(
                InlineKeyboardButton(f"🧩 Lengkapi [{i}] {brg}", callback_data=f"multi_pick_{i-1}")
            )
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
        field_wajib = [
            "TANGGAL",
            "NAMA",
            "BARANG",
            "JUMLAH",
            "TOTAL",
            "STATUS",
            "METODE_PEMBAYARAN",
        ]
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
            markup.add(
                InlineKeyboardButton(f"✏️ Edit [{i}] {brg}", callback_data=f"multi_pick_{i-1}")
            )
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
        markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
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
                markup.add(
                    InlineKeyboardButton(
                        f"🧩 Lengkapi [{i}] {brg}", callback_data=f"multi_pick_{i-1}"
                    )
                )
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
            safe_edit_message(
                ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup
            )
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
                markup.add(
                    InlineKeyboardButton(f"✏️ Edit [{i}] {brg}", callback_data=f"multi_pick_{i-1}")
                )
            markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_edit_back"))
            markup.add(InlineKeyboardButton("❌ Batalkan", callback_data="btn_buang"))
            safe_edit_message(
                ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup
            )
            return

        if chat_id not in ctx.user_sessions:
            return
        if "multi_results" not in sess or sess.get("multi_edit_index") is None:
            ctx.bot.answer_callback_query(call.id, "Sesi batch kedaluwarsa.")
            return
        if sess.get("multi_edit_mode") == "missing_only":
            idx = sess.get("multi_edit_index")
            try:
                idx = int(idx)
            except Exception:
                idx = None
            results = sess.get("multi_results") or []
            if idx is not None and 0 <= idx < len(results):
                miss = results[idx].get("missing_fields") or []
                if field_target not in set(miss):
                    try:
                        ctx.bot.answer_callback_query(
                            call.id,
                            "⚠️ Mode Lengkapi: hanya bisa isi field yang kosong.",
                            show_alert=True,
                        )
                    except Exception:
                        pass
                    return
        sess["state"] = "awaiting_edit_teks_multi"
        sess["field_target"] = field_target
        sess["summary_msg_id"] = msg_idx
        pesan_panduan = f"✏️ Silakan ketik nilai <b>{field_target}</b> yang benar lalu kirim:"
        msg = safe_edit_message(ctx.bot, pesan_panduan, chat_id, msg_idx, parse_mode="HTML")
        ctx.bot.register_next_step_handler(msg, tangani_revisi_manual_multi)
        return

        if chat_id not in ctx.user_sessions or "temp_matches" not in ctx.user_sessions[chat_id]:
            ctx.bot.answer_callback_query(call.id, "❌ Sesi kedaluwarsa. Silakan ulangi perintah.")
            return

        matches = ctx.user_sessions[chat_id]["temp_matches"]
        safe_answer_callback_query(ctx.bot, call)  # Menghilangkan icon loading di button

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
                # Jika entitas hilang, kita coba reconstruct dari text (jika ada)
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
            # Find row_idx
            row_idx = m["row_idx"]

            # Lengkapi data
            harga_baru = parse_rupiah(entitas.get("HARGA") or "0")
            satuan_baru = entitas.get("SATUAN")

            ctx.user_sessions[chat_id]["pending_price_update"] = {
                "row": row_idx,
                "barang": m["nama"],
                "harga": harga_baru,
                "satuan": satuan_baru,
            }

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("✅ Ya, Terapkan ke Semua", callback_data="btn_bulk_price_yes"),
                InlineKeyboardButton("❌ Tidak, Barang Ini Saja", callback_data="btn_bulk_price_no"),
                InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
            )
            safe_edit_message(
                ctx.bot,
                f"🔄 <b>UPDATE HARGA: {m['nama']}</b>\n\n"
                f"Ditemukan transaksi lain dengan barang yang sama.\n"
                f"Apakah Anda ingin menerapkan harga <code>{format_rupiah(harga_baru)}</code> ke <b>SEMUA</b> transaksi <code>{m['nama']}</code> yang belum lunas?",
                chat_id,
                msg_id,
                parse_mode="HTML",
                reply_markup=markup,
            )

        elif data.startswith("pick_edit_row_"):
            idx = int(data.replace("pick_edit_row_", ""))
            m = matches[idx]
            row_idx = m["row_idx"]
            ctx.user_sessions[chat_id]["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_id
            msg = safe_edit_message(
                ctx.bot,
                f"💰 Berapa harga baru untuk <b>{m['nama']}</b> ({m['satuan']})?\n(Harga saat ini: {format_rupiah(m['harga'])})",
                chat_id,
                msg_id,
                parse_mode="HTML",
            )
            ctx.bot.register_next_step_handler(msg, _mb_terima_harga_edit)

        elif data.startswith("pick_del_row_"):
            idx = int(data.replace("pick_del_row_", ""))
            m = matches[idx]
            row_idx = m["row_idx"]

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_hapus_{row_idx}"),
                InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
            )
            safe_edit_message(
                ctx.bot,
                f"🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Apakah Anda yakin ingin menghapus barang ini dari Master Data?\n\n"
                f"📦 <b>Nama:</b> {m['nama']}\n"
                f"💰 <b>Harga:</b> <code>{format_rupiah(m['harga'])}</code>\n"
                f"📐 <b>Satuan:</b> {m['satuan']}\n",
                chat_id,
                msg_id,
                parse_mode="HTML",
                reply_markup=markup,
            )


def _handle_master_dan_pelunasan_impl(call):
    chat_id = call.message.chat.id
    cmd = call.data
    msg_idx = call.message.message_id
    sess = ctx.user_sessions.get(chat_id, {})

    logger.info(f"[MB HANDLER] Starting: cmd='{cmd}', chat_id={chat_id}")

    # Handle old prep_ callbacks (backward compatibility)
    if cmd.startswith("prep_"):
        safe_answer_callback_query(ctx.bot, call)
        safe_edit_message(
            ctx.bot, "❌ Tombol sudah tidak berlaku. Silakan kirim perintah baru.", chat_id, msg_idx
        )
        return

    if cmd == "ms_menu":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        # HAPUS SEMUA SESSION USER TOTAL (menghilangkan state mb_input_nama yang sisa!)
        if chat_id in ctx.user_sessions:
            ctx.user_sessions.pop(chat_id, None)
        teks = (
            "📐 <b>MASTER SATUAN</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Kelola daftar satuan (pcs, bungkus, karton, dll)."
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
            InlineKeyboardButton("➕ Tambah Baru", callback_data="ms_tambah"),
            InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
            InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
        )
        markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)
        return

    # ─────────────── MASTER BARANG ───────────────
    if cmd == "mb_list":
        semua = get_all_barang(ctx.db_barang)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Belum ada data barang.", chat_id, msg_idx)
            return
        teks, markup = render_daftar_master_barang(semua)
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    elif cmd == "mb_hapus_all":
        semua = get_all_barang(ctx.db_barang)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Belum ada data barang.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🧹 Ya, Hapus Semua", callback_data="mb_do_hapus_all"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(
            ctx.bot,
            "🧹 <b>KONFIRMASI HAPUS SEMUA</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Anda akan menghapus <b>{len(semua)}</b> item dari Master Barang.\n\n"
            "<b>PERINGATAN:</b> tindakan ini tidak bisa dibatalkan.",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup,
        )

    elif cmd == "mb_do_hapus_all":
        try:
            semua = get_all_barang(ctx.db_barang)
            hapus_semua_barang(ctx.db_barang)
            safe_edit_message(
                ctx.bot,
                "✅ <b>MASTER BARANG TERHAPUS</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Total dihapus: <b>{len(semua)}</b>",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
        except Exception:
            pass

    elif cmd == "mb_tambah":
        msg_idx = call.message.message_id
        ctx.user_sessions.ensure(chat_id).update({"state": "mb_input_nama", "mb_msg_id": msg_idx})
        msg = safe_edit_message(
            ctx.bot,
            "➕ <b>Tambah Barang Baru</b>\n\nKetik <b>nama barang</b> baru:",
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        ctx.bot.register_next_step_handler(msg, _mb_terima_nama)

    elif cmd == "mb_edit":
        semua = get_all_barang(ctx.db_barang)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada barang untuk diedit.", chat_id, msg_idx)
            return
        if hasattr(ctx.user_sessions, "ensure"):
            sess = ctx.user_sessions.ensure(chat_id)
        else:
            sess = ctx.user_sessions.setdefault(chat_id, {})
        sess["mb_edit_msg_id"] = msg_idx
        sess["mb_msg_id"] = msg_idx
        _render_mb_edit_picker(chat_id, msg_idx, semua, query=None, page=1)

    elif cmd.startswith("mb_edit_page_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            page = int(cmd.replace("mb_edit_page_", ""))
        except Exception:
            page = 1
        try:
            semua = get_all_barang(ctx.db_barang)
            q = ""
            try:
                if hasattr(ctx.user_sessions, "ensure"):
                    sess = ctx.user_sessions.ensure(chat_id)
                else:
                    sess = ctx.user_sessions.setdefault(chat_id, {})
                q = sess.get("mb_edit_query") or ""
            except Exception:
                q = ""
            _render_mb_edit_picker(chat_id, msg_idx, semua, query=q, page=page)
        except Exception as e:
            logger.error(f"Error loading mb_edit_page {page}: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memuat halaman", show_alert=True)

    elif cmd == "mb_edit_search":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        if hasattr(ctx.user_sessions, "ensure"):
            sess = ctx.user_sessions.ensure(chat_id)
        else:
            sess = ctx.user_sessions.setdefault(chat_id, {})
        msg = safe_edit_message(
            ctx.bot,
            "🔎 <b>CARI BARANG (EDIT)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Ketik kata kunci nama barang.\n\n"
            "Contoh: <code>willo</code> / <code>pia</code>\n"
            "<i>Ketik 'batal' untuk kembali.</i>",
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        if msg:
            sess["mb_edit_msg_id"] = msg.message_id
        ctx.bot.register_next_step_handler_by_chat_id(chat_id, _mb_edit_search_input)

    elif cmd.startswith("mb_edit_") and not any(
        sub in cmd for sub in ["nama_", "harga_", "satuan_", "semua_", "unit_", "page_", "search"]
    ):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_edit_", ""))
        except ValueError:
            safe_edit_message(ctx.bot, "❌ Data tidak valid.", chat_id, msg_idx)
            return
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if not target:
            ctx.bot.answer_callback_query(
                call.id, "❌ Data barang tidak ditemukan.", show_alert=True
            )
            safe_edit_message(ctx.bot, "❌ Data barang tidak ditemukan.", chat_id, msg_idx)
            return

        ctx.user_sessions.setdefault(chat_id, {})["mb_edit_row"] = row_idx
        ctx.user_sessions[chat_id]["mb_msg_id"] = msg_idx

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("✏️ Edit Nama", callback_data=f"mb_edit_nama_{row_idx}"),
            InlineKeyboardButton("💰 Edit Harga", callback_data=f"mb_edit_harga_{row_idx}"),
        )
        markup.add(
            InlineKeyboardButton("📐 Edit Satuan", callback_data=f"mb_edit_satuan_{row_idx}"),
            InlineKeyboardButton("🔄 Edit Semua", callback_data=f"mb_edit_semua_{row_idx}"),
        )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))

        teks = (
            f"✏️ <b>EDIT MASTER BARANG</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Nama:</b> {target['nama']}\n"
            f"💰 <b>Harga:</b> <code>{format_rupiah(target['harga'])}</code>\n"
            f"📐 <b>Satuan:</b> {target['satuan']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Silakan pilih bagian yang ingin diedit:</i>"
        )
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    elif cmd.startswith("mb_edit_nama_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_edit_nama_", ""))
            ctx.user_sessions.setdefault(chat_id, {})["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_idx
            try:
                ctx.bot.clear_step_handler_by_chat_id(chat_id)
            except Exception as e:
                logger.debug(f"Clear step handler error: {e}")
            msg = safe_edit_message(
                ctx.bot,
                "✏️ Ketik <b>nama baru</b> untuk barang ini:",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            ctx.bot.register_next_step_handler(msg, _mb_terima_nama_edit_single)
        except Exception as e:
            logger.error(f"Error in mb_edit_nama: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal membuka editor", show_alert=True)

    elif cmd.startswith("mb_edit_harga_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_edit_harga_", ""))
            ctx.user_sessions.setdefault(chat_id, {})["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_idx
            try:
                ctx.bot.clear_step_handler_by_chat_id(chat_id)
            except Exception as e:
                logger.debug(f"Clear step handler error: {e}")
            msg = safe_edit_message(
                ctx.bot,
                "💰 Ketik <b>harga baru</b> (angka saja, mis: <code>15000</code>):",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            ctx.bot.register_next_step_handler(msg, _mb_terima_harga_edit_single)
        except Exception as e:
            logger.error(f"Error in mb_edit_harga: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal membuka editor", show_alert=True)

    elif cmd.startswith("mb_edit_satuan_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_edit_satuan_", ""))
            ctx.user_sessions.setdefault(chat_id, {})["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_idx
            try:
                ctx.bot.clear_step_handler_by_chat_id(chat_id)
            except Exception as e:
                logger.debug(f"Clear step handler error: {e}")
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("pcs", callback_data=f"mb_edit_unit_pcs_{row_idx}"),
                InlineKeyboardButton("dus", callback_data=f"mb_edit_unit_dus_{row_idx}"),
                InlineKeyboardButton("pak", callback_data=f"mb_edit_unit_pak_{row_idx}"),
                InlineKeyboardButton("karton", callback_data=f"mb_edit_unit_karton_{row_idx}"),
            )
            markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
            safe_edit_message(
                ctx.bot,
                "📐 Pilih atau ketik <b>satuan baru</b> untuk barang ini:",
                chat_id,
                msg_idx,
                parse_mode="HTML",
                reply_markup=markup,
            )
            ctx.bot.register_next_step_handler_by_chat_id(chat_id, _mb_terima_satuan_edit_single)
        except Exception as e:
            logger.error(f"Error in mb_edit_satuan: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal membuka satuan", show_alert=True)

    elif cmd.startswith("mb_edit_unit_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            parts = cmd.replace("mb_edit_unit_", "").split("_")
            unit = parts[0]
            row_idx = int(parts[1])
            try:
                ctx.bot.clear_step_handler_by_chat_id(chat_id)
            except Exception as e:
                logger.debug(f"Clear step handler error: {e}")
            try:
                semua = get_all_barang(ctx.db_barang)
                target = next((b for b in semua if b["row_idx"] == row_idx), None)
                if target:
                    update_barang(ctx.db_barang, row_idx, satuan=unit)
                    safe_edit_message(
                        ctx.bot,
                        f"✅ <b>Satuan barang berhasil diperbarui!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📦 <b>Barang:</b> {target['nama']}\n"
                        f"📐 <b>Satuan Lama:</b> {target['satuan']}\n"
                        f"✨ <b>Satuan Baru:</b> <b>{unit}</b>",
                        chat_id,
                        msg_idx,
                        parse_mode="HTML",
                    )
                ctx.user_sessions.pop(chat_id, None)
            except Exception as e:
                logger.error(f"Error updating barang satuan: {e}")
                ctx.bot.answer_callback_query(
                    call.id, "❌ Gagal memperbarui satuan", show_alert=True
                )
        except Exception as e:
            logger.error(f"Error in mb_edit_unit: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memproses", show_alert=True)

    elif cmd.startswith("mb_edit_semua_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_edit_semua_", ""))
            ctx.user_sessions.setdefault(chat_id, {})["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = msg_idx
            try:
                ctx.bot.clear_step_handler_by_chat_id(chat_id)
            except Exception as e:
                logger.debug(f"Clear step handler error: {e}")
            msg = safe_edit_message(
                ctx.bot,
                "🔄 <b>EDIT SEMUA FIELD</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                "✏️ Langkah 1: Ketik <b>nama baru</b> untuk barang ini:",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            ctx.bot.register_next_step_handler(msg, _mb_terima_nama_edit_wizard)
        except Exception as e:
            logger.error(f"Error in mb_edit_semua: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal membuka editor", show_alert=True)

    elif cmd.startswith("mb_wizard_unit_"):
        unit = cmd.replace("mb_wizard_unit_", "")
        sess["mb_pending_satuan"] = unit
        from handlers.crud_barang import _mb_terima_satuan_edit_wizard

        _mb_terima_satuan_edit_wizard(None, chat_id=chat_id, message_id_target=msg_idx)

    elif cmd == "mb_hapus":
        semua = get_all_barang(ctx.db_barang)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada barang untuk dihapus.", chat_id, msg_idx)
            return
        if hasattr(ctx.user_sessions, "ensure"):
            sess = ctx.user_sessions.ensure(chat_id)
        else:
            sess = ctx.user_sessions.setdefault(chat_id, {})
        sess["mb_hapus_msg_id"] = msg_idx
        sess["mb_msg_id"] = msg_idx
        _render_mb_hapus_picker(chat_id, msg_idx, semua, query=None, page=1)

    elif cmd.startswith("mb_hapus_page_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            page = int(cmd.replace("mb_hapus_page_", ""))
        except Exception:
            page = 1
        try:
            semua = get_all_barang(ctx.db_barang)
            q = ""
            try:
                if hasattr(ctx.user_sessions, "ensure"):
                    sess = ctx.user_sessions.ensure(chat_id)
                else:
                    sess = ctx.user_sessions.setdefault(chat_id, {})
                q = sess.get("mb_hapus_query") or ""
            except Exception:
                q = ""
            _render_mb_hapus_picker(chat_id, msg_idx, semua, query=q, page=page)
        except Exception as e:
            logger.error(f"Error loading mb_hapus_page {page}: {e}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal memuat halaman", show_alert=True)

    elif cmd == "mb_hapus_search":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        if hasattr(ctx.user_sessions, "ensure"):
            sess = ctx.user_sessions.ensure(chat_id)
        else:
            sess = ctx.user_sessions.setdefault(chat_id, {})
        msg = safe_edit_message(
            ctx.bot,
            "🔎 <b>CARI BARANG (HAPUS)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Ketik kata kunci nama barang.\n\n"
            "Contoh: <code>willo</code> / <code>pia</code>\n"
            "<i>Ketik 'batal' untuk kembali.</i>",
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        if msg:
            sess["mb_hapus_msg_id"] = msg.message_id
            sess["mb_msg_id"] = msg.message_id
        ctx.bot.register_next_step_handler(msg, _mb_hapus_search_input)

    elif cmd == "mb_hapus_all":
        safe_answer_callback_query(ctx.bot, call)
        if hasattr(ctx.user_sessions, "ensure"):
            sess = ctx.user_sessions.ensure(chat_id)
        else:
            sess = ctx.user_sessions.setdefault(chat_id, {})
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🧹 Ya, Hapus Semua", callback_data="mb_do_hapus_all"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(
            ctx.bot,
            "🧹 <b>KONFIRMASI HAPUS SEMUA BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ PERINGATAN: Ini akan menghapus SEMUA barang di Master Data!\n"
            "Apakah Anda yakin ingin melanjutkan?",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup,
        )

    elif cmd == "mb_do_hapus_all":
        safe_answer_callback_query(ctx.bot, call)
        try:
            semua = get_all_barang(ctx.db_barang)
            for barang in semua:
                if "row_idx" in barang:
                    hapus_barang(ctx.db_barang, barang["row_idx"])
            safe_edit_message(
                ctx.bot,
                "✅ <b>SEMUANYA BARANG BERHASIL DIHAPUS</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Semua barang di Master Data telah dihapus.",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
        except Exception as e:
            logger.error(f"Error deleting all barang: {e}")
            safe_answer_callback_query(
                ctx.bot, call, "❌ Gagal menghapus semua barang", show_alert=True
            )

    elif cmd.startswith("mb_hapus_prep_"):
        safe_answer_callback_query(ctx.bot, call)
        try:
            row_idx = int(cmd.replace("mb_hapus_prep_", "").strip())
        except ValueError as e:
            logger.error(f"[DEBUG] Failed to parse mb_hapus_prep row_idx: {e}")
            safe_edit_message(
                ctx.bot, "❌ Data tidak valid. Silakan ulangi perintah.", chat_id, msg_idx
            )
            return
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if not target:
            safe_answer_callback_query(ctx.bot, call, "❌ Barang tidak ditemukan.", show_alert=True)
            safe_edit_message(ctx.bot, "❌ Barang tidak ditemukan.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_do_hapus_{row_idx}"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(
            ctx.bot,
            "🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Apakah Anda yakin ingin menghapus barang ini?\n\n"
            f"📦 <b>Nama:</b> {target['nama']}\n"
            f"💰 <b>Harga:</b> <code>{format_rupiah(target['harga'])}</code>\n"
            f"📐 <b>Satuan:</b> {target['satuan']}\n",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup,
        )

    elif cmd.startswith("mb_hapus_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            cmd_part = cmd.replace("mb_hapus_", "").strip()
            logger.info(f"[DEBUG] Processing mb_hapus_ command: cmd={cmd}, cmd_part={cmd_part}")
            row_idx = int(cmd_part)
        except ValueError as e:
            logger.error(f"[DEBUG] Failed to parse row_idx: {e}")
            safe_edit_message(
                ctx.bot, "❌ Data tidak valid. Silakan ulangi perintah.", chat_id, msg_idx
            )
            return
        semua = get_all_barang(ctx.db_barang)
        target = next((b for b in semua if b["row_idx"] == row_idx), None)
        if not target:
            safe_answer_callback_query(ctx.bot, call, "❌ Barang tidak ditemukan.", show_alert=True)
            safe_edit_message(ctx.bot, "❌ Barang tidak ditemukan.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_do_hapus_{row_idx}"),
            InlineKeyboardButton("❌ Batal", callback_data="mb_batal"),
        )
        safe_edit_message(
            ctx.bot,
            "🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Apakah Anda yakin ingin menghapus barang ini?\n\n"
            f"📦 <b>Nama:</b> {target['nama']}\n"
            f"💰 <b>Harga:</b> <code>{format_rupiah(target['harga'])}</code>\n"
            f"📐 <b>Satuan:</b> {target['satuan']}\n",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup,
        )

    elif cmd.startswith("mb_do_hapus_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("mb_do_hapus_", ""))
            hapus_barang(ctx.db_barang, row_idx)
            safe_edit_message(
                ctx.bot, "✅ Barang berhasil dihapus dari Master Barang.", chat_id, msg_idx
            )
        except Exception as e:
            logger.error(f"Error deleting barang {row_idx}: {e}")
            safe_answer_callback_query(ctx.bot, call, "❌ Gagal menghapus barang", show_alert=True)

    elif cmd == "mb_batal":
        logger.info(f"[PENGATURAN DEBUG] Handling mb_batal")
        if chat_id in ctx.user_sessions:
            ctx.user_sessions[chat_id]["state"] = "cancelled"
            ctx.user_sessions.pop(chat_id, None)
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception as e:
            logger.error(f"[PENGATURAN DEBUG] Error clearing step handler: {e}")
        logger.info(f"[PENGATURAN DEBUG] Calling safe_edit_message with '❌ Aksi dibatalkan.'")
        safe_edit_message(ctx.bot, "❌ Aksi dibatalkan.", chat_id, msg_idx)

    elif cmd == "mb_konfirm_simpan":
        try:
            id_baru = tambah_barang(
                ctx.db_barang,
                sess.get("mb_nama_baru"),
                sess.get("mb_harga_baru"),
                sess.get("mb_satuan_baru", "pcs"),
            )
            safe_edit_message(
                ctx.bot,
                f"✅ <b>Barang berhasil ditambahkan!</b>\nID: <code>{id_baru}</code> | Nama: <b>{sess.get('mb_nama_baru')}</b>",
                chat_id,
                msg_idx,
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Error adding barang: {e}")
            safe_answer_callback_query(
                ctx.bot, call, "❌ Gagal menambahkan barang.", show_alert=True
            )
            safe_edit_message(ctx.bot, "❌ Gagal menambahkan barang.", chat_id, msg_idx)
        ctx.user_sessions.pop(chat_id, None)

    elif cmd.startswith("mb_unit_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        unit = cmd.replace("mb_unit_", "")
        sess["mb_satuan_baru"] = unit
        _mb_terima_satuan(None, chat_id=chat_id, message_id_target=msg_idx)

    elif cmd == "mb_do_update_price":
        logger.info(f"[PENGATURAN DEBUG] Handling mb_do_update_price for chat_id={chat_id}")
        logger.info(f"[PENGATURAN DEBUG] Session state: {sess}")
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        row_idx = sess.get("mb_edit_row")
        harga_baru = sess.get("mb_pending_harga")
        logger.info(f"[PENGATURAN DEBUG] mb_edit_row={row_idx}, mb_pending_harga={harga_baru}")
        if row_idx and harga_baru:
            try:
                update_barang(ctx.db_barang, row_idx, harga=harga_baru)
                logger.info(f"[PENGATURAN DEBUG] Barang updated successfully")
                safe_edit_message(
                    ctx.bot,
                    f"✅ Harga berhasil diperbarui menjadi <b>{format_rupiah(harga_baru)}</b>.",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.error(f"Error updating barang price: {e}", exc_info=True)
                ctx.bot.answer_callback_query(
                    call.id, "❌ Gagal memperbarui harga barang.", show_alert=True
                )
                safe_edit_message(ctx.bot, "❌ Gagal memperbarui harga barang.", chat_id, msg_idx)
        else:
            logger.warning(
                f"[PENGATURAN DEBUG] Missing data for price update: row_idx={row_idx}, harga_baru={harga_baru}"
            )
            ctx.bot.answer_callback_query(
                call.id, "❌ Data tidak lengkap. Ulangi perintah.", show_alert=True
            )
            safe_edit_message(ctx.bot, "❌ Terjadi kesalahan data sesi.", chat_id, msg_idx)
        ctx.user_sessions.pop(chat_id, None)

    elif cmd.startswith("mb_apply_price_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        sub = cmd.replace("mb_apply_price_", "")
        harga_baru = sess.get("mb_pending_harga")
        matches = sess.get("temp_matches", [])

        if not harga_baru or not matches:
            safe_edit_message(ctx.bot, "❌ Sesi kedaluwarsa.", chat_id, msg_idx)
            return

        try:
            if sub == "all":
                # Update Semua
                for m in matches:
                    semua = get_all_barang(ctx.db_barang)
                    row_idx = next(
                        (
                            b["row_idx"]
                            for b in semua
                            if b["nama"] == m["nama"] and b["satuan"] == m["satuan"]
                        ),
                        None,
                    )
                    if row_idx:
                        update_barang(ctx.db_barang, row_idx, harga=harga_baru)
                safe_edit_message(
                    ctx.bot,
                    f"✅ Harga <b>{len(matches)}</b> barang berhasil diperbarui menjadi <b>{format_rupiah(harga_baru)}</b>.",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
            else:
                # Update Salah Satu
                idx = int(sub)
                m = matches[idx]
                semua = get_all_barang(ctx.db_barang)
                row_idx = next(
                    (
                        b["row_idx"]
                        for b in semua
                        if b["nama"] == m["nama"] and b["satuan"] == m["satuan"]
                    ),
                    None,
                )
                if row_idx:
                    update_barang(ctx.db_barang, row_idx, harga=harga_baru)
                safe_edit_message(
                    ctx.bot,
                    f"✅ Harga <b>{m['nama']}</b> berhasil diperbarui menjadi <b>{format_rupiah(harga_baru)}</b>.",
                    chat_id,
                    msg_idx,
                    parse_mode="HTML",
                )
        except Exception as e:
            logger.error(f"Error applying price update: {e}")
            ctx.bot.answer_callback_query(
                call.id, "❌ Gagal memperbarui harga barang.", show_alert=True
            )
            safe_edit_message(ctx.bot, "❌ Gagal memperbarui harga barang.", chat_id, msg_idx)
        ctx.user_sessions.pop(chat_id, None)

    # ─────────────── MASTER METODE ───────────────
    elif cmd == "mm_list":
        semua = get_all_metode(ctx.db_metode)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Belum ada data metode.", chat_id, msg_idx)
            return
        teks = "📋 <b>DAFTAR MASTER METODE</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for m in semua:
            teks += f"• <b>{m['nama']}</b> — <code>{m['keyword'] or '-'}</code>\n"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("➕ Tambah Baru", callback_data="mm_tambah"),
            InlineKeyboardButton("✏️ Edit Keyword", callback_data="mm_edit"),
        )
        markup.add(InlineKeyboardButton("🗑️ Hapus Metode", callback_data="mm_hapus"))
        markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    elif cmd == "mm_tambah":
        ctx.user_sessions.ensure(chat_id).update({"state": "mm_input_nama"})
        msg = safe_edit_message(
            ctx.bot,
            "➕ <b>Tambah Metode Baru</b>\n\nKetik <b>nama metode</b> (mis: <code>Transfer BNI</code>):",
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        ctx.bot.register_next_step_handler(msg, _mm_terima_nama)

    elif cmd == "mm_edit":
        semua = get_all_metode(ctx.db_metode)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada metode.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        for m in semua:
            markup.add(
                InlineKeyboardButton(f"✏️ {m['nama']}", callback_data=f"mm_edit_{m['row_idx']}")
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mm_batal"))
        safe_edit_message(
            ctx.bot,
            "Pilih metode yang ingin diedit keyword-nya:",
            chat_id,
            msg_idx,
            reply_markup=markup,
        )

    elif cmd.startswith("mm_edit_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        row_idx = int(cmd.replace("mm_edit_", ""))
        ctx.user_sessions.setdefault(chat_id, {})["mm_edit_row"] = row_idx
        msg = safe_edit_message(
            ctx.bot,
            "🔑 Ketik <b>keyword baru</b> (pisah koma, mis: <code>bni, tf bni, via bni</code>):",
            chat_id,
            msg_idx,
            parse_mode="HTML",
        )
        ctx.bot.register_next_step_handler(msg, _mm_terima_keyword_edit)

    elif cmd == "mm_hapus":
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        semua = get_all_metode(ctx.db_metode)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada metode.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        for m in semua:
            markup.add(
                InlineKeyboardButton(f"🗑️ {m['nama']}", callback_data=f"mm_hapus_{m['row_idx']}")
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="mm_batal"))
        safe_edit_message(
            ctx.bot, "Pilih metode yang ingin dihapus:", chat_id, msg_idx, reply_markup=markup
        )

    elif cmd.startswith("mm_hapus_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        row_idx = int(cmd.replace("mm_hapus_", ""))
        try:
            hapus_metode(ctx.db_metode, row_idx)
            safe_edit_message(ctx.bot, "✅ Metode berhasil dihapus.", chat_id, msg_idx)
        except Exception:
            logger.error(f"Error deleting metode {row_idx}")
            ctx.bot.answer_callback_query(call.id, "❌ Gagal menghapus metode.", show_alert=True)

    elif cmd == "mm_batal":
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        semua = get_all_metode(ctx.db_metode)
        if not semua:
            safe_edit_message(ctx.bot, "📭 Belum ada data metode.", chat_id, msg_idx)
            return
        teks = "📋 <b>DAFTAR MASTER METODE</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for m in semua:
            teks += f"• <b>{m['nama']}</b> — <code>{m['keyword'] or '-'}</code>\n"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("➕ Tambah Baru", callback_data="mm_tambah"),
            InlineKeyboardButton("✏️ Edit Keyword", callback_data="mm_edit"),
        )
        markup.add(InlineKeyboardButton("🗑️ Hapus Metode", callback_data="mm_hapus"))
        markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    # ─────────────── MASTER SATUAN ───────────────
    elif cmd == "ms_list":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        semua = get_all_satuan()
        teks = "📋 <b>DAFTAR MASTER SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for s in semua:
            teks += f"• <b>{s['nama_satuan']}</b>\n"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
            InlineKeyboardButton("➕ Tambah Baru", callback_data="ms_tambah"),
            InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
            InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
        )
        markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    elif cmd == "ms_tambah":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        # Clear session except we need to keep track of msg_idx
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]
        sess = ctx.user_sessions.ensure(chat_id)
        sess["ms_msg_idx"] = msg_idx
        sess["state"] = "ms_input_nama"  # Set state explicitly
        # Kirim pesan BARU untuk minta input (bukan edit pesan lama)
        msg = ctx.bot.send_message(
            chat_id,
            "➕ <b>Tambah Satuan Baru</b>\n\nKetik <b>nama satuan</b> (misal: <code>bungkus</code> atau <code>karton</code>):",
            parse_mode="HTML",
        )
        sess["ms_input_msg_id"] = msg.message_id  # Simpan ID pesan input ini untuk dihapus nanti
        ctx.bot.register_next_step_handler(msg, _ms_terima_nama)

    elif cmd == "ms_edit":
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        semua = get_all_satuan()
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada satuan untuk diedit.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        for s in semua:
            markup.add(
                InlineKeyboardButton(f"✏️ {s['nama_satuan']}", callback_data=f"ms_edit_{s['id']}")
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="ms_batal"))
        safe_edit_message(
            ctx.bot, "Pilih satuan yang ingin diedit:", chat_id, msg_idx, reply_markup=markup
        )

    elif cmd.startswith("ms_edit_"):
        try:
            ctx.bot.clear_step_handler_by_chat_id(chat_id)
        except Exception:
            pass
        safe_answer_callback_query(ctx.bot, call)
        id_satuan = int(cmd.replace("ms_edit_", ""))
        semua = get_all_satuan()
        target = next((s for s in semua if s["id"] == id_satuan), None)
        if not target:
            safe_edit_message(ctx.bot, "❌ Satuan tidak ditemukan.", chat_id, msg_idx)
            return
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]
        sess = ctx.user_sessions.ensure(chat_id)
        sess["ms_msg_idx"] = msg_idx
        sess["ms_edit_id"] = id_satuan
        sess["state"] = "ms_edit_nama"  # Set state explicitly
        # Kirim pesan BARU untuk edit
        msg = ctx.bot.send_message(
            chat_id,
            f"✏️ Edit Satuan\n━━━━━━━━━━━━━━━━━━━━━━\nSatuan saat ini: <b>{target['nama_satuan']}</b>\n\nKetik nama satuan baru:",
            parse_mode="HTML",
        )
        sess["ms_input_msg_id"] = msg.message_id  # Simpan ID pesan input ini untuk dihapus nanti
        ctx.bot.register_next_step_handler(msg, _ms_terima_nama_edit)

    elif cmd == "ms_confirm_add":
        safe_answer_callback_query(ctx.bot, call)
        sess = ctx.user_sessions.ensure(chat_id)
        nama = sess.get("ms_pending_nama")
        if not nama:
            safe_edit_message(ctx.bot, "❌ Sesi kedaluwarsa.", chat_id, msg_idx)
            return

        try:
            # Simpan satuan
            id_baru = tambah_satuan(nama)

            # Tampilkan daftar master satuan
            semua = get_all_satuan()
            teks = "📋 <b>DAFTAR MASTER SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for s in semua:
                teks += f"• <b>{s['nama_satuan']}</b>\n"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
                InlineKeyboardButton("➕ Tambah Lagi", callback_data="ms_tambah"),
                InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
                InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
            )
            markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))

            safe_edit_message(
                ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup
            )
            ctx.user_sessions.pop(chat_id, None)
        except Exception as e:
            safe_edit_message(ctx.bot, f"❌ Gagal simpan: {e}", chat_id, msg_idx)

    elif cmd == "ms_confirm_edit":
        safe_answer_callback_query(ctx.bot, call)
        sess = ctx.user_sessions.ensure(chat_id)
        id_satuan = sess.get("ms_edit_id")
        nama_baru = sess.get("ms_pending_nama_edit")
        if not id_satuan or not nama_baru:
            safe_edit_message(ctx.bot, "❌ Sesi kedaluwarsa.", chat_id, msg_idx)
            return

        try:
            # Update satuan
            update_satuan(id_satuan, nama_satuan=nama_baru)

            # Tampilkan daftar master satuan
            semua = get_all_satuan()
            teks = "📋 <b>DAFTAR MASTER SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for s in semua:
                teks += f"• <b>{s['nama_satuan']}</b>\n"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
                InlineKeyboardButton("➕ Tambah Lagi", callback_data="ms_tambah"),
                InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
                InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
            )
            markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))

            safe_edit_message(
                ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup
            )
            ctx.user_sessions.pop(chat_id, None)
        except Exception as e:
            safe_edit_message(ctx.bot, f"❌ Gagal update: {e}", chat_id, msg_idx)

    elif cmd == "ms_hapus":
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        semua = get_all_satuan()
        if not semua:
            safe_edit_message(ctx.bot, "📭 Tidak ada satuan untuk dihapus.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        for s in semua:
            markup.add(
                InlineKeyboardButton(f"🗑️ {s['nama_satuan']}", callback_data=f"ms_hapus_{s['id']}")
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="ms_batal"))
        safe_edit_message(
            ctx.bot, "Pilih satuan yang ingin dihapus:", chat_id, msg_idx, reply_markup=markup
        )

    elif cmd.startswith("ms_hapus_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        id_satuan = int(cmd.replace("ms_hapus_", ""))
        semua = get_all_satuan()
        target = next((s for s in semua if s["id"] == id_satuan), None)
        if not target:
            safe_edit_message(ctx.bot, "❌ Satuan tidak ditemukan.", chat_id, msg_idx)
            return
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"ms_do_hapus_{id_satuan}"),
            InlineKeyboardButton("❌ Batal", callback_data="ms_batal"),
        )
        safe_edit_message(
            ctx.bot,
            f"🗑️ <b>KONFIRMASI HAPUS SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\nApakah Anda yakin ingin menghapus satuan <b>{target['nama_satuan']}</b>?",
            chat_id,
            msg_idx,
            parse_mode="HTML",
            reply_markup=markup,
        )

    elif cmd.startswith("ms_do_hapus_"):
        safe_answer_callback_query(ctx.bot, call)
        id_satuan = int(cmd.replace("ms_do_hapus_", ""))
        try:
            hapus_satuan(id_satuan)
            semua = get_all_satuan()
            teks = "📋 <b>DAFTAR MASTER SATUAN</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for s in semua:
                teks += f"• <b>{s['nama_satuan']}</b>\n"
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
                InlineKeyboardButton("➕ Tambah Baru", callback_data="ms_tambah"),
                InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
                InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
            )
            markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
            safe_edit_message(
                ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup
            )
        except Exception as e:
            logger.error(f"Error deleting satuan {id_satuan}: {e}")
            safe_edit_message(ctx.bot, f"❌ Gagal menghapus satuan: {e}", chat_id, msg_idx)

    elif cmd == "ms_batal":
        safe_answer_callback_query(ctx.bot, call)
        teks = "📐 <b>MASTER SATUAN</b>\n"
        teks += "━━━━━━━━━━━━━━━━━━━━━━\n"
        teks += "Kelola daftar satuan (pcs, bungkus, karton, dll)."
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📋 Lihat Daftar", callback_data="ms_list"),
            InlineKeyboardButton("➕ Tambah Baru", callback_data="ms_tambah"),
            InlineKeyboardButton("✏️ Edit Satuan", callback_data="ms_edit"),
            InlineKeyboardButton("🗑️ Hapus Satuan", callback_data="ms_hapus"),
        )
        markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
        safe_edit_message(ctx.bot, teks, chat_id, msg_idx, parse_mode="HTML", reply_markup=markup)

    # ─────────────── PELUNASAN ───────────────
    elif cmd.startswith("pel_pilih_"):
        safe_answer_callback_query(ctx.bot, call)  # Dismiss loading
        try:
            row_idx = int(cmd.replace("pel_pilih_", ""))
        except ValueError:
            safe_edit_message(ctx.bot, "❌ Data tidak valid.", chat_id, msg_idx)
            return
        hutang_list = ctx.user_sessions.get(chat_id, {}).get("hutang_list", [])
        info = next((h for h in hutang_list if h["row_index"] == row_idx), None)
        if info:
            nominal = ctx.user_sessions[chat_id].get("nominal_bayar")
            _tampilkan_konfirmasi_pelunasan(chat_id, msg_idx, info, nominal)
        else:
            safe_edit_message(ctx.bot, "❌ Data tidak ditemukan.", chat_id, msg_idx)

    elif cmd == "pel_konfirm_ya":
        row_idx = sess.get("pel_row_idx")
        nominal = sess.get("pel_nominal", 0)
        nama = sess.get("pel_nama", "-")

        if not row_idx:
            safe_edit_message(ctx.bot, "❌ Data sesi tidak valid.", chat_id, msg_idx)
            return

        safe_edit_message(ctx.bot, "⏳ Mencatat pembayaran...", chat_id, msg_idx)
        hasil = proses_bayar_tambahan(
            ctx.db_transaksi,
            ctx.db_histori,
            row_idx,
            nominal,
            nama,
            catatan=f"Pembayaran {format_rupiah(nominal)}",
        )

        if hasil["sukses"]:
            tagihan_baru = hasil["tagihan_baru"]
            info_tagihan = (
                f"\n⚠️ <b>Jumlah Tagihan:</b> {format_rupiah(tagihan_baru)}"
                if tagihan_baru > 0
                else "\n✅ <b>Tagihan LUNAS!</b>"
            )
            sukses = (
                f"✅ <b>PEMBAYARAN TERCATAT!</b>\n"
                f"👤 Nama: <b>{nama}</b>\n"
                f"💸 Dibayar: <code>{format_rupiah(nominal)}</code>"
                f"{info_tagihan}"
            )
            safe_edit_message(ctx.bot, sukses, chat_id, msg_idx, parse_mode="HTML")
        else:
            safe_edit_message(ctx.bot, f"❌ Gagal mencatat: {hasil.get('error')}", chat_id, msg_idx)

        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]


# Wrapper function with error handling
def handle_master_dan_pelunasan(call):
    """Wrapper around _handle_master_dan_pelunasan_impl with error handling"""
    try:
        _handle_master_dan_pelunasan_impl(call)
    except Exception as e:
        logger.error(f"[MB HANDLER ERROR] Exception in handle_master_dan_pelunasan: {e}")
        logger.error(f"[MB HANDLER ERROR] Traceback:\n{traceback.format_exc()}")

        try:
            chat_id = call.message.chat.id
            msg_idx = call.message.message_id
            error_msg = str(e)[:100] if str(e) else "Unknown error"
            safe_edit_message(
                ctx.bot, f"❌ Terjadi kesalahan: {error_msg}", chat_id, msg_idx, parse_mode="HTML"
            )
        except Exception as e2:
            logger.error(f"[MB HANDLER ERROR] Could not send error message: {e2}")
