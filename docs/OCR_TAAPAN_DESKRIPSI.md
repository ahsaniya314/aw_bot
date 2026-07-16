# Deskripsi Tahapan OCR

## d. Pencocokan Pola dan Ekstraksi Fitur

### Pencocokan Pola (Pattern Matching)

**Definisi:**
Pencocokan Pola adalah tahapan dalam proses OCR di mana software mengisolasi citra karakter (glyph) dan membandingkannya dengan glyph yang tersimpan dalam database sistem. Font dan skala dalam gambar akan dicocokkan dengan pola yang dikenali.

**Proses:**
1. **Segmentasi Karakter** - Memisahkan setiap karakter dari teks yang terdeteksi
2. **Isolasi Glyph** - Mengambil citra visual masing-masing karakter
3. **Database Matching** - Membandingkan glyph dengan database font yang tersimpan
4. **Font Recognition** - Mengidentifikasi jenis font dan skala yang digunakan
5. **Pattern Validation** - Memvalidasi apakah pola sesuai dengan karakter yang dikenali

**Tujuan:**
- Mengidentifikasi karakter berdasarkan bentuk visualnya
- Mencocokkan font dan skala untuk meningkatkan akurasi
- Membedakan karakter yang mirip (misal: '0' vs 'O', '1' vs 'l')

**Catatan Penting:**
Proses ini akan berjalan dengan baik bila font yang digunakan dalam gambar merupakan font yang umum digunakan dan tersedia dalam database OCR.

---

### Ekstraksi Fitur (Feature Extraction)

**Definisi:**
Ekstraksi Fitur adalah tahapan OCR di mana glyph diurai menjadi fitur-fitur spesifik seperti garis, lengkungan, dan perpotongan garis. Fitur-fitur tersebut kemudian dicocokkan dengan beragam glyph yang telah tersimpan sebelumnya.

**Proses:**
1. **Line Detection** - Mendeteksi garis lurus dalam karakter
2. **Curve Detection** - Mengidentifikasi lengkungan dan kurva
3. **Intersection Analysis** - Menganalisis perpotongan garis
4. **Feature Vector Generation** - Membuat vektor fitur yang merepresentasikan karakter
5. **Feature Matching** - Mencocokkan vektor fitur dengan database glyph

**Fitur yang Diekstrak:**
- **Garis (Lines)** - Garis horizontal, vertikal, dan diagonal
- **Lengkungan (Curves)** - Kurva dan lingkaran
- **Perpotongan (Intersections)** - Titik di mana garis bertemu
- **Titik Akhir (Endpoints)** - Ujung dari garis atau kurva
- **Luas Area (Area)** - Ukuran area karakter
- **Rasio Aspek (Aspect Ratio)** - Perbandingan lebar dan tinggi

**Tujuan:**
- Mengubah citra visual menjadi data numerik yang dapat diproses
- Meningkatkan akurasi pengenalan dengan analisis geometri
- Memungkinkan pengenalan karakter dengan font yang tidak umum
- Membantu membedakan karakter yang secara visual mirip

---

## Hubungan Antara Pencocokan Pola dan Ekstraksi Fitur

Pencocokan Pola dan Ekstraksi Fitur adalah dua pendekatan komplementer dalam OCR:

| Pendekatan | Metode | Kelebihan |
|------------|--------|-----------|
| **Pencocokan Pola** | Template matching (membandingkan dengan database) | Cepat untuk font yang umum |
| **Ekstraksi Fitur** | Analisis geometri (menganalisis struktur karakter) | Akurat untuk font yang bervariasi |

Keduanya digunakan bersama untuk meningkatkan akurasi pengenalan teks, terutama untuk:
- Dokumen dengan font yang bervariasi
- Kualitas gambar yang rendah
- Karakter yang secara visual mirip
- Dokumen dengan layout yang kompleks

---

## Catatan Teknis

Dalam implementasi sistem OCR ini:
- **Pencocokan Pola** diimplementasikan dalam `step4_pencocokan_pola()`
- **Ekstraksi Fitur** diimplementasikan dalam `step5_ekstraksi_fitur()`
- Keduanya menggunakan output dari tahap Pengenalan Teks
- Hasilnya disimpan dalam laporan JSON untuk dokumentasi dan analisis
