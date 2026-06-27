# Panduan Deployment ke Hugging Face Spaces

Berikut adalah langkah demi langkah untuk mendeploy bot sistem Anda ke Hugging Face Spaces!

---

## 📋 Prasyarat
1. Akun Hugging Face (https://huggingface.co/join)
2. Token Bot Telegram dari @BotFather
3. Project Supabase beserta URL dan Service Role Key
4. Git repository (opsional tapi disarankan)

---

## 🚀 Langkah-langkah Deployment

### 1. Buat Space Baru di Hugging Face
1. Buka https://huggingface.co/spaces
2. Klik **Create new Space**
3. Isi detail Space:
   - **Space name**: Misal `aw-production-bot`
   - **Owner**: Pilih akun Anda
   - **License**: Pilih sesuai kebutuhan (misal MIT)
   - **SDK**: Pilih **Docker**
   - **Docker template**: Pilih **Blank**
4. Klik **Create Space**

### 2. Atur Secrets/Variabel Lingkungan
Di halaman Space Anda, buka tab **Settings** → **Variables and secrets**:
Klik **New secret** untuk menambahkan variabel berikut:

| Nama Secret | Nilai |
|-------------|-------|
| `TELEGRAM_BOT_TOKEN` | Token bot Anda dari @BotFather |
| `TELEGRAM_BOT_ADMIN_IDS` | ID Telegram admin (pisahkan dengan koma, misal: `123456789,987654321`) |
| `SUPABASE_URL` | URL project Supabase Anda |
| `SUPABASE_KEY` | **Service Role Key** Supabase (jangan gunakan Public Key!) |

*(Opsional)* Jika ingin menggunakan Webhook (lebih stabil untuk Hugging Face):
| Nama Secret | Nilai |
|-------------|-------|
| `USE_WEBHOOK` | `true` |
| `TELEGRAM_WEBHOOK_PATH_SECRET` | String rahasia untuk path webhook (misal: `my-super-secret-path-123`) |

### 3. Upload Kode ke Space
Anda punya dua pilihan:

#### Opsi A: Upload via Git (Direkomendasikan)
1. Di halaman Space Anda, copy URL Git repository (contoh: `https://huggingface.co/spaces/username/aw-production-bot`)
2. Di folder proyek lokal Anda:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add space https://huggingface.co/spaces/username/aw-production-bot
   git push -u space main
   ```
3. Anda akan diminta login: gunakan **Username Hugging Face** dan **Access Token** (buat token di https://huggingface.co/settings/tokens → buat token dengan izin `write`)

#### Opsi B: Upload Manual via UI
1. Di halaman Space Anda, klik tab **Files and versions**
2. Klik **Upload files**
3. Drag & drop semua file proyek Anda (kecuali folder/node_modules, .venv, dll.)
4. Klik **Commit changes**

### 4. Tunggu Build Selesai
Setelah kode diupload, Hugging Face akan otomatis build Docker image.
- Anda bisa melihat progress di tab **Logs**
- Jika berhasil, status Space akan menjadi **Running**
- Bot akan mengirim pesan notifikasi ke admin jika deployment berhasil!

---

## 🔧 Troubleshooting Umum

### Error: "Invalid API key" Supabase
Pastikan Anda menggunakan **Service Role Key**, bukan Public Key!
Dapatkan di: Supabase Dashboard → Project Settings → API → Service Role

### Error: PaddleOCR tidak berjalan
Pastikan `Dockerfile` sudah menyertakan dependensi sistem:
- `libgl1-mesa-glx`
- `libglib2.0-0`
- `libsm6`
- `libxext6`
- `libxrender-dev`
- `libgomp1`

### Bot tidak merespon?
- Cek apakah Space statusnya **Running**
- Cek logs di tab **Logs** Space Anda
- Pastikan token bot Telegram benar

---

## 📱 Menggunakan Bot
Setelah deployment berhasil:
1. Cari bot Anda di Telegram (username sesuai yang Anda set di @BotFather)
2. Mulai chat dengan `/start`
3. Bot siap digunakan!

---

## 🌐 Menghubungkan Dashboard Vercel dengan Backend HF
Setelah backend berhasil di-deploy di Hugging Face:
1. Dapatkan URL Space Anda (contoh: `https://username-aw-production-bot.hf.space`)
2. Buka project Vercel Anda → Settings → Environment Variables
3. Ubah `NEXT_PUBLIC_API_URL` menjadi URL Space Hugging Face Anda
4. Redeploy dashboard Vercel
