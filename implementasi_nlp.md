# Implementasi NLP Rule-Based pada Sistem Bot

Sistem ini menggunakan **NLP Rule-Based** — yaitu kombinasi **Regex (pola teks)**, **Fuzzy Matching (kemiripan kata)**, dan **Kamus/Dictionary** — untuk memahami pesan user. Tidak menggunakan model AI/machine learning.

---

## Bagian 1: Konfigurasi Awal

### 1.1 Konfigurasi di `.env`

File: `.env` (baris 44-54 & 139)

Setting environment variable untuk mengaktifkan dan mengonfigurasi NLP:

```env
# Pilih tipe model NLP (rule-based)
NLP_MODEL_TYPE=rule_based

# Batas minimum kepercayaan (70%)
NLP_CONFIDENCE_THRESHOLD=0.7

# Batas minimum skor fuzzy matching (85 dari 100)
NLP_FUZZY_THRESHOLD=85

# Aktifkan fitur NLP
ENABLE_NLP=true
```

### 1.2 Membaca Konfigurasi di Kode

File: `config/settings.py` (baris 59-64)

Kelas Settings membaca nilai dari `.env` agar bisa diakses oleh semua modul NLP:

```python
import os

NLP_MODEL_TYPE: str = os.getenv("NLP_MODEL_TYPE", "rule_based")
NLP_CONFIDENCE_THRESHOLD: float = float(os.getenv("NLP_CONFIDENCE_THRESHOLD", "0.7"))
NLP_FUZZY_THRESHOLD: int = int(os.getenv("NLP_FUZZY_THRESHOLD", "85"))
```

---

## Bagian 2: Library yang Digunakan

### 2.1 Library Bawaan Python (Tidak Perlu Install)

| Library    | Fungsi                                           |
| ---------- | ------------------------------------------------ |
| `re`       | Regex untuk mencari dan mengganti pola teks      |
| `datetime` | Menghitung tanggal relatif (kemarin, besok, dll) |
| `logging`  | Mencatat log untuk debugging                     |
| `os`       | Membaca environment variable                     |

### 2.2 Library External (Harus Install)

| Library     | Versi | Fungsi                                     |
| ----------- | ----- | ------------------------------------------ |
| `rapidfuzz` | 3.9.0 | Menghitung kemiripan kata (fuzzy matching) |

---

## Bagian 3: Data NLP (Kamus & Pattern)

File: `nlp/embedded_data.py`

Ini adalah "otak data" dari sistem. Berisi 3 komponen utama:

### 3.1 `NORMALIZATION_DICT` — Kamus Koreksi Teks

Digunakan untuk membersihkan teks user sebelum diproses:

```python
NORMALIZATION_DICT = {
    # Koreksi typo
    "typo_corrections": {
        "prmen": "permen",
        "kmarin": "kemarin"
    },
    # Singkatan
    "abbreviations": {
        "tgl": "tanggal",
        "bln": "bulan",
        "ctn": "karton"
    },
    # Sinonim
    "synonyms": {
        "aksi_tambah": ["tambah", "input", "masukin"],
        "aksi_hapus": ["hapus", "delete", "buang"]
    }
}
```

### 3.2 `INTENT_PATTERNS` — Pola Intent

Kumpulan contoh kalimat untuk setiap intent (niat user):

```python
INTENT_PATTERNS = {
    "tambah_transaksi_lunas_cash": [
        "pak budi pesan permen 10 dus tunai",
        "catat pesanan bu ani brownis 5 box cash"
    ],
    "cek_penjualan_hari_ini": [
        "berapa total penjualan hari ini",
        "cek omzet hari ini"
    ]
}
```

### 3.3 `NLP_TRAINING_EXAMPLES` — Contoh dengan Entitas

Dataset contoh lengkap dengan entitas yang sudah dilabeli (digunakan sebagai fallback hint):

```python
NLP_TRAINING_EXAMPLES = [
    {
        "text": "pak budi pesan permen coklat 10 dus tunai",
        "intent": "tambah_transaksi_lunas_cash",
        "entities": {
            "nama_pelanggan": "pak budi",
            "barang": "permen coklat",
            "jumlah": "10",
            "satuan": "dus"
        }
    }
]
```

---

## Bagian 4: Preprocessing — Normalisasi Teks

File: `nlp/normalizer.py`

Tahap pertama: membersihkan dan menormalisasi teks user.

### Alur Normalisasi

```
Input: "prmen1 wiilo 10 ctn kmarin pk budi"
  ↓
1. Hapus angka 0/1 yang menempel di huruf
   "prmen1" → "prmen"
  ↓
2. Ubah semua huruf menjadi kecil
   "prmen wiilo 10 ctn kmarin pk budi"
  ↓
3. Ganti angka dalam kata menjadi huruf (0→o, 1→l)
  ↓
4. Cek KAMUS_ALIAS (nama barang)
   "wiilo" → "Willo"
  ↓
5. Koreksi typo dari NORMALIZATION_DICT
   "prmen" → "permen"
   "ctn" → "karton"
  ↓
6. Fuzzy matching untuk kata yang belum terkoreksi
   "kmarin" → "kemarin" (skor 91)
  ↓
Output: "permen willo 10 karton kemarin pk budi"
```

---

## Bagian 5: Processing — Ekstraksi Entitas & Intent

Setelah teks dinormalisasi, sistem mengekstrak informasi penting dan menentukan intent user.

### 5.1 Ekstraksi Entitas

File: `nlp/extractor.py`

Mendeteksi semua informasi dari kalimat user:

| Entitas           | Keterangan               |
| ----------------- | ------------------------ |
| TANGGAL           | Kapan transaksi terjadi? |
| NAMA              | Siapa pelanggan?         |
| AKSI              | Mau ngapain?             |
| BARANG            | Barang apa?              |
| JUMLAH            | Berapa banyak?           |
| SATUAN            | Satuannya apa?           |
| HARGA             | Berapa harganya?         |
| STATUS            | Lunas/Hutang/Dicicil?    |
| METODE_PEMBAYARAN | Cash/Transfer?           |

#### Cara Ekstraksi Setiap Entitas

1. **Tanggal**: Menggunakan regex dan `datetime` untuk mendeteksi format tanggal (DD/MM/YYYY, "kemarin", "besok", dll)
2. **Nama**: Menggunakan regex untuk mendeteksi prefix (pak/bu/mas/mbak) + nama
3. **Barang**:
   - Cek exact match di daftar barang database
   - Jika tidak ada, gunakan fuzzy matching
   - Fallback ke KAMUS_ALIAS
4. **Jumlah & Satuan**: Regex untuk mendeteksi angka + satuan, lalu fuzzy matching untuk koreksi satuan
5. **Harga**: Regex untuk mendeteksi format harga (15k, 2.5jt, dll)
6. **Status & Metode**: Keyword matching

### 5.2 Identifikasi Intent

File: `nlp/intent_matcher.py` & `nlp/extractor.py`

Menentukan niat user dari teks yang sudah diproses:

1. **Fuzzy Match dengan Dataset**: Bandingkan teks user dengan `INTENT_PATTERNS` menggunakan fuzzy matching (skor ≥ 80)
2. **Mapping Intent**: Konversi intent dari dataset ke intent sistem
3. **Rule-Based Fallback**: Jika fuzzy match gagal, tentukan intent dari AKSI yang sudah diekstrak
4. **Manual Fallback**: Cek keyword sederhana sebagai fallback terakhir

---

## Bagian 6: Alur Lengkap NLP

File: `nlp/processor.py`

Ini adalah entry point utama yang memanggil semua tahapan NLP:

```
User input: "kmarin pk budi beli prmen 10 ctn tf"
  ↓
1. Normalisasi Teks (normalizer.py)
   Hasil: "kemarin pak budi beli permen 10 karton transfer"
  ↓
2. Ekstraksi Entitas (extractor.py)
   - TANGGAL: 29-06-2026
   - NAMA: Pak Budi
   - AKSI: Tambah Penjualan
   - BARANG: Permen
   - JUMLAH: 10 karton
   - METODE: Transfer
   - STATUS: Lunas
  ↓
3. Identifikasi Intent (intent_matcher.py)
   - Fuzzy match dataset: skor 92
   - Intent: "Catat_Penjualan_Lunas"
  ↓
Output: Intent + Entitas yang siap diproses oleh handler
```

---

## Rangkuman Teknik Rule-Based

### Fuzzy Matching (rapidfuzz)

Digunakan untuk mengoreksi typo dan mencari kemiripan kata:

| Kegunaan                 | Skor Minimum |
| ------------------------ | ------------ |
| Koreksi status keyword   | 80           |
| Koreksi bigram (2 kata)  | 90           |
| Koreksi unigram (1 kata) | 85           |
| Match barang             | 80           |
| Match satuan             | 80           |
| Match intent             | 80           |

### Regex (re)

Digunakan untuk mendeteksi pola teks:

- Tanggal: DD/MM/YYYY, "kemarin", "besok"
- Nama: "pak budi", "bu ani"
- Jumlah+satuan: "10 dus", "5 karton"
- Harga: "15k", "2.5jt"
- Slang: "tf" → "transfer", "pk" → "pak"
