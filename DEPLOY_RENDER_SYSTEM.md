# Panduan Mudah Deploy Bot & Dashboard ke Render.com 🚀

Panduan ini dibuat sesederhana mungkin agar Anda bisa men-deploy (mengonlinekan) **AW Production Bot** dan **Dashboard Web** Anda ke Render.com dengan mudah.

---

## 🗺️ Gambaran Sederhana Cara Kerja
Sistem Anda dibagi menjadi 2 bagian yang berjalan secara otomatis:
1. **Backend (Bot Telegram & Database Connector)**: Berjalan di Render sebagai *Web Service* menggunakan Docker (agar sistem membaca gambar nota bisa bekerja).
2. **Frontend (Dashboard Web)**: Berjalan di Render sebagai *Static Site* (Gratis dan super cepat).

---

## 🔧 Langkah 1: Deploy Backend (Bot Telegram)

Bagian ini penting agar Bot Telegram Anda bisa membalas chat dan memproses gambar nota.

### A. Persiapan awal
1. Pastikan kode Anda sudah di-upload ke **GitHub** Anda.
2. Siapkan token bot dari `@BotFather` dan akun **Supabase** Anda.

### B. Cara Setup di Render.com
1. Masuk ke [Render.com](https://render.com) dan buat akun/login.
2. Klik tombol **New +** (warna biru di kanan atas) lalu pilih **Web Service**.
3. Hubungkan akun GitHub Anda dan pilih repository bot Anda.
4. Isi data berikut pada formulir:
   * **Name**: `bot-backend` (atau nama bebas)
   * **Region**: `Singapore` (paling cepat untuk pengguna Indonesia)
   * **Runtime**: Pilih **Docker** (Render otomatis mendeteksi file Docker yang sudah ada)
   * **Instance Type**: Pilih **Free**

### C. Mengisi Kunci Rahasia (Environment Variables)
Scroll ke bawah, klik tombol **Advanced**, lalu cari bagian **Environment Variables**. Masukkan kunci-kunci berikut:

| Nama Kunci | Isi / Value |
| :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Token bot Anda dari `@BotFather` |
| `TELEGRAM_BOT_ADMIN_IDS` | ID Telegram Anda (contoh: `12345678`) |
| `SUPABASE_URL` | URL Supabase Anda |
| `SUPABASE_KEY` | *Service Role Key* Supabase Anda |
| `OCR_PRELOAD_ON_START` | Tulis `false` (supaya server hemat RAM) |

5. Klik tombol **Create Web Service** di paling bawah.
6. Tunggu 5-10 menit sampai proses build selesai dan statusnya berubah menjadi **Live**.

---

## 🖥️ Langkah 2: Deploy Frontend (Dashboard Web)

Bagian ini agar Anda bisa melihat grafik penjualan dan hutang lewat web browser.

### A. Cara Setup di Render.com
1. Klik tombol **New +** lagi di Render dashboard, lalu pilih **Static Site**.
2. Pilih repository GitHub Anda yang sama.
3. Isi data berikut pada formulir:
   * **Name**: `bot-dashboard`
   * **Root Directory**: Tulis `dashboard-web` (ini sangat penting!)
   * **Build Command**: Tulis `npm install && npm run build`
   * **Publish Directory**: Tulis `out`

### B. Menghubungkan ke Backend
Di bagian bawah formulir, tambahkan **Environment Variable** berikut:

* **Key**: `NEXT_PUBLIC_API_URL`
* **Value**: URL backend yang Anda dapatkan dari Langkah 1 (contoh: `https://bot-backend.onrender.com`)

4. Klik **Create Static Site**. Tunggu 2-3 menit hingga selesai.

---

## 📊 Hasil yang Didapatkan & Cara Tes

Setelah semua proses selesai (status berubah jadi **Live**), Anda akan mendapatkan hasil berikut:

1. **Bot Telegram Aktif**:
   * Cari bot Anda di Telegram, lalu ketik `/start`. Bot akan langsung membalas.
   * Admin akan mendapatkan pesan otomatis: `"✅ Bot AW Production Berhasil Dijalankan."`
2. **Dashboard Web Bisa Diakses**:
   * Klik link website yang diberikan oleh Render di Langkah 2 (misalnya `https://bot-dashboard.onrender.com`).
   * Website dashboard akan langsung menampilkan tabel transaksi Anda.

---

## 💡 Tips Penting
> [!IMPORTANT]
> Karena menggunakan layanan **Free (Gratis)** dari Render, bot Anda akan otomatis "tertidur" jika tidak ada aktivitas selama 15 menit. Jika bot tertidur, respon pertamanya akan lambat (sekitar 50 detik) karena bot harus bangun terlebih dahulu.
>
> **Trik agar Bot tidak pernah tidur gratisan:**
> Gunakan layanan gratis seperti [UptimeRobot](https://uptimerobot.com) untuk otomatis mengunjungi link API backend Anda (contoh: `https://bot-backend.onrender.com/api/keepalive`) setiap 10 menit sekali. Dengan begitu, bot akan aktif terus 24 jam!
