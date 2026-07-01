import logging
import re
from time import perf_counter

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.bot_context import ctx
from core.master_data import cari_harga_default, format_rupiah, parse_rupiah
from services.cache_manager import get_cached_barang
from services.debt_tracker import hitung_sisa_tagihan
from services.ui_common import _friendly_field_name, _missing_keys_multi, _missing_keys_single
from utils.security import safe_edit_message

logger = logging.getLogger("bot_logger")

_TELEGRAM_MSG_LIMIT = 4096


def _truncate_telegram_html(text, max_len=_TELEGRAM_MSG_LIMIT - 120):
    if not text or len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "\n\n<i>... (pesan dipotong — gunakan tombol halaman)</i>"


def apply_batch_financials(results, batch_payment_total=None):
    results = results or []
    line_items = []
    grand_total = 0

    for res in results:
        ent = res.get("entitas", {}) or {}
        total_num = parse_rupiah(ent.get("TOTAL") or 0)
        if total_num <= 0 and ent.get("HARGA") and ent.get("JUMLAH"):
            try:
                qty = int(re.search(r"\d+", str(ent["JUMLAH"])).group())
                total_num = parse_rupiah(ent["HARGA"]) * qty
                ent["TOTAL"] = format_rupiah(total_num)
            except Exception:
                total_num = 0
        line_items.append((res, ent, total_num))
        grand_total += total_num

    batch_payment_total = int(batch_payment_total or 0)
    if batch_payment_total > 0 and grand_total > 0:
        applied_total = min(batch_payment_total, grand_total)
        raw_allocations = []
        allocated = 0
        for idx, (_res, _ent, total_num) in enumerate(line_items):
            if idx == len(line_items) - 1:
                nominal = applied_total - allocated
            else:
                nominal = int((applied_total * total_num) / grand_total)
                allocated += nominal
            raw_allocations.append(max(0, min(total_num, nominal)))

        for (res, ent, total_num), nominal in zip(line_items, raw_allocations):
            tagihan = max(0, total_num - nominal)
            if nominal <= 0:
                status = "HUTANG"
            elif nominal >= total_num:
                status = "LUNAS"
            else:
                status = "DICICIL"
            ent["NOMINAL_BAYAR"] = format_rupiah(nominal)
            ent["_CALC_NOMINAL"] = nominal
            ent["_CALC_TAGIHAN"] = tagihan
            ent["_CALC_UANG_MASUK"] = nominal
            ent["_CALC_STATUS"] = status.title()
            res["entitas"] = ent
        return results

    for res, ent, total_num in line_items:
        status = str(ent.get("STATUS") or "Hutang").upper()
        nominal = parse_rupiah(ent.get("NOMINAL_BAYAR") or 0)
        if nominal == 0:
            if status == "LUNAS":
                nominal = total_num
            elif status == "DICICIL":
                frac = ent.get("_CICIL_FRACTION") or 0.5
                nominal = int(total_num * frac)
            else:
                nominal = 0
            ent["NOMINAL_BAYAR"] = format_rupiah(nominal)

        tagihan = max(0, total_num - nominal)
        ent["_CALC_NOMINAL"] = nominal
        ent["_CALC_TAGIHAN"] = tagihan
        ent["_CALC_UANG_MASUK"] = nominal
        ent["_CALC_STATUS"] = status.title()
        res["entitas"] = ent
    return results


def _build_read_page_markup(sess, ringkasan_teks, page, total_pages):
    if total_pages > 1:
        markup = InlineKeyboardMarkup(row_width=2)
        tombol = []
        if page > 1:
            tombol.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"read_page_{page - 1}"))
        if page < total_pages:
            tombol.append(InlineKeyboardButton("Next ➡️", callback_data=f"read_page_{page + 1}"))
        if tombol:
            markup.add(*tombol)
    else:
        markup = InlineKeyboardMarkup(row_width=1)

    if sess.get("entitas", {}).get("NAMA") and "LAPORAN TAGIHAN" in ringkasan_teks:
        markup.row(InlineKeyboardButton("💳 Bayar Tagihan Ini", callback_data="btn_masuk_pelunasan"))

    if total_pages > 1:
        markup.row(InlineKeyboardButton("🔎 Cari Riwayat Lain", callback_data="riwayat_cari_lain"))
        markup.row(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
    else:
        markup.add(InlineKeyboardButton("🔎 Cari Riwayat Lain", callback_data="riwayat_cari_lain"))
        markup.add(InlineKeyboardButton("❌ Tutup Laporan", callback_data="btn_buang"))

    return markup


def kirim_halaman_read(chat_id, page=1, message_id_to_edit=None, call_id=None):
    bot = ctx.bot
    user_sessions = ctx.user_sessions

    if chat_id not in user_sessions or user_sessions[chat_id].get("action") != "reading_pagination":
        if call_id:
            bot.answer_callback_query(
                call_id, "❌ Sesi berakhir, silakan minta laporan lagi", show_alert=True
            )
        return

    sess = user_sessions[chat_id]
    data_list = sess["data_list"]
    total_pages = sess["total_pages"]
    ringkasan_teks = sess.get("ringkasan_teks", "")
    sess["current_page"] = page

    start_idx = (page - 1) * ctx.ITEM_PER_PAGE
    end_idx = start_idx + ctx.ITEM_PER_PAGE
    halaman_data = data_list[start_idx:end_idx]

    rendered_text = ""
    # Hanya render detail jika BUKAN mode Dashboard Harian
    if sess.get("konteks_agregasi") != "Dashboard Harian":
        for item in halaman_data:
            emo_bayar = (
                "✅"
                if "lunas" in item["Status"].lower()
                else "⏳"
                if any(k in item["Status"].lower() for k in ["cicil", "dicicil", "nyicil", "dp"])
                else "🔴"
            )
            # Tampilkan Jumlah Tagihan jika ada piutang
            _tagihan_val = item.get("Tagihan", "")
            baris_tagihan_read = (
                f"⚠️ <b>Tagihan:</b> <code>{_tagihan_val}</code>\n"
                if _tagihan_val and _tagihan_val not in ("0", "")
                else ""
            )
            _uang_masuk_val = item.get("UangMasuk", "")
            baris_uang_masuk_read = (
                f"💸 <b>Uang Masuk:</b> <code>{_uang_masuk_val}</code>\n"
                if _uang_masuk_val and _uang_masuk_val not in ("",)
                else ""
            )
            _harga_val = item.get("Harga", "")
            baris_harga_read = (
                f"💰 <b>Harga Satuan:</b> <code>{_harga_val}</code>\n"
                if _harga_val and _harga_val not in ("",)
                else ""
            )
            _metode_val = item.get("Metode", "")
            baris_metode_read = (
                f"🏦 <b>Metode:</b> <b>{_metode_val}</b>\n"
                if _metode_val and _metode_val not in ("-", "")
                else ""
            )
            layout = (
                f"👤 <b>Pelanggan:</b> {item['Nama']}\n"
                f"📅 <b>Tanggal:</b> {item['Tgl']}\n"
                f"🛒 <b>Item:</b> {item['Jml']} {item['Brg']}\n"
                f"{baris_harga_read}"
                f"💵 <b>Total:</b> <code>{item['Total']}</code>\n"
                f"📊 <b>Status:</b> {emo_bayar} {item['Status']}\n"
                f"{baris_metode_read}"
                f"{baris_tagihan_read}"
                f"{baris_uang_masuk_read}"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            rendered_text += layout

    if total_pages > 1:
        teks_info = (
            f"📋 <b>Laporan Penjualan</b>\n\n{ringkasan_teks}{rendered_text}"
            f"📄 <i>Menampilkan Halaman {page} dari {total_pages}</i>"
        )
    else:
        teks_info = f"📋 <b>Laporan Penjualan</b>\n\n{ringkasan_teks}{rendered_text}"

    teks_info = _truncate_telegram_html(teks_info)
    markup = _build_read_page_markup(sess, ringkasan_teks, page, total_pages)

    if message_id_to_edit:
        try:
            result = safe_edit_message(
                bot, teks_info, chat_id, message_id_to_edit, reply_markup=markup, parse_mode="HTML"
            )
            if result is None and call_id:
                bot.answer_callback_query(call_id, "❌ Gagal memperbarui tampilan", show_alert=True)
        except Exception as e:
            logger.error(f"Error displaying page {page}: {e}")
            if call_id:
                bot.answer_callback_query(call_id, "❌ Gagal memperbarui tampilan", show_alert=True)


def susun_balasan_update(chat_id, message_id_target):
    bot = ctx.bot
    user_sessions = ctx.user_sessions

    if chat_id not in user_sessions:
        return
    sess = user_sessions[chat_id]
    entitas = sess["entitas"]
    sess["state"] = "pending_update"
    sess["action"] = "update_data"
    sess["summary_msg_id"] = message_id_target

    # Kalkulasi preview Jumlah Tagihan & Uang Masuk
    _total_num = parse_rupiah(entitas.get("TOTAL") or 0)
    _nominal_sum = parse_rupiah(entitas.get("NOMINAL_BAYAR") or 0)
    _status_val = entitas.get("STATUS") or ""
    _tagihan, _uang_masuk, _ = hitung_sisa_tagihan(_total_num, _nominal_sum, _status_val)

    sess["action"] = "update_data"
    # Existing code continues
    upd_info = sess.get("update_info", {})
    lama = upd_info.get("uang_masuk_lama", 0)
    baru = upd_info.get("nominal_baru", 0)
    status_awal = upd_info.get("status_awal", "")

    # Kalkulasi dua skenario
    total_jika_tambah = lama + baru
    total_jika_koreksi = baru

    # Peringatan jika sudah lunas tapi ditambah cicilan
    warning_lunas = ""
    if status_awal == "Lunas" and baru > 0:
        warning_lunas = f"⚠️ <b>PERINGATAN:</b> Pembeli atas nama <b>{entitas.get('NAMA')}</b> sudah <b>LUNAS</b>.\n\n"

    # Header rincian pembayaran (hanya muncul jika ada uang masuk baru)
    info_akumulasi = ""
    if baru > 0:
        info_akumulasi = (
            f"━━━━━━━━━━━━━━━━━━\n"
            f"2️⃣ <b>KOREKSI</b> ➡️ Jadi <code>{format_rupiah(total_jika_koreksi)}</code> (Menimpa)\n"
        )

    # Untuk preview sisa tagihan, kita gunakan skenario "Tambah" sebagai default preview
    _tagihan, _, _ = hitung_sisa_tagihan(_total_num, total_jika_tambah, _status_val)
    baris_tagihan = (
        f"⚠️ <b>Sisa Tagihan (Jika Tambah):</b> <code>{format_rupiah(_tagihan)}</code>"
        if _tagihan > 0
        else "✅ <b>Status:</b> LUNAS"
    )

    # Info Extra
    info_extra = ""
    if sess.get("edit_notice"):
        info_extra = f"\n💡 <b>Info:</b> {sess['edit_notice']}\n"
        del sess["edit_notice"]

    if sess.get("multi_matches") and len(sess["multi_matches"]) > 1:
        info_extra += f"⚠️ <i>Ditemukan {len(sess['multi_matches'])} barang mirip. Klik 'Brg' untuk memilih.</i>\n"

    balasan = (
        f"📝 <b>Konfirmasi PENGUBAHAN Data (Update)</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{warning_lunas}"
        f"📅 <b>Tanggal:</b> <b>{entitas.get('TANGGAL') or '-'}</b>\n"
        f"👤 <b>Nama:</b> <b>{entitas.get('NAMA') or '-'}</b>\n"
        f"📦 <b>Barang:</b> <b>{entitas.get('BARANG') or '-'}</b>\n"
        f"🔢 <b>Jumlah:</b> <b>{entitas.get('JUMLAH') or '-'}</b>\n"
        f"💰 <b>Harga:</b> <b>{entitas.get('HARGA') or '-'}</b>\n"
        f"💵 <b>Total:</b> <b>{entitas.get('TOTAL') or '-'}</b>\n"
        f"💳 <b>Status:</b> <b>{entitas.get('STATUS') or '-'}</b>\n"
        f"🏦 <b>Metode:</b> <b>{entitas.get('METODE_PEMBAYARAN') or '-'}</b>\n"
        f"{info_akumulasi}"
        f"{baris_tagihan}\n"
        f"{info_extra}"
        "━━━━━━━━━━━━━━━━━━\n"
        "<i>Pilih tindakan atau edit parameter lainnya:</i>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    current_mode = sess.get("update_mode")
    if baru > 0:
        if current_mode:
            markup.add(InlineKeyboardButton("✅ Kirim Update", callback_data="btn_update_kirim"))
        else:
            markup.row(
                InlineKeyboardButton("➕ Tambah Cicilan", callback_data="upd_mode_tambah"),
                InlineKeyboardButton("✏️ Koreksi Data", callback_data="upd_mode_koreksi"),
            )
    else:
        markup.add(InlineKeyboardButton("✅ Kirim Update", callback_data="btn_update_kirim"))

    markup.add(InlineKeyboardButton("🛠️ Edit Parameter", callback_data="btn_masuk_edit"))
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="btn_batal_edit"))

    try:
        safe_edit_message(
            bot,
            text=balasan,
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
            reply_markup=markup,
        )
    except Exception:
        pass


def susun_balasan_resume(chat_id, message_id_target, is_expert=False, confirm_force=False):
    bot = ctx.bot
    user_sessions = ctx.user_sessions

    sess = user_sessions[chat_id]
    entitas = sess["entitas"]
    hasil_nlp = sess["hasil_nlp"]

    # Amankan status State ke Standby
    sess["state"] = "pending_insert"
    sess["action"] = "input_data"
    sess["summary_msg_id"] = message_id_target

    # Kalkulasi preview Jumlah Tagihan & Uang Masuk untuk ditampilkan di ringkasan
    _total_num = parse_rupiah(entitas.get("TOTAL") or 0)
    _nominal_num = parse_rupiah(entitas.get("NOMINAL_BAYAR") or 0)
    _status_val = entitas.get("STATUS") or ""
    _tagihan, _uang_masuk, _ = hitung_sisa_tagihan(_total_num, _nominal_num, _status_val)

    baris_uang_masuk = (
        f"💸 <b>Uang Masuk:</b> <b>{format_rupiah(_uang_masuk)}</b>\n" if _uang_masuk > 0 else ""
    )
    baris_tagihan = (
        f"⚠️ <b>Jumlah Tagihan:</b> <b>{format_rupiah(_tagihan)}</b>\n" if _tagihan > 0 else ""
    )

    # Label Harga Bawaan & Validasi Satuan
    lbl_harga = "💰 <b>Harga Satuan:</b>"
    warning_satuan = ""
    if ctx.IS_DB_CONNECTED and entitas.get("BARANG"):
        matches = cari_harga_default(
            ctx.db_barang, entitas["BARANG"], satuan_cari=entitas.get("SATUAN")
        )
        if matches:
            info_h = matches[0]
            if entitas.get("HARGA") and format_rupiah(info_h["harga"]) == entitas["HARGA"]:
                lbl_harga = "📋 <b>Harga Bawaan:</b>"

            satuan_db = info_h.get("satuan", "pcs").lower()
            satuan_chat = entitas.get("SATUAN")

            if satuan_chat and satuan_chat.lower() != satuan_db:
                all_units = [m["satuan"].lower() for m in matches]
                if satuan_chat.lower() not in all_units:
                    warning_satuan = f" ⚠️ <i>(Satuan '{satuan_chat}' tidak ada di Master)</i>"

    # Info Extra (Notice Edit / Multi Match)
    info_extra = ""
    if sess.get("edit_notice"):
        info_extra = f"\n💡 <b>Info:</b> {sess['edit_notice']}\n"
        del sess["edit_notice"]

    if sess.get("multi_matches") and len(sess["multi_matches"]) > 1:
        info_extra += f"⚠️ <i>Ditemukan {len(sess['multi_matches'])} barang mirip. Klik 'Brg' untuk memilih.</i>\n"

    aksi = entitas.get("AKSI") or ""
    if aksi == "Catat Pelunasan":
        field_wajib = ["TANGGAL", "NAMA", "NOMINAL_BAYAR"]
    else:
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
    warning_missing = ""
    peringatan_lengkapi = ""
    if missing:
        label = []
        for m in missing:
            if m == "TANGGAL":
                label.append("Tanggal")
            elif m == "NAMA":
                label.append("Nama")
            elif m == "BARANG":
                label.append("Barang")
            elif m == "JUMLAH":
                label.append("Jumlah")
            elif m == "TOTAL":
                label.append("Total")
            elif m == "STATUS":
                label.append("Status")
            elif m == "METODE_PEMBAYARAN":
                label.append("Metode")
            elif m == "NOMINAL_BAYAR":
                label.append("Nominal")
        warning_missing = (
            "⚠️ <b>DATA BELUM LENGKAP:</b> " + ", ".join(label) + "\n━━━━━━━━━━━━━━━━━━\n"
        )
        peringatan_lengkapi = (
            "⚠️ <i>Lengkapi field yang kosong lewat tombol <b>Lengkapi Data</b>.</i>\n\n"
        )

    if aksi == "Catat Pelunasan":
        balasan = (
            "💬 <b>Rangkuman Ekstraksi Mesin</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"{warning_missing}"
            f"{peringatan_lengkapi}"
            f"📅 <b>Tanggal:</b> <b>{entitas.get('TANGGAL') or '-'}</b>\n"
            f"👤 <b>Nama:</b> <b>{entitas.get('NAMA') or '-'}</b>\n"
            f"⚙️ <b>Aksi:</b> <b>{entitas.get('AKSI') or '-'}</b>\n"
            f"💳 <b>Status Bayar:</b> <b>{entitas.get('STATUS') or '-'}</b>\n"
            f"🏦 <b>Metode:</b> <b>{entitas.get('METODE_PEMBAYARAN') or '-'}</b>\n"
            f"💸 <b>Nominal Bayar:</b> <b>{entitas.get('NOMINAL_BAYAR') or '-'}</b>\n"
            f"{info_extra}"
            "━━━━━━━━━━━━━━━━━━\n"
            f"✅ <i>Terbaca (belum diproses): {entitas.get('NAMA') or 'Pelanggan'} membayar cicilan {entitas.get('NOMINAL_BAYAR') or ''}.</i>\n\n"
            "<i>Data belum diproses sebelum Anda klik tombol <b>Proses Pelunasan</b> di bawah.</i>"
        )
    else:
        balasan = (
            "💬 <b>Rangkuman Ekstraksi Mesin</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"{warning_missing}"
            f"{peringatan_lengkapi}"
            f"📅 <b>Tanggal:</b> <b>{entitas.get('TANGGAL') or '-'}</b>\n"
            f"👤 <b>Nama:</b> <b>{entitas.get('NAMA') or '-'}</b>\n"
            f"⚙️ <b>Aksi:</b> <b>{entitas.get('AKSI') or '-'}</b>\n"
            f"📦 <b>Barang:</b> <b>{entitas.get('BARANG') or '-'}</b>\n"
            f"🔢 <b>Jumlah:</b> <b>{entitas.get('JUMLAH') or '-'}</b>{warning_satuan}\n"
            f"{lbl_harga} <b>{entitas.get('HARGA') or '-'}</b>\n"
            f"💵 <b>Total Harga:</b> <b>{entitas.get('TOTAL') or '-'}</b>\n"
            f"💳 <b>Status Bayar:</b> <b>{entitas.get('STATUS') or '-'}</b>\n"
            f"🏦 <b>Metode:</b> <b>{entitas.get('METODE_PEMBAYARAN') or '-'}</b>\n"
            f"{baris_uang_masuk}"
            f"{baris_tagihan}"
            f"{info_extra}"
            "━━━━━━━━━━━━━━━━━━\n"
            f"✅ <i>Terbaca (belum disimpan): {entitas.get('NAMA') or 'Pembeli'} membeli {entitas.get('JUMLAH') or 'barang'} {entitas.get('BARANG') or ''}.</i>\n\n"
            "<i>Data belum masuk database sebelum Anda klik tombol <b>Kirim Data</b> di bawah.</i>"
        )

    if is_expert:
        balasan = (
            "🤖 <b>[Mode Mahir] Data dikenali dengan lengkap!</b>\nBerikut ringkasannya:\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📅 <b>Tanggal:</b> <b>{entitas.get('TANGGAL') or '-'}</b>\n"
            f"👤 <b>Nama Pelanggan:</b> <b>{entitas.get('NAMA') or '-'}</b>\n"
            f"📦 <b>Nama Barang:</b> <b>{entitas.get('BARANG') or '-'}</b>\n"
            f"🔢 <b>Jumlah:</b> <b>{entitas.get('JUMLAH') or '-'}</b>{warning_satuan}\n"
            f"💰 <b>Harga Satuan:</b> <b>{entitas.get('HARGA') or '-'}</b>\n"
            f"💵 <b>Total Harga:</b> <b>{entitas.get('TOTAL') or '-'}</b>\n"
            f"💳 <b>Status Pembayaran:</b> <b>{entitas.get('STATUS') or '-'}</b>\n"
            f"🏦 <b>Metode Pembayaran:</b> <b>{entitas.get('METODE_PEMBAYARAN') or '-'}</b>\n"
            f"⚠️ <b>Jumlah Tagihan:</b> <b>{format_rupiah(_tagihan)}</b>\n"
            f"💸 <b>Jumlah Uang Masuk:</b> <b>{format_rupiah(_uang_masuk)}</b>\n"
            f"{info_extra}"
            "━━━━━━━━━━━━━━━━━━\n"
            "<i>Apakah data ini sudah benar dan siap dikirim ke database?</i>"
        )

    markup = InlineKeyboardMarkup(row_width=2)
    if aksi == "Catat Pelunasan":
        if missing:
            markup.add(
                InlineKeyboardButton("⚠️ Lengkapi Data", callback_data="btn_lengkapi"),
                InlineKeyboardButton("🛠️ Ubah Data", callback_data="btn_masuk_edit"),
            )
            markup.add(
                InlineKeyboardButton("💳 Proses Pelunasan", callback_data="btn_masuk_pelunasan")
            )
        else:
            markup.add(
                InlineKeyboardButton("💳 Proses Pelunasan", callback_data="btn_masuk_pelunasan"),
                InlineKeyboardButton("✏️ Edit Parameter", callback_data="btn_masuk_edit"),
            )
    else:
        if missing:
            if confirm_force:
                markup.add(
                    InlineKeyboardButton("⚠️ Lengkapi Data", callback_data="btn_lengkapi"),
                    InlineKeyboardButton("🛠️ Ubah Data", callback_data="btn_masuk_edit"),
                )
                markup.add(InlineKeyboardButton("✅ Tetap Kirim", callback_data="btn_kirim_force"))
            else:
                markup.add(
                    InlineKeyboardButton("⚠️ Lengkapi Data", callback_data="btn_lengkapi"),
                    InlineKeyboardButton("🛠️ Ubah Data", callback_data="btn_masuk_edit"),
                )
                markup.add(InlineKeyboardButton("✅ Kirim Data", callback_data="btn_kirim"))
        else:
            markup.add(
                InlineKeyboardButton("✅ Kirim Data", callback_data="btn_kirim"),
                InlineKeyboardButton("✏️ Edit Parameter", callback_data="btn_masuk_edit"),
            )
    markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))

    try:
        safe_edit_message(
            bot,
            text=balasan,
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
            reply_markup=markup,
        )
    except Exception:
        pass  # Handle unchanged status


def susun_balasan_conversational(chat_id, message_id_target, missing_fields):
    sess = ctx.user_sessions[chat_id]
    susun_balasan_resume(
        chat_id, message_id_target, confirm_force=(sess.get("state") == "confirm_empty_submit")
    )


def tampilkan_menu_kriteria_edit(chat_id, message_id_target, mode="all"):
    """
    Switch View menjadi mode pilihan tombol parameter edit.
    """
    bot = ctx.bot
    user_sessions = ctx.user_sessions

    # Pastikan mengganti State
    user_sessions[chat_id]["state"] = "editing_menu"

    sess = user_sessions[chat_id]
    sess["edit_mode"] = mode
    entitas = sess.get("entitas", {}) or {}
    missing = sess.get("missing_fields")
    if not isinstance(missing, list):
        missing = _missing_keys_single(entitas)
        sess["missing_fields"] = missing

    tgl = entitas.get("TANGGAL") or "-"
    nama = entitas.get("NAMA") or "-"
    barang = entitas.get("BARANG") or "-"
    jumlah = entitas.get("JUMLAH") or "-"
    satuan = entitas.get("SATUAN") or "-"
    harga = entitas.get("HARGA") or "-"
    total = entitas.get("TOTAL") or "-"
    status = entitas.get("STATUS") or "-"
    metode = entitas.get("METODE_PEMBAYARAN") or "-"
    nominal = entitas.get("NOMINAL_BAYAR") or "-"

    missing_label = ""
    if missing:
        friendly = [_friendly_field_name(m) for m in missing]
        missing_label = f"⚠️ <b>Data belum lengkap:</b> {', '.join(friendly)}\n━━━━━━━━━━━━━━━━━━\n"

    judul = "🧩 <b>LENGKAPI DATA</b>" if mode == "missing_only" else "🛠️ <b>UBAH DATA</b>"
    teks = (
        f"{judul}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{missing_label}"
        "Berikut data yang terbaca saat ini:\n\n"
        f"📅 <b>Tanggal:</b> <b>{tgl}</b>\n"
        f"👤 <b>Nama:</b> <b>{nama}</b>\n"
        f"📦 <b>Barang:</b> <b>{barang}</b>\n"
        f"🔢 <b>Jumlah:</b> <b>{jumlah}</b>\n"
        f"📐 <b>Satuan:</b> <b>{satuan}</b>\n"
        f"💰 <b>Harga:</b> <b>{harga}</b>\n"
        f"💵 <b>Total:</b> <b>{total}</b>\n"
        f"💳 <b>Status:</b> <b>{status}</b>\n"
        f"🏦 <b>Metode:</b> <b>{metode}</b>\n"
        f"💸 <b>DP/Cicil:</b> <b>{nominal}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "<i>Klik tombol di bawah untuk mengubah/melengkapi.</i>"
    )

    def _btn_label(key, base):
        return f"⚠️ {base}" if key in set(missing or []) else base

    markup = InlineKeyboardMarkup(row_width=2)

    btns = [
        ("TANGGAL", "📅 Tanggal", "edit_TANGGAL"),
        ("NAMA", "👤 Nama", "edit_NAMA"),
        ("BARANG", "📦 Barang", "edit_BARANG"),
        ("JUMLAH", "🔢 Jumlah", "edit_JUMLAH"),
        ("SATUAN", "📐 Satuan", "edit_SATUAN"),
        ("HARGA", "💰 Harga", "edit_HARGA"),
        ("TOTAL", "💵 Total", "edit_TOTAL"),
        ("STATUS", "💳 Status", "edit_STATUS"),
        ("METODE_PEMBAYARAN", "🏦 Metode", "edit_METODE_PEMBAYARAN"),
        ("NOMINAL_BAYAR", "💸 DP/Cicil", "edit_NOMINAL_BAYAR"),
    ]

    shown = 0
    for key, base, cb in btns:
        if mode == "missing_only":
            if key not in set(missing or []):
                continue
            label = _btn_label(key, base)
        else:
            label = (
                _btn_label(key, base)
                if key
                in {"TANGGAL", "NAMA", "BARANG", "JUMLAH", "TOTAL", "STATUS", "METODE_PEMBAYARAN"}
                else base
            )
        markup.add(InlineKeyboardButton(label, callback_data=cb))
        shown += 1

    if mode == "missing_only" and shown == 0:
        teks = (
            "✅ <b>DATA SUDAH LENGKAP</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Tidak ada field wajib yang kosong.\n\n"
            "<i>Gunakan 'Ubah Data' jika ingin mengubah nilai yang sudah terisi.</i>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("🔙 Kembali", callback_data="btn_batal_edit"))
    markup.row(InlineKeyboardButton("🔙 Kembali", callback_data="btn_batal_edit"))

    safe_edit_message(
        bot,
        text=teks,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )


def tampilkan_menu_kriteria_edit_multi(chat_id, message_id_target, item_index, mode="all"):
    bot = ctx.bot
    sess = ctx.user_sessions.get(chat_id)
    if not sess or "multi_results" not in sess:
        return

    results = sess.get("multi_results") or []
    if item_index < 0 or item_index >= len(results):
        return

    sess["multi_edit_index"] = item_index
    sess["state"] = "editing_menu_multi"
    sess["multi_edit_mode"] = mode

    ent = results[item_index].get("entitas", {}) or {}
    missing = results[item_index].get("missing_fields")
    if not isinstance(missing, list):
        missing = _missing_keys_multi(ent)
        results[item_index]["missing_fields"] = missing

    missing_label = ""
    if missing:
        missing_label = f"⚠️ <b>Data belum lengkap:</b> {', '.join([_friendly_field_name(m) for m in missing])}\n━━━━━━━━━━━━━━━━━━\n"

    judul = (
        "🧩 <b>LENGKAPI DATA (BATCH)</b>"
        if mode == "missing_only"
        else "🛠️ <b>UBAH DATA (BATCH)</b>"
    )
    teks = (
        f"{judul}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{missing_label}"
        f"👤 <b>Item:</b> <b>[{item_index+1}]</b>\n\n"
        f"📅 <b>Tanggal:</b> <b>{ent.get('TANGGAL') or '-'}</b>\n"
        f"👤 <b>Nama:</b> <b>{ent.get('NAMA') or '-'}</b>\n"
        f"📦 <b>Barang:</b> <b>{ent.get('BARANG') or '-'}</b>\n"
        f"🔢 <b>Jumlah:</b> <b>{ent.get('JUMLAH') or '-'}</b>\n"
        f"📐 <b>Satuan:</b> <b>{ent.get('SATUAN') or '-'}</b>\n"
        f"💰 <b>Harga:</b> <b>{ent.get('HARGA') or '-'}</b>\n"
        f"💵 <b>Total:</b> <b>{ent.get('TOTAL') or '-'}</b>\n"
        f"💳 <b>Status:</b> <b>{ent.get('STATUS') or '-'}</b>\n"
        f"🏦 <b>Metode:</b> <b>{ent.get('METODE_PEMBAYARAN') or '-'}</b>\n"
        f"💸 <b>DP/Cicil:</b> <b>{ent.get('NOMINAL_BAYAR') or '-'}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "<i>Klik tombol di bawah untuk mengubah/melengkapi.</i>"
    )

    def _btn_label(key, base):
        return f"⚠️ {base}" if key in set(missing or []) else base

    btns = [
        ("TANGGAL", "📅 Tanggal", "multi_edit_TANGGAL"),
        ("NAMA", "👤 Nama", "multi_edit_NAMA"),
        ("BARANG", "📦 Barang", "multi_edit_BARANG"),
        ("JUMLAH", "🔢 Jumlah", "multi_edit_JUMLAH"),
        ("SATUAN", "📐 Satuan", "multi_edit_SATUAN"),
        ("HARGA", "💰 Harga", "multi_edit_HARGA"),
        ("TOTAL", "💵 Total", "multi_edit_TOTAL"),
        ("STATUS", "💳 Status", "multi_edit_STATUS"),
        ("METODE_PEMBAYARAN", "🏦 Metode", "multi_edit_METODE_PEMBAYARAN"),
        ("NOMINAL_BAYAR", "💸 DP/Cicil", "multi_edit_NOMINAL_BAYAR"),
    ]

    markup = InlineKeyboardMarkup(row_width=2)
    shown = 0
    for key, base, cb in btns:
        if mode == "missing_only" and key not in set(missing or []):
            continue
        label = _btn_label(key, base) if mode == "missing_only" else base
        markup.add(InlineKeyboardButton(label, callback_data=cb))
        shown += 1

    if mode == "missing_only" and shown == 0:
        teks = (
            "✅ <b>ITEM SUDAH LENGKAP</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Tidak ada field wajib yang kosong pada item ini.\n\n"
            "<i>Gunakan 'Ubah Batch' jika ingin mengubah nilai yang sudah terisi.</i>"
        )
        markup = InlineKeyboardMarkup(row_width=1)

    markup.row(InlineKeyboardButton("🔙 Kembali", callback_data="btn_multi_pick_back"))
    safe_edit_message(
        bot,
        text=teks,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )


def susun_balasan_multi_resume(chat_id, message_id_target):
    """Menampilkan ringkasan dari beberapa transaksi sekaligus (Versi Premium)"""
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    render_start = perf_counter()

    sess = user_sessions.get(chat_id)
    if not sess or "multi_results" not in sess:
        return

    results = sess["multi_results"]
    count = len(results)
    apply_batch_financials(results, sess.get("multi_batch_payment_total"))
    cached_barang = get_cached_barang() if ctx.IS_DB_CONNECTED else []

    info_extra = ""
    if sess.get("edit_notice"):
        info_extra = f"💡 <b>Info:</b> {sess['edit_notice']}\n\n"
        del sess["edit_notice"]

    summary_text = (
        f"📊 <b>REKAP PENJUALAN BANYAK</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Terdeteksi <b>{count} data</b> transaksi baru.\n\n"
        f"{info_extra}"
    )

    total_omzet = 0
    total_masuk = 0
    any_missing = False
    missing_items = 0
    lookup_total_ms = 0.0

    for i, res in enumerate(results, 1):
        ent = res["entitas"]
        # Jika barang ditemukan di master data tapi harga kosong, coba cari
        if ctx.IS_DB_CONNECTED and ent.get("BARANG") and not ent.get("HARGA"):
            if not ent.get("SATUAN") and ent.get("JUMLAH"):
                m_sat = re.search(
                    r"\d+\s*(dus|pcs|toples|pack|bungkus|karton|bks|buah|botol|kg|bal|kantong|lusin|koli|roll|meter|lembar|box|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul|gelas|cup|can|sachet|pak)\b",
                    str(ent.get("JUMLAH")),
                    re.IGNORECASE,
                )
                if m_sat:
                    ent["SATUAN"] = m_sat.group(1).lower()
            lookup_start = perf_counter()
            matches = cari_harga_default(
                ctx.db_barang,
                ent["BARANG"],
                satuan_cari=ent.get("SATUAN"),
                semua_barang=cached_barang,
            )
            lookup_total_ms += (perf_counter() - lookup_start) * 1000
            if matches:
                ent["HARGA"] = format_rupiah(matches[0]["harga"])
                if ent.get("JUMLAH"):
                    try:
                        jml_num = int(re.search(r"\d+", str(ent["JUMLAH"])).group())
                        ent["TOTAL"] = format_rupiah(jml_num * matches[0]["harga"])
                    except:
                        pass
        else:
            if ent.get("HARGA") and ent.get("JUMLAH") and not ent.get("TOTAL"):
                try:
                    jml_num = int(re.search(r"\d+", str(ent["JUMLAH"])).group())
                    hrg_num = parse_rupiah(ent["HARGA"])
                    ent["TOTAL"] = format_rupiah(jml_num * hrg_num)
                except:
                    pass

        if not ent.get("STATUS"):
            ent["STATUS"] = "Hutang"

        nama = (ent.get("NAMA") or "Tanpa Nama").upper()
        brg = ent.get("BARANG") or "-"
        jml = ent.get("JUMLAH") or "0"
        tot_str = ent.get("TOTAL") or "Rp 0"
        status = (ent.get("STATUS") or "Hutang").upper()
        total_num = parse_rupiah(tot_str)
        nominal = int(ent.get("_CALC_UANG_MASUK", parse_rupiah(ent.get("NOMINAL_BAYAR") or 0)) or 0)
        tagihan = int(ent.get("_CALC_TAGIHAN", max(0, total_num - nominal)) or 0)
        status = str(ent.get("_CALC_STATUS") or status).upper()
        total_omzet += total_num
        total_masuk += nominal

        st_emoji = "✅" if status == "LUNAS" else "⏳" if status == "DICICIL" else "🔴"

        missing_keys = _missing_keys_multi(ent)
        res["missing_fields"] = missing_keys
        if missing_keys:
            any_missing = True
            missing_items += 1

        summary_text += f"👤 <b>[{i}] {nama}</b>\n"
        summary_text += f"📅 Tanggal: <b>{ent.get('TANGGAL') or '-'}</b>\n"
        summary_text += f"📦 Barang: <b>{brg}</b>\n"
        summary_text += f"🔢 Jumlah: <b>{jml}</b>\n"
        summary_text += f"💰 Harga: <b>{ent.get('HARGA') or '-'}</b>\n"
        summary_text += f"💵 Total: <code>{tot_str}</code>\n"
        summary_text += f"{st_emoji} Status: <b>{status}</b>\n"
        summary_text += f"🏦 Metode: <b>{ent.get('METODE_PEMBAYARAN') or '-'}</b>"

        if status == "DICICIL":
            summary_text += f"\n💸 Uang Masuk: <code>{format_rupiah(nominal)}</code>\n"
            summary_text += f"⚠️ Sisa Tagihan: <code>{format_rupiah(tagihan)}</code>"
        elif status == "HUTANG":
            summary_text += f"\n💸 Uang Masuk: <code>{format_rupiah(0)}</code>\n"
            summary_text += f"⚠️ Sisa Tagihan: <code>{format_rupiah(total_num)}</code>"
        else:
            summary_text += f"\n💸 Uang Masuk: <code>{format_rupiah(nominal)}</code>"

        if missing_keys:
            summary_text += f"\n⚠️ Data kurang: <i>{', '.join([_friendly_field_name(m) for m in missing_keys])}</i>"

        summary_text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"

    summary_text += (
        f"📈 <b>RINGKASAN BATCH</b>\n"
        f"💰 Total Omzet: <code>{format_rupiah(total_omzet)}</code>\n"
        f"💸 Total Uang Masuk: <code>{format_rupiah(total_masuk)}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        + (
            f"⚠️ <b>PERINGATAN:</b> Ada <b>{missing_items}</b> item yang belum lengkap. Klik <b>Lengkapi Batch</b> untuk mengisi field yang kosong.\n"
            if any_missing
            else ""
        )
        + f"<i>Klik tombol di bawah untuk menyimpan semua data secara bersamaan ke Database.</i>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    if any_missing:
        markup.add(
            InlineKeyboardButton("🧩 Lengkapi Batch", callback_data="btn_multi_lengkapi"),
            InlineKeyboardButton("🛠️ Ubah Batch", callback_data="btn_multi_edit"),
        )
    else:
        markup.add(InlineKeyboardButton("🛠️ Ubah Batch", callback_data="btn_multi_edit"))
    markup.add(InlineKeyboardButton("✅ Simpan Semua", callback_data="btn_multi_kirim"))
    markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))

    safe_edit_message(
        bot, summary_text, chat_id, message_id_target, parse_mode="HTML", reply_markup=markup
    )
    logger.info(
        "[Perf][ui] chat_id=%s lookup_harga_ms=%.1f render_multi_resume_ms=%.1f items=%s",
        chat_id,
        lookup_total_ms,
        (perf_counter() - render_start) * 1000,
        count,
    )
