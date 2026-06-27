"""
Text Handler — Router utama untuk pesan teks natural language
"""
import re
import logging
from datetime import datetime
from time import perf_counter

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.bot_context import ctx
from utils.security import authorized_only, safe_edit_message, sanitize_input, log_exception, notify_admins, safe_delete_message
from services.cache_manager import get_cached_barang, get_cached_metode
from nlp.processor import proses_nlp
from nlp.normalizer import koreksi_teks
from core.master_data import (
    format_rupiah, parse_rupiah, cari_harga_default, normalisasi_tanggal_gs,
    get_all_barang, tambah_barang, update_barang
)
from handlers.handler_dashboard import tangani_dashboard_harian, tangani_dashboard_custom_date, handle_dashboard_date_input
from handlers.command_handler import (
    send_welcome, cmd_dashboard, cmd_master_barang, cmd_menu, cmd_panduan,
    build_reply_keyboard, get_dashboard_web_url, cmd_catat, cmd_foto,
    cmd_cari, cmd_riwayat, cmd_hutang
)
from services.ui_transaksi import susun_balasan_resume

logger = logging.getLogger("bot_logger")


_BATCH_DATE_RE = re.compile(r"\b(\d{1,2})\s*[/\-–—]\s*(\d{1,2})\s*[/\-–—]\s*(\d{2,4})\b")


def _extract_batch_context_from_text(user_text, mapping_metode=None):
    text = str(user_text or "").strip()
    lower = text.lower()
    context = {}

    # Tanggal global pada awal batch, mis. "2/06/2026 budi santoso pesan ..."
    m_date = _BATCH_DATE_RE.search(text)
    if m_date:
        try:
            dd = int(m_date.group(1))
            mm = int(m_date.group(2))
            yy = int(m_date.group(3))
            if yy < 100:
                yy += 2000
            context["TANGGAL"] = f"{dd:02d}-{mm:02d}-{yy:04d}"
        except Exception:
            pass

    # Nama eksplisit "nama: budi santoso"
    m_named = re.search(r"\bnama\s*[:=]\s*([a-zA-Z][a-zA-Z\s\.'-]{1,80})", text, re.IGNORECASE)
    if m_named:
        context["NAMA"] = re.sub(r"\s+", " ", m_named.group(1)).strip().title()
    else:
        # Nama natural sebelum kata kerja transaksi
        text_wo_date = text[m_date.end():].strip(" ,.-") if m_date else text
        m_name = re.search(
            r"^([a-zA-Z][a-zA-Z\s\.'-]{1,80}?)\s+(?:pesan|beli|ambil|order|mau|minta)\b",
            text_wo_date,
            re.IGNORECASE,
        )
        if m_name:
            context["NAMA"] = re.sub(r"\s+", " ", m_name.group(1)).strip().title()

    if any(k in lower for k in ["cicil", "dicicil", "dicil", "nyicil", "dp", "belum lunas"]):
        context["STATUS"] = "Dicicil"
    elif "belum bayar" in lower or "hutang" in lower:
        context["STATUS"] = "Hutang"
    elif "lunas" in lower:
        context["STATUS"] = "Lunas"

    m_nominal = re.search(
        r"(?:bayar|dicicil|dicil|cicil|dp|uang muka|sebesar|sejumlah)\b.*?\b(?:rp\s*)?([\d\.,]+(?:\s*(?:k|jt|juta|rb|ribu|jutaan))?)\b",
        lower,
        re.IGNORECASE,
    )
    if m_nominal:
        nominal = parse_rupiah(m_nominal.group(1))
        if nominal > 0:
            context["NOMINAL_BAYAR"] = format_rupiah(nominal)

    metode = None
    for kw, nama_metode in (mapping_metode or {}).items():
        if kw and kw.lower() in lower:
            metode = nama_metode
            break
    if not metode:
        if re.search(r"\b(tf|trf|transfer)\b", lower):
            metode = "Transfer"
        elif re.search(r"\b(tunai|cash|kontan)\b", lower):
            metode = "Tunai"
        elif re.search(r"\bqris\b", lower):
            metode = "QRIS"
    if metode:
        context["METODE_PEMBAYARAN"] = metode

    return context


def _looks_like_structured_block_text(user_text):
    text = str(user_text or "")
    if "\n" not in text:
        return False
    lines = [ln.strip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n") if ln.strip()]
    if len(lines) < 4:
        return False
    date_lines = sum(1 for ln in lines if _BATCH_DATE_RE.search(ln))
    markers = 0
    for ln in lines:
        low = ln.lower()
        if re.search(r"\bnama(?:\s+sales)?\s*[:=]\s*", low):
            markers += 1
        if "nama produk" in low or "bayar cicilan" in low or "angsuran" in low:
            markers += 1
        if re.search(r"\b\d+\s*(ctn|cen|cth|karton|dus|bungkus|pcs|box|pack|bks)\b", low):
            markers += 1
    return date_lines >= 2 and markers >= 3


def _extract_fast_date(text):
    raw = str(text or "").strip().lower()
    if not raw:
        return None
    if "hari ini" in raw:
        return datetime.now().strftime("%d-%m-%Y")
    if "kemarin" in raw or "kemaren" in raw:
        try:
            from datetime import timedelta
            return (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
        except Exception:
            return None
    m = _BATCH_DATE_RE.search(raw)
    if m:
        try:
            dd = int(m.group(1))
            mm = int(m.group(2))
            yy = int(m.group(3))
            if yy < 100:
                yy += 2000
            return f"{dd:02d}-{mm:02d}-{yy:04d}"
        except Exception:
            return None
    return None


def _build_fast_text_route(user_text):
    text = re.sub(r"\s+", " ", str(user_text or "")).strip()
    lower = text.lower()
    if not text:
        return None

    if any(k in lower for k in ["pembeli terbanyak", "buyer terbanyak", "top buyer"]):
        ent = {"AKSI": "Read Data", "KONTEKS_AGREGASI": "Pembeli Terbanyak"}
        tgl = _extract_fast_date(text)
        if tgl:
            ent["TANGGAL"] = tgl
        return {"entitas": ent, "loading": "⏳ Memuat pembeli terbanyak..."}

    if any(k in lower for k in ["siapa yang masih hutang", "siapa yg masih hutang", "siapa yang punya hutang", "siapa yg msh hutang", "daftar hutang", "tampilkan daftar hutang"]):
        ent = {"AKSI": "Read Data", "KONTEKS_AGREGASI": "Tunggakan Terbanyak", "STATUS": "Hutang"}
        tgl = _extract_fast_date(text)
        if tgl:
            ent["TANGGAL"] = tgl
        return {"entitas": ent, "loading": "⏳ Memuat daftar hutang..."}

    m_read = re.match(r"^(?:tampilkan|lihat|cek|cari|show)\s+(?:pesanan|transaksi|orderan|order|penjualan)\s+(.+)$", text, re.IGNORECASE)
    if m_read:
        target = re.sub(r"\s+", " ", m_read.group(1)).strip(" .,:;-")
        ent = {"AKSI": "Read Data"}
        tgl = _extract_fast_date(target)
        if tgl:
            ent["TANGGAL"] = tgl
        nama = re.sub(_BATCH_DATE_RE, "", target).strip(" .,:;-")
        if nama and nama.lower() not in {"hari ini", "kemarin", "kemaren"}:
            ent["NAMA"] = nama.title()
        return {"entitas": ent, "loading": "⏳ Mencari data pesanan..."}

    for prefixes, aksi, loading in [
        (["hapus produk", "hapus barang", "hapus item", "delete barang", "delete item"], "Hapus Barang", "⏳ Memuat data barang untuk dihapus..."),
        (["harga produk", "harga barang", "cek harga", "cek harga produk", "cek harga barang", "tampilkan harga produk", "tampilkan harga barang"], "Cek Harga Barang", "⏳ Memuat informasi harga barang..."),
    ]:
        for prefix in prefixes:
            if lower.startswith(prefix):
                sisa = text[len(prefix):].strip(" .,:;-")
                ent = {"AKSI": aksi}
                if sisa:
                    ent["BARANG"] = sisa
                return {"entitas": ent, "loading": loading}

    return None

def _terima_multi_nama_pemesan(message):
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    chat_id = message.chat.id
    text = (message.text or "").strip()
    sess = user_sessions.get(chat_id)
    if not sess or sess.get("state") != "awaiting_multi_nama":
        return

    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    if text.lower() in {"batal", "cancel", "stop", "exit"}:
        try:
            safe_edit_message(bot, "❌ <b>Dibatalkan.</b> Silakan ketik perintah baru.", chat_id, sess.get("prompt_msg_id") or message.message_id, parse_mode="HTML", reply_markup=None)
        except Exception:
            pass
        try:
            # Reset seluruh sesi!
            del user_sessions[chat_id]
        except Exception:
            # Jika gagal hapus, bersihkan semua dan set state ke standby
            sess.clear()
            sess["state"] = "standby"
        return

    nama = sanitize_input(text).strip()
    if not nama:
        msg = safe_edit_message(
            bot,
            "👤 <b>Siapa nama pemesan produk ini?</b>\n\nContoh: <code>Ritna</code>\n<i>Ketik 'batal' untuk membatalkan.</i>",
            chat_id,
            sess.get("prompt_msg_id") or message.message_id,
            parse_mode="HTML",
        )
        bot.register_next_step_handler(msg, _terima_multi_nama_pemesan)
        return

    results = sess.get("multi_results") or []
    for item in results:
        ent = item.get("entitas", {}) or {}
        if not ent.get("NAMA"):
            ent["NAMA"] = nama.title()
        item["entitas"] = ent

    sess["state"] = "pending_multi_insert"
    from services.ui_transaksi import susun_balasan_multi_resume
    susun_balasan_multi_resume(chat_id, sess.get("prompt_msg_id") or message.message_id)


def handle_text_message(message):
    """Handle text message - natural language input seperti 'pak andi ambil permen 5 dus bayar tunai'"""
    bot = ctx.bot
    user_sessions = ctx.user_sessions
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_text = message.text
    teks_clean = user_text.strip()

    # Skip command messages
    if user_text.startswith('/'):
        return

    # ==============================
    # CEK KATA "BATAL" ATAU PERINTAH MENU TERLEBIH DAHULU
    # Agar user bisa membatalkan/mengganti perintah meskipun dalam state apapun
    # ==============================
    sess = user_sessions.get(chat_id)
    teks_upper = teks_clean.upper()
    
    # Daftar semua tombol menu yang harus tetap berfungsi
    tombol_menu = ["🏠 Menu Utama", "MENU", "MENU UTAMA"]
    tombol_catat = ["📝 Catat Penjualan", "CATAT", "CATAT PENJUALAN", "📝 Catat"]
    tombol_foto = ["📷 Input Foto Nota", "INPUT FOTO", "FOTO", "📷 Input Foto"]
    tombol_dashboard = ["🌐 Dasbor Web", "DASBOR WEB", "DASHBOARD WEBSITE", "📊 Dashboard", "DASHBOARD", "🌐 Dashboard Website"]
    tombol_cari = ["🔎 Cari Pesanan", "CARI PESANAN", "CARI"]
    tombol_riwayat = ["📑 Riwayat", "📑 Riwayat Transaksi", "RIWAYAT", "RIWAYAT PESANAN"]
    tombol_hutang = ["💰 Cek Hutang", "CEK HUTANG", "HUTANG"]
    tombol_barang = ["📦 Kelola Barang", "📦 Daftar Barang", "KELOLA BARANG", "DAFTAR BARANG", "LIST BARANG"]
    tombol_satuan = ["📐 Kelola Satuan", "KELOLA SATUAN", "MASTER SATUAN", "DAFTAR SATUAN", "TAMBAH SATUAN"]
    tombol_panduan = ["📘 Panduan", "PANDUAN", "GUIDE", "BUKU PANDUAN"]
    tombol_bantuan = ["❓ Bantuan", "BANTUAN", "HELP"]
    
    is_menu_command = (teks_clean in tombol_menu or teks_upper in [t.upper() for t in tombol_menu] or
                      teks_clean in tombol_catat or teks_upper in [t.upper() for t in tombol_catat] or
                      teks_clean in tombol_foto or teks_upper in [t.upper() for t in tombol_foto] or
                      teks_clean in tombol_dashboard or teks_upper in [t.upper() for t in tombol_dashboard] or
                      teks_clean in tombol_cari or teks_upper in [t.upper() for t in tombol_cari] or
                      teks_clean in tombol_riwayat or teks_upper in [t.upper() for t in tombol_riwayat] or
                      teks_clean in tombol_hutang or teks_upper in [t.upper() for t in tombol_hutang] or
                      teks_clean in tombol_barang or teks_upper in [t.upper() for t in tombol_barang] or
                      teks_clean in tombol_satuan or (teks_upper in ["TAMBAH SATUAN", "KELOLA SATUAN", "MASTER SATUAN", "DAFTAR SATUAN"]) or
                      teks_clean in tombol_panduan or teks_upper in [t.upper() for t in tombol_panduan] or
                      teks_clean in tombol_bantuan or teks_upper in [t.upper() for t in tombol_bantuan])
    
    # Jika itu perintah menu atau "batal", reset sesi!
    if (teks_clean.lower() in {"batal", "cancel", "stop", "exit"} or is_menu_command) and sess and sess.get("state") and sess.get("state") != "standby":
        try:
            del user_sessions[chat_id]
        except Exception:
            sess.clear()
            sess["state"] = "standby"
        if teks_clean.lower() in {"batal", "cancel", "stop", "exit"}:
            bot.reply_to(message, "❌ <b>Dibatalkan.</b> Silakan ketik perintah baru.", parse_mode="HTML")
            return
    # Clear old entitas if we're starting a new command (not continuing a transaction)
    if sess and sess.get("state") == "standby" and "entitas" in sess:
        sess["entitas"] = {}

    # ==============================
    # SKIP HANDLER UNTUK STEP INPUT (KECUALI PERINTAH MENU DAN EDIT)
    # Jika user sedang dalam proses input (ms, mb, mm, pending) tapi bukan perintah menu
    # ==============================
    if sess:
        state = sess.get("state")
        
        # JANGAN skip jika state adalah awaiting_edit_teks atau awaiting_edit_teks_multi!
        if state in ["awaiting_edit_teks", "awaiting_edit_teks_multi"]:
            # Handle edit states!
            if state == "awaiting_edit_teks":
                from handlers.crud_transaksi import tangani_revisi_manual
                tangani_revisi_manual(message)
                return
            elif state == "awaiting_edit_teks_multi":
                from handlers.crud_transaksi import tangani_revisi_manual_multi
                tangani_revisi_manual_multi(message)
                return

        if state == "awaiting_riwayat_search":
            from handlers.callback_transaksi import _handle_riwayat_search_input
            _handle_riwayat_search_input(message)
            return
        
        # Cek apakah dalam wizard state, atau ada ms/step info
        skip = False
        if state:
            if (str(state).startswith("ms_") or 
                str(state).startswith("mb_") or 
                str(state).startswith("mm_") or 
                str(state).startswith("pending_") or 
                (str(state).startswith("awaiting_") and state not in ["awaiting_edit_teks", "awaiting_edit_teks_multi", "awaiting_dashboard_date", "awaiting_riwayat_search"])):
                skip = True
                logger.info(f"Skipping text handler karena state = {state}")
        
        # Cek apakah sedang dalam proses ms (master satuan)
        if not skip and ("ms_msg_idx" in sess or "ms_edit_id" in sess):
            skip = True
            logger.info("Skipping text handler karena dalam proses master satuan")
        
        if skip:
            return

    # ✨ HANDLING TOMBOL REPLY KEYBOARD & KEYWORDS
    
    # Daftar semua tombol baru untuk pengenalan
    tombol_menu = ["🏠 Menu Utama", "MENU", "MENU UTAMA"]
    tombol_catat = ["📝 Catat Penjualan", "CATAT", "CATAT PENJUALAN", "📝 Catat"]
    tombol_foto = ["📷 Input Foto Nota", "INPUT FOTO", "FOTO", "📷 Input Foto"]
    tombol_dashboard = ["🌐 Dasbor Web", "DASBOR WEB", "DASHBOARD WEBSITE", "📊 Dashboard", "DASHBOARD", "🌐 Dashboard Website"]
    tombol_cari = ["🔎 Cari Pesanan", "CARI PESANAN", "CARI"]
    tombol_riwayat = ["📑 Riwayat Transaksi", "RIWAYAT", "RIWAYAT PESANAN", "📑 Riwayat"]
    tombol_hutang = ["💰 Cek Hutang", "CEK HUTANG", "HUTANG"]
    tombol_barang = ["📦 Daftar Barang", "DAFTAR BARANG", "LIST BARANG"]
    tombol_satuan = ["📐 Kelola Satuan", "KELOLA SATUAN", "MASTER SATUAN", "DAFTAR SATUAN", "TAMBAH SATUAN"]
    tombol_panduan = ["📘 Panduan", "PANDUAN", "GUIDE", "BUKU PANDUAN"]
    tombol_bantuan = ["❓ Bantuan", "BANTUAN", "HELP"]
    
    if teks_clean in tombol_menu or teks_upper in [t.upper() for t in tombol_menu]:
        cmd_menu(message)
        return
    elif teks_clean in tombol_catat or teks_upper in [t.upper() for t in tombol_catat]:
        cmd_catat(message)
        return
    elif teks_clean in tombol_foto or teks_upper in [t.upper() for t in tombol_foto]:
        cmd_foto(message)
        return
    elif teks_clean in tombol_dashboard or teks_upper in [t.upper() for t in tombol_dashboard]:
        cmd_dashboard(message)
        return
    elif ("HARI INI" in teks_upper) and any(k in teks_upper for k in ["TRANSAKSI", "TRANSAKI", "PESANAN"]) and any(k in teks_upper for k in ["TAMPIL", "TAMPILKAN", "LIHAT", "CEK", "SHOW"]):
        if not ctx.IS_DB_CONNECTED:
            bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
            return
        tgl = normalisasi_tanggal_gs("hari ini")
        if not tgl:
            bot.reply_to(message, "❌ Gagal menentukan tanggal hari ini.")
            return
        sess = user_sessions.ensure(chat_id)
        sess["entitas"] = {"AKSI": "Read Data", "TANGGAL": tgl}
        msg_proses = bot.reply_to(message, f"⏳ Memuat transaksi hari ini ({tgl})...")
        from handlers.crud_transaksi import tangani_read_data
        tangani_read_data(chat_id, msg_proses.message_id)
        return
    elif teks_clean in tombol_cari or teks_upper in [t.upper() for t in tombol_cari]:
        cmd_cari(message)
        return
    elif teks_clean in tombol_riwayat or teks_upper in [t.upper() for t in tombol_riwayat]:
        cmd_riwayat(message)
        return
    elif teks_clean in tombol_hutang or teks_upper in [t.upper() for t in tombol_hutang]:
        cmd_hutang(message)
        return
    elif teks_clean in tombol_barang or teks_upper in [t.upper() for t in tombol_barang]:
        if not ctx.IS_DB_CONNECTED:
            bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses Master Barang.")
            return
        msg_proses = bot.reply_to(message, "⏳ Memuat daftar produk...")
        sess = user_sessions.ensure(chat_id)
        sess.update({"entitas": {"AKSI": "Cek Harga Barang"}})
        from handlers.crud_barang import tangani_cek_harga_chat
        tangani_cek_harga_chat(chat_id, msg_proses.message_id)
        return
    # Hanya match exact phrase untuk satuan, bukan bagian dari kata lain
    elif teks_clean in tombol_satuan or (teks_upper in ["TAMBAH SATUAN", "KELOLA SATUAN", "MASTER SATUAN", "DAFTAR SATUAN"]):
        from handlers.command_handler import cmd_master_satuan
        cmd_master_satuan(message)
        return
    elif teks_clean in tombol_panduan or teks_upper in [t.upper() for t in tombol_panduan]:
        cmd_panduan(message)
        return
    elif teks_clean in tombol_bantuan or teks_upper in [t.upper() for t in tombol_bantuan]:
        send_welcome(message)
        return
    elif teks_clean == "📦 Kelola Barang" or teks_upper in ["KELOLA BARANG", "TAMBAH BARANG", "INPUT BARANG", "TAMBAH PRODUK", "INPUT PRODUK", "TAMBAH ITEM", "BARANG BARU"]:
        from handlers.command_handler import cmd_master_barang
        cmd_master_barang(message)
        return

    # Rate limiting
    if not ctx.rate_limiter.is_allowed(user_id):
        logger.warning(f"Rate limit exceeded untuk user {user_id} pada text message")
        bot.reply_to(message, "⏱️ Terlalu banyak request. Tunggu sebentar...")
        return

    sess = user_sessions.ensure(chat_id)
    need_keyboard = not bool(sess.get("ui_keyboard_shown"))
    if need_keyboard:
        sess["ui_keyboard_shown"] = True

    teks_upper = (user_text or "").upper()
    if any(k in teks_upper for k in ["TOMBOL HILANG", "TOMBOLNYA HILANG", "TOMBOL KOK HILANG", "KEYBOARD HILANG"]):
        bot.reply_to(message, "💡 Gunakan tombol biru <b>Menu</b> di sebelah kiri kolom chat untuk akses semua fitur.", parse_mode="HTML")
        return

    # Sanitize input
    user_text = sanitize_input(user_text)
    logger.info(f"User {user_id} kirim: {user_text[:80]}")

    fast_route = _build_fast_text_route(user_text)
    if fast_route:
        sess.update({"entitas": fast_route["entitas"]})
        msg_proses = bot.reply_to(message, fast_route["loading"])
        logger.info(
            "[Perf][chat] chat_id=%s fast_route=%s",
            chat_id,
            fast_route["entitas"].get("AKSI") or fast_route["entitas"].get("KONTEKS_AGREGASI"),
        )
        from handlers.crud_transaksi import tangani_read_data
        from handlers.crud_barang import tangani_cek_harga_chat, tangani_hapus_barang_chat

        aksi_fast = fast_route["entitas"].get("AKSI")
        if aksi_fast == "Read Data":
            tangani_read_data(chat_id, msg_proses.message_id)
        elif aksi_fast == "Cek Harga Barang":
            tangani_cek_harga_chat(chat_id, msg_proses.message_id)
        elif aksi_fast == "Hapus Barang":
            tangani_hapus_barang_chat(chat_id, msg_proses.message_id)
        return

    # Shortcut: tampilkan daftar produk/barang tanpa NLP panjang
    if ("DAFTAR" in teks_upper or "LIST" in teks_upper) and ("PRODUK" in teks_upper or "BARANG" in teks_upper) and any(k in teks_upper for k in ["TAMPIL", "TAMPILKAN", "LIHAT", "CEK"]):
        if not ctx.IS_DB_CONNECTED:
            bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses Master Barang.")
            return
        msg_proses = bot.reply_to(message, "⏳ Memuat daftar produk...")
        sess.update({"entitas": {"AKSI": "Cek Harga Barang"}})
        from handlers.crud_barang import tangani_cek_harga_chat
        tangani_cek_harga_chat(chat_id, msg_proses.message_id)
        return

    def _extract_customer_name(text):
        teks = (text or "").strip()
        if not teks:
            return ""
        teks = re.sub(r"^\s*(ini\s+data|data)\s+", "", teks, flags=re.IGNORECASE).strip()
        teks = re.sub(r"\s+", " ", teks).strip()
        return teks.title()

    def _extract_year(text):
        teks = (text or "").strip()
        m = re.search(r"\b(\d{4}|\d{2})\b", teks)
        if not m:
            return None
        y = m.group(1)
        if len(y) == 2:
            y = "20" + y
        try:
            y_int = int(y)
            if 2000 <= y_int <= 2100:
                return y_int
        except Exception:
            return None
        return None

    def _extract_product(text):
        teks = (text or "").strip()
        if not teks:
            return ""
        teks = re.sub(r"^\s*(produk|barang|item)\s+", "", teks, flags=re.IGNORECASE).strip()
        teks = re.sub(r"\s+", " ", teks).strip()
        return teks

    def _finalize_ocr_session(sess, nama=None, tahun=None, produk=None, prompt_msg_id=None):
        ocr_text = sess.get("ocr_text", "")
        ringkas = sess.get("ringkas") or {}

        all_b = get_cached_barang()
        daftar_b = [b["nama"] for b in all_b]
        mapping_m = get_cached_metode()

        bagian = []
        if nama:
            bagian.append(nama)
        if produk:
            bagian.append(produk)
        if ringkas.get("qty") and ringkas.get("unit"):
            bagian.append(f"{ringkas['qty']} {ringkas['unit']}")
        if ringkas.get("day") and ringkas.get("month") and (tahun or ringkas.get("year")):
            y = tahun or ringkas.get("year")
            bagian.append(f"{ringkas['day']}-{ringkas['month']}-{y}")
        bagian.append(ocr_text)

        combined_text = " ".join([b for b in bagian if b]).strip()
        combined_text = koreksi_teks(combined_text, daftar_barang=daftar_b)
        results_nlp = proses_nlp(
            combined_text,
            daftar_barang=daftar_b,
            mapping_metode=mapping_m,
            already_normalized=True,
        )
        hasil_nlp = results_nlp[0] if results_nlp else {"entitas": {}}
        entitas = hasil_nlp.get("entitas", {}) or {}

        if nama:
            entitas["NAMA"] = nama
        if produk:
            entitas["BARANG"] = produk

        if ringkas.get("qty") and ringkas.get("unit"):
            entitas["JUMLAH"] = f"{ringkas['qty']} {ringkas['unit']}"
            entitas["SATUAN"] = ringkas["unit"]

        # Normalisasi tanggal untuk kasus seperti "kamis 7 nop 2024"
        if entitas.get("TANGGAL"):
            entitas["TANGGAL"] = normalisasi_tanggal_gs(entitas["TANGGAL"])
        elif ringkas.get("day") and ringkas.get("month") and (tahun or ringkas.get("year")):
            y = tahun or ringkas.get("year")
            entitas["TANGGAL"] = f"{ringkas['day']}-{ringkas['month']}-{y}"

        if not entitas.get("AKSI"):
            entitas["AKSI"] = "Tambah Penjualan"

        teks_lower = combined_text.lower()
        if not entitas.get("STATUS"):
            entitas["STATUS"] = "Lunas" if any(k in teks_lower for k in ["lunas", "dibayar"]) else "Hutang"

        if not entitas.get("METODE_PEMBAYARAN"):
            if any(k in teks_lower for k in ["transfer", "tf", "trf"]):
                entitas["METODE_PEMBAYARAN"] = "Transfer"
            elif any(k in teks_lower for k in ["tunai", "cash", "kontan"]):
                entitas["METODE_PEMBAYARAN"] = "Tunai"
            else:
                pass

        # Auto-lookup harga & hitung total jika memungkinkan
        if ctx.IS_DB_CONNECTED and entitas.get("BARANG") and not entitas.get("HARGA"):
            matches = cari_harga_default(ctx.db_barang, entitas["BARANG"], satuan_cari=entitas.get("SATUAN"))
            if matches:
                info_h = matches[0]
                entitas["HARGA"] = format_rupiah(info_h["harga"])
                entitas["SATUAN"] = info_h.get("satuan") or entitas.get("SATUAN")

        if entitas.get("HARGA") and entitas.get("JUMLAH") and not entitas.get("TOTAL"):
            try:
                _m = re.search(r"\d+", str(entitas["JUMLAH"]))
                if not _m:
                    raise ValueError("Jumlah tidak valid")
                jml_num = int(_m.group())
                hrg_num = parse_rupiah(entitas["HARGA"])
                entitas["TOTAL"] = format_rupiah(jml_num * hrg_num)
            except Exception:
                pass

        # Jika masih ada field inti yang kosong, arahkan ke mode lengkapi data
        wajib = ["TANGGAL", "NAMA", "BARANG", "JUMLAH", "STATUS", "METODE_PEMBAYARAN"]
        missing = [k for k in wajib if not entitas.get(k)]

        sess.update({"hasil_nlp": hasil_nlp, "entitas": entitas})

        if missing:
            sess["state"] = "pending_confirmation"
            if prompt_msg_id:
                susun_balasan_resume(chat_id, prompt_msg_id)
            else:
                msg = bot.send_message(chat_id, "🔄 Menyusun rangkuman data...")
                susun_balasan_resume(chat_id, msg.message_id)
            return

        sess["state"] = "pending_confirmation"
        if prompt_msg_id:
            susun_balasan_resume(chat_id, prompt_msg_id)
        else:
            msg = bot.send_message(chat_id, "🔄 Menyusun rangkuman data OCR...")
            susun_balasan_resume(chat_id, msg.message_id)

    # ✨ OCR FLOW: Jika bot sedang menunggu nama pelanggan dari input foto
    if chat_id in user_sessions and user_sessions[chat_id].get("state") in ["awaiting_ocr_year", "awaiting_ocr_product", "awaiting_ocr_customer"]:
        sess = user_sessions[chat_id]
        prompt_msg_id = sess.get("prompt_msg_id")
        
        # Tangani batal!
        if text.lower() in {"batal", "cancel", "stop", "exit"}:
            try:
                safe_edit_message(bot, "❌ <b>Dibatalkan.</b> Silakan ketik perintah baru.", chat_id, prompt_msg_id or message.message_id, parse_mode="HTML", reply_markup=None)
            except Exception:
                pass
            try:
                del user_sessions[chat_id]
            except Exception:
                sess.clear()
                sess["state"] = "standby"
            return

        # Tahun
        if sess.get("state") == "awaiting_ocr_year":
            y = _extract_year(user_text)
            if not y:
                bot.reply_to(message, "⚠️ Tahun tidak terbaca. Contoh: <code>2024</code>", parse_mode="HTML")
                return
            sess["ringkas"] = sess.get("ringkas") or {}
            sess["ringkas"]["year"] = y
            sess["state"] = "awaiting_ocr_product"
            safe_edit_message(
                bot,
                "📦 <b>Ini pesanan untuk produk/barang apa?</b>\n\nContoh: <code>willo</code>",
                chat_id,
                prompt_msg_id,
                parse_mode="HTML"
            )
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception:
                pass
            return

        # Produk
        if sess.get("state") == "awaiting_ocr_product":
            prod = _extract_product(user_text)
            if not prod:
                bot.reply_to(message, "⚠️ Produk tidak terbaca. Contoh: <code>willo</code>", parse_mode="HTML")
                return
            sess["produk"] = prod
            sess["state"] = "awaiting_ocr_customer"
            safe_edit_message(
                bot,
                "📸 <b>Ini data penjualan siapa?</b>\n\nContoh: <code>Pak Edi</code>",
                chat_id,
                prompt_msg_id,
                parse_mode="HTML"
            )
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception:
                pass
            return

        # Nama pelanggan
        if sess.get("state") == "awaiting_ocr_customer":
            nama = _extract_customer_name(user_text)
            if not nama:
                bot.reply_to(message, "⚠️ Nama tidak terbaca. Contoh: <code>Pak Edi</code>", parse_mode="HTML")
                return
            tahun = (sess.get("ringkas") or {}).get("year")
            produk = sess.get("produk") or (sess.get("entitas") or {}).get("BARANG")
            _finalize_ocr_session(sess, nama=nama, tahun=tahun, produk=produk, prompt_msg_id=prompt_msg_id)
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception:
                pass
            return

    # Wizard / edit flows — fallback jika step handler hilang (restart bot, sesi persisten)
    if chat_id in user_sessions:
        sess_wizard = user_sessions[chat_id]
        wizard_state = sess_wizard.get("state")

        # Skip seluruh wizard flow jika ini state master satuan (ms_)
        if wizard_state and str(wizard_state).startswith("ms_"):
            return

        if teks_clean.lower() in {"batal", "cancel", "stop", "exit"} and wizard_state and wizard_state != "standby":
            try:
                del user_sessions[chat_id]
            except Exception:
                sess_wizard.clear()
                sess_wizard["state"] = "standby"
            bot.reply_to(message, "❌ <b>Dibatalkan.</b> Silakan ketik perintah baru.", parse_mode="HTML")
            return

        if wizard_state == "awaiting_edit_teks":
            from handlers.crud_transaksi import tangani_revisi_manual
            tangani_revisi_manual(message)
            return

        if wizard_state == "awaiting_edit_teks_multi":
            from handlers.crud_transaksi import tangani_revisi_manual_multi
            tangani_revisi_manual_multi(message)
            return

        if wizard_state == "mb_awaiting_name":
            from handlers.crud_barang import _mb_terima_nama
            _mb_terima_nama(message)
            return

        mb_wizard = wizard_state and (
            str(wizard_state).startswith("mb_")
            or wizard_state in ("mb_awaiting_name", "mb_input_nama")
        )

        if mb_wizard and sess_wizard.get("mb_nama_baru") and "mb_harga_baru" not in sess_wizard:
            from handlers.crud_barang import _mb_terima_harga
            _mb_terima_harga(message)
            return

        if mb_wizard and sess_wizard.get("mb_nama_baru") and sess_wizard.get("mb_harga_baru"):
            from handlers.crud_barang import _mb_terima_satuan
            _mb_terima_satuan(message)
            return

        if wizard_state == "mb_hapus_browse":
            from handlers.callback_pengaturan import _mb_hapus_search_input
            _mb_hapus_search_input(message)
            return

        if wizard_state == "mb_edit_browse":
            from handlers.callback_pengaturan import _mb_edit_search_input
            _mb_edit_search_input(message)
            return

    # ✨ DASHBOARD: Cek apakah user sedang input tanggal dashboard
    if handle_dashboard_date_input(bot, message, ctx.db_transaksi, user_sessions):
        return

    try:
        perf_total_start = perf_counter()
        # Kirim pesan loading
        msg_proses = bot.reply_to(
            message,
            "Sedang diproses...",
            reply_markup=(build_reply_keyboard() if need_keyboard else None)
        )

        # Ambil data dari Cache (Cepat!)
        all_b = get_cached_barang()
        daftar_b = [b["nama"] for b in all_b]
        mapping_m = get_cached_metode()
        structured_doc_mode = False
        structured_payment_entries = []
        nlp_stage_ms = 0.0

        if _looks_like_structured_block_text(user_text):
            try:
                structured_start = perf_counter()
                from handlers.photo_handler import (
                    _build_structured_nlp_input,
                    _build_sales_results_from_ocr_entries,
                )
                _nlp_text, structured_payment_entries, _sales_contexts, sales_entries = _build_structured_nlp_input(user_text)
                if sales_entries:
                    results_nlp = _build_sales_results_from_ocr_entries(sales_entries, daftar_b, mapping_m)
                    structured_doc_mode = True
                else:
                    results_nlp = []
                nlp_stage_ms = (perf_counter() - structured_start) * 1000
            except Exception:
                results_nlp = []
        else:
            results_nlp = []

        if not results_nlp:
            nlp_start = perf_counter()
            user_text_norm = koreksi_teks(user_text, daftar_barang=daftar_b)
            results_nlp = proses_nlp(
                user_text_norm,
                db_metode=ctx.db_metode,
                daftar_barang=daftar_b,
                mapping_metode=mapping_m,
                already_normalized=True,
            )
            nlp_stage_ms = (perf_counter() - nlp_start) * 1000

        logger.info(
            "[Perf][chat] chat_id=%s structured=%s nlp_ms=%.1f results=%s",
            chat_id,
            structured_doc_mode,
            nlp_stage_ms,
            len(results_nlp or []),
        )

        if not results_nlp:
            if user_sessions.get(chat_id, {}).get("state") in ["filling_missing_fields", "confirm_empty_submit"]:
                # If they are filling missing fields but NLP failed, just proceed with old entities
                # We will check missing fields again
                hasil_nlp = {"entitas": {}}
                results_nlp = [hasil_nlp]
            else:
                friendly_err = (
                    "Maaf, saya belum menangkap maksudnya.\n\n"
                    "💡 Contoh yang bisa Anda ketik:\n"
                    "- <code>Pak Andi ambil willo 5 karton lunas tunai</code>\n"
                    "- <code>cek penjualan hari ini</code>\n"
                    "- <code>tampilkan daftar produk</code>\n\n"
                    "Atau klik tombol menu di bawah."
                )
                safe_edit_message(bot, friendly_err, chat_id, msg_proses.message_id)
                return

        # Handle Multi-Entry
        if len(results_nlp) > 1:
            valid_results = [r for r in results_nlp if r["entitas"].get("AKSI") or r["entitas"].get("NAMA") or r["entitas"].get("BARANG")]
            if len(valid_results) > 1:
                base_aksi = None
                for r in valid_results:
                    if r.get("entitas", {}).get("AKSI"):
                        base_aksi = r["entitas"]["AKSI"]
                        break

                if base_aksi == "Tambah Barang":
                    if not ctx.IS_DB_CONNECTED:
                        safe_edit_message(bot, "❌ Mode Offline: Tidak dapat mengakses Master Barang.", chat_id, msg_proses.message_id)
                        return

                    semua_existing = get_all_barang(ctx.db_barang)
                    existing_map = {}
                    placeholder_map = {}
                    generic_names = {"permen", "serbuk", "roti", "pia", "roti pia", "roti/pia", "roti pia (generik)"}
                    for b in semua_existing:
                        n = str(b.get("nama", "")).strip().lower()
                        u = str(b.get("satuan", "")).strip().lower()
                        if n and u:
                            existing_map[(n, u)] = b.get("row_idx")
                        try:
                            h = int(b.get("harga") or 0)
                        except Exception:
                            h = 0
                        if n in generic_names and u and h > 0 and b.get("row_idx"):
                            placeholder_map[(u, h)] = b.get("row_idx")

                    def _pick_specific_name(raw_text):
                        t = (raw_text or "").lower()
                        mapping = [
                            (["wiilo", "wilo", "willo"], "Willo"),
                            (["bemmbeng", "bembeng", "bengbeng", "beem-beeng"], "Bemmbeng"),
                            (["cholatos", "chocholetus"], "Cholatos"),
                            (["adangrow"], "Adangrow"),
                            (["miksu"], "Miksu"),
                            (["getbory", "siiperquuen"], "Getbory"),
                            (["lolipop", "lalipop", "lollipop"], "Lolipop"),
                            (["roti pia bulus", "pia bulus", "bulus"], "Roti Pia (Bulus)"),
                            (["roti pia roda", "pia roda", "roda"], "Roti Pia (Roda)"),
                            (["roti pia potong", "pia potong", "potong"], "Roti Pia (Potong)"),
                        ]
                        for keys, val in mapping:
                            if any(k in t for k in keys):
                                return val
                        return None

                    base_harga_raw = None
                    base_satuan = None
                    for r0 in valid_results:
                        e0 = r0.get("entitas", {})
                        if not base_harga_raw and e0.get("HARGA"):
                            base_harga_raw = e0.get("HARGA")
                        if not base_satuan and e0.get("SATUAN"):
                            base_satuan = e0.get("SATUAN")
                        if base_harga_raw and base_satuan:
                            break

                    hasil_lines = []
                    ok = 0
                    updated = 0
                    fail = 0

                    for r in valid_results:
                        e = r.get("entitas", {})
                        e["AKSI"] = "Tambah Barang"
                        nama = e.get("BARANG")
                        harga_raw = e.get("HARGA") or base_harga_raw
                        satuan = e.get("SATUAN") or base_satuan
                        picked = _pick_specific_name(r.get("original_text", ""))
                        if picked and (not nama or str(nama or "").strip().lower() in generic_names):
                            nama = picked
                        elif picked and "roti pia" in str(nama or "").lower():
                            nama = picked

                        if not nama or not harga_raw or not satuan:
                            fail += 1
                            missing = []
                            if not nama: missing.append("nama")
                            if not harga_raw: missing.append("harga")
                            if not satuan: missing.append("satuan")
                            hasil_lines.append(f"• ❌ Gagal: data kurang ({', '.join(missing)})")
                            continue

                        try:
                            harga_num = parse_rupiah(harga_raw)
                            key = (str(nama).strip().lower(), str(satuan).strip().lower())
                            row_idx = existing_map.get(key)
                            if row_idx:
                                update_barang(ctx.db_barang, row_idx, harga=harga_num, satuan=satuan)
                                updated += 1
                                hasil_lines.append(f"• 🔄 {nama} — <code>{format_rupiah(harga_num)}</code> / {satuan}")
                            else:
                                placeholder_row = placeholder_map.get((str(satuan).strip().lower(), harga_num))
                                if placeholder_row:
                                    update_barang(ctx.db_barang, placeholder_row, nama=nama, harga=harga_num, satuan=satuan)
                                    updated += 1
                                    hasil_lines.append(f"• 🔄 {nama} — <code>{format_rupiah(harga_num)}</code> / {satuan}")
                                    existing_map[key] = placeholder_row
                                else:
                                    new_id = tambah_barang(ctx.db_barang, nama, harga_num, satuan)
                                    ok += 1
                                    hasil_lines.append(f"• ✅ {nama} — <code>{format_rupiah(harga_num)}</code> / {satuan}")
                                    if new_id:
                                        existing_map[key] = new_id
                        except Exception as ex:
                            fail += 1
                            hasil_lines.append(f"• ❌ {nama} / {satuan} — <code>{str(ex)[:60]}</code>")

                    teks = (
                        "<b>HASIL TAMBAH BARANG (BULK)</b>\n"
                        "━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"✅ Ditambah: <b>{ok}</b>\n"
                        f"🔄 Diupdate: <b>{updated}</b>\n"
                        f"❌ Gagal: <b>{fail}</b>\n"
                        "━━━━━━━━━━━━━━━━━━━━━━\n"
                        + "\n".join(hasil_lines)
                    )
                    safe_edit_message(bot, teks, chat_id, msg_proses.message_id, parse_mode="HTML")
                    try:
                        user_sessions[chat_id]["state"] = "standby"
                        user_sessions[chat_id]["entitas"] = {}
                    except Exception:
                        pass
                    return

                # ✨ CONTEXT INHERITANCE: Salin konteks lama (misal Nama/Tgl/Metode) ke setiap item
                existing_state = user_sessions.get(chat_id, {}).get("state")
                # Only inherit old context if we're adding sales (not for search/delete!)
                context_lama = {}
                if existing_state in ["filling_missing_fields", "confirm_empty_submit", "pending_confirmation"] and (len(valid_results) > 0 and valid_results[0].get("entitas", {}).get("AKSI") == "Tambah Penjualan"):
                    context_lama = user_sessions[chat_id].get("entitas", {}).copy()

                if structured_doc_mode:
                    context_pesan = {}
                    if valid_results and isinstance(valid_results[0], dict):
                        ent0 = valid_results[0].get("entitas", {}) or {}
                        for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN"]:
                            if ent0.get(k):
                                context_pesan[k] = ent0.get(k)
                else:
                    context_pesan = _extract_batch_context_from_text(user_text, mapping_m)
                    if valid_results and isinstance(valid_results[0], dict):
                        ent0 = valid_results[0].get("entitas", {}) or {}
                        for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN", "STATUS", "NOMINAL_BAYAR"]:
                            if ent0.get(k) and not context_pesan.get(k):
                                context_pesan[k] = ent0.get(k)
                
                lookup_total_ms = 0.0
                for item in valid_results:
                    # Gabungkan: Data dari chat terbaru menimpa konteks lama
                    gabungan = context_lama.copy()
                    for k, v in context_pesan.items():
                        if v and not gabungan.get(k):
                            gabungan[k] = v
                    for k, v in item["entitas"].items():
                        if v: gabungan[k] = v
                    
                    # Pastikan AKSI terpasang
                    if base_aksi == "Tambah Penjualan":
                        gabungan["AKSI"] = "Tambah Penjualan"
                    elif not gabungan.get("AKSI"):
                        gabungan["AKSI"] = "Tambah Penjualan"

                    if structured_doc_mode:
                        for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN"]:
                            if context_pesan.get(k):
                                gabungan[k] = context_pesan[k]
                    else:
                        # Untuk batch natural-language, paksa konteks global yang lebih dapat dipercaya.
                        for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN", "STATUS"]:
                            if context_pesan.get(k):
                                gabungan[k] = context_pesan[k]

                        if context_pesan.get("NOMINAL_BAYAR") and str(gabungan.get("STATUS", "")).strip().lower() == "dicicil":
                            gabungan["NOMINAL_BAYAR"] = context_pesan["NOMINAL_BAYAR"]

                    if not gabungan.get("SATUAN") and gabungan.get("JUMLAH"):
                        m_sat = re.search(
                            r"\d+\s*(dus|pcs|toples|pack|bungkus|karton|bks|buah|botol|kg|bal|kantong|lusin|koli|roll|meter|lembar|box|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul|gelas|cup|can|sachet|pak|ctn|cen|cth)\b",
                            str(gabungan["JUMLAH"]),
                            re.IGNORECASE,
                        )
                        if m_sat:
                            gabungan["SATUAN"] = m_sat.group(1).lower()
                    
                    # Lookup harga otomatis untuk setiap item di multi-entry
                    if ctx.IS_DB_CONNECTED and gabungan.get("BARANG") and not gabungan.get("HARGA"):
                        lookup_start = perf_counter()
                        matches = cari_harga_default(
                            ctx.db_barang,
                            gabungan["BARANG"],
                            satuan_cari=gabungan.get("SATUAN"),
                            semua_barang=all_b,
                        )
                        lookup_total_ms += (perf_counter() - lookup_start) * 1000
                        if matches:
                            info_h = matches[0]
                            gabungan["HARGA"] = format_rupiah(info_h["harga"])
                            gabungan["SATUAN"] = info_h["satuan"]
                            if gabungan.get("JUMLAH"):
                                try:
                                    _m = re.search(r"\d+", str(gabungan["JUMLAH"]))
                                    if not _m:
                                        raise ValueError("Jumlah tidak valid")
                                    jml_n = int(_m.group())
                                    gabungan["TOTAL"] = format_rupiah(jml_n * info_h["harga"])
                                except: pass
                    
                    # Apply default date like single item does
                    aksi = gabungan.get("AKSI")
                    if not gabungan.get("TANGGAL") and not gabungan.get("SEMUA") and not (aksi == "Read Data" and gabungan.get("NAMA")):
                        gabungan["TANGGAL"] = datetime.now().strftime("%d-%m-%Y")
                    
                    item["entitas"] = gabungan

                sess.update({
                    "multi_results": valid_results,
                    "state": "pending_multi_insert"
                })
                if structured_doc_mode:
                    total_payment = int(sum(int(p.get("amount") or 0) for p in (structured_payment_entries or [])))
                    if total_payment > 0:
                        sess["multi_batch_payment_total"] = total_payment
                        sess["multi_batch_context"] = {
                            "STATUS": "Dicicil",
                            "NOMINAL_BAYAR": format_rupiah(total_payment),
                        }
                        for item in valid_results:
                            ent = item.get("entitas", {}) or {}
                            ent["STATUS"] = "Dicicil"
                            item["entitas"] = ent
                    else:
                        sess.pop("multi_batch_payment_total", None)
                        sess.pop("multi_batch_context", None)
                    sess.pop("ocr_payment_apply_plan", None)
                elif context_pesan:
                    sess["multi_batch_context"] = context_pesan.copy()
                    nominal_batch = parse_rupiah(context_pesan.get("NOMINAL_BAYAR") or 0)
                    if nominal_batch > 0 and str(context_pesan.get("STATUS", "")).strip().lower() == "dicicil":
                        sess["multi_batch_payment_total"] = nominal_batch
                    else:
                        sess.pop("multi_batch_payment_total", None)
                any_nama = any((it.get("entitas", {}) or {}).get("NAMA") for it in valid_results)
                if not any_nama:
                    sess["state"] = "awaiting_multi_nama"
                    sess["prompt_msg_id"] = msg_proses.message_id
                    msg = safe_edit_message(
                        bot,
                        "👤 <b>Siapa nama pemesan produk ini?</b>\n\nContoh: <code>Ritna</code>\n<i>Ketik 'batal' untuk membatalkan.</i>",
                        chat_id,
                        msg_proses.message_id,
                        parse_mode="HTML",
                    )
                    bot.register_next_step_handler(msg, _terima_multi_nama_pemesan)
                    return
                from services.ui_transaksi import susun_balasan_multi_resume
                logger.info(
                    "[Perf][chat] chat_id=%s lookup_harga_multi_ms=%.1f items=%s",
                    chat_id,
                    lookup_total_ms,
                    len(valid_results),
                )
                render_start = perf_counter()
                susun_balasan_multi_resume(chat_id, msg_proses.message_id)
                logger.info(
                    "[Perf][chat] chat_id=%s render_rekap_ms=%.1f total_ms=%.1f",
                    chat_id,
                    (perf_counter() - render_start) * 1000,
                    (perf_counter() - perf_total_start) * 1000,
                )
                return
            elif valid_results:
                results_nlp = valid_results

        hasil_nlp = results_nlp[0]
        entitas = hasil_nlp.get("entitas", {})
        intent = hasil_nlp.get("intent")
        aksi = entitas.get("AKSI")

        # --- SESSION MERGING (Interactive NLP) ---
        # Hanya merge jika aksi barunya tetap "Tambah Penjualan" atau belum ditentukan
        if user_sessions.get(chat_id, {}).get("state") in ["filling_missing_fields", "confirm_empty_submit"] and aksi in [None, "Tambah Penjualan"]:
            old_entitas = user_sessions[chat_id].get("entitas", {})
            for k, v in entitas.items():
                if v:
                    old_entitas[k] = v
            entitas = old_entitas
            entitas["AKSI"] = "Tambah Penjualan"
            # Reset state for re-validation
            user_sessions[chat_id]["state"] = "standby"
        else:
            # User beralih perintah (misal: dari input pesanan ke "tampilkan semua", "hapus", etc.)
            # Maka batalkan proses input sebelumnya and CLEAR ENTIRE SESSION entitas!
            user_sessions[chat_id]["state"] = "standby"
            entitas = {k: v for k, v in entitas.items() if v}  # Only keep new non-empty fields
            user_sessions[chat_id]["entitas"] = entitas

        # ── Auto-lookup harga dari Master Barang jika HARGA kosong (Kecuali jika ingin Set Harga) ──
        if ctx.IS_DB_CONNECTED and entitas.get("BARANG") and not entitas.get("HARGA") and entitas.get("AKSI") != "Set Harga Barang":
            lookup_start = perf_counter()
            matches = cari_harga_default(
                ctx.db_barang,
                entitas["BARANG"],
                satuan_cari=entitas.get("SATUAN"),
                semua_barang=all_b,
            )
            logger.info(
                "[Perf][chat] chat_id=%s lookup_harga_single_ms=%.1f",
                chat_id,
                (perf_counter() - lookup_start) * 1000,
            )
            if matches:
                info_harga = matches[0]
                entitas["HARGA"] = format_rupiah(info_harga["harga"])
                entitas["SATUAN"] = info_harga["satuan"]
                if len(matches) > 1:
                    user_sessions[chat_id]["multi_matches"] = matches

                if entitas.get("JUMLAH"):
                    try:
                        _m = re.search(r"\d+", str(entitas["JUMLAH"]))
                        if not _m:
                            raise ValueError("Jumlah tidak valid")
                        jml_num = int(_m.group())
                        entitas["TOTAL"] = format_rupiah(jml_num * info_harga["harga"])
                    except Exception:
                        pass
        else:
            if entitas.get("HARGA") and entitas.get("JUMLAH") and not entitas.get("TOTAL"):
                try:
                    _m = re.search(r"\d+", str(entitas["JUMLAH"]))
                    if not _m:
                        raise ValueError("Jumlah tidak valid")
                    jml_num = int(_m.group())
                    hrg_num = parse_rupiah(entitas["HARGA"])
                    entitas["TOTAL"] = format_rupiah(jml_num * hrg_num)
                except Exception:
                    pass

        # ✨ VALIDASI INTEGRITAS DATA (Cegah harga/jumlah 0)
        if entitas.get("AKSI") == "Tambah Penjualan":
            try:
                jml_val = 1
                if entitas.get("JUMLAH"):
                    jml_match = re.search(r"\d+", str(entitas["JUMLAH"]))
                    if jml_match: jml_val = int(jml_match.group())
                
                hrg_val = 0
                if entitas.get("HARGA"):
                    hrg_val = parse_rupiah(entitas["HARGA"])
                
                if jml_val <= 0:
                    safe_edit_message(bot, "⚠️ <b>Jumlah tidak valid.</b>\nJumlah barang harus lebih dari 0. Mohon perbaiki pesan Anda.", chat_id, msg_proses.message_id, parse_mode="HTML")
                    return
                
                # Jika harga 0 dan bukan barang bonus/gratis, beri peringatan
                if hrg_val <= 0 and "gratis" not in str(entitas.get("BARANG", "")).lower() and "bonus" not in str(entitas.get("BARANG", "")).lower():
                    # Kita tetap izinkan tapi beri peringatan di resume nanti
                    pass
            except Exception as e:
                logger.error(f"Error validating entities: {e}")

        # Simpan ke session — OVERWRITE entire entitas to remove old keys!
        sess = user_sessions.ensure(chat_id)
        sess["hasil_nlp"] = hasil_nlp
        # Only keep keys that are actually present in the NEW entitas (no old leftover fields!)
        new_entitas = {k: v for k, v in entitas.items() if v is not None and str(v).strip() != ""}
        sess["entitas"] = new_entitas

        # --- LOGIKA KHUSUS: PEMBAYARAN SETENGAH ---
        if entitas.get("NOMINAL_BAYAR") == "SETENGAH" and entitas.get("TOTAL"):
            try:
                total_val = parse_rupiah(entitas["TOTAL"])
                if total_val > 0:
                    setengah_val = total_val // 2
                    entitas["NOMINAL_BAYAR"] = format_rupiah(setengah_val)
                    entitas["STATUS"] = "Dicicil"
            except: pass

        intent = hasil_nlp.get("intent")
        aksi = entitas.get("AKSI")
        konteks_agregasi = entitas.get("KONTEKS_AGREGASI")

        # --- FALLBACK DEFAULT VALUES ---
        # Jika sedang mencari data (Read Data) dengan filter NAMA, jangan default ke hari ini
        # agar riwayat transaksi orang tersebut bisa tampil semua.
        if not entitas.get("TANGGAL") and not entitas.get("SEMUA") and not (aksi == "Read Data" and entitas.get("NAMA")):
            entitas["TANGGAL"] = datetime.now().strftime("%d-%m-%Y")
        if not entitas.get("STATUS") and entitas.get("NOMINAL_BAYAR"):
            _nom = parse_rupiah(entitas["NOMINAL_BAYAR"])
            _tot = parse_rupiah(entitas.get("TOTAL") or 0)
            if _nom > 0 and _nom < _tot:
                entitas["STATUS"] = "Cicil"
            elif _nom >= _tot and _tot > 0:
                entitas["STATUS"] = "Lunas"
        if not entitas.get("METODE_PEMBAYARAN") and entitas.get("STATUS") in ["Lunas", "Cicil", "LUNAS", "DICICIL"]:
            # Jika ada pembayaran tapi gak ada metode, default ke Tunai saja atau dibiarkan kosong untuk ditanya?
            pass

        # ✨ CHIT-CHAT: Sapaan / Hallo
        if intent == "Chit_Chat":
            pesan_panduan = (
                "👋 <b>Halo! Saya Bot Penjualan A&W Production.</b>\n\n"
                "Saya bisa membantu Anda mencatat penjualan, cek stok, dan dashboard keuangan.\n\n"
                "<b>Contoh Perintah:</b>\n"
                "• <i>\"Hari ini Budi ambil permen 2 dus lunas\"</i>\n"
                "• <i>\"Cek penjualan hari ini\"</i>\n"
                "• <i>\"Berapa harga permen?\"</i>\n"
                "• <i>\"Hapus pesanan Udin\"</i>\n\n"
                "Ketik perintah Anda atau gunakan tombol menu di bawah."
            )
            safe_edit_message(bot, pesan_panduan, chat_id, msg_proses.message_id, parse_mode="HTML")
            return

        # Import handler functions lazily to avoid circular imports
        from handlers.crud_transaksi import tangani_read_data, tangani_update_status, tangani_delete_data, tangani_catat_pelunasan
        from handlers.crud_barang import tangani_tambah_barang_chat, tangani_cek_harga_chat, tangani_set_harga_chat, tangani_hapus_barang_chat
        from handlers.command_handler import cmd_master_barang
        from services.ui_transaksi import susun_balasan_resume

        # ✨ DASHBOARD: Deteksi dashboard harian
        if konteks_agregasi == "Dashboard Harian":
            tgl_nlp = entitas.get("TANGGAL")
            hari_ini = datetime.now().strftime("%d-%m-%Y")
            if tgl_nlp and tgl_nlp != hari_ini:
                tangani_dashboard_custom_date(bot, chat_id, msg_proses.message_id, ctx.db_transaksi, tgl_nlp)
            else:
                tangani_dashboard_harian(bot, chat_id, msg_proses.message_id, ctx.db_transaksi)
        elif aksi == "Tambah Barang":
            tangani_tambah_barang_chat(chat_id, msg_proses.message_id)
        elif aksi == "Cek Harga Barang":
            tangani_cek_harga_chat(chat_id, msg_proses.message_id)
        elif aksi == "Set Harga Barang":
            tangani_set_harga_chat(chat_id, msg_proses.message_id)
        elif aksi == "Hapus Barang":
            tangani_hapus_barang_chat(chat_id, msg_proses.message_id)
        elif aksi == "Master Data Menu":
            cmd_master_barang(message)
            try: bot.delete_message(chat_id, msg_proses.message_id)
            except: pass
        elif aksi == "Catat Pelunasan":
            tangani_catat_pelunasan(chat_id, msg_proses.message_id)
        elif aksi == "Update Status":
            tangani_update_status(chat_id, msg_proses.message_id)
        elif aksi == "Read Data":
            tangani_read_data(chat_id, msg_proses.message_id)
        elif aksi == "Delete Data":
            tangani_delete_data(chat_id, msg_proses.message_id)
        elif aksi == "Tambah Penjualan":
            # --- VALIDASI FIELD WAJIB ---
            field_wajib = ["TANGGAL", "NAMA", "BARANG", "JUMLAH", "TOTAL", "STATUS", "METODE_PEMBAYARAN"]
            missing = [f for f in field_wajib if not entitas.get(f)]
            
            if missing:
                user_sessions[chat_id]["state"] = "pending_confirmation"
                susun_balasan_resume(chat_id, msg_proses.message_id)
            else:
                susun_balasan_resume(chat_id, msg_proses.message_id, is_expert=True)
        else:
            susun_balasan_resume(chat_id, msg_proses.message_id)
    except Exception as e:
        log_exception("Error teks prosesor", e)
        notify_admins(f"❌ <b>Error Text Handler</b>\nUser: <code>{user_id}</code>\nChat: <code>{chat_id}</code>\nPesan: <code>{str(e)[:200]}</code>")
        bot.reply_to(message, "❌ Terjadi error saat memproses pesan. Coba ketik ulang perintahnya.")


def register_handlers(bot):
    """Register text handler ke bot instance."""
    bot.message_handler(content_types=['text'])(authorized_only(handle_text_message))
