# Panduan Evaluasi Model NLP dan OCR dari Awal sampai Akhir!

Berikut adalah langkah demi langkah untuk menguji akurasi model NLP dan OCR Anda menggunakan Jupyter Lab!

---

## 🚀 Langkah 1: Instal Dependensi

Pertama, kita install semua dependensi yang dibutuhkan (termasuk Jupyter Lab dan library visualisasi):

### Windows (PowerShell):
```powershell
# 1. Pastikan Anda berada di folder proyek
cd c:\Users\FINN\Documents\BOT

# 2. Aktifkan virtual environment (jika ada)
.\.venv\Scripts\Activate.ps1

# 3. Install dependensi dev (termasuk Jupyter Lab)
pip install -e .[dev]
```

---

## 🚀 Langkah 2: Buat Folder Sample Images (Untuk OCR)

Jika Anda ingin mengevaluasi OCR, buat folder `sample_images` dan tarik beberapa gambar nota/contoh:

```powershell
# Di folder proyek:
mkdir sample_images
```

Kemudian, tarik gambar nota (contoh: struk toko, nota transaksi) ke dalam folder ini!

---

## 🚀 Langkah 3: Jalankan Jupyter Lab!

Setelah semua dependensi terinstal, jalankan Jupyter Lab dengan perintah berikut:

```powershell
jupyter lab
```

Ini akan membuka browser Anda secara otomatis di alamat `http://localhost:8888/`!

---

## 🚀 Langkah 4: Buka dan Jalankan Notebook

Di Jupyter Lab:
1. Klik folder `notebooks` di sidebar kiri
2. Buka file `01_Evaluasi_NLP_OCR.ipynb`
3. Jalankan cell satu per satu dengan tombol `Shift + Enter` atau tombol ▶️ di toolbar!

---

## 📊 Apa yang Akan Anda Dapatkan dari Notebook?

Dari notebook ini, Anda akan mendapatkan:
1. **Akurasi model NLP**: Berapa persen intent yang bisa diprediksi dengan benar!
2. **Contoh salah prediksi**: Intent mana yang sering salah, sehingga Anda bisa menambah contoh kalimat!
3. **Confusion matrix**: Lihat intent mana yang sering tertukar!
4. **Demo OCR**: Coba proses gambar nota Anda sendiri dan lihat apakah teks bisa diekstrak dengan benar!

---

## 🔧 Cara Meningkatkan Performa NLP

Jika akurasi NLP masih rendah:
1. Lihat "Contoh salah prediksi" di notebook!
2. Tambahkan contoh kalimat yang sering salah ke `files/nlp_dataset.json` atau `files/nlp_dataset.csv`
3. Regenerate `nlp/embedded_data.py` dengan:
   ```powershell
   python scripts/embed_nlp_data.py
   ```

---

Selamat mencoba! 🎉
