# Panduan Bukti Preprocessing & Proses OCR

Dokumen ini menjelaskan cara menggunakan sistem bukti preprocessing dan OCR untuk keperluan penelitian.


## Struktur Bukti yang Dihasilkan

Setelah menjalankan proses, Anda akan mendapatkan file bukti di direktori `ocr_preprocessing_proof/`:

| No | Nama File | Keterangan |
|----|-----------|------------|
| 1 | `nama_file_01_original.png` | Gambar asli sebelum preprocessing |
| 2 | `nama_file_02_resized.png` | Hasil langkah 1: Resize gambar |
| 3 | `nama_file_03_padded.png` | Hasil langkah 2: Padding gambar |
| 4 | `nama_file_04_color_normalized.png` | Hasil langkah 3: Konversi & normalisasi warna |
| 5 | `nama_file_05_deskewed.png` | Hasil langkah 4: De-skewing (koreksi kemiringan) |
| 6 | `nama_file_06_ocr_visualization.png` | Bukti proses OCR: bounding box, teks, skor akurasi |


## Cara Menggunakan

### 1. Menggunakan Script Demo

```bash
python scripts/test_ocr_preprocessing.py
```

Script ini akan:
- Mencari gambar contoh di direktori `files/`
- Menjalankan preprocessing + OCR
- Menyimpan semua bukti di direktori `ocr_preprocessing_proof/`
- Menampilkan ringkasan hasil


### 2. Menggunakan dalam Kode Anda Sendiri

```python
from services.ocr_service import OCRService

# Inisialisasi OCR Service
ocr = OCRService(preprocessor_output_dir="bukti_penelitian_saya")

# Jalankan OCR dengan bukti lengkap
teks_hasil, bukti = ocr.extract_text_with_preprocessing_proof(
    image_path="gambar_anda.jpg",
    base_filename="penelitian_001"
)

# Akses bukti
print("Teks OCR:", teks_hasil)
print("Path bukti OCR:", bukti["06_ocr_visualization"]["image_path"])
```


## Keterangan Visualisasi OCR (`*_06_ocr_visualization.png`)

Pada gambar bukti OCR, Anda akan melihat:

- **Kotak Hijau**: Bounding box (area teks yang terdeteksi)
- **Teks Biru**: Teks yang berhasil diekstraksi
- **Angka Merah**: Skor akurasi/confidence (0.00 - 1.00, semakin tinggi semakin baik)
- **Info di Sudut Kiri Atas**:
  - Total kotak teks yang terdeteksi
  - Rata-rata skor akurasi


## Contoh Penggunaan untuk Penelitian

Anda bisa memasukkan gambar-gambar bukti ini ke dalam laporan penelitian pada bagian:
1. **Metodologi**: Menjelaskan langkah preprocessing yang dilakukan
2. **Hasil**: Menampilkan contoh visualisasi OCR dan perbandingan sebelum/sesudah preprocessing
3. **Analisis**: Membahas skor akurasi dan efektivitas preprocessing


## Modifikasi Parameter Preprocessing

Jika ingin mengubah parameter preprocessing (misal ukuran resize, padding, dll.), edit file `services/ocr_preprocessor.py`:

- `resize_image()`: Ubah `max_width` atau `target_size`/`scale_factor`
- `pad_image()`: Ubah `padding_size` atau `padding_color`
- `convert_and_normalize_color()`: Ubah parameter CLAHE
- `deskew_image()`: Ubah threshold sudut rotasi
