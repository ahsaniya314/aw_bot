"""
Command Handlers — /start, /help, /dashboard, /master_barang, /master_metode
"""
import os
import logging
import ipaddress
from datetime import datetime
from urllib.parse import urlparse
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.bot_context import ctx
from utils.security import authorized_only, safe_edit_message
from handlers.handler_dashboard import tangani_dashboard_harian

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


GUIDE_PAGES = {
    "guide_home": (
        "📘 <b>PANDUAN AW PRODUCTION</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Bot ini dipakai untuk mencatat, mencari, dan mengecek transaksi penjualan secara cepat.\n\n"
        "Topik utama:\n"
        "• Input penjualan via teks atau foto\n"
        "• Cari pesanan & riwayat transaksi\n"
        "• Cek hutang dan catat pelunasan\n"
        "• Kelola barang dan satuan\n"
        "• Buka dashboard web\n\n"
        "💡 <i>Tips:</i> Ketik <code>menu</code> kapan saja untuk kembali ke menu utama."
    ),
    "guide_input": (
        "📝 <b>PANDUAN INPUT PENJUALAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Sistem menerima input penjualan dengan bahasa natural.\n\n"
        "Contoh:\n"
        "• <code>Pak Andi ambil willo 5 karton lunas tunai</code>\n"
        "• <code>Udin ambil brownis 10 bungkus dicicil 200000 tf</code>\n\n"
        "Kriteria data yang paling baik:\n"
        "• Ada <b>nama pelanggan</b>\n"
        "• Ada <b>barang</b>\n"
        "• Ada <b>jumlah + satuan</b>\n"
        "• Jika dicicil, sertakan <b>nominal bayar</b> dan metode\n\n"
        "Jika ada field yang kurang, bot akan menampilkan tombol untuk melengkapi data."
    ),
    "guide_ocr": (
        "📷 <b>PANDUAN OCR (FOTO)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Gunakan foto nota/catatan jika ingin input transaksi lebih cepat.\n\n"
        "Agar pembacaan akurat:\n"
        "• Foto terang dan tidak blur\n"
        "• Tulisan tanggal terlihat jelas\n"
        "• Nama pelanggan dipisah dari daftar barang\n"
        "• Nominal cicilan/pelunasan ditulis tegas, mis. <code>bayar cicilan: 300000</code>\n\n"
        "Contoh format yang bagus:\n"
        "• <code>20-06-2026</code>\n"
        "• <code>Nama: Budi Budis</code>\n"
        "• <code>Willo 10 karton</code>\n"
        "• <code>bayar cicilan: 300000</code>\n\n"
        "Jika hasil OCR belum tepat, gunakan tombol edit sebelum data diproses."
    ),
    "guide_search": (
        "🔎 <b>PANDUAN CARI & RIWAYAT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Gunakan <b>Cari Pesanan</b> untuk mencari transaksi tertentu.\n"
        "Gunakan <b>Riwayat</b> untuk menampilkan daftar transaksi sesuai filter.\n\n"
        "Contoh pencarian yang didukung:\n"
        "• <code>pak andi</code>\n"
        "• <code>willo</code>\n"
        "• <code>20-06-2026</code>\n"
        "• <code>hari ini</code>\n\n"
        "Jika muncul form pencarian nama, cukup balas nama pelanggan lalu bot akan memuat hasilnya."
    ),
    "guide_dashboard": (
        "🌐 <b>PANDUAN DASBOR WEB</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Menu <b>Dasbor Web</b> membuka dashboard melalui link web.\n\n"
        "Fungsi utamanya:\n"
        "• Ringkasan omzet\n"
        "• Uang masuk dan tagihan\n"
        "• Rekap transaksi per tanggal\n"
        "• Pemantauan performa penjualan\n\n"
        "Jika link tidak terbuka, periksa URL publik dashboard pada server."
    ),
    "guide_barang": (
        "📦 <b>PANDUAN KELOLA BARANG</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Gunakan menu <b>Kelola Barang</b> untuk:\n"
        "• Lihat daftar\n"
        "• Tambah barang & harga\n"
        "• Edit harga\n"
        "• Hapus barang\n\n"
        "Semakin rapi master barang, semakin akurat pencarian harga default dan hasil OCR."
    ),
    "guide_satuan": (
        "📐 <b>PANDUAN KELOLA SATUAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Gunakan menu <b>Kelola Satuan</b> untuk menambah atau merapikan satuan barang.\n\n"
        "Contoh satuan yang umum:\n"
        "• <code>pcs</code>\n"
        "• <code>bungkus</code>\n"
        "• <code>karton</code>\n"
        "• <code>dus</code>\n\n"
        "Satuan yang konsisten membantu bot menghitung total dan mencocokkan harga dengan benar."
    ),
    "guide_hutang": (
        "💰 <b>PANDUAN HUTANG & PELUNASAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Contoh cek hutang:\n"
        "• <code>apa yang belum lunas</code>\n"
        "• <code>siapa yang masih hutang</code>\n"
        "• <code>cek hutang budi budis</code>\n\n"
        "Contoh pelunasan:\n"
        "• <code>Budi Budis bayar hutang 300000 cash</code>\n"
        "• <code>Budi Budis bayar cicilan 300000 transfer</code>\n\n"
        "Untuk OCR, tulis jelas seperti:\n"
        "• <code>Nama: Budi Budis</code>\n"
        "• <code>bayar cicilan: 300000</code>"
    ),
    "guide_troubleshoot": (
        "🧯 <b>TIPS PEMAKAIAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "• Jika tombol tidak merespons, ketik <code>menu</code>.\n"
        "• Jika riwayat tidak keluar, pastikan nama pelanggan benar.\n"
        "• Jika OCR salah baca, kirim foto lebih terang dan lurus.\n"
        "• Jika total tidak muncul, cek harga barang dan satuannya.\n"
        "• Jika mode offline, koneksi database perlu diperiksa."
    )
}


def build_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    # Row 1: Fast Inputs
    markup.add(
        InlineKeyboardButton("📝 Catat (Teks)", callback_data="quick_input_text"),
        InlineKeyboardButton("📷 Catat (Foto)", callback_data="quick_input_ocr")
    )
    # Row 2: Search and Dashboard
    dashboard_web_btn = build_dashboard_web_button()
    if dashboard_web_btn:
        markup.add(
            InlineKeyboardButton("🔍 Cari Transaksi", callback_data="quick_search_menu"),
            dashboard_web_btn,
        )
    else:
        markup.add(
            InlineKeyboardButton("🔍 Cari Transaksi", callback_data="quick_search_menu"),
            InlineKeyboardButton("📊 Dashboard Bot", callback_data="dashboard_refresh")
        )
    # Row 3: History and Debts
    markup.add(
        InlineKeyboardButton("📑 Riwayat", callback_data="read_all_transaksi"),
        InlineKeyboardButton("💰 Cek Hutang", callback_data="read_filter_hutang")
    )
    # Row 4: Master Settings
    markup.add(
        InlineKeyboardButton("📦 Kelola Barang", callback_data="mb_list"),
        InlineKeyboardButton("📐 Kelola Satuan", callback_data="ms_menu")
    )
    markup.add(
        InlineKeyboardButton("💳 Metode Bayar", callback_data="mm_list")
    )
    # Row 5: Guides and Help
    markup.add(
        InlineKeyboardButton("📘 Panduan", callback_data="help_guide"),
        InlineKeyboardButton("❓ Bantuan", callback_data="quick_help")
    )
    # Row 6: Actions
    markup.row(InlineKeyboardButton("❌ Tutup Menu", callback_data="btn_buang"))
    return markup


def build_reply_keyboard():
    from telebot.types import ReplyKeyboardMarkup, KeyboardButton
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📘 Panduan"),
        KeyboardButton("🔎 Cari Pesanan")
    )
    markup.add(
        KeyboardButton("📑 Riwayat"),
        KeyboardButton("🌐 Dasbor Web")
    )
    markup.add(
        KeyboardButton("💰 Cek Hutang"),
        KeyboardButton("📐 Kelola Satuan")
    )
    markup.add(KeyboardButton("📦 Kelola Barang"))
    return markup


def build_guide_markup(active_key="guide_home"):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🏠 Utama", callback_data="guide_home"),
        InlineKeyboardButton("📝 Input", callback_data="guide_input")
    )
    markup.add(
        InlineKeyboardButton("📷 OCR", callback_data="guide_ocr"),
        InlineKeyboardButton("🔎 Cari", callback_data="guide_search")
    )
    markup.add(
        InlineKeyboardButton("💰 Hutang", callback_data="guide_hutang"),
        InlineKeyboardButton("🌐 Dasbor", callback_data="guide_dashboard")
    )
    markup.add(
        InlineKeyboardButton("📦 Barang", callback_data="guide_barang"),
        InlineKeyboardButton("📐 Satuan", callback_data="guide_satuan")
    )
    markup.row(InlineKeyboardButton("🧯 Tips", callback_data="guide_troubleshoot"))
    markup.add(
        InlineKeyboardButton("🏠 Menu", callback_data="menu_main"),
        InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
    )
    return markup


def build_menu_text():
    status_db = "🟢 Online (Connected)" if ctx.IS_DB_CONNECTED else "🔴 Offline"
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return (
        "⚡ <b>KASIR PINTAR AW PRODUCTION</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🖥️ <b>Status Database:</b> <b>{status_db}</b>\n"
        f"🕒 <b>Update:</b> <code>{current_time}</code>\n\n"
        "Gunakan tombol di bawah untuk:\n"
        "• membuka panduan\n"
        "• mencari pesanan dan riwayat\n"
        "• mengecek hutang pelanggan\n"
        "• membuka dasbor web\n"
        "• mengelola barang dan satuan"
    )


def build_guide_page_text(page_key):
    return GUIDE_PAGES.get(page_key, GUIDE_PAGES["guide_home"])


def send_welcome(message):
    """Command /start dan /help - Show welcome message with premium UI"""
    bot = ctx.bot
    user_id = message.from_user.id
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    if not ctx.rate_limiter.is_allowed(user_id):
        logger.warning(f"Rate limit exceeded untuk user {user_id}")
        bot.reply_to(message, "⏱️ <b>Terlalu banyak request.</b>\nMohon tunggu sebentar...", parse_mode="HTML")
        return

    logger.info(f"User {user_id} (chat {chat_id}) gunakan /start atau /help")

    teks_sapaan = f"""👋 <b>Halo, {first_name}!</b>

Selamat datang di <b>AW Production Bot</b>.

Bot ini membantu Anda untuk:
• mencari pesanan pelanggan
• melihat riwayat transaksi
• mengecek hutang dan pelunasan
• membuka dasbor web
• mengelola barang dan satuan

📘 Gunakan tombol <b>Panduan</b> jika ingin melihat format input yang benar.
"""
    reply_markup = build_reply_keyboard()
    bot.send_message(chat_id, teks_sapaan, parse_mode="HTML", reply_markup=reply_markup)


def cmd_menu(message):
    bot = ctx.bot
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not ctx.rate_limiter.is_allowed(user_id):
        bot.reply_to(message, "⏱️ <b>Terlalu banyak request.</b>\nMohon tunggu sebentar...", parse_mode="HTML")
        return
    
    # Tampilkan menu utama langsung
    reply_markup = build_reply_keyboard()
    bot.send_message(chat_id, build_menu_text(), parse_mode="HTML", reply_markup=reply_markup)


def cmd_panduan(message):
    bot = ctx.bot
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not ctx.rate_limiter.is_allowed(user_id):
        bot.reply_to(message, "⏱️ <b>Terlalu banyak request.</b>\nMohon tunggu sebentar...", parse_mode="HTML")
        return
    bot.send_message(chat_id, build_guide_page_text("guide_home"), parse_mode="HTML", reply_markup=build_guide_markup("guide_home"))


def cmd_dashboard(message):
    """Command untuk menampilkan dashboard harian"""
    bot = ctx.bot
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not ctx.rate_limiter.is_allowed(user_id):
        logger.warning(f"Rate limit exceeded untuk user {user_id} pada /dashboard")
        bot.reply_to(message, "⏱️ Terlalu banyak request. Tunggu sebentar...")
        return

    logger.info(f"User {user_id} gunakan /dashboard")

    if not ctx.IS_DB_CONNECTED:
        logger.error(f"Database tidak terhubung, user {user_id} tidak bisa akses dashboard")
        bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return

    try:
        msg_loading = bot.reply_to(message, "⏳ Memuat dashboard...")
        tangani_dashboard_harian(bot, chat_id, msg_loading.message_id, ctx.db_transaksi)
    except Exception as e:
        logger.error(f"Error pada /dashboard user {user_id}: {e}")
        bot.reply_to(message, f"❌ Error membuka dashboard: {str(e)[:100]}")


def cmd_master_barang(message):
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline aktif, tidak bisa akses Master Barang.")
        return
    teks = (
        "🛒 <b>MASTER DATA BARANG</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Kelola daftar barang & harga default Anda."
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📋 Lihat Daftar",  callback_data="mb_list"),
        InlineKeyboardButton("➕ Tambah Baru",   callback_data="mb_tambah"),
        InlineKeyboardButton("✏️ Edit Harga",    callback_data="mb_edit"),
        InlineKeyboardButton("🗑️ Hapus Barang",  callback_data="mb_hapus"),
    )
    markup.add(
        InlineKeyboardButton("❌ Batal / Tutup",  callback_data="btn_buang"),
    )
    bot.reply_to(message, teks, parse_mode="HTML", reply_markup=markup)


def cmd_master_metode(message):
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline aktif.")
        return
    teks = (
        "🏦 <b>MASTER METODE PEMBAYARAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Kelola daftar metode pembayaran."
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📋 Lihat Daftar",   callback_data="mm_list"),
        InlineKeyboardButton("➕ Tambah Baru",    callback_data="mm_tambah"),
        InlineKeyboardButton("✏️ Edit Keyword",   callback_data="mm_edit"),
        InlineKeyboardButton("🗑️ Hapus Metode",   callback_data="mm_hapus"),
    )
    bot.reply_to(message, teks, parse_mode="HTML", reply_markup=markup)


def cmd_master_satuan(message):
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline aktif.")
        return
    teks = (
        "📐 <b>MASTER SATUAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Kelola daftar satuan (pcs, bungkus, karton, dll)."
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📋 Lihat Daftar",   callback_data="ms_list"),
        InlineKeyboardButton("➕ Tambah Baru",    callback_data="ms_tambah"),
        InlineKeyboardButton("✏️ Edit Satuan",    callback_data="ms_edit"),
        InlineKeyboardButton("🗑️ Hapus Satuan",   callback_data="ms_hapus"),
    )
    markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
    bot.reply_to(message, teks, parse_mode="HTML", reply_markup=markup)


def cmd_dedup_transaksi(message):
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline aktif.")
        return

    try:
        from database import db_client
        rows = db_client.get_semua_transaksi_db()
        dup_ids = db_client.find_adjacent_duplicate_transaksi_ids(rows)
        if not dup_ids:
            bot.reply_to(message, "✅ Tidak ada duplikat terdeteksi.")
            return

        sess = ctx.user_sessions.ensure(chat_id)
        sess["dedup_transaksi_ids"] = dup_ids

        teks = (
            "🧹 <b>BERSIHKAN DUPLIKAT TRANSAKSI</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Ditemukan <b>{len(dup_ids)}</b> transaksi duplikat (identik & berurutan).\n\n"
            "Klik tombol di bawah untuk menghapus duplikat."
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(f"🧹 Hapus ({len(dup_ids)})", callback_data="trx_dedup_yes"),
            InlineKeyboardButton("❌ Batal", callback_data="trx_dedup_no"),
        )
        bot.reply_to(message, teks, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"❌ Gagal memindai duplikat: {str(e)[:120]}")


def set_bot_commands(bot):
    """Mengatur daftar commands yang muncul di Menu Button (tombol biru di sebelah kiri kolom chat).
    Semua fungsi Reply Keyboard lama sudah dipindahkan ke sini."""
    from telebot.types import BotCommand
    commands = [
        BotCommand("menu", "🏠 Menu Utama"),
        BotCommand("catat", "📝 Catat Penjualan"),
        BotCommand("foto", "📷 Catat via Foto (OCR)"),
        BotCommand("dashboard", "📊 Dashboard Penjualan"),
        BotCommand("cari", "🔍 Cari Transaksi"),
        BotCommand("riwayat", "📑 Riwayat Transaksi"),
        BotCommand("hutang", "💰 Cek Hutang Pelanggan"),
        BotCommand("master_barang", "📦 Kelola Data Barang"),
        BotCommand("master_satuan", "📐 Kelola Satuan"),
        BotCommand("master_metode", "💳 Kelola Metode Bayar"),
        BotCommand("panduan", "📘 Panduan & Bantuan"),
        BotCommand("help", "❓ Bantuan Langsung"),
    ]
    try:
        bot.set_my_commands(commands)
        logger.info("[INIT] Daftar commands berhasil diatur!")
    except Exception as e:
        logger.warning(f"[INIT] Gagal mengatur daftar commands: {e}")


def cmd_catat(message):
    """Command /catat — shortcut untuk catat penjualan via teks."""
    bot = ctx.bot
    chat_id = message.chat.id
    
    teks = (
        "✍️ <b>PENCATATAN TRANSAKSI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Silakan pilih metode input transaksi di bawah ini:\n\n"
        "📝 <b>Teks:</b> Ketik manual detail pesanan secara fleksibel.\n"
        "📷 <b>Foto:</b> Kirim foto nota/struk, bot akan membaca otomatis."
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📝 Catat via Teks", callback_data="quick_input_text"),
        InlineKeyboardButton("📷 Catat via Foto (OCR)", callback_data="quick_input_ocr")
    )
    markup.add(
        InlineKeyboardButton("🔍 Cari Transaksi", callback_data="quick_search_menu"),
        InlineKeyboardButton("🏠 Menu Utama", callback_data="menu_main")
    )
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)


def cmd_foto(message):
    """Command /foto — shortcut untuk input via foto OCR."""
    bot = ctx.bot
    chat_id = message.chat.id
    teks = (
        "📸 <b>INPUT TRANSAKSI VIA FOTO (OCR)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Silakan kirimkan foto nota/struk/list pesanan Anda.\n\n"
        "✨ <b>Tips Hasil Terbaik:</b>\n"
        "1. Pastikan foto cukup terang & tulisan terbaca jelas.\n"
        "2. Ambil foto secara tegak lurus (tidak miring).\n\n"
        "<i>Asisten AI akan memproses & mengekstrak data pesanan otomatis.</i>"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📘 Pelajari Tips OCR", callback_data="guide_ocr"),
        InlineKeyboardButton("📝 Catat via Teks", callback_data="quick_input_text")
    )
    markup.add(
        InlineKeyboardButton("🏠 Menu Utama", callback_data="menu_main"),
        InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
    )
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)


def cmd_cari(message):
    """Command /cari — shortcut untuk cari pesanan."""
    bot = ctx.bot
    chat_id = message.chat.id
    teks = (
        "🔍 <b>PENCARIAN TRANSAKSI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Pilih kriteria pencarian transaksi di bawah ini untuk mempermudah menemukan data:"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("👤 Cari Nama", callback_data="quick_search_name"),
        InlineKeyboardButton("📅 Cari Tanggal", callback_data="quick_search_date"),
    )
    markup.add(
        InlineKeyboardButton("📦 Cari Barang", callback_data="quick_search_barang"),
        InlineKeyboardButton("💳 Cari Status Bayar", callback_data="quick_search_status"),
    )
    markup.add(
        InlineKeyboardButton("📑 Riwayat Lengkap", callback_data="read_all_transaksi"),
        InlineKeyboardButton("💰 Khusus Hutang", callback_data="read_filter_hutang"),
    )
    markup.add(
        InlineKeyboardButton("🏠 Menu Utama", callback_data="menu_main"),
        InlineKeyboardButton("❌ Tutup", callback_data="btn_buang")
    )
    bot.send_message(chat_id, teks, parse_mode="HTML", reply_markup=markup)


def cmd_riwayat(message):
    """Command /riwayat — shortcut untuk riwayat transaksi."""
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "SEMUA": True}
    msg_proses = bot.reply_to(message, "⏳ Memuat riwayat transaksi...")
    from handlers.crud_transaksi import tangani_read_data
    tangani_read_data(chat_id, msg_proses.message_id)


def cmd_hutang(message):
    """Command /hutang — shortcut untuk cek hutang."""
    bot = ctx.bot
    chat_id = message.chat.id
    if not ctx.IS_DB_CONNECTED:
        bot.reply_to(message, "❌ Mode Offline: Tidak dapat mengakses data.")
        return
    sess = ctx.user_sessions.ensure(chat_id)
    sess["entitas"] = {"AKSI": "Read Data", "STATUS": "Hutang", "KONTEKS_AGREGASI": "Summary Jatuh Tempo"}
    msg_proses = bot.reply_to(message, "⏳ Memuat daftar hutang...")
    from handlers.crud_transaksi import tangani_read_data
    tangani_read_data(chat_id, msg_proses.message_id)


def register_handlers(bot):
    """Register semua command handlers ke bot instance."""
    try:
        bot.delete_my_commands()
        from telebot.types import MenuButtonDefault
        bot.set_chat_menu_button(menu_button=MenuButtonDefault(type="default"))
        logger.info("[OK] Bot commands dan menu button berhasil dihapus!")
    except Exception as e:
        logger.warning(f"[WARNING] Gagal hapus bot commands/menu: {e}")
    
    bot.message_handler(commands=['start', 'help'])(authorized_only(send_welcome))
    bot.message_handler(commands=['menu'])(authorized_only(cmd_menu))
    bot.message_handler(commands=['catat'])(authorized_only(cmd_catat))
    bot.message_handler(commands=['foto'])(authorized_only(cmd_foto))
    bot.message_handler(commands=['cari'])(authorized_only(cmd_cari))
    bot.message_handler(commands=['riwayat'])(authorized_only(cmd_riwayat))
    bot.message_handler(commands=['hutang'])(authorized_only(cmd_hutang))
    bot.message_handler(commands=['panduan', 'guide'])(authorized_only(cmd_panduan))
    bot.message_handler(commands=['dashboard'])(authorized_only(cmd_dashboard))
    bot.message_handler(commands=['master_barang'])(cmd_master_barang)
    bot.message_handler(commands=['master_satuan'])(cmd_master_satuan)
    bot.message_handler(commands=['master_metode'])(cmd_master_metode)
    bot.message_handler(commands=['dedup_transaksi'])(authorized_only(cmd_dedup_transaksi))
