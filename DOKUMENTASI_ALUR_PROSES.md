# Panduan Alur Pemrosesan Data NLP

Dokumen ini menjelaskan secara detail bagaimana data diproses saat ada input masuk ke sistem.

---

## 📋 Ringkasan Alur Proses

```
Input Teks Mentah
    ↓
[1] Pemisahan Multi-Entry
    ↓
[2] Text Cleaning & Normalization
    ↓
[3] Fuzzy Matching (Levenshtein Distance)
    ↓
[4] Ekstraksi Entitas (Regex)
    ↓
[5] Penentuan Intent
    ↓
[6] Post-Processing & Override
    ↓
[7] Penyusunan Data Transaksi
    ↓
[8] Simpan ke Database
```

---

## 🔍 Detail Setiap Langkah

### 1️⃣ Input Data
**Deskripsi**: Menerima teks mentah dari pengguna (bisa dari chat, OCR, dll.)

**Contoh Input**:
```
"hari ini pak andi pesan permen 10 dus lunas tunai"
```

---

### 2️⃣ Pemisahan Multi-Entry (`split_multi_entries`)
**File**: `nlp/processor.py`

**Fungsi**: Memisahkan teks yang berisi multiple transaksi menjadi entri terpisah.

**Pemisah yang Didukung**:
- Koma (`,`)
- Titik koma (`;`)
- Baris baru (`\n`)
- Pipe (`|`)
- Kata "dan" (jika diikuti penunjuk waktu)
- Perubahan tanggal

**Contoh**:
```
Input:  "permen 10 dus, meses 5 bungkus"
Output: ["permen 10 dus", "meses 5 bungkus"]
```

---

### 3️⃣ Text Cleaning & Lowercase
**File**: `nlp/extractor.py` (bagian slang preprocessor)

**Fungsi**:
- Konversi seluruh teks ke huruf kecil
- Normalisasi slang (misal: "trf" → "transfer", "sdh" → "sudah")
- Koreksi leet speak (misal: "5o" → "50")
- Menghapus karakter yang tidak perlu

**Contoh Normalisasi Slang**:
| Slang | Normal |
|-------|--------|
| trf | transfer |
| tf | transfer |
| sdh | sudah |
| udh | sudah |
| blm | belum |
| rb | ribu |
| jt | juta |
| bsk | besok |
| kmrn | kemarin |

---

### 4️⃣ Tokenization & Fuzzy Matching (`koreksi_teks`)
**File**: `nlp/normalizer.py`

#### 4.1 Dictionary Lookup
Pertama, sistem memeriksa apakah kata ada di **`NORMALIZATION_DICT`**:
- `typo_corrections`: Koreksi typo umum
- `abbreviations`: Singkatan
- `synonyms`: Sinonim

#### 4.2 Levenshtein Distance
Menggunakan **`rapidfuzz`** untuk menghitung jarak edit antara kata input dengan kata di kamus:

```python
# Menggunakan fuzz.ratio untuk menghitung similarity
similarity = fuzz.ratio(input_word, dictionary_word)
```

**Threshold**:
- Bigram (2 kata): ≥ 90
- Unigram (1 kata): ≥ 85

#### 4.3 Perhitungan Similarity Score
- Score 0-100
- Semakin tinggi semakin mirip
- Hanya kata yang melebihi threshold yang dikoreksi

**Contoh**:
```
Input:  "prmen"
Look up: ["permen", "coklat", ...]
Similarity: fuzz.ratio("prmen", "permen") → 90+
Output: "permen"
```

---

### 5️⃣ Ekstraksi Entitas (`ekstrak_entitas`)
**File**: `nlp/extractor.py`

Menggunakan **Regex** untuk mengekstrak entitas penting:

#### Entitas yang Diekstrak:

| Entitas | Deskripsi | Contoh Pola Regex |
|---------|-----------|-------------------|
| **TANGGAL** | Tanggal transaksi | `\d{1,2}/\d{1,2}/\d{2,4}`, "hari ini", "kemarin" |
| **NAMA** | Nama pelanggan | `(pak\|bu\|mas\|mbak)\s+([a-z]+)` |
| **AKSI** | Aksi yang dilakukan | "tambah", "pesan", "laporan", "hapus" |
| **BARANG** | Nama barang | Dari `KAMUS_ALIAS` atau Master Data |
| **JUMLAH** | Kuantitas barang | `(\d+)\s*(dus\|pcs\|toples\|...)` |
| **HARGA** | Harga satuan | `harga\s*(?:rp\s*)?([\d\.,]+)` |
| **TOTAL** | Total harga | `total\s*(?:rp\s*)?([\d\.,]+)` |
| **STATUS** | Status pembayaran | "lunas", "hutang", "dicicil" |
| **METODE_PEMBAYARAN** | Metode bayar | "tunai", "transfer", "qris" |

#### Contoh Ekstraksi:
```
Input: "pak andi pesan permen 10 dus 50000 tunai"

Hasil:
{
  "TANGGAL": "19-06-2026",
  "NAMA": "Pak Andi",
  "AKSI": "Tambah Penjualan",
  "BARANG": "Permen Coklat",
  "JUMLAH": "10 dus",
  "STATUS": "Lunas",
  "METODE_PEMBAYARAN": "Tunai"
}
```

---

### 6️⃣ Penentuan Intent (`tentukan_intent`)
Berdasarkan entitas yang diekstrak, sistem menentukan intent:

| Intent | Keterangan |
|--------|------------|
| `Catat_Penjualan_Lunas` | Penjualan lunas |
| `Catat_Penjualan_Cicil` | Penjualan dicicil/hutang |
| `Pelunasan_Hutang` | Pencatatan pelunasan |
| `Read_Data` | Melihat laporan/transaksi |
| `CRUD_Barang` | Tambah/edit/hapus barang |
| `Update_Delete_Transaksi` | Update/hapus transaksi |

---

### 7️⃣ Post-Processing & Override (`_apply_multi_overrides`)
**File**: `nlp/processor.py`

Menangani kasus khusus:
- Global override ("semua lunas")
- Per-item override ("permen lunas, meses hutang")
- Warisan konteks (tanggal/nama dari entri sebelumnya)

---

### 8️⃣ Penyusunan Data Transaksi
Data disusun menjadi struktur transaksi yang lengkap:

```python
{
  "intent": "Catat_Penjualan_Lunas",
  "entitas": {
    "TANGGAL": "19-06-2026",
    "NAMA": "Pak Andi",
    "AKSI": "Tambah Penjualan",
    "BARANG": "Permen Coklat",
    "JUMLAH": "10 dus",
    "STATUS": "Lunas",
    "METODE_PEMBAYARAN": "Tunai"
  },
  "original_text": "pak andi pesan permen 10 dus lunas tunai"
}
```

---

### 9️⃣ Simpan ke Database
Setelah data terstruktur, disimpan ke database (Google Sheets/PostgreSQL).

---

## 📊 Contoh Lengkap Proses

### Input:
```
"hari ini pak andi pesan permen 10 dus 50000, meses 5 bungkus belum bayar"
```

### Langkah demi Langkah:

#### 1. Pemisahan Multi-Entry
```
["hari ini pak andi pesan permen 10 dus 50000", "meses 5 bungkus belum bayar"]
```

#### 2. Text Cleaning
```
"hari ini pak andi pesan permen 10 dus 50000" → lowercase + normalisasi slang
"meses 5 bungkus belum bayar" → lowercase + normalisasi slang
```

#### 3. Fuzzy Matching
```
"prmen" → "permen" (jika ada typo)
"mses" → "meses"
```

#### 4. Ekstraksi Entitas
**Entri 1**:
- TANGGAL: "19-06-2026"
- NAMA: "Pak Andi"
- BARANG: "Permen Coklat"
- JUMLAH: "10 dus"
- HARGA: "Rp 50.000"
- STATUS: (fallback, belum ditentukan)

**Entri 2**:
- BARANG: "Meses"
- JUMLAH: "5 bungkus"
- STATUS: "Hutang"
- TANGGAL: (warisan dari entri 1: "19-06-2026")
- NAMA: (warisan dari entri 1: "Pak Andi")

#### 5. Post-Processing
Status entri 1 menjadi "Lunas" (karena tidak disebutkan status dan ada entri lain yang "belum bayar")

#### 6. Hasil Akhir
```
[
  {
    "intent": "Catat_Penjualan_Lunas",
    "entitas": {
      "TANGGAL": "19-06-2026",
      "NAMA": "Pak Andi",
      "BARANG": "Permen Coklat",
      "JUMLAH": "10 dus",
      "HARGA": "Rp 50.000",
      "STATUS": "Lunas"
    }
  },
  {
    "intent": "Catat_Penjualan_Cicil",
    "entitas": {
      "TANGGAL": "19-06-2026",
      "NAMA": "Pak Andi",
      "BARANG": "Meses",
      "JUMLAH": "5 bungkus",
      "STATUS": "Hutang"
    }
  }
]
```

---

## 🛠️ File Penting

| File | Fungsi |
|------|--------|
| `nlp/processor.py` | Proses utama, pemisahan entry, post-processing |
| `nlp/normalizer.py` | Koreksi teks dengan fuzzy matching |
| `nlp/extractor.py` | Ekstraksi entitas dengan regex |
| `nlp/dictionaries.py` | Kamus alias barang, normalisasi dict |
| `nlp/intent_matcher.py` | Penentuan intent |

---

## 🚀 Cara Menjalankan Demo

Untuk melihat alur proses secara interaktif:

```bash
python demo_alur_proses.py
```
