"""
Callback Handler - Product (Barang) Management
"""
import logging
from telebot.types import CallbackQuery

from core.bot_context import ctx
from utils.security import safe_edit_message
from handlers.crud_barang import (
    tangani_tambah_barang_chat,
    tangani_cek_harga_chat,
    tangani_hapus_barang_chat,
    tangani_set_harga_chat,
)
from services.ui_pengaturan import render_daftar_master_barang
from core.master_data import get_all_barang

logger = logging.getLogger("bot_logger")

def register(bot):
    """Register all product-related callbacks."""
    
    @bot.callback_query_handler(func=lambda call: call.data == "mb_list")
    def handle_list_barang(call: CallbackQuery):
        """Menampilkan daftar master barang."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            barang_list = get_all_barang(ctx.db_barang)
            teks, markup = render_daftar_master_barang(barang_list)
            safe_edit_message(bot, teks, chat_id, message_id, parse_mode="HTML", reply_markup=markup)
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_LIST] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data == "mb_tambah")
    def handle_tambah_barang(call: CallbackQuery):
        """Tambah barang baru."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            ctx.user_sessions[chat_id]["state"] = "mb_awaiting_input"
            tangani_tambah_barang_chat(chat_id, message_id)
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_TAMBAH] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data == "mb_edit")
    def handle_edit_harga(call: CallbackQuery):
        """Edit harga barang."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            tangani_set_harga_chat(chat_id, message_id)
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_EDIT] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data == "mb_hapus")
    def handle_hapus_barang(call: CallbackQuery):
        """Hapus barang."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            tangani_hapus_barang_chat(chat_id, message_id)
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_HAPUS] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("mb_unit_"))
    def handle_unit_selection(call: CallbackQuery):
        """Handle unit/satuan selection from button press."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract satuan from callback_data
            satuan = call.data.replace("mb_unit_", "").strip()
            
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            
            # Store the satuan in session
            ctx.user_sessions[chat_id]["mb_satuan_baru"] = satuan
            
            # Import here to avoid circular imports
            from handlers.crud_barang import _mb_terima_satuan
            
            # Call satuan handler with stored satuan
            _mb_terima_satuan(None, chat_id=chat_id, message_id_target=message_id)
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_UNIT] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data == "mb_batal")
    def handle_batal(call: CallbackQuery):
        """Cancel operation."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Clear session
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            
            safe_edit_message(bot, "❌ Dibatalkan.", chat_id, message_id)
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_BATAL] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("mb_edit_"))
    def handle_edit_barang_by_idx(call: CallbackQuery):
        """Edit barang pilihan dari daftar."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract row_idx from callback_data
            row_idx = int(call.data.replace("mb_edit_", "").strip())
            
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            
            # Store row index for edit flow
            ctx.user_sessions[chat_id]["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = message_id
            
            # Get barang details
            from core.master_data import get_all_barang, format_rupiah
            semua = get_all_barang(ctx.db_barang)
            target = next((b for b in semua if b["row_idx"] == row_idx), None)
            
            if not target:
                bot.answer_callback_query(call.id, "❌ Barang tidak ditemukan", show_alert=True)
                return
            
            # Ask for new price
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
            
            safe_edit_message(
                bot,
                f"💰 Berapa harga baru untuk <b>{target['nama']}</b> ({target['satuan']})?\n(Harga saat ini: <code>{format_rupiah(target['harga'])}</code>)",
                chat_id, message_id, parse_mode="HTML", reply_markup=markup
            )
            
            # Register next step handler for price input
            msg = bot.send_message(chat_id, "Masukkan harga baru:")
            from handlers.crud_barang import _mb_terima_harga_edit
            bot.register_next_step_handler(msg, _mb_terima_harga_edit)
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_EDIT_IDX] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("pick_edit_row_"))
    def handle_pick_edit_row(call: CallbackQuery):
        """Handle selection dari daftar barang untuk edit."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract index from callback_data
            idx = int(call.data.replace("pick_edit_row_", "").strip())
            
            if chat_id not in ctx.user_sessions or "temp_matches" not in ctx.user_sessions[chat_id]:
                bot.answer_callback_query(call.id, "❌ Pilihan tidak valid", show_alert=True)
                return
            
            temp_matches = ctx.user_sessions[chat_id]["temp_matches"]
            if idx >= len(temp_matches):
                bot.answer_callback_query(call.id, "❌ Pilihan tidak valid", show_alert=True)
                return
            
            h = temp_matches[idx]
            semua = get_all_barang(ctx.db_barang)
            row_idx = next((b["row_idx"] for b in semua if b["nama"] == h["nama"] and b["satuan"] == h["satuan"]), None)
            
            if not row_idx:
                bot.answer_callback_query(call.id, "❌ Barang tidak ditemukan", show_alert=True)
                return
            
            ctx.user_sessions[chat_id]["mb_edit_row"] = row_idx
            ctx.user_sessions[chat_id]["mb_msg_id"] = message_id
            
            from core.master_data import format_rupiah
            
            # Ask for new price
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("❌ Batal", callback_data="mb_batal"))
            
            safe_edit_message(
                bot,
                f"💰 Berapa harga baru untuk <b>{h['nama']}</b> ({h['satuan']})?\n(Harga saat ini: <code>{format_rupiah(h['harga'])}</code>)",
                chat_id, message_id, parse_mode="HTML", reply_markup=markup
            )
            
            # Register next step handler for price input
            msg = bot.send_message(chat_id, "Masukkan harga baru:")
            from handlers.crud_barang import _mb_terima_harga_edit
            bot.register_next_step_handler(msg, _mb_terima_harga_edit)
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[PICK_EDIT_ROW] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("mb_apply_price_"))
    def handle_apply_price(call: CallbackQuery):
        """Terapkan harga baru ke barang pilihan."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            if chat_id not in ctx.user_sessions:
                bot.answer_callback_query(call.id, "❌ Sesi kedaluwarsa", show_alert=True)
                return
            
            session = ctx.user_sessions[chat_id]
            
            # Handle "apply to all" case
            if call.data == "mb_apply_price_all":
                if "temp_matches" not in session or "mb_pending_harga" not in session:
                    bot.answer_callback_query(call.id, "❌ Data tidak lengkap", show_alert=True)
                    return
                
                harga_baru = session["mb_pending_harga"]
                temp_matches = session["temp_matches"]
                
                from core.master_data import update_barang, get_all_barang, format_rupiah
                
                semua = get_all_barang(ctx.db_barang)
                count = 0
                for h in temp_matches:
                    row_idx = next((b["row_idx"] for b in semua if b["nama"] == h["nama"] and b["satuan"] == h["satuan"]), None)
                    if row_idx:
                        update_barang(ctx.db_barang, row_idx, harga_baru)
                        count += 1
                
                safe_edit_message(
                    bot,
                    f"✅ <b>HARGA BERHASIL DIUPDATE</b>\n━━━━━━━━━━━━━━━━━━━━━━\nHarga baru: {format_rupiah(harga_baru)}\nBarang yang diupdate: {count}",
                    chat_id, message_id, parse_mode="HTML"
                )
                
                if chat_id in ctx.user_sessions:
                    del ctx.user_sessions[chat_id]
                
                bot.answer_callback_query(call.id)
                return
            
            # Handle specific item selection
            idx = int(call.data.replace("mb_apply_price_", "").strip())
            
            if "temp_matches" not in session or "mb_pending_harga" not in session:
                bot.answer_callback_query(call.id, "❌ Data tidak lengkap", show_alert=True)
                return
            
            temp_matches = session["temp_matches"]
            if idx >= len(temp_matches):
                bot.answer_callback_query(call.id, "❌ Pilihan tidak valid", show_alert=True)
                return
            
            h = temp_matches[idx]
            harga_baru = session["mb_pending_harga"]
            
            from core.master_data import update_barang, get_all_barang, format_rupiah
            
            semua = get_all_barang(ctx.db_barang)
            row_idx = next((b["row_idx"] for b in semua if b["nama"] == h["nama"] and b["satuan"] == h["satuan"]), None)
            
            if not row_idx:
                bot.answer_callback_query(call.id, "❌ Barang tidak ditemukan", show_alert=True)
                return
            
            # Update price
            update_barang(ctx.db_barang, row_idx, harga_baru)
            
            safe_edit_message(
                bot,
                f"✅ <b>HARGA BERHASIL DIUBAH</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Barang:</b> {h['nama']}\n"
                f"📐 <b>Satuan:</b> {h['satuan']}\n"
                f"💰 <b>Harga Baru:</b> {format_rupiah(harga_baru)}",
                chat_id, message_id, parse_mode="HTML"
            )
            
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_APPLY_PRICE] Error: {e}")
            bot.answer_callback_query(call.id, f"❌ Error: {str(e)}", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("mb_hapus_prep_"))
    def handle_hapus_prep(call: CallbackQuery):
        """Prepare to delete barang - show confirmation."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract row_idx from callback_data
            row_idx = int(call.data.replace("mb_hapus_prep_", "").strip())
            
            if chat_id not in ctx.user_sessions:
                ctx.user_sessions[chat_id] = {}
            
            from core.master_data import get_all_barang, format_rupiah
            
            # Get barang details
            semua = get_all_barang(ctx.db_barang)
            target = next((b for b in semua if b["row_idx"] == row_idx), None)
            
            if not target:
                bot.answer_callback_query(call.id, "❌ Barang tidak ditemukan", show_alert=True)
                return
            
            # Show confirmation
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🗑️ Ya, Hapus", callback_data=f"mb_hapus_{row_idx}"),
                InlineKeyboardButton("❌ Batal", callback_data="mb_batal")
            )
            safe_edit_message(bot,
                f"🗑️ <b>KONFIRMASI HAPUS BARANG</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Apakah Anda yakin ingin menghapus barang ini dari Master Data?\n\n"
                f"📦 <b>Nama:</b> {target['nama']}\n💰 <b>Harga:</b> <code>{format_rupiah(target['harga'])}</code>\n"
                f"📐 <b>Satuan:</b> {target['satuan']}\n",
                chat_id, message_id, parse_mode="HTML", reply_markup=markup)
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_HAPUS_PREP] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("mb_hapus_") and not call.data.startswith("mb_hapus_prep_"))
    def handle_hapus_confirm(call: CallbackQuery):
        """Confirm delete barang."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract row_idx from callback_data
            row_idx_str = call.data.replace("mb_hapus_", "").strip()
            
            # Handle case where it's a number (delete), or other cases
            if not row_idx_str.isdigit():
                return
            
            row_idx = int(row_idx_str)
            
            from core.master_data import get_all_barang, format_rupiah, hapus_barang
            
            # Get barang details before deleting
            semua = get_all_barang(ctx.db_barang)
            target = next((b for b in semua if b["row_idx"] == row_idx), None)
            
            if not target:
                bot.answer_callback_query(call.id, "❌ Barang tidak ditemukan", show_alert=True)
                return
            
            # Delete from database
            hapus_barang(ctx.db_barang, row_idx)
            
            safe_edit_message(
                bot,
                f"✅ <b>BARANG BERHASIL DIHAPUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Nama:</b> {target['nama']}\n📐 <b>Satuan:</b> {target['satuan']}",
                chat_id, message_id, parse_mode="HTML"
            )
            
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_HAPUS] Error: {e}")
            bot.answer_callback_query(call.id, f"❌ Error: {str(e)}", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("pick_del_row_"))
    def handle_pick_del_row(call: CallbackQuery):
        """Handle selection dari daftar barang untuk delete."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            # Extract index from callback_data
            idx = int(call.data.replace("pick_del_row_", "").strip())
            
            if chat_id not in ctx.user_sessions or "temp_matches" not in ctx.user_sessions[chat_id]:
                bot.answer_callback_query(call.id, "❌ Pilihan tidak valid", show_alert=True)
                return
            
            temp_matches = ctx.user_sessions[chat_id]["temp_matches"]
            if idx >= len(temp_matches):
                bot.answer_callback_query(call.id, "❌ Pilihan tidak valid", show_alert=True)
                return
            
            hasil = temp_matches[idx]
            from core.master_data import format_rupiah
            
            # Show confirmation
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
                chat_id, message_id, parse_mode="HTML", reply_markup=markup)
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[PICK_DEL_ROW] Error: {e}")
            bot.answer_callback_query(call.id, "❌ Terjadi error", show_alert=True)
    def handle_confirm_update_price(call: CallbackQuery):
        """Confirm price update."""
        try:
            bot = ctx.bot
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            
            if chat_id not in ctx.user_sessions:
                bot.answer_callback_query(call.id, "❌ Sesi kedaluwarsa", show_alert=True)
                return
            
            session = ctx.user_sessions[chat_id]
            row_idx = session.get("mb_edit_row")
            harga_baru = session.get("mb_pending_harga")
            
            if not row_idx or not harga_baru:
                bot.answer_callback_query(call.id, "❌ Data tidak lengkap", show_alert=True)
                return
            
            # Import update function
            from core.master_data import update_barang, get_all_barang, format_rupiah
            
            # Get the barang and update
            semua = get_all_barang(ctx.db_barang)
            target = next((b for b in semua if b["row_idx"] == row_idx), None)
            
            if not target:
                bot.answer_callback_query(call.id, "❌ Data barang tidak ditemukan", show_alert=True)
                return
            
            # Update price
            update_barang(ctx.db_barang, row_idx, harga_baru)
            
            safe_edit_message(
                bot,
                f"✅ <b>HARGA BERHASIL DIUBAH</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 <b>Barang:</b> {target['nama']}\n"
                f"📐 <b>Satuan:</b> {target['satuan']}\n"
                f"💰 <b>Harga Baru:</b> {format_rupiah(harga_baru)}",
                chat_id, message_id, parse_mode="HTML"
            )
            
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"[MB_CONFIRM_UPDATE] Error: {e}")
            bot.answer_callback_query(call.id, f"❌ Error: {str(e)}", show_alert=True)

__all__ = ["register"]
