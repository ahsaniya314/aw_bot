import os
import threading
import time
import schedule
import json
from collections import deque
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, send_from_directory
from bot.core import bot, AUTHORIZED_ADMINS, ctx, logger
from utils.security import safe_debug_event

# Import scheduler task
from services import auto_reminder
from database import db_client
from database.db_client import ping_supabase_keep_alive

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Run migrations
try:
    from migrations.run_migrations import run_migrations
    run_migrations()
    logger.info("[OK] Migrations run successfully!")
except Exception as e:
    logger.warning(f"[WARNING] Could not run migrations automatically: {e}")
    logger.warning("[WARNING] Please run the SQL file manually in Supabase SQL Editor!")

app = Flask(__name__)

# Tambahkan CORS untuk izinkan akses dari dasbor web
try:
    from flask_cors import CORS
    CORS(app)
    logger.info("[OK] CORS enabled for all origins")
except ImportError:
    logger.warning("[WARNING] flask-cors not installed, CORS disabled")

_trx_cache = {"ts": 0.0, "data": None}
_keepalive_cache = {"ts": 0.0, "ok": None, "error": None}

_webhook_queue = deque()
_webhook_cv = threading.Condition()
_webhook_worker_started = False


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_webhook_path_secret() -> str:
    return (os.getenv("TELEGRAM_WEBHOOK_PATH_SECRET") or os.getenv("WEBHOOK_PATH_SECRET") or "").strip()


def _get_webhook_header_secret() -> str:
    return (os.getenv("TELEGRAM_WEBHOOK_SECRET_TOKEN") or os.getenv("WEBHOOK_SECRET_TOKEN") or "").strip()


def _build_webhook_url() -> str | None:
    explicit = (os.getenv("TELEGRAM_WEBHOOK_URL") or os.getenv("WEBHOOK_URL") or "").strip()
    if explicit:
        return explicit
    host = (os.getenv("SPACE_HOST") or "").strip()
    path_secret = _get_webhook_path_secret()
    if host and path_secret:
        return f"https://{host}/telegram/webhook/{path_secret}"
    base = (os.getenv("PUBLIC_BASE_URL") or os.getenv("APP_BASE_URL") or os.getenv("BASE_URL") or "").strip().rstrip("/")
    if base and path_secret:
        return f"{base}/telegram/webhook/{path_secret}"
    return None


def _enqueue_update(update_dict: dict) -> None:
    with _webhook_cv:
        _webhook_queue.append(update_dict)
        _webhook_cv.notify()


def _start_webhook_worker_if_needed() -> None:
    global _webhook_worker_started
    if _webhook_worker_started:
        return

    def _worker():
        from telebot import types as tb_types
        while True:
            with _webhook_cv:
                while not _webhook_queue:
                    _webhook_cv.wait()
                payload = _webhook_queue.popleft()
            try:
                upd = tb_types.Update.de_json(payload)
                if upd:
                    bot.process_new_updates([upd])
            except Exception as e:
                logger.error(f"[WEBHOOK] Failed processing update: {e}")

    threading.Thread(target=_worker, daemon=True).start()
    _webhook_worker_started = True
    logger.info("[WEBHOOK] Background worker started")


def _to_float(v):
    try:
        if v is None:
            return 0.0
        return float(v)
    except Exception:
        try:
            return float(str(v).replace(".", "").replace(",", ""))
        except Exception:
            return 0.0


def _parse_tanggal_ddmmyyyy(s):
    if not s:
        return None
    teks = str(s).strip()
    try:
        return datetime.strptime(teks, "%d-%m-%Y").date()
    except Exception:
        pass
    try:
        return datetime.strptime(teks[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def _get_transaksi_cached(ttl_seconds=60):
    now = time.time()
    if _trx_cache["data"] is not None and (now - _trx_cache["ts"]) < ttl_seconds:
        return _trx_cache["data"]
    data = db_client.get_semua_transaksi_db()
    _trx_cache["data"] = data
    _trx_cache["ts"] = now
    return data


def _maybe_ping_supabase_keep_alive(ttl_seconds=6 * 60 * 60):
    now = time.time()
    if _keepalive_cache["ok"] is not None and (now - _keepalive_cache["ts"]) < ttl_seconds:
        return _keepalive_cache["ok"], _keepalive_cache["error"]
    try:
        ok = bool(ping_supabase_keep_alive())
        err = None
    except Exception as e:
        ok = False
        err = str(e)
    _keepalive_cache["ts"] = now
    _keepalive_cache["ok"] = ok
    _keepalive_cache["error"] = err
    return ok, err


def _filter_last_days(rows, days):
    if not days:
        return rows
    try:
        days = int(days)
    except Exception:
        return rows
    if days <= 0:
        return rows
    batas = date.today() - timedelta(days=days - 1)
    out = []
    for r in rows:
        d = _parse_tanggal_ddmmyyyy(r.get("tanggal"))
        if d and d >= batas:
            out.append(r)
    return out


@app.route("/api/dashboard/summary")
def api_dashboard_summary():
    if not ctx.IS_DB_CONNECTED:
        # --- Data dummy ketika Mode Offline ---
        return jsonify({
            "ok": True,
            "range_days": 30,
            "total_transaksi": 128,
            "omzet": 15750000.0,
            "uang_masuk": 12500000.0,
            "piutang": 3250000.0,
            "status_count": {
                "lunas": 95,
                "dicicil": 20,
                "hutang": 10,
                "lain": 3
            }
        })

    days = request.args.get("days")
    rows = _get_transaksi_cached(ttl_seconds=10)
    rows = _filter_last_days(rows, days)
    safe_debug_event({
        "runId": "pre-fix",
        "hypothesisId": "F",
        "location": "app.py:169",
        "msg": "[DEBUG] dashboard summary queried",
        "data": {"days": days, "row_count": len(rows), "sample_tanggal": [r.get("tanggal") for r in rows[:5]]},
    })

    omzet = 0.0
    uang_masuk = 0.0
    piutang = 0.0
    total = 0
    st = {"lunas": 0, "dicicil": 0, "hutang": 0, "lain": 0}

    for r in rows:
        total += 1
        omzet += _to_float(r.get("total"))
        uang_masuk += _to_float(r.get("uang_masuk"))
        piutang += _to_float(r.get("tagihan"))
        s = str(r.get("status") or "").lower()
        if "lunas" in s:
            st["lunas"] += 1
        elif any(k in s for k in ["cicil", "dicicil", "nyicil", "dp"]):
            st["dicicil"] += 1
        elif "hutang" in s or "belum" in s:
            st["hutang"] += 1
        else:
            st["lain"] += 1

    return jsonify({
        "ok": True,
        "range_days": int(days) if (days and str(days).isdigit()) else None,
        "total_transaksi": total,
        "omzet": round(omzet, 2),
        "uang_masuk": round(uang_masuk, 2),
        "piutang": round(piutang, 2),
        "status_count": st
    })


@app.route("/api/dashboard/timeseries")
def api_dashboard_timeseries():
    if not ctx.IS_DB_CONNECTED:
        # --- Data dummy ketika Mode Offline ---
        return jsonify({
            "ok": True,
            "days": 30,
            "labels": ["01-06", "05-06", "10-06", "15-06", "20-06", "25-06", "30-06"],
            "omzet": [500000, 750000, 600000, 900000, 800000, 1200000, 1000000],
            "uang_masuk": [400000, 600000, 500000, 750000, 650000, 1000000, 850000],
            "piutang": [100000, 150000, 100000, 150000, 150000, 200000, 150000],
            "count": [5, 8, 6, 10, 9, 12, 10]
        })

    try:
        days = int(request.args.get("days", "14"))
    except Exception:
        days = 14
    days = max(3, min(days, 90))

    rows = _get_transaksi_cached(ttl_seconds=10)
    rows = _filter_last_days(rows, days)

    by_day = {}
    for r in rows:
        d = _parse_tanggal_ddmmyyyy(r.get("tanggal"))
        if not d:
            continue
        key = d.isoformat()
        if key not in by_day:
            by_day[key] = {"omzet": 0.0, "uang_masuk": 0.0, "piutang": 0.0, "count": 0}
        by_day[key]["omzet"] += _to_float(r.get("total"))
        by_day[key]["uang_masuk"] += _to_float(r.get("uang_masuk"))
        by_day[key]["piutang"] += _to_float(r.get("tagihan"))
        by_day[key]["count"] += 1

    labels = []
    omzet = []
    uang_masuk = []
    piutang = []
    count = []
    start = date.today() - timedelta(days=days - 1)
    for i in range(days):
        d = start + timedelta(days=i)
        key = d.isoformat()
        labels.append(d.strftime("%d-%m"))
        v = by_day.get(key, {"omzet": 0.0, "uang_masuk": 0.0, "piutang": 0.0, "count": 0})
        omzet.append(round(v["omzet"], 2))
        uang_masuk.append(round(v["uang_masuk"], 2))
        piutang.append(round(v["piutang"], 2))
        count.append(int(v["count"]))

    return jsonify({
        "ok": True,
        "days": days,
        "labels": labels,
        "omzet": omzet,
        "uang_masuk": uang_masuk,
        "piutang": piutang,
        "count": count
    })


@app.route("/api/dashboard/recent")
def api_dashboard_recent():
    if not ctx.IS_DB_CONNECTED:
        # --- Data dummy ketika Mode Offline ---
        return jsonify({
            "ok": True,
            "items": [
                {
                    "id": 1,
                    "tanggal": "2026-06-27",
                    "nama_pelanggan": "Andi",
                    "barang": "Kemeja",
                    "jumlah_satuan": 2,
                    "harga": 150000.0,
                    "total": 300000.0,
                    "status": "Lunas",
                    "metode_pembayaran": "Transfer",
                    "tagihan": 0.0,
                    "uang_masuk": 300000.0
                },
                {
                    "id": 2,
                    "tanggal": "2026-06-26",
                    "nama_pelanggan": "Budi",
                    "barang": "Celana",
                    "jumlah_satuan": 1,
                    "harga": 200000.0,
                    "total": 200000.0,
                    "status": "Dicicil",
                    "metode_pembayaran": "Cash",
                    "tagihan": 100000.0,
                    "uang_masuk": 100000.0
                },
                {
                    "id": 3,
                    "tanggal": "2026-06-25",
                    "nama_pelanggan": "Citra",
                    "barang": "Sepatu",
                    "jumlah_satuan": 1,
                    "harga": 350000.0,
                    "total": 350000.0,
                    "status": "Lunas",
                    "metode_pembayaran": "QRIS",
                    "tagihan": 0.0,
                    "uang_masuk": 350000.0
                }
            ]
        })

    try:
        limit = int(request.args.get("limit", "20"))
    except Exception:
        limit = 20
    limit = max(5, min(limit, 100))

    q = (request.args.get("q") or "").strip().lower()
    days = request.args.get("days")

    rows = _get_transaksi_cached(ttl_seconds=5)
    rows = _filter_last_days(rows, days)
    safe_debug_event({
        "runId": "pre-fix",
        "hypothesisId": "F",
        "location": "app.py:264",
        "msg": "[DEBUG] dashboard recent queried",
        "data": {"days": days, "q": q, "row_count": len(rows), "sample_rows": [{"id": r.get("id"), "tanggal": r.get("tanggal"), "nama": r.get("nama_pelanggan"), "barang": r.get("barang")} for r in rows[:5]]},
    })

    def _recent_sort_key(r):
        rid = r.get("id")
        try:
            return (0, int(rid))
        except Exception:
            created_at = str(r.get("created_at") or "")
            return (1, created_at, str(rid or ""))

    rows_sorted = sorted(rows, key=_recent_sort_key, reverse=True)
    out = []
    for r in rows_sorted:
        if q:
            blob = " ".join([
                str(r.get("id") or ""),
                str(r.get("tanggal") or ""),
                str(r.get("nama_pelanggan") or ""),
                str(r.get("barang") or ""),
                str(r.get("status") or ""),
                str(r.get("metode_pembayaran") or ""),
            ]).lower()
            if q not in blob:
                continue
        out.append({
            "id": r.get("id"),
            "tanggal": r.get("tanggal"),
            "nama_pelanggan": r.get("nama_pelanggan"),
            "barang": r.get("barang"),
            "jumlah_satuan": r.get("jumlah_satuan"),
            "harga": _to_float(r.get("harga")),
            "total": _to_float(r.get("total")),
            "status": r.get("status"),
            "metode_pembayaran": r.get("metode_pembayaran"),
            "tagihan": _to_float(r.get("tagihan")),
            "uang_masuk": _to_float(r.get("uang_masuk")),
        })
        if len(out) >= limit:
            break
    return jsonify({"ok": True, "items": out})


@app.route("/api/dashboard/top-customers")
def api_dashboard_top_customers():
    if not ctx.IS_DB_CONNECTED:
        # --- Data dummy ketika Mode Offline ---
        return jsonify({
            "ok": True,
            "items": [
                {"nama": "Andi", "omzet": 2500000.0, "piutang": 0.0, "count": 12},
                {"nama": "Budi", "omzet": 1800000.0, "piutang": 500000.0, "count": 8},
                {"nama": "Citra", "omzet": 1500000.0, "piutang": 0.0, "count": 10}
            ]
        })

    try:
        limit = int(request.args.get("limit", "8"))
    except Exception:
        limit = 8
    limit = max(3, min(limit, 20))

    days = request.args.get("days")
    rows = _get_transaksi_cached(ttl_seconds=10)
    rows = _filter_last_days(rows, days)

    agg = {}
    for r in rows:
        nama = (r.get("nama_pelanggan") or "Tanpa Nama").strip() or "Tanpa Nama"
        if nama not in agg:
            agg[nama] = {"omzet": 0.0, "piutang": 0.0, "count": 0}
        agg[nama]["omzet"] += _to_float(r.get("total"))
        agg[nama]["piutang"] += _to_float(r.get("tagihan"))
        agg[nama]["count"] += 1

    items = [
        {"nama": k, "omzet": round(v["omzet"], 2), "piutang": round(v["piutang"], 2), "count": v["count"]}
        for k, v in agg.items()
    ]
    items.sort(key=lambda x: x["omzet"], reverse=True)
    return jsonify({"ok": True, "items": items[:limit]})





@app.route('/dashboard')
@app.route('/dashboard/')
@app.route('/dashboard/<path:path>')
def serve_dashboard(path=''):
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard-web', 'out')
    
    # If path is empty, serve index.html
    if not path or path == '/':
        return send_from_directory(base_dir, 'index.html')
        
    # Check if the requested file exists directly in out folder (e.g. logo.png, favicon.ico)
    full_path = os.path.join(base_dir, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(base_dir, path)
        
    # Sometimes assets are requested relative to root e.g. /logo.png, let's catch it.
    # Check if it has no extension, maybe it is a static page (e.g. login -> login.html)
    _, ext = os.path.splitext(path)
    if not ext:
        html_path = f"{path}.html"
        if os.path.exists(os.path.join(base_dir, html_path)):
            return send_from_directory(base_dir, html_path)
        return send_from_directory(base_dir, 'index.html')
        
    return send_from_directory(base_dir, path)

# Add custom route to catch root level asset requests and redirect/serve from out directory
@app.route('/logo.png')
@app.route('/favicon.ico')
def serve_root_assets():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard-web', 'out')
    filename = request.path.lstrip('/')
    if os.path.exists(os.path.join(base_dir, filename)):
        return send_from_directory(base_dir, filename)
    return '', 404


@app.route('/')
def health_check():
    db_ok = None
    if ctx.IS_DB_CONNECTED:
        db_ok, _ = _maybe_ping_supabase_keep_alive()
    
    try:
        me = bot.get_me()
        bot_username = me.username if me else "unknown"
    except Exception as e:
        bot_username = f"error: {str(e)}"
        
    return {
        "status": "running",
        "bot_username": bot_username,
        "db_connected": ctx.IS_DB_CONNECTED,
        "db_keepalive_ok": db_ok
    }


@app.route('/health/db')
def health_db():
    ok, err = _maybe_ping_supabase_keep_alive(ttl_seconds=0)
    return {"ok": ok, "error": err}


@app.route('/health/ocr')
def health_ocr():
    ok = False
    err = None
    try:
        if ctx.ocr_service:
            warmup = str(request.args.get("warmup") or "").strip().lower() in {"1", "true", "yes", "y"}
            if warmup:
                ok = bool(ctx.ocr_service.load_model())
            else:
                ok = True
    except Exception as e:
        err = str(e)
    return {"ok": ok, "error": err}


@app.route('/api/diagnostic')
def api_diagnostic():
    import socket
    import requests
    
    results = {}
    
    # 1. Check Env Presence
    results["env"] = {
        "HAS_BOT_TOKEN": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "BOT_TOKEN_LEN": len(os.getenv("TELEGRAM_BOT_TOKEN") or ""),
        "HAS_SUPABASE_URL": bool(os.getenv("SUPABASE_URL")),
        "SUPABASE_URL_VAL": os.getenv("SUPABASE_URL"),
        "HAS_SUPABASE_KEY": bool(os.getenv("SUPABASE_KEY")),
        "SUPABASE_KEY_LEN": len(os.getenv("SUPABASE_KEY") or ""),
    }
    
    # 2. DNS Resolution Test
    dns = {}
    for host in ["api.telegram.org", "nfqkvdwdgmlxvqnkgtrf.supabase.co", "google.com"]:
        try:
            ip = socket.gethostbyname(host)
            dns[host] = f"OK: {ip}"
        except Exception as e:
            dns[host] = f"ERROR: {str(e)}"
    results["dns"] = dns
    
    # 3. HTTP Outbound Test
    http = {}
    for url in ["https://www.google.com", "https://api.telegram.org", "https://nfqkvdwdgmlxvqnkgtrf.supabase.co"]:
        try:
            r = requests.get(url, timeout=5)
            http[url] = f"OK (Status: {r.status_code})"
        except Exception as e:
            http[url] = f"ERROR: {str(e)}"
    results["http"] = http
    
    return jsonify(results)


@app.route("/telegram/webhook/<path_secret>", methods=["POST"])
def telegram_webhook(path_secret):
    expected_path = _get_webhook_path_secret()
    if not expected_path or path_secret != expected_path:
        return jsonify({"ok": False, "error": "Invalid webhook path"}), 403

    expected_header = _get_webhook_header_secret()
    if expected_header:
        got = (request.headers.get("X-Telegram-Bot-Api-Secret-Token") or "").strip()
        if got != expected_header:
            return jsonify({"ok": False, "error": "Invalid webhook token"}), 403
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "Invalid JSON"}), 400

    _start_webhook_worker_if_needed()
    _enqueue_update(data)
    return jsonify({"ok": True})

def run_scheduler():
    logger.info("[INIT] Scheduler thread started")
    # Setup schedules
    schedule.every().day.at("09:00").do(
        auto_reminder.jalankan_notifikasi_reminder,
        bot=bot,
        admin_ids=AUTHORIZED_ADMINS
    )
    schedule.every(3).days.do(ping_supabase_keep_alive)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_bot():
    logger.info("[INIT] Starting Telegram Bot in background thread...")
    try:
        use_webhook = _env_bool("USE_WEBHOOK", False) or _env_bool("TELEGRAM_USE_WEBHOOK", False)
        preload = _env_bool("OCR_PRELOAD_ON_START", False)
        is_hf = bool(
            os.getenv("SPACE_ID")
            or os.getenv("HF_SPACE_ID")
            or os.getenv("SPACE_HOST")
            or os.getenv("HF_HOME")
        )
        if preload and ctx.ocr_service:
            logger.info("[INIT] Pre-loading OCR model...")
            ctx.ocr_service.load_model()
        
        # Hapus menu button
        try:
            from telebot.types import MenuButtonDefault
            bot.set_chat_menu_button(menu_button=MenuButtonDefault(type="default"))
            logger.info("[INIT] Menu Button berhasil dihapus!")
        except Exception as e:
            logger.warning(f"[INIT] Gagal hapus Menu Button: {e}")
        
        if use_webhook:
            path_secret = _get_webhook_path_secret()
            if not path_secret:
                raise RuntimeError("TELEGRAM_WEBHOOK_PATH_SECRET belum di-set (wajib untuk webhook).")
            webhook_url = _build_webhook_url()
            if not webhook_url:
                raise RuntimeError("WEBHOOK_URL/TELEGRAM_WEBHOOK_URL atau SPACE_HOST belum tersedia untuk webhook.")

            secret_token = _get_webhook_header_secret()
            try:
                bot.remove_webhook()
            except Exception:
                pass
            try:
                if secret_token:
                    bot.set_webhook(url=webhook_url, secret_token=secret_token)
                else:
                    bot.set_webhook(url=webhook_url)
            except TypeError:
                bot.set_webhook(url=webhook_url)

            _start_webhook_worker_if_needed()
            logger.info(f"[WEBHOOK] Enabled: {webhook_url}")

        # Notifikasi ke Admin
        for admin_id in AUTHORIZED_ADMINS:
            try:
                if is_hf:
                    teks = "🚀 <b>Bot AW Production Berhasil Deploy ke Hugging Face!</b>\n\nSistem siap digunakan."
                else:
                    teks = "✅ <b>Bot AW Production Berhasil Dijalankan.</b>\n\nSistem siap digunakan."
                bot.send_message(admin_id, teks, parse_mode="HTML")
            except:
                pass

        if use_webhook:
            while True:
                time.sleep(3600)
        else:
            try:
                bot.remove_webhook()
            except Exception:
                pass
            # Skip pending messages from before restart to avoid 409 conflict
            # Retry with backoff if 409 conflict occurs (old instance still running in Telegram API)
            retry_count = 0
            max_retries = 5
            while retry_count < max_retries:
                try:
                    bot.infinity_polling(timeout=60, long_polling_timeout=30, skip_pending=True)
                    break
                except Exception as poll_error:
                    if "409" in str(poll_error) or "Conflict" in str(poll_error):
                        retry_count += 1
                        wait_time = min(30, 5 * retry_count)  # Exponential backoff: 5, 10, 15, 20, 25, 30 sec
                        logger.warning(f"[TELEGRAM 409] Bot conflict detected. Waiting {wait_time}s before retry ({retry_count}/{max_retries})...")
                        time.sleep(wait_time)
                    else:
                        raise
    except Exception as e:
        import traceback
        logger.error(f"[FATAL] Bot error: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    # Start scheduler thread
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Start bot thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Start Flask server for Hugging Face (Port 7860)
    port = int(os.environ.get("PORT", 7860))
    logger.info(f"[OK] Web Server running on port {port}")
    app.run(host='0.0.0.0', port=port)
