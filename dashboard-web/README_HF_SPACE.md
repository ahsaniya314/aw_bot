# AW Production Dashboard 🚀

Dashboard web untuk sistem manajemen transaksi AW Production, dibangun dengan Next.js dan di-deploy ke Hugging Face Spaces menggunakan Docker.

---

## Cara Deploy ke Hugging Face Spaces (Dengan Docker)

### 1. Buat Hugging Face Account

- Daftar/login di [huggingface.co](https://huggingface.co/)

### 2. Buat Space Baru

1. Klik **Spaces** di menu atas
2. Klik **Create new Space**
3. Isi form:
   - **Space name**: `aw-dashboard` (atau nama yang kamu inginkan)
   - **License**: Pilih sesuai kebutuhan (misal: MIT)
   - **Space SDK**: Pilih **Docker**
   - **Visibility**: Pilih **Public** atau **Private**
4. Klik **Create Space**

### 3. Push Kode ke Space

Setelah Space dibuat, kamu akan melihat instruksi Git. Jalankan di terminal:

```bash
cd dashboard-web

# Tambahkan remote Hugging Face (ganti USERNAME dan SPACE_NAME)
git remote add hf https://huggingface.co/spaces/USERNAME/aw-dashboard

# Push ke HF Spaces
git push hf main
```

**Ganti `USERNAME` dengan username Hugging Face kamu, dan `SPACE_NAME` sesuai nama Space!**

### 4. Tunggu Build & Deploy

Hugging Face akan otomatis build Docker image dan deploy proyek kamu. Tunggu beberapa menit (biasanya 3-7 menit)!

### 5. Selesai! 🎉

Dasbor kamu akan live di: `https://huggingface.co/spaces/USERNAME/aw-dashboard`

---

## Cara Mendapatkan Token Push (Jika Diminta)

1. Buka [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Klik **New token**
3. Isi name: `dashboard-deploy`
4. Role: **write**
5. Klik **Generate a token**
6. Salin token tersebut, gunakan sebagai **password** saat push!

---

## Local Development

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
```

---

## Fitur

- Dashboard ringkasan transaksi (data dummy untuk demo)
- Grafik tren penjualan
- Daftar transaksi terbaru
- Top pelanggan
