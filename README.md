---
title: AW Production Bot
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AW Production Telegram Bot

Sistem POS (Point of Sales) dan Kasir otomatis menggunakan Telegram Bot, Supabase, dan PaddleOCR.

## Fitur Utama
- 📸 **OCR Otomatis**: Mencatat pesanan langsung dari foto nota/list pesanan.
- 💰 **Manajemen Hutang**: Tracking cicilan dan sisa hutang pelanggan.
- 📊 **Laporan Real-time**: Dashboard transaksi harian dan bulanan.
- ☁️ **Cloud Native**: Deploy siap pakai di Hugging Face Spaces (Docker).

## Variabel Lingkungan (Secrets)
Pastikan Anda mengatur variabel berikut di Hugging Face Settings:
- `TELEGRAM_BOT_TOKEN`: Token dari BotFather.
- `TELEGRAM_BOT_ADMIN_IDS`: ID Telegram Admin (pisahkan dengan koma).
- `SUPABASE_URL`: URL project Supabase Anda.
- `SUPABASE_KEY`: API Key (Service Role lebih disarankan untuk backend).

## Deployment
Bot ini menggunakan Docker untuk menangani dependensi PaddleOCR. Entry point utama adalah `app.py` yang menjalankan Flask server (port 7860) dan bot di background.

## Dashboard Web (Next.js)
Untuk menjalankan dashboard modern dengan Next.js:
1. Navigasi ke direktori `dashboard-web/`
2. Install dependensi: `npm install`
3. Jalankan dev server: `npm run dev`
4. Akses di browser: [http://localhost:3000](http://localhost:3000)
