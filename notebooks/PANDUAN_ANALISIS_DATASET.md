# Panduan Analisis Dataset untuk Laporan Penelitian

Berikut adalah panduan LENGKAP untuk menggunakan dataset dan notebook analisis!

---

## 📦 File yang Telah Disiapkan:

### Di Folder `files/`:
Semua dataset Anda sekarang sudah disimpan di sini:
1. `nlp_normalization_dict.json`: Kamus koreksi typo, sinonim, dan singkatan
2. `nlp_dataset.json`: Dataset contoh kalimat per intent
3. `nlp_dataset.csv`: Dataset training dengan label entity
4. `valid_units.txt`: Daftar satuan produk yang valid

### Di Folder `notebooks/`:
Notebook untuk analisis dan laporan:
1. `01_Evaluasi_NLP_OCR.ipynb`: Evaluasi model NLP dan OCR
2. `02_Analisis_Dataset_Lengkap.ipynb`: Analisis dataset secara menyeluruh (untuk laporan)
3. `PANDUAN_ANALISIS_DATASET.md`: File ini

---

## 🚀 Cara Menggunakan:

### 1. Pastikan Semua Dataset Sudah Diekstrak
Jalankan script ini (jika belum):
```powershell
python scripts/export_datasets.py
```

### 2. Buka Notebook Analisis
1. Jalankan Jupyter Lab:
   ```powershell
   jupyter lab
   ```
2. Di Jupyter Lab, buka: `notebooks/02_Analisis_Dataset_Lengkap.ipynb`
3. Klik `Cell` → `Run All` untuk melihat semua analisis dan visualisasi!

---

## 📊 Apa yang Ada di Notebook Analisis:

Notebook `02_Analisis_Dataset_Lengkap.ipynb` berisi:
1. **Analisis Normalization Dataset**: Statistik dan contoh typo, sinonim, dan singkatan
2. **Analisis Intent Patterns**: Distribusi jumlah contoh kalimat per intent
3. **Analisis Training Dataset**: Statistik panjang kalimat dan distribusi intent
4. **Visualisasi**: Banyak grafik dan diagram yang siap dimasukkan ke laporan!
5. **Ringkasan Statistik**: Tabel ringkasan semua dataset yang dapat disalin langsung ke laporan

---

## 📝 Tips untuk Laporan Penelitian:

1. **Simpan Visualisasi**: Klik kanan pada grafik → `Save Image As...` untuk menyimpan sebagai gambar
2. **Ekspor Notebook**: `File` → `Export Notebook As...` → `HTML` atau `PDF` untuk lampiran laporan
3. **Salin Tabel**: Klik dan salin tabel data dari notebook ke laporan Anda

---

## 📂 Struktur Folder:
```
BOT/
├── files/                          # Semua dataset disini
│   ├── nlp_normalization_dict.json
│   ├── nlp_dataset.json
│   ├── nlp_dataset.csv
│   └── valid_units.txt
├── notebooks/                      # Notebook analisis
│   ├── 01_Evaluasi_NLP_OCR.ipynb
│   ├── 02_Analisis_Dataset_Lengkap.ipynb
│   ├── PANDUAN_ANALISIS_DATASET.md
│   └── README.md
├── scripts/
│   └── export_datasets.py          # Script export dataset
└── ...
```

---

Semoga bermanfaat untuk penelitian Anda! 🎉
