"""
CRUD Transaksi — read, delete, update, pelunasan, revisi manual, simpan multi
"""
import logging
import math
import re
from datetime import datetime

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.bot_context import ctx
from core.master_data import (
    cari_harga_default,
    format_rupiah,
    get_all_barang,
    normalisasi_tanggal_gs,
    parse_rupiah,
)
from database import db_client
from services.cache_manager import get_cached_barang, get_cached_metode
from services.debt_tracker import cari_hutang_aktif, hitung_sisa_tagihan, proses_bayar_tambahan
from services.ui_pengaturan import tampilkan_pilihan_barang
from services.ui_transaksi import (
    apply_batch_financials,
    kirim_halaman_read,
    susun_balasan_multi_resume,
    susun_balasan_resume,
    susun_balasan_update,
    tampilkan_menu_kriteria_edit,
)
from utils.helpers import bersihkan_nama, cocokkan_nama, hitung_ulang_total_dinamis
from utils.security import safe_debug_event, safe_edit_message

logger = logging.getLogger("bot_logger")


def _normalize_metode_pembayaran(value):
    s = str(value or "").strip().lower()
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    tokens = set(s.split(" "))
    if "transfer" in tokens or "tf" in tokens or "trf" in tokens:
        return "Transfer"
    if "tunai" in tokens or "cash" in tokens or "kontan" in tokens:
        return "Tunai"
    if "qris" in tokens:
        return "QRIS"
    return s.title()


def tangani_read_data(chat_id, message_id_target):
    if chat_id not in ctx.user_sessions:
        return
    sess = ctx.user_sessions[chat_id]
    entitas = sess.get("entitas", {})

    f_nama = entitas.get("NAMA")
    f_tanggal = entitas.get("TANGGAL")
    f_status = entitas.get("STATUS")
    f_barang = entitas.get("BARANG")
    f_harga = entitas.get("HARGA")  # Ambil filter harga
    f_metode = entitas.get("METODE_PEMBAYARAN")  # Filter Metode
    f_semua = entitas.get("SEMUA")
    konteks_agregasi = entitas.get("KONTEKS_AGREGASI")

    if not (
        f_nama
        or f_tanggal
        or f_status
        or f_barang
        or f_semua
        or f_harga
        or f_metode
        or konteks_agregasi
    ):
        safe_edit_message(
            ctx.bot,
            "🔍 Mohon lebih spesifik, siapakah atau kapan pesanan yang Anda cari? (Contoh: <i>Cek pesanan pak andi</i> atau <i>tampilkan semua transaksi</i>) ",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    if not ctx.IS_DB_CONNECTED:
        safe_edit_message(
            ctx.bot,
            "❌ Gagal Mengakses: Mode Offline aktif.",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    safe_edit_message(
        ctx.bot,
        f"🔍 Mencari data di Database dengan parameter (Nama: {f_nama or '-'}, Tgl: {f_tanggal or '-'}, Status: {f_status or '-'}, Brg: {f_barang or '-'}, Harga: {f_harga or '-'}, Metode: {f_metode or '-'}) ...",
        chat_id=chat_id,
        message_id=message_id_target,
    )

    def _extract_qty(value):
        try:
            m = re.search(r"\d+", str(value or ""))
            return int(m.group()) if m else 0
        except Exception:
            return 0

    def _build_read_match_item(r):
        total_raw = float(r.get("total", 0) or 0)
        tagihan_raw = float(r.get("tagihan", 0) or 0)
        uang_masuk_raw = float(r.get("uang_masuk", 0) or 0)
        paid_by_tagihan = max(0, total_raw - tagihan_raw)
        uang_masuk_eff = max(uang_masuk_raw, paid_by_tagihan)
        if uang_masuk_eff > total_raw:
            uang_masuk_eff = total_raw

        jumlah_raw = _extract_qty(r.get("jumlah_satuan", ""))
        return {
            "Tgl": r.get("tanggal", ""),
            "Nama": r.get("nama_pelanggan", ""),
            "Brg": r.get("barang", ""),
            "Jml": str(r.get("jumlah_satuan", "")),
            "Harga": format_rupiah(r.get("harga", 0)),
            "Total": format_rupiah(total_raw),
            "Status": r.get("status", ""),
            "Metode": r.get("metode_pembayaran", ""),
            "Tagihan": format_rupiah(tagihan_raw),
            "UangMasuk": format_rupiah(uang_masuk_eff),
            "_jumlah_raw": jumlah_raw,
            "_total_raw": int(total_raw),
            "_tagihan_raw": int(tagihan_raw),
            "_uang_masuk_raw": int(uang_masuk_eff),
        }

    try:
        cols_transaksi = "id,tanggal,nama_pelanggan,barang,jumlah_satuan,harga,total,status,metode_pembayaran,tagihan,uang_masuk"
        filters = []
        filters_no_date = []
        if f_nama:
            f = {"kolom": "nama_pelanggan", "nilai": f_nama, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)
        date_exact = False
        if f_tanggal:
            if len(f_tanggal) == 7 and "-" in f_tanggal:
                filters.append({"kolom": "tanggal", "nilai": f_tanggal, "operator": "ilike"})
            else:
                date_exact = True
                ddmm = str(f_tanggal)[:5]
                filters.append({"kolom": "tanggal", "nilai": ddmm, "operator": "ilike"})
        if f_status:
            s_cari = str(f_status).lower()
            if s_cari == "hutang":
                f = {"kolom": "tagihan", "nilai": 0, "operator": "gt"}
                filters.append(f)
                filters_no_date.append(f)
            elif s_cari == "lunas":
                f = {"kolom": "status", "nilai": "lunas", "operator": "ilike"}
                filters.append(f)
                filters_no_date.append(f)
            else:
                f = {"kolom": "status", "nilai": f_status, "operator": "ilike"}
                filters.append(f)
                filters_no_date.append(f)
        if f_barang:
            f = {"kolom": "barang", "nilai": f_barang, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)
        if f_harga:
            f_harga_num = parse_rupiah(f_harga)
            f = {"kolom": "harga", "nilai": f_harga_num, "operator": "eq"}
            filters.append(f)
            filters_no_date.append(f)
        if f_metode:
            f = {"kolom": "metode_pembayaran", "nilai": f_metode, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)
        if entitas.get("SATUAN"):
            f = {"kolom": "jumlah_satuan", "nilai": entitas.get("SATUAN"), "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)

        if filters:
            raw_data = db_client.get_transaksi_multi_filter(filters, columns=cols_transaksi)
        else:
            raw_data = db_client.get_semua_transaksi_db(columns=cols_transaksi)

        match_list = []
        for r in raw_data:
            if date_exact:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue
            match_list.append(_build_read_match_item(r))
            # Tetap simpan mapping untuk kompatibilitas jika masih ada fungsi lama
            ctx.db_transaksi.row_mapping[len(match_list)] = r["id"]

        if date_exact and f_tanggal and len(match_list) == 0:
            raw_data = (
                db_client.get_transaksi_multi_filter(filters_no_date, columns=cols_transaksi)
                if filters_no_date
                else db_client.get_semua_transaksi_db(columns=cols_transaksi)
            )
            for r in raw_data:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue
                match_list.append(_build_read_match_item(r))
                ctx.db_transaksi.row_mapping[len(match_list)] = r["id"]

    except Exception as e:
        safe_edit_message(
            ctx.bot,
            f"❌ Gagal memindai database: {e}",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    if len(match_list) == 0:
        debug_info = f"\n\n<i>(Debug: Tgl={f_tanggal or 'Semua'}, Status={f_status or 'Semua'}, Nama={f_nama or 'Semua'})</i>"
        if (
            date_exact
            and f_tanggal
            and len(str(f_tanggal)) >= 10
            and str(f_tanggal)[2] == "-"
            and str(f_tanggal)[5] == "-"
        ):
            ddmm = str(f_tanggal)[:5]
            by_date = {}
            kandidat = raw_data or []
            for r in kandidat:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if tgl_db and tgl_db.startswith(ddmm) and tgl_db != f_tanggal:
                    by_date[tgl_db] = by_date.get(tgl_db, 0) + 1
            if by_date:
                opsi = sorted(by_date.items(), key=lambda x: x[0], reverse=True)[:5]
                rekom_date, rekom_count = opsi[0]
                teks = (
                    f"📭 <b>Data tidak ditemukan</b> untuk tanggal <code>{f_tanggal}</code>.\n\n"
                    f"Tapi saya menemukan data di tanggal yang mirip:\n"
                    + "\n".join([f"• <code>{d}</code> ({c} data)" for d, c in opsi])
                    + "\n\nKlik tombol di bawah untuk membuka yang paling mendekati."
                    + debug_info
                )
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(
                    InlineKeyboardButton(
                        f"Tampilkan {rekom_date} ({rekom_count} data)",
                        callback_data=f"read_date_{rekom_date}",
                    )
                )
                markup.add(InlineKeyboardButton("❌ Tutup", callback_data="btn_buang"))
                safe_edit_message(
                    ctx.bot,
                    teks,
                    chat_id=chat_id,
                    message_id=message_id_target,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
                del ctx.user_sessions[chat_id]
                return

        safe_edit_message(
            ctx.bot,
            f"📭 <b>Data tidak ditemukan.</b>\nPastikan kriteria pencarian Anda sudah benar.{debug_info}",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    total_pages = math.ceil(len(match_list) / ctx.ITEM_PER_PAGE)

    # ==========================
    # AGREGASI HITUNGAN (DASHBOARD)
    # ==========================
    ringkasan_teks = ""
    if konteks_agregasi:
        total_omzet = 0  # Kolom F (Total Transaksi)
        total_uang_msk = 0  # Kolom J (Uang Masuk)
        total_tagihan = 0  # Kolom I (Sisa Tagihan)
        total_item = 0
        pelanggan_stats = {}  # {nama: {"total": 0, "item": 0, "count": 0, "tagihan": 0}}
        status_stats = {
            "Lunas": {"count": 0, "total": 0},
            "Dicicil": {"count": 0, "total": 0},
            "Hutang": {"count": 0, "total": 0},
        }

        for item in match_list:
            j_val = int(item.get("_jumlah_raw", 0) or 0)
            o_val = int(item.get("_total_raw", 0) or 0)
            t_val = int(item.get("_tagihan_raw", 0) or 0)
            uang_masuk_eff = int(item.get("_uang_masuk_raw", 0) or 0)

            total_item += j_val
            total_omzet += o_val
            total_tagihan += t_val
            total_uang_msk += uang_masuk_eff

            # 5. Hitung Breakdown Status
            st_raw = item["Status"].lower()
            if "lunas" in st_raw:
                status_stats["Lunas"]["count"] += 1
                status_stats["Lunas"]["total"] += o_val
            elif any(k in st_raw for k in ["cicil", "dp"]):
                status_stats["Dicicil"]["count"] += 1
                status_stats["Dicicil"]["total"] += o_val
            else:
                status_stats["Hutang"]["count"] += 1
                status_stats["Hutang"]["total"] += o_val

            # Hitung stats per pelanggan untuk fitur "Terbanyak"
            nama_p = item["Nama"]
            if nama_p not in pelanggan_stats:
                pelanggan_stats[nama_p] = {"total": 0, "item": 0, "count": 0, "tagihan": 0}
            pelanggan_stats[nama_p]["total"] += o_val
            pelanggan_stats[nama_p]["item"] += j_val
            pelanggan_stats[nama_p]["count"] += 1
            pelanggan_stats[nama_p]["tagihan"] += t_val

        top_name = (
            max(pelanggan_stats, key=lambda k: pelanggan_stats[k]["total"])
            if pelanggan_stats
            else None
        )

        # --- LOGIKA KHUSUS: TAGIHAN PER ORANG (Spesifik) ---
        if f_nama and konteks_agregasi in ["Total Tunggakan", "Total Transaksi"] and not f_semua:
            ringkasan_teks = f"👤 <b>LAPORAN TAGIHAN: {f_nama.upper()}</b>\n"
            ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"

            # Gunakan pencocokan nama yang lebih fleksibel daripada dictionary key lookup langsung
            stats = None
            for p_nama, p_stats in pelanggan_stats.items():
                if cocokkan_nama(f_nama, p_nama):
                    stats = p_stats
                    f_nama = p_nama  # Gunakan nama resmi dari DB untuk judul
                    break

            if stats:
                ringkasan_teks += (
                    f"⚠️ <b>Total Hutang:</b> <code>{format_rupiah(stats['tagihan'])}</code>\n"
                )
                ringkasan_teks += f"💸 <b>Sudah Dibayar:</b> <code>{format_rupiah(stats['total'] - stats['tagihan'])}</code>\n"
                ringkasan_teks += (
                    f"📦 <b>Total Pesanan:</b> {stats['item']} Item ({stats['count']} Nota)\n"
                )
                ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"

                if stats["tagihan"] > 0:
                    ringkasan_teks += "💡 <i>Gunakan tombol di bawah untuk mencatat pelunasan.</i>\n"
                else:
                    ringkasan_teks += "✅ <b>STATUS: SEMUA LUNAS</b>\n"
            else:
                ringkasan_teks += "📭 <i>Tidak ada riwayat transaksi ditemukan.</i>\n"

        else:
            ringkasan_teks = "📊 <b>DASHBOARD ANALITIK PENJUALAN</b> 📊\n"

            if (
                f_tanggal
                or f_semua
                or f_status
                or f_barang
                or f_metode
                or (konteks_agregasi and konteks_agregasi != "Tunggakan Terbanyak")
            ):
                ringkasan_teks += f"📅 <b>LAPORAN ({f_tanggal or 'Hari Ini'})</b>\n"
                ringkasan_teks += (
                    f"💰 <b>Omzet Kotor:</b> <code>{format_rupiah(total_omzet)}</code>\n"
                )
                ringkasan_teks += (
                    f"💸 <b>Uang Masuk:</b> <code>{format_rupiah(total_uang_msk)}</code>\n"
                )
                ringkasan_teks += (
                    f"⚠️ <b>Sisa Tagihan:</b> <code>{format_rupiah(total_tagihan)}</code>\n"
                )
                ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"
                ringkasan_teks += "📋 <b>BREAKDOWN STATUS</b>\n"
                for s, val in status_stats.items():
                    ringkasan_teks += (
                        f"• {s}: {val['count']} Trx (<code>{format_rupiah(val['total'])}</code>)\n"
                    )

                if top_name:
                    ringkasan_teks += f"🏆 <b>Top Buyer:</b> {top_name}\n"

                ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"

                # Tampilkan TOP Pelanggan jika ada
                ringkasan_teks += f"👤 <b>TOP PELANGGAN (Berdasarkan Nominal)</b>\n"
                for i, (nama, stats) in enumerate(list(pelanggan_stats.items())[:5], 1):
                    medali = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "👤"
                    ringkasan_teks += f"{medali} <b>{nama}</b>: <code>{format_rupiah(stats['total'])}</code> ({stats['count']} trx)\n"

                ringkasan_teks += f"\n📈 <b>Total Akumulasi Filter</b>\n"
                ringkasan_teks += (
                    f"💰 <b>Total Uang:</b> <code>{format_rupiah(total_omzet)}</code>\n"
                )
                ringkasan_teks += f"📦 <b>Total Item:</b> {total_item}\n"

        if konteks_agregasi in ["Total Tunggakan", "Tunggakan Terbanyak"]:
            ringkasan_teks += f"\n🏦 <b>LAPORAN PIUTANG / TAGIHAN</b>\n"
            ringkasan_teks += (
                f"⚠️ <b>Total Sisa Tagihan:</b> <code>{format_rupiah(total_tagihan)}</code>\n"
            )
            ringkasan_teks += (
                f"💸 <b>Total Uang Masuk:</b> <code>{format_rupiah(total_uang_msk)}</code>\n"
            )
            ringkasan_teks += f"📦 <b>Total Item Terkait:</b> {total_item}\n"
            ringkasan_teks += f"👥 <b>Jumlah Debitur:</b> {len(pelanggan_stats)}\n"

            if konteks_agregasi == "Tunggakan Terbanyak":
                ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"
                ringkasan_teks += "🔴 <b>TOP PENUNGGAK (Piutang Terbesar)</b>\n"
                # Urutkan berdasarkan tagihan terbesar
                top_debitors = sorted(
                    pelanggan_stats.items(), key=lambda x: x[1]["tagihan"], reverse=True
                )
                for i, (nama, stats) in enumerate(top_debitors[:10], 1):
                    ringkasan_teks += (
                        f"{i}. <b>{nama}</b>: <code>{format_rupiah(stats['tagihan'])}</code>\n"
                    )
        elif konteks_agregasi == "Summary Uang Masuk" or konteks_agregasi == "Uang Masuk":
            ringkasan_teks += f"📥 <b>LAPORAN UANG MASUK (KAS)</b>\n"
            ringkasan_teks += (
                f"💰 <b>Total Uang Masuk:</b> <code>{format_rupiah(total_uang_msk)}</code>\n"
            )
            ringkasan_teks += (
                f"📉 <b>Sisa Piutang:</b> <code>{format_rupiah(total_tagihan)}</code>\n"
            )
            ringkasan_teks += f"📑 <b>Total Nota Terproses:</b> {len(match_list)}\n"
        elif konteks_agregasi == "Summary Omzet" or konteks_agregasi == "Total Transaksi":
            ringkasan_teks += f"📈 <b>LAPORAN HASIL PENJUALAN</b>\n"
            ringkasan_teks += (
                f"💰 <b>Total Omzet (Kotor):</b> <code>{format_rupiah(total_omzet)}</code>\n"
            )
            ringkasan_teks += (
                f"💵 <b>Total Uang Masuk:</b> <code>{format_rupiah(total_uang_msk)}</code>\n"
            )
            ringkasan_teks += f"📦 <b>Total Item Terjual:</b> {total_item}\n"
        elif konteks_agregasi == "Summary Barang":
            ringkasan_teks += f"📦 <b>LAPORAN PESANAN BARANG</b>\n"
            ringkasan_teks += f"🛒 <b>Total Volume:</b> {total_item} Item\n"
            ringkasan_teks += f"💰 <b>Nilai Barang:</b> <code>{format_rupiah(total_omzet)}</code>\n"
            ringkasan_teks += f"📑 <b>Jumlah Baris:</b> {len(match_list)}\n"
        elif konteks_agregasi == "Summary Total Barang":
            ringkasan_teks += f"📦 <b>TOTAL BARANG TERJUAL</b>\n"
            ringkasan_teks += f"🛒 <b>Volume Keluar:</b> {total_item} Item\n"
            ringkasan_teks += f"📅 <b>Periode:</b> {f_tanggal or 'Semua Waktu'}\n"
        elif konteks_agregasi == "Summary Lunas":
            ringkasan_teks += f"✅ <b>LAPORAN TRANSAKSI LUNAS</b>\n"
            ringkasan_teks += (
                f"💰 <b>Total Uang Masuk:</b> <code>{format_rupiah(total_uang_msk)}</code>\n"
            )
            ringkasan_teks += f"📑 <b>Jumlah Nota Lunas:</b> {len(match_list)}\n"
            ringkasan_teks += f"📦 <b>Total Volume:</b> {total_item} Item\n"
        elif konteks_agregasi == "Summary Jatuh Tempo":
            ringkasan_teks += f"⏰ <b>PENGINGAT JATUH TEMPO</b>\n"
            ringkasan_teks += (
                f"⚠️ <b>Total Tagihan:</b> <code>{format_rupiah(total_tagihan)}</code>\n"
            )
            ringkasan_teks += f"👥 <b>Jumlah Debitur:</b> {len(pelanggan_stats)}\n"
            ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n"
            for nama, stats in pelanggan_stats.items():
                ringkasan_teks += (
                    f"👤 <b>{nama}</b>: <code>{format_rupiah(stats['tagihan'])}</code>\n"
                )

    ringkasan_teks += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    ctx.user_sessions[chat_id]["action"] = "reading_pagination"
    ctx.user_sessions[chat_id]["data_list"] = match_list
    ctx.user_sessions[chat_id]["current_page"] = 1
    ctx.user_sessions[chat_id]["total_pages"] = total_pages
    ctx.user_sessions[chat_id]["ringkasan_teks"] = ringkasan_teks
    ctx.user_sessions[chat_id]["konteks_agregasi"] = konteks_agregasi

    kirim_halaman_read(chat_id, 1, message_id_target)


def tangani_delete_data(chat_id, message_id_target):
    if chat_id not in ctx.user_sessions:
        return
    sess = ctx.user_sessions[chat_id]
    entitas = sess.get("entitas", {})

    f_nama = entitas.get("NAMA")
    f_tanggal = entitas.get("TANGGAL")
    f_barang = entitas.get("BARANG")
    f_semua = entitas.get("SEMUA")

    if not (f_nama or f_tanggal or f_barang or f_semua):
        safe_edit_message(
            ctx.bot,
            "❌ Gagal, mohon sebutkan kriteria spesifik (nama/tanggal/barang) atau perintah <b>'hapus semua data'</b>.",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    if not ctx.IS_DB_CONNECTED:
        safe_edit_message(
            ctx.bot,
            "❌ Gagal Mengakses: Mode Offline aktif.",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    safe_edit_message(
        ctx.bot,
        f"🗑️ Mencari data dengan parameter (Nama: {f_nama or '-'}, Tgl: {f_tanggal or '-'}, Brg: {f_barang or '-'}, Semua: {f_semua or '-'}) untuk dihapus...",
        chat_id=chat_id,
        message_id=message_id_target,
    )

    try:
        cols_transaksi = "id,tanggal,nama_pelanggan,barang,jumlah_satuan,harga,total,status,metode_pembayaran,tagihan,uang_masuk"
        filters = []
        filters_no_date = []
        date_exact = False
        if f_nama:
            f = {"kolom": "nama_pelanggan", "nilai": f_nama, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)
        if f_tanggal:
            if len(f_tanggal) == 7 and "-" in f_tanggal:
                filters.append({"kolom": "tanggal", "nilai": f_tanggal, "operator": "ilike"})
            else:
                date_exact = True
                ddmm = str(f_tanggal)[:5]
                filters.append({"kolom": "tanggal", "nilai": ddmm, "operator": "ilike"})
        if f_barang:
            f = {"kolom": "barang", "nilai": f_barang, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)

        if filters:
            raw_data = db_client.get_transaksi_multi_filter(filters, columns=cols_transaksi)
        else:
            raw_data = db_client.get_semua_transaksi_db(columns=cols_transaksi)

        match_list = []
        for r in raw_data:
            if date_exact:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue
            nama_gs = r.get("nama_pelanggan", "")
            tgl_gs = r.get("tanggal", "")
            barang_gs = r.get("barang", "")

            row = [
                tgl_gs,
                nama_gs,
                barang_gs,
                str(r.get("jumlah_satuan", "")),
                str(r.get("harga", 0)),
                str(r.get("total", 0)),
                r.get("status", ""),
                r.get("metode_pembayaran", ""),
                str(r.get("tagihan", 0)),
                str(r.get("uang_masuk", 0)),
            ]
            match_list.append(
                {
                    "row_index": r["id"],
                    "nama": nama_gs,
                    "barang": barang_gs,
                    "tanggal": tgl_gs,
                    "row_full": row,
                }
            )
            # Simpan mapping ID untuk operasi delete
            ctx.db_transaksi.row_mapping[r["id"]] = r["id"]

        if date_exact and f_tanggal and len(match_list) == 0:
            raw_data = (
                db_client.get_transaksi_multi_filter(filters_no_date, columns=cols_transaksi)
                if filters_no_date
                else db_client.get_semua_transaksi_db(columns=cols_transaksi)
            )
            for r in raw_data:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue
                nama_gs = r.get("nama_pelanggan", "")
                tgl_gs = r.get("tanggal", "")
                barang_gs = r.get("barang", "")

                row = [
                    tgl_gs,
                    nama_gs,
                    barang_gs,
                    str(r.get("jumlah_satuan", "")),
                    str(r.get("harga", 0)),
                    str(r.get("total", 0)),
                    r.get("status", ""),
                    r.get("metode_pembayaran", ""),
                    str(r.get("tagihan", 0)),
                    str(r.get("uang_masuk", 0)),
                ]
                match_list.append(
                    {
                        "row_index": r["id"],
                        "nama": nama_gs,
                        "barang": barang_gs,
                        "tanggal": tgl_gs,
                        "row_full": row,
                    }
                )
                ctx.db_transaksi.row_mapping[r["id"]] = r["id"]

    except Exception as e:
        safe_edit_message(
            ctx.bot,
            f"❌ Gagal memindai database: {e}",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    if len(match_list) == 0:
        safe_edit_message(
            ctx.bot,
            f"❌ Tidak ditemukan data penjualan yang sesuai dengan kriteria penghapusan tersebut.",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
    elif len(match_list) == 1:
        siapkan_konfirmasi_delete(chat_id, message_id_target, match_list[0])
    else:
        if f_semua or len(match_list) > 10:
            siapkan_konfirmasi_delete_masal(chat_id, message_id_target, match_list)
        else:
            teks_konflik = (
                f"🗑️ <b>KONFIRMASI PENGHAPUSAN DATA</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Ditemukan <b>{len(match_list)} data</b> yang cocok.\n"
                f"Pilih nomor data yang ingin dihapus:\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            markup = InlineKeyboardMarkup(row_width=3)
            buttons = []

            for i, ml in enumerate(match_list, start=1):
                row = ml["row_full"]
                tgl = row[0] if len(row) > 0 else "-"
                nama = row[1] if len(row) > 1 else "-"
                brg = row[2] if len(row) > 2 else "-"
                jml = row[3] if len(row) > 3 else "-"
                harga = row[4] if len(row) > 4 else "-"
                total = row[5] if len(row) > 5 else "-"
                status = row[6] if len(row) > 6 else "-"
                metode = row[7] if len(row) > 7 else "-"

                status_emoji = (
                    "✅"
                    if "lunas" in str(status).lower()
                    else "⏳"
                    if any(k in str(status).lower() for k in ["cicil", "dicicil", "dp"])
                    else "🔴"
                )

                teks_konflik += (
                    f"┌─── <b>[{i}] {nama}</b> ───\n"
                    f"│ 📅 Tanggal  : {tgl}\n"
                    f"│ 📦 Barang    : {jml} {brg}\n"
                    f"│ 💰 Harga     : {harga}\n"
                    f"│ 💵 Total      : {total}\n"
                    f"│ {status_emoji} Status    : {status}\n"
                    f"│ 🏦 Metode   : {metode}\n"
                    f"└────────────────\n\n"
                )
                buttons.append(
                    InlineKeyboardButton(
                        f"🗑️ Hapus #{i}", callback_data=f"delres_{ml['row_index']}"
                    )
                )

            sess["hapus_data"] = match_list
            markup.add(*buttons)
            markup.row(
                InlineKeyboardButton(
                    "💣 Hapus Semua Terdeteksi", callback_data="btn_delete_bulk_trigger"
                )
            )
            markup.add(InlineKeyboardButton("❌ Batalkan Semua", callback_data="btn_buang"))

            safe_edit_message(
                ctx.bot,
                teks_konflik,
                chat_id=chat_id,
                message_id=message_id_target,
                parse_mode="HTML",
                reply_markup=markup,
            )


def siapkan_konfirmasi_delete(chat_id, message_id_target, info_row):
    sess = ctx.user_sessions[chat_id]
    sess["delete_target_row"] = info_row["row_index"]

    row = info_row["row_full"]

    balasan = (
        f"⚠️ <b>PERINGATAN PENGHAPUSAN PERMANEN</b> ⚠️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Apakah Anda yakin ingin menghapus data penjualan berikut?\n\n"
        f"👤 <b>Nama:</b> {row[1]}\n"
        f"📦 <b>Detail:</b> {row[3]} {row[2]}\n"
        f"📅 <b>Tanggal:</b> {row[0]}\n\n"
        f"🚨 <i>Tindakan ini tidak bisa dibatalkan dari sistem.</i>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ya, Hapus!", callback_data="btn_delete_yes"),
        InlineKeyboardButton("❌ Tidak, Batalkan", callback_data="btn_delete_no"),
    )

    safe_edit_message(
        ctx.bot,
        balasan,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )


def siapkan_konfirmasi_delete_masal(chat_id, message_id_target, match_list):
    sess = ctx.user_sessions[chat_id]
    ent = sess.get("entitas", {})
    # Urutkan secara descending agar penghapusan via indeks tidak menggeser indeks target lainnya
    row_indices = sorted([ml["row_index"] for ml in match_list], reverse=True)
    sess["delete_masal_rows"] = row_indices
    sess["delete_masal_count"] = len(match_list)

    kriteria = []
    if ent.get("NAMA"):
        kriteria.append(f"Nama: {ent['NAMA']}")
    if ent.get("TANGGAL"):
        kriteria.append(f"Tgl: {ent['TANGGAL']}")
    if ent.get("BARANG"):
        kriteria.append(f"Brg: {ent['BARANG']}")

    kriteria_str = ", ".join(kriteria) if kriteria else "Seluruh Data"

    balasan = (
        f"⚠️ <b>KONFIRMASI PENGHAPUSAN MASAL</b> ⚠️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Kriteria: <b>{kriteria_str}</b>\n"
        f"Jumlah Terdeteksi: <b>{len(match_list)} data</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Apakah Anda yakin ingin menghapus <b>SEMUA</b> data tersebut?\n\n"
        f"🚨 <i>Tindakan ini permanen dan tidak bisa dibatalkan.</i>"
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💣 Ya, Hapus Semua!", callback_data="btn_delete_masal_yes"),
        InlineKeyboardButton("❌ Tidak, Batalkan", callback_data="btn_delete_no"),
    )

    safe_edit_message(
        ctx.bot,
        balasan,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )


def siapkan_konfirmasi_update(chat_id, message_id_target, info_row):
    sess = ctx.user_sessions[chat_id]
    sess["is_update_mode"] = True
    sess["update_target_row"] = info_row["row_index"]

    row = info_row["row_full"]
    ent_nlp = sess["entitas"]

    # Merge Strategy: Pertahankan original data dari Database (terutama nama),
    # lalu timpa dengan ekstraksi NLP jika ada (untuk Harga, Jumlah, Status).
    new_tgl = ent_nlp.get("TANGGAL") or row[0]
    new_nama = row[1]  # Selalu gunakan nama database aslinya agar tidak rusak
    new_brg = ent_nlp.get("BARANG") or row[2]
    new_jml = ent_nlp.get("JUMLAH") or row[3]
    new_harga = ent_nlp.get("HARGA") or row[4]

    # Ambil nominal bayar dari NLP jika ada
    nominal_nlp = ent_nlp.get("NOMINAL_BAYAR")

    # Logika Status: Jika ada nominal baru, otomatis ubah Hutang -> Dicicil
    status_raw = ent_nlp.get("STATUS") or row[6]
    if nominal_nlp is not None and status_raw in ("Hutang", "Belum Lunas", "Unset"):
        new_status = "Dicicil"
    else:
        new_status = status_raw

    new_metode = ent_nlp.get("METODE_PEMBAYARAN") or (row[7] if len(row) > 7 else "-")

    # === FITUR BARU: AUTO-PRICE LOOKUP SAAT GANTI BARANG ===
    # Jika barang diubah, cari harga barunya di Master Data
    if ent_nlp.get("BARANG") and ent_nlp.get("BARANG").lower() != row[2].lower():
        # Cari di ctx.db_barang
        matches = cari_harga_default(ctx.db_barang, new_brg)
        if matches:
            new_harga = format_rupiah(matches[0]["harga"])
            ctx.bot.send_message(
                chat_id,
                f"💰 Produk diubah ke <b>{new_brg}</b>. Harga otomatis disesuaikan ke <code>{new_harga}</code>.",
                parse_mode="HTML",
            )
        else:
            ctx.bot.send_message(
                chat_id,
                f"⚠️ Harga untuk <b>{new_brg}</b> tidak ditemukan di Master Data. Menggunakan harga lama.",
                parse_mode="HTML",
            )

    # Kalkulasi ulang total jika diperlukan (jika jumlah atau harga diganti)
    try:
        j_num = int(re.sub(r"[^\d]", "", str(new_jml))) if new_jml else 0
        h_num = int(re.sub(r"[^\d]", "", str(new_harga))) if new_harga else 0
        if j_num > 0 and h_num > 0:
            new_total = format_rupiah(j_num * h_num)
        else:
            new_total = row[5]  # Fallback
    except:
        new_total = row[5]

    # Akumulasi Uang Masuk: Jika ada nominal baru di NLP, tambahkan ke nilai lama di database
    try:
        uang_masuk_lama = parse_rupiah(row[9]) if len(row) > 9 else 0
    except:
        uang_masuk_lama = 0

    if nominal_nlp is not None:
        # User menyebutkan nominal baru -> Tambahkan ke akumulasi lama
        new_nominal = uang_masuk_lama + parse_rupiah(nominal_nlp)
    else:
        # User tidak menyebutkan nominal -> Tetap gunakan nilai lama
        new_nominal = uang_masuk_lama

    sess["entitas"] = {
        "TANGGAL": new_tgl,
        "NAMA": new_nama,
        "BARANG": new_brg,
        "JUMLAH": new_jml,
        "HARGA": new_harga,
        "TOTAL": new_total,
        "STATUS": new_status,
        "METODE_PEMBAYARAN": new_metode,
        "NOMINAL_BAYAR": nominal_nlp,  # Simpan input aslinya dulu
    }

    # Simpan rincian untuk kalkulasi dinamis di summary
    sess["update_info"] = {
        "uang_masuk_lama": uang_masuk_lama,
        "nominal_baru": parse_rupiah(nominal_nlp) if nominal_nlp else 0,
        "status_awal": row[6],
    }

    safe_edit_message(
        ctx.bot, "🔄 Mempersiapkan Data...", chat_id=chat_id, message_id=message_id_target
    )
    susun_balasan_update(chat_id, message_id_target)


def tangani_catat_pelunasan(chat_id, message_id_target):
    """Flow utama saat NLP mendeteksi aksi 'Catat Pelunasan'."""
    if chat_id not in ctx.user_sessions:
        return
    sess = ctx.user_sessions[chat_id]
    entitas = sess.get("entitas", {})

    f_nama = entitas.get("NAMA")
    f_nominal = entitas.get("NOMINAL_BAYAR")

    if not f_nama:
        safe_edit_message(
            ctx.bot,
            "❓ Mohon sebutkan nama pelanggan yang ingin dicatat pembayarannya.\n"
            "<i>Contoh: <code>tambahan bayar pak andi 50rb</code></i>",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    if not ctx.IS_DB_CONNECTED:
        safe_edit_message(
            ctx.bot, "❌ Mode Offline aktif.", chat_id=chat_id, message_id=message_id_target
        )
        del ctx.user_sessions[chat_id]
        return

    safe_edit_message(
        ctx.bot,
        f"🔍 Mencari hutang aktif atas nama <b>{f_nama}</b>...",
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
    )

    hutang_list = cari_hutang_aktif(ctx.db_transaksi, f_nama, cocokkan_nama)

    if not hutang_list:
        # Try using the same approach as tangani_read_data to find any transactions for this name
        import logging

        logger = logging.getLogger("bot_logger")
        logger.info("[DEBUG] cari_hutang_aktif found nothing, trying read data approach")

        try:
            filters = []
            filters_no_date = []
            date_exact = False

            # Add name filter
            if f_nama:
                f = {"kolom": "nama_pelanggan", "nilai": f_nama, "operator": "ilike"}
                filters.append(f)
                filters_no_date.append(f)

            logger.info(f"[DEBUG] Using filters: {filters}")
            raw_data = (
                db_client.get_transaksi_multi_filter(filters)
                if filters
                else db_client.get_semua_transaksi_db()
            )

            match_list = []
            for r in raw_data:
                nama_gs = r.get("nama_pelanggan", "")
                if not cocokkan_nama(f_nama, nama_gs):
                    continue

                tgl_gs = r.get("tanggal", "")
                barang_gs = r.get("barang", "")
                status_gs = r.get("status", "").lower()

                total_raw = float(r.get("total", 0) or 0)
                tagihan_raw = float(r.get("tagihan", 0) or 0)
                uang_masuk_raw = float(r.get("uang_masuk", 0) or 0)

                # Calculate tagihan if not set
                if tagihan_raw <= 0 and status_gs in ["hutang", "dicicil", "belum lunas"]:
                    tagihan_raw = max(0, total_raw - uang_masuk_raw)

                if tagihan_raw <= 0:
                    continue

                logger.info(
                    f"[DEBUG] Found candidate transaction: id={r['id']}, nama={nama_gs}, tagihan={tagihan_raw}"
                )

                match_list.append(
                    {
                        "row_index": r["id"],
                        "nama": nama_gs,
                        "barang": barang_gs,
                        "tanggal": tgl_gs,
                        "total": format_rupiah(r.get("total", 0)),
                        "tagihan": tagihan_raw,
                        "tagihan_str": format_rupiah(tagihan_raw),
                        "uang_masuk": uang_masuk_raw,
                        "uang_masuk_str": format_rupiah(uang_masuk_raw),
                        "status": r.get("status", ""),
                        "metode": r.get("metode_pembayaran", "-"),
                        "row_full": r,
                    }
                )

            hutang_list = match_list
            logger.info(f"[DEBUG] Found {len(hutang_list)} transactions via read data approach")

        except Exception as e:
            logger.error(f"[DEBUG] Error in read data approach: {e}")

    if not hutang_list:
        safe_edit_message(
            ctx.bot,
            f"❌ Tidak ditemukan sisa tagihan aktif atas nama <b>{f_nama}</b>.",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    sess["hutang_list"] = hutang_list
    sess["nominal_bayar"] = f_nominal

    if len(hutang_list) == 1:
        # Langsung ke konfirmasi
        _tampilkan_konfirmasi_pelunasan(chat_id, message_id_target, hutang_list[0], f_nominal)
    else:
        # Tampilkan pilihan nota
        teks = (
            f"⚠️ Ditemukan <b>{len(hutang_list)} nota aktif</b> atas nama <b>{f_nama}</b>.\n"
            "Pilih nota mana yang ingin dibayar:\n\n"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        for i, h in enumerate(hutang_list):
            teks += (
                f"<b>[{i+1}]</b> {h['tanggal']} | {h['barang']} | "
                f"Sisa: <code>{h['tagihan_str']}</code>\n"
            )
            markup.add(
                InlineKeyboardButton(
                    f"[{i+1}] {h['barang']} — Tagihan {h['tagihan_str']}",
                    callback_data=f"pel_pilih_{h['row_index']}",
                )
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="btn_buang"))
        safe_edit_message(
            ctx.bot,
            teks,
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
            reply_markup=markup,
        )


def _tampilkan_konfirmasi_pelunasan(chat_id, message_id_target, info_hutang, nominal_bayar):
    """Tampilkan kartu konfirmasi sebelum mencatat pembayaran."""
    sess = ctx.user_sessions[chat_id]
    sess["pel_row_idx"] = info_hutang["row_index"]
    sess["pel_nama"] = info_hutang["nama"]

    tagihan_lama = info_hutang["tagihan"]
    nom_val = parse_rupiah(nominal_bayar) if nominal_bayar else 0

    if nom_val > 0:
        tagihan_baru = max(0, tagihan_lama - nom_val)
        status_ket = (
            "Lunas ✅" if tagihan_baru == 0 else f"Nyicil ⏳ (tagihan {format_rupiah(tagihan_baru)})"
        )
        ket_bayar = format_rupiah(nom_val)
        sess["pel_nominal"] = nom_val
    else:
        # Anggap pelunasan penuh
        tagihan_baru = 0
        status_ket = "Lunas ✅"
        ket_bayar = format_rupiah(tagihan_lama) + " (pelunasan penuh)"
        sess["pel_nominal"] = tagihan_lama

    sess["pel_tagihan_baru"] = tagihan_baru

    balasan = (
        "💰 <b>KONFIRMASI PEMBAYARAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Nama:</b> {info_hutang['nama']}\n"
        f"📦 <b>Barang:</b> {info_hutang['barang']}\n"
        f"📅 <b>Tgl Transaksi:</b> {info_hutang['tanggal']}\n"
        f"💵 <b>Total Transaksi:</b> <code>{info_hutang['total']}</code>\n"
        f"🔴 <b>Jumlah Tagihan:</b> <code>{info_hutang['tagihan_str']}</code>\n"
        f"💚 <b>Sudah Dibayar:</b> <code>{info_hutang['uang_masuk_str']}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Bayar Sekarang:</b> <code>{ket_bayar}</code>\n"
        f"📊 <b>Status Baru:</b> {status_ket}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Konfirmasi pembayaran ini?</i>"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ya, Catat!", callback_data="pel_konfirm_ya"),
        InlineKeyboardButton("❌ Batal", callback_data="btn_buang"),
    )
    safe_edit_message(
        ctx.bot,
        balasan,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )


def tangani_revisi_manual(message):
    """Intercept ketika user mengetik String Manual untuk memperbaiki kesalahan NLP"""
    chat_id = message.chat.id

    # Verifikasi keselamatan session memory
    if (
        chat_id not in ctx.user_sessions
        or ctx.user_sessions[chat_id].get("state") != "awaiting_edit_teks"
    ):
        # Jika gagal atau session kedaluwarsa jatuh disini
        return

    sess = ctx.user_sessions[chat_id]
    entitas = sess["entitas"]
    target_field = sess["field_target"]
    msg_lama_id = sess["summary_msg_id"]

    # 1. Update Parameter dengan ketikan baru!!
    if target_field == "NOMINAL_BAYAR" and sess.get("is_update_mode"):
        # Jangan dijumlahkan dulu, simpan sebagai input baru
        input_val = parse_rupiah(message.text)
        if "update_info" not in sess:
            sess["update_info"] = {}
        sess["update_info"]["nominal_baru"] = input_val
        entitas["NOMINAL_BAYAR"] = input_val  # Simpan aslinya agar preview bekerja

        # Auto-promote status jika dari Hutang
        if entitas.get("STATUS") in ("Hutang", "Belum Lunas", "Unset"):
            entitas["STATUS"] = "Dicicil"
    else:
        # Field lain bersifat menimpa (overwrite)
        if target_field == "METODE_PEMBAYARAN":
            entitas[target_field] = _normalize_metode_pembayaran(message.text)
        else:
            entitas[target_field] = message.text

    # 2. Cerdas! Lakukan Otomatisasi Perhitungan Ulang Kalkulator Jika harga/jumlah berubah
    if target_field == "BARANG":
        # === FITUR BARU: AUTO-PRICE LOOKUP SAAT GANTI BARANG VIA EDIT ===
        new_brg = message.text
        matches = cari_harga_default(ctx.db_barang, new_brg, satuan_cari=entitas.get("SATUAN"))
        if len(matches) == 1:
            h_m = matches[0]
            entitas["BARANG"] = h_m["nama"]  # Gunakan nama resmi dari DB
            entitas["HARGA"] = format_rupiah(h_m["harga"])
            entitas["SATUAN"] = h_m["satuan"]
            hitung_ulang_total_dinamis(entitas)
            sess["edit_notice"] = f"Harga disesuaikan ke <code>{entitas['HARGA']}</code>."
        elif len(matches) > 1:
            # Sediakan pilihan
            tampilkan_pilihan_barang(chat_id, msg_lama_id, matches)
            return
        else:
            sess["edit_notice"] = f"Barang <b>{new_brg}</b> tidak ditemukan di Master Data."

    elif target_field == "SATUAN":
        # === FITUR BARU: AUTO-PRICE LOOKUP SAAT GANTI SATUAN VIA EDIT ===
        new_sat = message.text.strip()
        brg_ref = entitas.get("BARANG")
        if brg_ref:
            matches = cari_harga_default(ctx.db_barang, brg_ref, satuan_cari=new_sat)
            if matches:
                h_m = matches[0]
                entitas["HARGA"] = format_rupiah(h_m["harga"])
                entitas["SATUAN"] = h_m["satuan"]
                sess[
                    "edit_notice"
                ] = f"Harga otomatis berubah ke <code>{entitas['HARGA']}</code> ({h_m['satuan']})."
            else:
                sess[
                    "edit_notice"
                ] = f"Satuan <b>{new_sat}</b> untuk <b>{brg_ref}</b> tidak ditemukan di Master Data."

    if target_field in ["JUMLAH", "HARGA", "SATUAN"]:
        hitung_ulang_total_dinamis(entitas)

    # 3. Lempar Kembali View menjadi layaknya semua selesai
    if sess.get("is_update_mode"):
        susun_balasan_update(chat_id, msg_lama_id)
    else:
        susun_balasan_resume(chat_id, msg_lama_id)

    # Note Tambahan: Jika mau pesan user (message) dihapus agar rapi
    try:
        # Menghapus Teks Ketikan Pengguna sebagai cleaning
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass


def tangani_revisi_manual_multi(message):
    """Terima input revisi manual untuk mode Edit Batch (multi_results)."""
    chat_id = message.chat.id

    if (
        chat_id not in ctx.user_sessions
        or ctx.user_sessions[chat_id].get("state") != "awaiting_edit_teks_multi"
    ):
        return

    sess = ctx.user_sessions[chat_id]
    msg_lama_id = sess.get("summary_msg_id")
    target_field = sess.get("field_target")
    idx = sess.get("multi_edit_index")

    if idx is None or "multi_results" not in sess:
        return

    try:
        idx = int(idx)
    except Exception:
        return

    results = sess.get("multi_results") or []
    if idx < 0 or idx >= len(results):
        return

    entitas = results[idx].get("entitas", {}) or {}
    input_text = (message.text or "").strip()
    if not input_text:
        sess["edit_notice"] = "Nilai kosong diabaikan."
        susun_balasan_multi_resume(chat_id, msg_lama_id)
        return

    if target_field == "METODE_PEMBAYARAN":
        input_text = _normalize_metode_pembayaran(input_text)

    if target_field:
        entitas[target_field] = input_text

    if target_field == "BARANG":
        matches = cari_harga_default(ctx.db_barang, input_text, satuan_cari=entitas.get("SATUAN"))
        if len(matches) == 1:
            h_m = matches[0]
            entitas["BARANG"] = h_m["nama"]
            entitas["HARGA"] = format_rupiah(h_m["harga"])
            entitas["SATUAN"] = h_m["satuan"]
            hitung_ulang_total_dinamis(entitas)
            sess[
                "edit_notice"
            ] = f"Item #{idx+1}: harga disesuaikan ke <code>{entitas['HARGA']}</code>."
        elif len(matches) > 1 and msg_lama_id:
            sess["multi_edit_index"] = idx
            tampilkan_pilihan_barang(
                chat_id, msg_lama_id, matches, callback_prefix=f"multi_pick_brg_{idx}"
            )
            return
        else:
            sess[
                "edit_notice"
            ] = f"Item #{idx+1}: barang <b>{input_text}</b> tidak ditemukan di Master."

    elif target_field == "SATUAN":
        brg_ref = entitas.get("BARANG")
        if brg_ref:
            matches = cari_harga_default(ctx.db_barang, brg_ref, satuan_cari=input_text)
            if matches:
                h_m = matches[0]
                entitas["HARGA"] = format_rupiah(h_m["harga"])
                entitas["SATUAN"] = h_m["satuan"]
                hitung_ulang_total_dinamis(entitas)
                sess[
                    "edit_notice"
                ] = f"Item #{idx+1}: harga berubah ke <code>{entitas['HARGA']}</code> ({h_m['satuan']})."
            else:
                sess[
                    "edit_notice"
                ] = f"Item #{idx+1}: satuan <b>{input_text}</b> tidak ada untuk <b>{brg_ref}</b>."

    elif target_field in ["JUMLAH", "HARGA", "TOTAL"]:
        hitung_ulang_total_dinamis(entitas)

    results[idx]["entitas"] = entitas
    sess["multi_results"] = results
    sess["state"] = "editing_menu_multi"

    if msg_lama_id:
        susun_balasan_multi_resume(chat_id, msg_lama_id)

    try:
        ctx.bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass


def tangani_update_status(chat_id, message_id_target):
    if chat_id not in ctx.user_sessions:
        return
    sess = ctx.user_sessions[chat_id]
    entitas = sess.get("entitas", {})

    f_nama = entitas.get("NAMA")
    f_tanggal = entitas.get("TANGGAL")
    f_barang = entitas.get("BARANG")
    f_semua = entitas.get("SEMUA")

    if not (f_nama or f_tanggal or f_barang or f_semua):
        safe_edit_message(
            ctx.bot,
            "❌ Gagal, mohon sebutkan kriteria pesanan yang ingin diupdate (nama/tanggal/barang).",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    if not ctx.IS_DB_CONNECTED:
        safe_edit_message(
            ctx.bot,
            "❌ Gagal Mengakses: Mode Offline aktif.",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    safe_edit_message(
        ctx.bot,
        f"🔍 Mencari database untuk diupdate dengan parameter (Nama: {f_nama or '-'}, Tgl: {f_tanggal or '-'}, Brg: {f_barang or '-'}, Semua: {f_semua or '-'}) ...",
        chat_id=chat_id,
        message_id=message_id_target,
    )

    try:
        filters = []
        filters_no_date = []
        date_exact = False
        if f_nama:
            f = {"kolom": "nama_pelanggan", "nilai": f_nama, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)
        if f_tanggal:
            if len(f_tanggal) == 7 and "-" in f_tanggal:
                filters.append({"kolom": "tanggal", "nilai": f_tanggal, "operator": "ilike"})
            else:
                date_exact = True
                ddmm = str(f_tanggal)[:5]
                filters.append({"kolom": "tanggal", "nilai": ddmm, "operator": "ilike"})
        if f_barang:
            f = {"kolom": "barang", "nilai": f_barang, "operator": "ilike"}
            filters.append(f)
            filters_no_date.append(f)

        if filters:
            raw_data = db_client.get_transaksi_multi_filter(filters)
        else:
            raw_data = db_client.get_semua_transaksi_db()

        match_list = []
        for r in raw_data:
            if date_exact:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue

            nama_gs = r.get("nama_pelanggan", "")
            tgl_gs = r.get("tanggal", "")
            barang_gs = r.get("barang", "")
            status_gs = r.get("status", "").lower()

            match_nama = True
            match_barang = True

            if f_semua:
                pass
            else:
                if f_nama:
                    match_nama = cocokkan_nama(f_nama, nama_gs)
                if f_barang:
                    match_barang = str(f_barang).lower() in str(barang_gs).lower()

            if f_semua or (match_nama and match_barang):
                # Cek Multi-Satuan: Jika di entitas ada satuan, pastikan satuan di database cocok
                satuan_chat = entitas.get("SATUAN")
                satuan_gs = str(r.get("jumlah_satuan", "")).lower()

                match_unit = True
                if satuan_chat and satuan_chat.lower() not in satuan_gs:
                    match_unit = False

                if match_unit:
                    row = [
                        tgl_gs,
                        nama_gs,
                        barang_gs,
                        str(r.get("jumlah_satuan", "")),
                        str(r.get("harga", 0)),
                        str(r.get("total", 0)),
                        r.get("status", ""),
                        r.get("metode_pembayaran", ""),
                        str(r.get("tagihan", 0)),
                        str(r.get("uang_masuk", 0)),
                    ]
                    # Simpan mapping ID untuk operasi update
                    ctx.db_transaksi.row_mapping[r["id"]] = r["id"]

                    # Jika aksi adalah 'Update Status' otomatis, prioritaskan nota yang belum lunas
                    if (
                        entitas.get("STATUS")
                        or entitas.get("METODE_PEMBAYARAN")
                        or entitas.get("NOMINAL_BAYAR")
                    ):
                        # Hanya masukkan ke match_list jika belum lunas (Hutang/Dicicil)
                        if "lunas" not in status_gs:
                            match_list.append(
                                {
                                    "row_index": r["id"],
                                    "nama": nama_gs,
                                    "barang": barang_gs,
                                    "row_full": row,
                                }
                            )
                    else:
                        match_list.append(
                            {
                                "row_index": r["id"],
                                "nama": nama_gs,
                                "barang": barang_gs,
                                "row_full": row,
                            }
                        )

        if date_exact and f_tanggal and len(match_list) == 0:
            raw_data = (
                db_client.get_transaksi_multi_filter(filters_no_date)
                if filters_no_date
                else db_client.get_semua_transaksi_db()
            )
            for r in raw_data:
                tgl_db = normalisasi_tanggal_gs(r.get("tanggal", ""))
                if not tgl_db or (f_tanggal != tgl_db):
                    continue

                nama_gs = r.get("nama_pelanggan", "")
                tgl_gs = r.get("tanggal", "")
                barang_gs = r.get("barang", "")
                status_gs = r.get("status", "").lower()

                match_nama = True
                match_barang = True

                if f_semua:
                    pass
                else:
                    if f_nama:
                        match_nama = cocokkan_nama(f_nama, nama_gs)
                    if f_barang:
                        match_barang = str(f_barang).lower() in str(barang_gs).lower()

                if f_semua or (match_nama and match_barang):
                    # Cek Multi-Satuan: Jika di entitas ada satuan, pastikan satuan di database cocok
                    satuan_chat = entitas.get("SATUAN")
                    satuan_gs = str(r.get("jumlah_satuan", "")).lower()

                    match_unit = True
                    if satuan_chat and satuan_chat.lower() not in satuan_gs:
                        match_unit = False

                    if match_unit:
                        row = [
                            tgl_gs,
                            nama_gs,
                            barang_gs,
                            str(r.get("jumlah_satuan", "")),
                            str(r.get("harga", 0)),
                            str(r.get("total", 0)),
                            r.get("status", ""),
                            r.get("metode_pembayaran", ""),
                            str(r.get("tagihan", 0)),
                            str(r.get("uang_masuk", 0)),
                        ]
                        # Simpan mapping ID untuk operasi update
                        ctx.db_transaksi.row_mapping[r["id"]] = r["id"]

                        # Jika aksi adalah 'Update Status' otomatis, prioritaskan nota yang belum lunas
                        if (
                            entitas.get("STATUS")
                            or entitas.get("METODE_PEMBAYARAN")
                            or entitas.get("NOMINAL_BAYAR")
                        ):
                            # Hanya masukkan ke match_list jika belum lunas (Hutang/Dicicil)
                            if "lunas" not in status_gs:
                                match_list.append(
                                    {
                                        "row_index": r["id"],
                                        "nama": nama_gs,
                                        "barang": barang_gs,
                                        "row_full": row,
                                    }
                                )
                        else:
                            match_list.append(
                                {
                                    "row_index": r["id"],
                                    "nama": nama_gs,
                                    "barang": barang_gs,
                                    "row_full": row,
                                }
                            )

    except Exception as e:
        safe_edit_message(
            ctx.bot,
            f"❌ Gagal memindai database: {e}",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
        return

    if len(match_list) == 0:
        safe_edit_message(
            ctx.bot,
            f"❌ Tidak ditemukan pesanan yang sesuai kriteria tersebut untuk diubah.",
            chat_id=chat_id,
            message_id=message_id_target,
        )
        del ctx.user_sessions[chat_id]
    elif len(match_list) == 1:
        # CEK: Jika ada status/nominal di entitas, lakukan AUTO-UPDATE tanpa tanya lagi
        if (
            entitas.get("STATUS")
            or entitas.get("NOMINAL_BAYAR")
            or entitas.get("METODE_PEMBAYARAN")
        ):
            lakukan_auto_update_data(chat_id, message_id_target, match_list[0], entitas)
        else:
            siapkan_konfirmasi_update(chat_id, message_id_target, match_list[0])
    else:
        # Jika lebih dari satu, tampilkan daftar untuk dipilih
        teks_konflik = (
            f"✏️ <b>PILIH NOTA UNTUK UPDATE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Ditemukan <b>{len(match_list)} data</b> (Belum Lunas) untuk <b>{f_nama}</b>.\n"
            f"Pilih nota yang ingin diproses:\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        buttons = []

        for i, ml in enumerate(match_list[:10], start=1):
            row = ml["row_full"]
            tgl = row[0] if len(row) > 0 else "-"
            nama = row[1] if len(row) > 1 else "-"
            brg = row[2] if len(row) > 2 else "-"
            jml = row[3] if len(row) > 3 else "-"
            harga = row[4] if len(row) > 4 else "-"
            total = row[5] if len(row) > 5 else "-"
            status = row[6] if len(row) > 6 else "-"
            metode = row[7] if len(row) > 7 else "-"

            status_emoji = (
                "✅"
                if "lunas" in str(status).lower()
                else "⏳"
                if any(k in str(status).lower() for k in ["cicil", "dicicil", "dp"])
                else "🔴"
            )

            teks_konflik += (
                f"┌─── <b>[{i}] {nama}</b> ───\n"
                f"│ 📅 Tanggal  : {tgl}\n"
                f"│ 📦 Barang    : {jml} {brg}\n"
                f"│ 💰 Harga     : {harga}\n"
                f"│ 💵 Total      : {total}\n"
                f"│ {status_emoji} Status    : {status}\n"
                f"│ 🏦 Metode   : {metode}\n"
                f"└────────────────\n\n"
            )
            buttons.append(
                InlineKeyboardButton(f"✏️ Ubah #{i}", callback_data=f"resolve_{ml['row_index']}")
            )

        sess["konflik_data"] = match_list
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("❌ Batalkan Semua", callback_data="btn_buang"))

        safe_edit_message(
            ctx.bot,
            teks_konflik,
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
            reply_markup=markup,
        )


def lakukan_auto_update_data(chat_id, message_id_target, match_item, entitas):
    """Fungsi untuk update status/nominal secara otomatis jika data match hanya 1"""
    row_idx = match_item["row_index"]
    row_data = match_item["row_full"]

    new_status = entitas.get("STATUS")
    new_metode = entitas.get("METODE_PEMBAYARAN")
    new_nominal = entitas.get("NOMINAL_BAYAR")

    try:
        # Ambil data lama
        old_status = row_data[6]
        old_metode = row_data[7]
        old_tagihan = parse_rupiah(row_data[8])
        old_uang_masuk = parse_rupiah(row_data[9])
        total_nota = parse_rupiah(row_data[5])

        updates = []

        # Logika Pelunasan / Cicilan Tambahan
        if new_nominal:
            bayar_num = parse_rupiah(new_nominal)
            # Gunakan fungsi dari debt_tracker
            proses_bayar_tambahan(
                ctx.db_transaksi, ctx.db_histori, row_idx, bayar_num, new_metode or old_metode
            )
            msg_final = f"✅ <b>Update Berhasil!</b>\n\nPelanggan: <b>{match_item['nama']}</b>\nBarang: <b>{match_item['barang']}</b>\nBayar: <code>{format_rupiah(bayar_num)}</code>\nStatus otomatis diperbarui berdasarkan sisa tagihan."
        else:
            # Update status/metode saja
            data_update = {}
            if new_status:
                data_update["status"] = new_status.title()
                # Jika status jadi lunas, otomatis isi uang masuk = total
                if new_status.lower() == "lunas":
                    data_update["uang_masuk"] = total_nota
                    data_update["tagihan"] = 0
            if new_metode:
                data_update["metode_pembayaran"] = new_metode.title()

            if data_update:
                from database import db_client

                db_client.update_transaksi_db(row_idx, data_update)

            msg_final = f"✅ <b>Data Diperbarui!</b>\n\nPelanggan: <b>{match_item['nama']}</b>\nBarang: <b>{match_item['barang']}</b>\nStatus: <code>{new_status or old_status}</code>\nMetode: <code>{new_metode or old_metode}</code>"

        safe_edit_message(
            ctx.bot, msg_final, chat_id=chat_id, message_id=message_id_target, parse_mode="HTML"
        )
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]

    except Exception as e:
        safe_edit_message(
            ctx.bot, f"❌ Gagal auto-update: {e}", chat_id=chat_id, message_id=message_id_target
        )


def tangani_simpan_transaksi(chat_id, message_id_target):
    """Menyimpan data transaksi tunggal dari sesi ke Database Relasional dan Flat (Backward Compatibility)"""
    sess = ctx.user_sessions.get(chat_id)
    safe_debug_event(
        {
            "runId": "pre-fix",
            "hypothesisId": "B",
            "location": "handlers/crud_transaksi.py:1296",
            "msg": "[DEBUG] enter tangani_simpan_transaksi",
            "data": {
                "chat_id": chat_id,
                "has_session": bool(sess),
                "has_entitas": bool((sess or {}).get("entitas")),
                "entitas": (sess or {}).get("entitas"),
            },
        }
    )
    if not sess or "entitas" not in sess:
        safe_edit_message(
            ctx.bot,
            "❌ Data tidak ditemukan. Silakan unggah foto kembali.",
            chat_id,
            message_id_target,
        )
        return

    ent = sess["entitas"]
    safe_edit_message(ctx.bot, "⏳ Sedang menyimpan transaksi...", chat_id, message_id_target)

    hari_ini_str = datetime.now().strftime("%d-%m-%Y")

    try:
        nama_pelanggan = ent.get("NAMA") or "Tanpa Nama"
        tanggal_pesanan = ent.get("TANGGAL") or hari_ini_str
        t_norm = normalisasi_tanggal_gs(tanggal_pesanan)
        if t_norm:
            tanggal_pesanan = t_norm
        status_pesanan = (ent.get("STATUS") or "Lunas").title()
        metode_pesanan = ent.get("METODE_PEMBAYARAN") or "-"
        cached_barang = get_cached_barang() if ctx.IS_DB_CONNECTED else []

        # Lengkapi harga jika belum ada
        if ctx.IS_DB_CONNECTED and ent.get("BARANG") and not ent.get("HARGA"):
            matches = cari_harga_default(
                ctx.db_barang,
                ent["BARANG"],
                satuan_cari=ent.get("SATUAN"),
                semua_barang=cached_barang,
            )
            if matches:
                ent["HARGA"] = format_rupiah(matches[0]["harga"])

        hrg_str = str(ent.get("HARGA") or "0")
        jml_str = str(ent.get("JUMLAH") or "1")

        try:
            hrg_num = int(re.sub(r"[^\d]", "", hrg_str)) if re.sub(r"[^\d]", "", hrg_str) else 0
            jml_num = int(re.search(r"\d+", jml_str).group()) if re.search(r"\d+", jml_str) else 1
        except:
            hrg_num, jml_num = 0, 1

        subtotal_item = hrg_num * jml_num
        ent["TOTAL"] = format_rupiah(subtotal_item)

        nom_str = ent.get("NOMINAL_BAYAR") or "Rp 0"
        nominal_bayar_item = parse_rupiah(nom_str)
        if nominal_bayar_item == 0:
            if status_pesanan.upper() == "LUNAS":
                nominal_bayar_item = subtotal_item
                ent["NOMINAL_BAYAR"] = format_rupiah(nominal_bayar_item)
            elif status_pesanan.upper() == "DICICIL":
                frac = ent.get("_CICIL_FRACTION") or 0.5
                nominal_bayar_item = int(subtotal_item * frac)
                ent["NOMINAL_BAYAR"] = format_rupiah(nominal_bayar_item)

        item_tagihan, item_uang_masuk, _ = hitung_sisa_tagihan(
            subtotal_item, nominal_bayar_item, status_pesanan
        )

        # Cek Duplikat di flat table
        data_flat = {
            "tanggal": tanggal_pesanan,
            "nama_pelanggan": nama_pelanggan,
            "barang": ent.get("BARANG") or "-",
            "jumlah_satuan": jml_str,
            "harga": hrg_num,
            "total": subtotal_item,
            "status": status_pesanan,
            "metode_pembayaran": metode_pesanan,
            "tagihan": item_tagihan,
            "uang_masuk": item_uang_masuk,
        }

        dup_id = db_client.find_duplicate_transaksi_flat(data_flat)
        if dup_id:
            safe_debug_event(
                {
                    "runId": "pre-fix",
                    "hypothesisId": "B",
                    "location": "handlers/crud_transaksi.py:1368",
                    "msg": "[DEBUG] duplicate single transaction detected",
                    "data": {"chat_id": chat_id, "dup_id": dup_id, "data_flat": data_flat},
                }
            )
            sukses_text = (
                f"⚠️ <b>DATA TRANSAKSI SUDAH ADA (DUPLIKAT)!</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Transaksi dengan rincian ini sudah tercatat sebelumnya dengan ID <b>{dup_id}</b>.\n"
                f"Tidak ada data baru yang ditambahkan."
            )
            safe_edit_message(ctx.bot, sukses_text, chat_id, message_id_target, parse_mode="HTML")
            if chat_id in ctx.user_sessions:
                del ctx.user_sessions[chat_id]
            return

        # 1. Dapatkan atau Buat Pelanggan
        pelanggan_id = db_client.get_or_create_pelanggan(nama_pelanggan)

        # 2. Buat Pesanan Induk
        data_pesanan = {
            "pelanggan_id": pelanggan_id,
            "tanggal": tanggal_pesanan,
            "status": status_pesanan,
            "metode_pembayaran": metode_pesanan,
            "total": subtotal_item,
            "tagihan": item_tagihan,
            "uang_masuk": item_uang_masuk,
        }
        res_pesanan = db_client.insert_pesanan(data_pesanan)
        pesanan_id = res_pesanan[0]["id"]
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "C",
                "location": "handlers/crud_transaksi.py:1393",
                "msg": "[DEBUG] single pesanan inserted",
                "data": {
                    "chat_id": chat_id,
                    "pesanan_id": pesanan_id,
                    "data_pesanan": data_pesanan,
                },
            }
        )

        # 3. Simpan Pesanan Item
        b_id = None
        if ent.get("BARANG"):
            b_res = (
                db_client.get_supabase()
                .table("master_barang")
                .select("id")
                .ilike("nama_barang", f"%{ent['BARANG']}%")
                .execute()
            )
            if b_res.data:
                b_id = b_res.data[0]["id"]

        data_item = {
            "pesanan_id": pesanan_id,
            "barang_id": b_id,
            "jumlah_satuan": jml_str,
            "harga_satuan": hrg_num,
            "subtotal": subtotal_item,
        }
        db_client.insert_pesanan_item(data_item)

        # 4. FLAT TABLE (Backward Compatibility)
        flat_rows = db_client.insert_transaksi_db(data_flat)
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "D",
                "location": "handlers/crud_transaksi.py:1413",
                "msg": "[DEBUG] single transaksi flat inserted",
                "data": {"chat_id": chat_id, "data_flat": data_flat, "flat_rows": flat_rows},
            }
        )

        sukses_text = (
            f"✅ <b>BERHASIL MENYIMPAN TRANSAKSI!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Tanggal: <b>{tanggal_pesanan}</b>\n"
            f"Pelanggan: <b>{nama_pelanggan}</b>\n"
            f"Barang: <b>{ent.get('BARANG') or '-'}</b>\n"
            f"Total: <b>{ent.get('TOTAL') or '-'}</b>\n"
            f"Status: <b>{status_pesanan}</b> ({metode_pesanan})\n"
            f"ID Pesanan: <b>{pesanan_id}</b>\n\n"
            f"Silakan cek /dashboard untuk melihat pembaruan.\n"
            f"Jika tidak muncul, gunakan /dashboard → Pilih Tanggal → <code>{tanggal_pesanan}</code>."
        )
        safe_edit_message(ctx.bot, sukses_text, chat_id, message_id_target, parse_mode="HTML")
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]

    except Exception as e:
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "E",
                "location": "handlers/crud_transaksi.py:1430",
                "msg": "[DEBUG] single save exception",
                "data": {"chat_id": chat_id, "error": str(e)},
            }
        )
        logger.error(f"Error simpan transaksi tunggal: {e}")
        safe_edit_message(ctx.bot, f"❌ Gagal menyimpan transaksi: {e}", chat_id, message_id_target)


def tangani_simpan_multi(chat_id, message_id_target):
    """Menyimpan seluruh transaksi dalam batch ke Database Relasional (Fase 2)"""
    sess = ctx.user_sessions.get(chat_id)
    safe_debug_event(
        {
            "runId": "pre-fix",
            "hypothesisId": "B",
            "location": "handlers/crud_transaksi.py:1435",
            "msg": "[DEBUG] enter tangani_simpan_multi",
            "data": {
                "chat_id": chat_id,
                "has_session": bool(sess),
                "multi_count": len((sess or {}).get("multi_results") or []),
            },
        }
    )
    if not sess or "multi_results" not in sess:
        ctx.bot.answer_callback_query(chat_id, "Data tidak ditemukan.")
        return

    results = sess["multi_results"]
    safe_edit_message(
        ctx.bot,
        f"⏳ Sedang menyimpan {len(results)} item ke Database Relasional...",
        chat_id,
        message_id_target,
    )

    hari_ini_str = datetime.now().strftime("%d-%m-%Y")

    try:
        # Asumsikan bulk ini adalah pesanan dari 1 pelanggan yang sama (berdasarkan item pertama)
        ent_utama = results[0]["entitas"]
        nama_pelanggan = ent_utama.get("NAMA") or "Tanpa Nama"
        tanggal_pesanan = ent_utama.get("TANGGAL") or hari_ini_str
        t_norm = normalisasi_tanggal_gs(tanggal_pesanan)
        if t_norm:
            tanggal_pesanan = t_norm
        status_pesanan = ent_utama.get("STATUS") or "Lunas"
        metode_pesanan = ent_utama.get("METODE_PEMBAYARAN") or "-"
        apply_batch_financials(results, sess.get("multi_batch_payment_total"))
        cached_barang = get_cached_barang() if ctx.IS_DB_CONNECTED else []

        # Hitung akumulasi total seluruh item di batch beserta detail keuangan per item
        akumulasi_total = 0
        total_uang_masuk_batch = 0
        total_tagihan_batch = 0

        for res in results:
            ent = res["entitas"]
            if ctx.IS_DB_CONNECTED and ent.get("BARANG") and not ent.get("HARGA"):
                matches = cari_harga_default(
                    ctx.db_barang,
                    ent["BARANG"],
                    satuan_cari=ent.get("SATUAN"),
                    semua_barang=cached_barang,
                )
                if matches:
                    ent["HARGA"] = format_rupiah(matches[0]["harga"])

            hrg_str = str(ent.get("HARGA") or "0")
            jml_str = str(ent.get("JUMLAH") or "1")

            try:
                hrg_num = int(re.sub(r"[^\d]", "", hrg_str)) if re.sub(r"[^\d]", "", hrg_str) else 0
                jml_num = (
                    int(re.search(r"\d+", jml_str).group()) if re.search(r"\d+", jml_str) else 1
                )
            except:
                hrg_num, jml_num = 0, 1

            subtotal_item = hrg_num * jml_num
            akumulasi_total += subtotal_item

            # Cari/kalkulasi nominal bayar spesifik item dari yang sudah dipersiapkan di resume
            status_item = (ent.get("STATUS") or status_pesanan or "Lunas").title()
            tot_str_item = format_rupiah(subtotal_item)
            ent["TOTAL"] = tot_str_item

            nominal_bayar_item = int(
                ent.get("_CALC_UANG_MASUK", parse_rupiah(ent.get("NOMINAL_BAYAR") or 0)) or 0
            )
            item_tagihan = int(
                ent.get("_CALC_TAGIHAN", max(0, subtotal_item - nominal_bayar_item)) or 0
            )
            status_item = ent.get("_CALC_STATUS", status_item)
            ent["NOMINAL_BAYAR"] = format_rupiah(nominal_bayar_item)
            ent["_CALC_TAGIHAN"] = item_tagihan
            ent["_CALC_UANG_MASUK"] = nominal_bayar_item
            ent["_CALC_STATUS"] = status_item

            total_uang_masuk_batch += nominal_bayar_item
            total_tagihan_batch += item_tagihan

        status_final_batch = "Lunas"
        if total_tagihan_batch > 0:
            if total_uang_masuk_batch > 0:
                status_final_batch = "Dicicil"
            else:
                status_final_batch = "Hutang"

        # 1. Dapatkan atau Buat Pelanggan
        pelanggan_id = db_client.get_or_create_pelanggan(nama_pelanggan)

        # 2. Buat Pesanan Induk
        data_pesanan = {
            "pelanggan_id": pelanggan_id,
            "tanggal": tanggal_pesanan,
            "status": status_final_batch,
            "metode_pembayaran": metode_pesanan,
            "total": akumulasi_total,
            "tagihan": total_tagihan_batch,
            "uang_masuk": total_uang_masuk_batch,
        }
        res_pesanan = db_client.insert_pesanan(data_pesanan)
        pesanan_id = res_pesanan[0]["id"]
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "C",
                "location": "handlers/crud_transaksi.py:1525",
                "msg": "[DEBUG] multi pesanan inserted",
                "data": {
                    "chat_id": chat_id,
                    "pesanan_id": pesanan_id,
                    "data_pesanan": data_pesanan,
                },
            }
        )

        # 3. Simpan Pesanan Items
        flat_inserted = []
        for res in results:
            ent = res["entitas"]

            # Ekstrak harga
            hrg_str = str(ent.get("HARGA") or "0")
            jml_str = str(ent.get("JUMLAH") or "1")
            try:
                hrg_num = int(re.sub(r"[^\d]", "", hrg_str)) if re.sub(r"[^\d]", "", hrg_str) else 0
                jml_num = (
                    int(re.search(r"\d+", jml_str).group()) if re.search(r"\d+", jml_str) else 1
                )
            except:
                hrg_num, jml_num = 0, 1

            # Cari barang_id (Opsional, fallback ke null jika tak cocok 100%)
            b_id = None
            if ent.get("BARANG"):
                b_res = (
                    db_client.get_supabase()
                    .table("master_barang")
                    .select("id")
                    .ilike("nama_barang", f"%{ent['BARANG']}%")
                    .execute()
                )
                if b_res.data:
                    b_id = b_res.data[0]["id"]

            data_item = {
                "pesanan_id": pesanan_id,
                "barang_id": b_id,
                "jumlah_satuan": jml_str,
                "harga_satuan": hrg_num,
                "subtotal": hrg_num * jml_num,
            }
            db_client.insert_pesanan_item(data_item)

            # 4. FLAT TABLE (Backward Compatibility & Read Data Support)
            data_flat = {
                "tanggal": tanggal_pesanan,
                "nama_pelanggan": nama_pelanggan,
                "barang": ent.get("BARANG") or "-",
                "jumlah_satuan": jml_str,
                "harga": hrg_num,
                "total": hrg_num * jml_num,
                "status": ent.get("_CALC_STATUS", status_final_batch),
                "metode_pembayaran": metode_pesanan,
                "tagihan": ent.get("_CALC_TAGIHAN", 0),
                "uang_masuk": ent.get("_CALC_UANG_MASUK", 0),
            }
            flat_rows = db_client.insert_transaksi_db(data_flat)
            flat_inserted.append({"barang": ent.get("BARANG") or "-", "rows": flat_rows})
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "D",
                "location": "handlers/crud_transaksi.py:1570",
                "msg": "[DEBUG] multi transaksi flat inserted",
                "data": {
                    "chat_id": chat_id,
                    "tanggal": tanggal_pesanan,
                    "count": len(flat_inserted),
                    "flat_inserted": flat_inserted,
                },
            }
        )

        sukses_text = (
            f"✅ <b>BERHASIL SIMPAN BATCH (RELASIONAL)!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Tanggal: <b>{tanggal_pesanan}</b>\n"
            f"Telah tersimpan <b>{len(results)} item</b> ke dalam 1 ID Pesanan ({pesanan_id}).\n"
            f"Silakan cek /dashboard untuk melihat pembaruan.\n"
            f"Jika tidak muncul, gunakan /dashboard → Pilih Tanggal → <code>{tanggal_pesanan}</code>."
        )
        safe_edit_message(ctx.bot, sukses_text, chat_id, message_id_target, parse_mode="HTML")
        if chat_id in ctx.user_sessions:
            del ctx.user_sessions[chat_id]

    except Exception as e:
        safe_debug_event(
            {
                "runId": "pre-fix",
                "hypothesisId": "E",
                "location": "handlers/crud_transaksi.py:1583",
                "msg": "[DEBUG] multi save exception",
                "data": {"chat_id": chat_id, "error": str(e)},
            }
        )
        logger.error(f"Error bulk append relasional: {e}")
        safe_edit_message(
            ctx.bot, f"❌ Gagal menyimpan batch ke skema baru: {e}", chat_id, message_id_target
        )


def tangani_catat_pelunasan(chat_id, message_id_target):
    """Flow utama saat NLP mendeteksi aksi 'Catat Pelunasan'."""
    if chat_id not in ctx.user_sessions:
        return
    sess = ctx.user_sessions[chat_id]
    entitas = sess.get("entitas", {})

    f_nama = entitas.get("NAMA")
    f_nominal = entitas.get("NOMINAL_BAYAR")

    if not f_nama:
        safe_edit_message(
            ctx.bot,
            "❓ Mohon sebutkan nama pelanggan yang ingin dicatat pembayarannya.\n"
            "<i>Contoh: <code>tambahan bayar pak andi 50rb</code></i>",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    if not ctx.IS_DB_CONNECTED:
        safe_edit_message(
            ctx.bot, "❌ Mode Offline aktif.", chat_id=chat_id, message_id=message_id_target
        )
        del ctx.user_sessions[chat_id]
        return

    safe_edit_message(
        ctx.bot,
        f"🔍 Mencari hutang aktif atas nama <b>{f_nama}</b>...",
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
    )

    hutang_list = cari_hutang_aktif(ctx.db_transaksi, f_nama, cocokkan_nama)

    if not hutang_list:
        safe_edit_message(
            ctx.bot,
            f"✅ Tidak ditemukan sisa tagihan aktif atas nama <b>{f_nama}</b>.",
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
        )
        del ctx.user_sessions[chat_id]
        return

    sess["hutang_list"] = hutang_list
    sess["nominal_bayar"] = f_nominal

    if len(hutang_list) == 1:
        # Langsung ke konfirmasi
        _tampilkan_konfirmasi_pelunasan(chat_id, message_id_target, hutang_list[0], f_nominal)
    else:
        # Tampilkan pilihan nota
        teks = (
            f"⚠️ Ditemukan <b>{len(hutang_list)} nota aktif</b> atas nama <b>{f_nama}</b>.\n"
            "Pilih nota mana yang ingin dibayar:\n\n"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        for i, h in enumerate(hutang_list):
            teks += (
                f"<b>[{i+1}]</b> {h['tanggal']} | {h['barang']} | "
                f"Sisa: <code>{h['tagihan_str']}</code>\n"
            )
            markup.add(
                InlineKeyboardButton(
                    f"[{i+1}] {h['barang']} — Tagihan {h['tagihan_str']}",
                    callback_data=f"pel_pilih_{h['row_index']}",
                )
            )
        markup.add(InlineKeyboardButton("❌ Batal", callback_data="btn_buang"))
        safe_edit_message(
            ctx.bot,
            teks,
            chat_id=chat_id,
            message_id=message_id_target,
            parse_mode="HTML",
            reply_markup=markup,
        )


def _tampilkan_konfirmasi_pelunasan(chat_id, message_id_target, info_hutang, nominal_bayar):
    """Tampilkan kartu konfirmasi sebelum mencatat pembayaran."""
    sess = ctx.user_sessions[chat_id]
    sess["pel_row_idx"] = info_hutang["row_index"]
    sess["pel_nama"] = info_hutang["nama"]

    tagihan_lama = info_hutang["tagihan"]
    nom_val = parse_rupiah(nominal_bayar) if nominal_bayar else 0

    if nom_val > 0:
        tagihan_baru = max(0, tagihan_lama - nom_val)
        status_ket = (
            "Lunas ✅" if tagihan_baru == 0 else f"Nyicil ⏳ (tagihan {format_rupiah(tagihan_baru)})"
        )
        ket_bayar = format_rupiah(nom_val)
        sess["pel_nominal"] = nom_val
    else:
        # Anggap pelunasan penuh
        tagihan_baru = 0
        status_ket = "Lunas ✅"
        ket_bayar = format_rupiah(tagihan_lama) + " (pelunasan penuh)"
        sess["pel_nominal"] = tagihan_lama

    sess["pel_tagihan_baru"] = tagihan_baru

    balasan = (
        "💰 <b>KONFIRMASI PEMBAYARAN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Nama:</b> {info_hutang['nama']}\n"
        f"📦 <b>Barang:</b> {info_hutang['barang']}\n"
        f"📅 <b>Tgl Transaksi:</b> {info_hutang['tanggal']}\n"
        f"💵 <b>Total Transaksi:</b> <code>{info_hutang['total']}</code>\n"
        f"🔴 <b>Jumlah Tagihan:</b> <code>{info_hutang['tagihan_str']}</code>\n"
        f"💚 <b>Sudah Dibayar:</b> <code>{info_hutang['uang_masuk_str']}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Bayar Sekarang:</b> <code>{ket_bayar}</code>\n"
        f"📊 <b>Status Baru:</b> {status_ket}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Konfirmasi pembayaran ini?</i>"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Ya, Catat!", callback_data="pel_konfirm_ya"),
        InlineKeyboardButton("❌ Batal", callback_data="btn_buang"),
    )
    safe_edit_message(
        ctx.bot,
        balasan,
        chat_id=chat_id,
        message_id=message_id_target,
        parse_mode="HTML",
        reply_markup=markup,
    )
