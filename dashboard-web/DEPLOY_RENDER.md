# Panduan Deploy ke Render (Bos Kocak) 🚀

Panduan lengkap deploy dasbor web ke Render.com

---

## Prasyarat

1. Akun Render (daftar di [render.com](https://render.com)) - FREE tier available!
2. Repository GitHub/GitLab/Bitbucket (sudah di-push)
3. Dasbor web sudah siap di folder `dashboard-web/`

---

## Langkah 1: Push ke GitHub/GitLab (Jika Belum)

Pastikan kode sudah di-push ke repository:

```bash
cd dashboard-web
git add .
git commit -m "Siap deploy ke Render"
git push origin main
```

---

## Langkah 2: Buat Web Service di Render

1. Buka [dashboard.render.com](https://dashboard.render.com)
2. Klik tombol **"New +"** → Pilih **"Web Service"**
3. Hubungkan akun GitHub/GitLab Anda (jika belum)
4. Pilih repository yang berisi dasbor web Anda
5. Klik **"Connect"**

---

## Langkah 3: Konfigurasi Web Service

Isi form dengan data berikut:

| Field | Value |
|-------|-------|
| **Name** | `dashboard-aw-production` (atau nama bebas) |
| **Region** | Pilih yang terdekat (misal: Singapore) |
| **Branch** | `main` |
| **Root Directory** | `dashboard-web` (ini penting!) |
| **Runtime** | `Node` |
| **Build Command** | `npm install && npm run build` |
| **Start Command** | `npx next start -p $PORT` |
| **Instance Type** | Pilih **Free** (untuk hemat!) |

---

## Langkah 4: Advanced (Opsional)

Jika butuh environment variables:
1. Klik **"Advanced"**
2. Tambahkan variables seperti:
   - `NODE_ENV`: `production`
3. Klik **"Add Environment Variable"**

---

## Langkah 5: Deploy!

1. Klik tombol **"Create Web Service"**
2. Tunggu beberapa menit (Render sedang build dan deploy)
3. Setelah selesai, Anda akan mendapatkan URL seperti:
   - `https://dashboard-aw-production.onrender.com`

---

## Struktur Root Directory Penting!

Pastikan di repository Anda:
```
your-repo/
├── dashboard-web/          <-- Root directory di Render
│   ├── src/
│   │   └── app/
│   ├── package.json
│   └── next.config.ts
└── (file/folder lain boleh ada)
```

---

## Troubleshooting Bos Kocak!

### Masalah 1: Build Gagal - Path Salah
**Solusi**: Pastikan **Root Directory** diisi dengan `dashboard-web` (huruf kecil semua!)

### Masalah 2: Port Error
**Solusi**: Pastikan **Start Command** adalah `npx next start -p $PORT` (JANGAN gunakan port tetap seperti 3000!)

### Masalah 3: Module Not Found
**Solusi**: Pastikan semua dependencies ada di `package.json` dan `.gitignore` tidak mengabaikan `node_modules` (biarkan saja `.gitignore` default Next.js)

### Masalah 4: Lama Banget Buildnya
**Solusi**: Normal untuk free tier, sabar bos! Atau upgrade ke paid plan kalo butuh lebih cepet.

---

## Setelah Deploy Berhasil!

1. Buka URL yang diberikan Render
2. Test semua fitur dasbor
3. Bagikan ke temen-temen! 😎

---

## Tips Penting Bos Kocak!

1. **Auto-Deploy**: Setiap push ke `main` branch, Render otomatis deploy ulang!
2. **Custom Domain**: Bisa menambahkan domain sendiri di tab **"Settings" → "Custom Domains"**
3. **Logs**: Lihat log build/deploy di tab **"Logs"** untuk debugging
4. **Free Tier Limitation**: Akan sleep jika tidak ada traffic selama 15 menit, tapi akan wake up saat diakses

---

## File Penting yang Sudah Dioptimalkan

- [next.config.ts](file:///c:/Users/FINN/Documents/BOT/dashboard-web/next.config.ts) - Konfigurasi untuk Render
- [package.json](file:///c:/Users/FINN/Documents/BOT/dashboard-web/package.json) - Script build & start

---

Selamat deploy bos kocak! 🎉 Semoga lancar jaya!
