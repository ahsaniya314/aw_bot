# Implementasi NLP pada Sistem Bot — Step by Step

> [!IMPORTANT]
> Semua berdasarkan kode nyata di sistem Anda. Tidak ada yang ditambahkan atau dikarang.
>
> NLP di sistem Anda menggunakan pendekatan **Rule-Based** — yaitu kombinasi **Regex** (pola teks) + **Fuzzy Matching** (kemiripan kata) + **Kamus/Dictionary** (data statis & database). Tidak menggunakan model AI/machine learning.

---

## Step 1: Setting Environment Variable di `.env`

**File**: [.env](file:///c:/Users/FINN/Documents/BOT/.env) — **baris 44-54**

### 1a. Pilih tipe model NLP (baris 48)

```env
NLP_MODEL_TYPE=rule_based
```

Memberitahu sistem bahwa NLP menggunakan pendekatan **rule-based** (berbasis aturan regex + kamus), bukan model AI seperti distilbert atau indobert.

### 1b. Setting threshold confidence (baris 51)

```env
NLP_CONFIDENCE_THRESHOLD=0.7
```

Batas minimum kepercayaan (`0.7` = 70%) agar hasil NLP dianggap valid.

### 1c. Setting threshold fuzzy matching (baris 54)

```env
NLP_FUZZY_THRESHOLD=85
```

Batas minimum skor kemiripan kata (`85` dari `100`) agar fuzzy matching dianggap cocok. Misal: "prmen" dibandingkan "permen" → skor 83 → **tidak lolos**. "prmen" dibandingkan "permen" dengan skor 86 → **lolos**.

### 1d. Aktifkan fitur NLP (baris 139)

```env
ENABLE_NLP=true
```

Feature flag untuk mengaktifkan layanan NLP.

### Library di Step 1

**Tidak ada library.** `.env` hanya file teks biasa.

---

## Step 2: Settings Class Membaca `.env`

**File**: [config/settings.py](file:///c:/Users/FINN/Documents/BOT/config/settings.py) — **baris 59-64**

### Apa yang dilakukan

```python
# Baris 62 — Baca tipe model, default "rule_based"
NLP_MODEL_TYPE: str = os.getenv("NLP_MODEL_TYPE", "rule_based")

# Baris 63 — Baca threshold confidence, default 0.7
NLP_CONFIDENCE_THRESHOLD: float = float(os.getenv("NLP_CONFIDENCE_THRESHOLD", "0.7"))

# Baris 64 — Baca threshold fuzzy, default 85
NLP_FUZZY_THRESHOLD: int = int(os.getenv("NLP_FUZZY_THRESHOLD", "85"))
```

### Fungsinya

Jembatan antara `.env` dan kode Python. Semua modul NLP mengakses konfigurasi lewat `settings`.

### Library di Step 2

| Library | Tipe | Fungsi |
|---|---|---|
| `os` | 🟢 Bawaan Python | `os.getenv()` untuk baca environment variable |

---

## Step 3: Data NLP — Kamus, Dataset, dan Pattern

**File**: [nlp/embedded_data.py](file:///c:/Users/FINN/Documents/BOT/nlp/embedded_data.py) — **7.374 baris, 210 KB**

Ini adalah **"otak" data** dari NLP. File terbesar di seluruh sistem. Berisi 3 komponen utama:

### 3a. `NORMALIZATION_DICT` — Kamus Koreksi Typo & Singkatan

```python
NORMALIZATION_DICT = {
    "typo_corrections": {
        "prmen": "permen",      # typo → benar
        "kmarin": "kemarin",
        "wiilo": "willo",
        "tamhbahkan": "tambah",
        ...
    },
    "abbreviations": {
        "tgl": "tanggal",
        "bln": "bulan",
        ...
    },
    "synonyms": {
        "aksi_tambah": ["tambah", "input", "masukin", ...],
        "aksi_hapus": ["hapus", "delete", "buang", ...],
        ...
    }
}
```

**Fungsi**: Menerjemahkan kata yang salah ketik atau disingkat menjadi kata yang benar sebelum diproses.

### 3b. `INTENT_PATTERNS` — Pola untuk Mengenali Niat User

```python
INTENT_PATTERNS = {
    "tambah_transaksi_lunas_cash": [
        "pak budi pesan permen 10 dus tunai",
        "catat pesanan bu ani brownis 5 box cash hari ini",
        ...
    ],
    "cek_penjualan_hari_ini": [
        "berapa total penjualan hari ini",
        "cek omzet hari ini",
        ...
    ],
    ...
}
```

**Fungsi**: Kumpulan contoh kalimat untuk setiap intent. Saat user mengetik, kalimatnya dibandingkan (fuzzy) dengan semua contoh ini untuk mencari intent yang paling cocok.

### 3c. `NLP_TRAINING_EXAMPLES` — Contoh Training dengan Entitas

```python
NLP_TRAINING_EXAMPLES = [
    {
        "text": "pak budi pesan permen coklat 10 dus tunai",
        "intent": "tambah_transaksi_lunas_cash",
        "entities": {
            "nama_pelanggan": "pak budi",
            "barang": "permen coklat",
            "jumlah": "10",
            "satuan": "dus",
            ...
        }
    },
    ...
]
```

**Fungsi**: Dataset contoh lengkap dengan entitas yang sudah dilabeli. Digunakan sebagai **fallback hint** — jika kalimat user mirip dengan contoh di dataset, entitas dari contoh bisa dijadikan petunjuk.

### Library di Step 3

**Tidak ada library.** File ini hanya berisi data Python murni (dictionary dan list).

---

## Step 4: Preprocessing — Normalisasi & Koreksi Teks

**File**: [nlp/normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) — **175 baris**
**File**: [nlp/dictionaries.py](file:///c:/Users/FINN/Documents/BOT/nlp/dictionaries.py) — **283 baris**

Ini adalah tahap pertama saat teks user masuk. Teks "kotor" dari user dibersihkan dan dinormalisasi.

### 4a. Fungsi `koreksi_teks()` di normalizer.py

Alur koreksi teks dari awal sampai akhir:

```
Input: "prmen1 wiilo 10 ctn kmarin pk budi"
                    ↓
PASS 0 (baris 19): Hapus angka 0/1 yang menempel di huruf
   "prmen1" → "prmen"
                    ↓
PASS 1 (baris 22): Lowercase semua
   "prmen wiilo 10 ctn kmarin pk budi"
                    ↓
PASS 2 (baris 25-26): Ganti angka dalam kata → huruf
   "will0" → "willo", "l0lipop" → "lolipop"
                    ↓
PASS 1.5 (baris 56-76): Cek KAMUS_ALIAS
   "wiilo" → ada di KAMUS_ALIAS → "Willo"
                    ↓
PASS 2 (baris 78-107): Koreksi typo dari NORMALIZATION_DICT
   "prmen" → "permen" (dari typo_corrections)
   "ctn" → "karton" (dari abbreviations)
                    ↓
PASS 3 (baris 109-169): FUZZY MATCHING ⭐
   Kata yang belum terkoreksi dicari kemiripannya:
   - Bigram (2 kata): skor ≥ 90
   - Unigram (1 kata): skor ≥ 85
   "kmarin" → fuzzy match → "kemarin" (skor 91)
                    ↓
Output: "permen willo 10 karton kemarin pk budi"
```

### 4b. Di mana Fuzzy Matching dipakai di Step 4

| Lokasi | Baris | Apa yang dilakukan |
|---|---|---|
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 125-129 | Status keyword fuzzy | Kata seperti "lunwas" dicari kemiripannya dengan {"lunas", "hutang", ...}. Skor ≥ 80 → koreksi |
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 131-146 | Bigram fuzzy (2 kata) | Gabungan 2 kata dicari kemiripannya dengan `DAFTAR_KATA_KUNCI`. Skor ≥ 90 → koreksi |
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 148-164 | Unigram fuzzy (1 kata) | 1 kata dicari kemiripannya dengan `DAFTAR_KATA_KUNCI`. Skor ≥ 85 → koreksi |

### 4c. Di mana Regex dipakai di Step 4

| Lokasi | Baris | Apa yang dilakukan |
|---|---|---|
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 19 | `re.sub(r'(\b[a-zA-Z]+)([01])\b', ...)` | Hapus angka 0/1 di akhir kata |
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 25-26 | `re.sub(r'([a-zA-Z])0([a-zA-Z]*)', ...)` | Ganti 0→o dan 1→l dalam kata |
| [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) baris 52 | `re.sub(re.escape(phrase), token, ...)` | Lindungi frasa status ("belum lunas") agar tidak rusak |

### 4d. KAMUS_ALIAS — dictionaries.py

Kamus ini memetakan alias/singkatan/typo nama barang ke nama resmi:

```python
KAMUS_ALIAS = {
    "millo": "Permen Coklat",
    "bengbeng": "Bembeng",
    "pia potong": "Roti Pia (Potong)",
    "bronis": "Brownis",
    ...
}
```

Kamus ini **dinamis** — dimuat saat startup dari:
1. Data statis (`KAMUS_ALIAS_STATIS` baris 10-178)
2. Database (`get_all_barang()` baris 196-210)
3. Master catalog (`MASTER_BARANG_CATALOG` baris 213-218)

### Library di Step 4

| Library | Tipe | Fungsi |
|---|---|---|
| `re` | 🟢 Bawaan Python | Regex untuk membersihkan angka, mendeteksi pola, dan proteksi frasa |
| `rapidfuzz` | 🔵 **Harus install** (`3.9.0`) | `process.extractOne()` + `fuzz.ratio` untuk menghitung kemiripan kata |
| `logging` | 🟢 Bawaan Python | Pencatatan log |

---

## Step 5: Ekstraksi Entitas — Mendeteksi Siapa, Apa, Kapan, Berapa

**File**: [nlp/extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) — **1.121 baris**

Setelah teks dinormalisasi di Step 4, teks masuk ke `ekstrak_entitas()` (baris 131). Fungsi ini mendeteksi **semua informasi** dari kalimat user.

### Entitas yang Diekstrak

```python
entitas = {
    "TANGGAL": None,           # Kapan?
    "NAMA": None,              # Siapa?
    "AKSI": None,              # Mau ngapain?
    "BARANG": None,            # Barang apa?
    "JUMLAH": None,            # Berapa banyak?
    "HARGA": None,             # Berapa harganya?
    "SATUAN": None,            # Satuannya apa?
    "TOTAL": None,             # Total berapa?
    "STATUS": None,            # Lunas/Hutang/Dicicil?
    "NOMINAL_BAYAR": None,     # Bayar berapa?
    "METODE_PEMBAYARAN": None, # Cash/Transfer?
    "SEMUA": False,            # Semua data?
    "KONTEKS_AGREGASI": None,  # Jenis laporan?
    "KONDISI": None            # Filter khusus?
}
```

### 5a. Tahap 0 — Slang Preprocessor (baris 148-230)

```
Input: "kmarin pk budi beli prmen 10 ctn tf"
                    ↓
Slang map: 200+ pola regex menerjemahkan singkatan gaul
   "kmarin" → "kemarin"
   "pk" → "pak"
   "tf" → "transfer"
   "ctn" → "karton"
                    ↓
Output: "kemarin pak budi beli permen 10 karton transfer"
```

**Teknik**: Semua `re.sub(pattern, replacement)` — 200+ aturan regex di `slang_map` dictionary.

### 5b. Ekstraksi TANGGAL (baris 315-399)

```
Deteksi tanggal dari teks, mendukung banyak format:

"kemarin"           → hitung: hari_ini - 1 hari
"hari ini"          → hitung: hari_ini
"besok"             → hitung: hari_ini + 1 hari
"3 hari lalu"       → hitung: hari_ini - 3 hari
"kemarin senin"     → hitung: senin minggu lalu
"28/11/2025"        → parse: DD/MM/YYYY
"28 november 2025"  → parse: DD Bulan YYYY
"tanggal 5"         → parse: tanggal 5 bulan ini
```

**Teknik**: 
- **Regex** (`re.search`) untuk mendeteksi pola tanggal di baris 318-368
- **Python `datetime`** untuk menghitung tanggal relatif

### 5c. Deteksi AKSI / Konteks (baris 401-471)

```
Mendeteksi apa yang user mau lakukan:

"dashboard"              → AKSI: "Read Data", KONTEKS: "Dashboard Harian"
"siapa pembeli terbanyak"→ AKSI: "Read Data", KONTEKS: "Pembeli Terbanyak"
"total tagihan"          → AKSI: "Read Data", KONTEKS: "Total Tunggakan"
"set harga brownis"      → AKSI: "Set Harga Barang"
"bayar hutang pak budi"  → AKSI: "Catat Pelunasan"
"hapus transaksi"        → AKSI: "Delete Data"
"pak budi pesan permen"  → AKSI: "Tambah Penjualan"
```

**Teknik**: **Keyword matching** — `any(k in teks_lower for k in [...])` — mencari kata kunci dalam teks.

### 5d. Ekstraksi NAMA (baris 473-573)

```
Strategi 2 lapis:

1. Dengan prefix (prioritas tinggi):
   "pak budi"  → Regex: r"(pak|bu|mas|mbak|kak) ([a-z]+)" → "Pak Budi"

2. Tanpa prefix (fallback):
   Kata yang bukan angka, bukan barang, bukan kata kerja,
   panjang ≥ 3 huruf → dianggap nama orang
```

**Teknik**: **Regex** untuk mendeteksi pola prefix + nama. **Exclusion list** (500+ kata di `ignore_for_name`) untuk memfilter kata yang bukan nama.

### 5e. Ekstraksi BARANG (baris 575-677) ⭐

```
Strategi 3 lapis:

1. PRIORITAS: Cek dari Master Data (database)
   "brownis" ada di daftar_barang? → Ya → BARANG = "Brownis"

2. Jika tidak ada exact match → FUZZY MATCH ⭐
   "bronis" fuzzy match dengan daftar_barang → skor 85 → BARANG = "Brownis"

3. FALLBACK: Cek dari KAMUS_ALIAS (kamus statis)
   "bengbeng" ada di KAMUS_ALIAS? → Ya → BARANG = "Bembeng"
   Jika tidak → fuzzy match dengan KAMUS_ALIAS → skor 80+
```

**Teknik**: 
- **Exact match**: `b_l in teks_lower` (pencocokan string langsung)
- **Fuzzy match**: `process.extractOne(kata, daftar, scorer=fuzz.token_sort_ratio)` dengan skor minimum 80
- **Sorting**: Jika banyak kandidat, pilih yang paling spesifik (non-generik, posisi paling awal, nama paling panjang)

### 5f. Ekstraksi JUMLAH & SATUAN (baris 679-761)

```
"10 dus"      → Regex: r"(\d+)\s*([a-zA-Z]+)" → JUMLAH: "10 dus", SATUAN: "dus"
"sebanyak 50" → Regex: r"(?:sebanyak|jumlah)\s*(\d+)" → JUMLAH: "50"

Fuzzy match satuan:
"krton" → fuzzy match VALID_UNITS → "karton" (skor 85)
"bks"   → langsung dikonversi → "bungkus"
```

**Teknik**: **Regex** untuk mendeteksi pola angka + satuan. **Fuzzy matching** (`fuzzy_match_satuan()` baris 108-128) untuk mengoreksi typo satuan.

### 5g. Ekstraksi HARGA, TOTAL, NOMINAL (baris 763-784)

```
"harga 15k"        → Regex → parse "15k" → Rp 15.000
"total 2.5jt"      → Regex → parse "2.5jt" → Rp 2.500.000
"bayar 500rb"      → Regex → parse "500rb" → Rp 500.000
"bayar setengah"   → Keyword → NOMINAL_BAYAR = "SETENGAH"
```

**Teknik**: **Regex** untuk mendeteksi pola harga + fungsi `parse_price_shorthand()` dari [dictionaries.py](file:///c:/Users/FINN/Documents/BOT/nlp/dictionaries.py) baris 254-281 untuk mengkonversi shorthand (`k`, `rb`, `jt`) ke angka.

### 5h. Deteksi STATUS & METODE PEMBAYARAN (baris 786-838)

```
STATUS:
"dicicil setengah"  → "Dicicil"
"belum lunas"       → "Hutang"
"lunas"             → "Lunas"

METODE:
"transfer" / "tf"   → "Transfer"
"tunai" / "cash"    → "Tunai"
"qris" / "gopay"    → Sesuai nama
```

**Teknik**: **Keyword matching** (`any(k in teks_lower for k in [...])`) dan **regex** (`re.search(r"\bbelum\b", ...)`).

### Library di Step 5

| Library | Tipe | Fungsi |
|---|---|---|
| `re` | 🟢 Bawaan Python | 50+ pola regex untuk mendeteksi tanggal, nama, barang, harga, satuan, slang |
| `datetime` | 🟢 Bawaan Python | Menghitung tanggal relatif (kemarin, besok, 3 hari lalu) |
| `rapidfuzz` | 🔵 **Harus install** (`3.9.0`) | Fuzzy match barang, satuan, dan dataset hint |
| `logging` | 🟢 Bawaan Python | Pencatatan log |

---

## Step 6: Identifikasi Intent — Menentukan Niat User

**File**: [nlp/intent_matcher.py](file:///c:/Users/FINN/Documents/BOT/nlp/intent_matcher.py) — **111 baris**
**File**: [nlp/extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) — **baris 1052-1119**

Setelah entitas diekstrak, sistem menentukan **intent** (niat) user.

### 6a. Fuzzy Match dengan Dataset — `match_intent_from_dataset()` (intent_matcher.py baris 54-77)

```
Input: "berapa total penjualan hari ini"
                    ↓
Bandingkan (fuzzy) dengan semua contoh di INTENT_PATTERNS:
  - "cek_penjualan_hari_ini": ["berapa total penjualan hari ini", ...]  → skor 100
  - "tambah_transaksi_lunas_cash": ["pak budi pesan permen 10 dus"]     → skor 25
                    ↓
Pilih skor tertinggi ≥ 80
                    ↓
"cek_penjualan_hari_ini" → mapping → "Read_Analitik_Penjualan"
```

**Teknik**: `process.extractOne(text, patterns, scorer=fuzz.token_set_ratio)` — membandingkan input user dengan ratusan contoh kalimat menggunakan fuzzy matching.

### 6b. Mapping Intent Dataset → Intent Sistem (intent_matcher.py baris 14-51)

```python
DATASET_TO_SYSTEM_INTENT = {
    "greeting"                          → "Chit_Chat",
    "cek_penjualan_hari_ini"            → "Read_Analitik_Penjualan",
    "tambah_transaksi_lunas_cash"       → "Catat_Penjualan_Lunas",
    "tambah_transaksi_cicilan_cash"     → "Catat_Penjualan_Cicil",
    "bayar_hutang"                      → "Pelunasan_Hutang",
    "hapus_transaksi"                   → "Update_Delete_Transaksi",
    "tambah_produk"                     → "CRUD_Barang",
    ...
}
```

### 6c. Rule-Based Fallback — `tentukan_intent()` (extractor.py baris 1052-1119)

Jika fuzzy match gagal (skor < 85), intent ditentukan dari AKSI yang sudah diekstrak di Step 5:

```
AKSI "Tambah Penjualan" + STATUS "Lunas"  → "Catat_Penjualan_Lunas"
AKSI "Tambah Penjualan" + STATUS "Hutang" → "Catat_Penjualan_Cicil"
AKSI "Read Data" + KONTEKS "Total Tunggakan" → "Read_Analitik_Hutang"
AKSI "Catat Pelunasan"                    → "Pelunasan_Hutang"
AKSI "Chit Chat"                          → "Chit_Chat"
```

### 6d. Manual Fallback — `tentukan_intent_manual()` (intent_matcher.py baris 80-93)

Fallback terakhir jika semuanya gagal — cek keyword sederhana:

```python
if "halo" in text or "pagi" in text → "Chit_Chat"
if "semua" in text and "transaksi" in text → "Read_Transaksi_Spesifik"
else → "Unknown"
```

### Library di Step 6

| Library | Tipe | Fungsi |
|---|---|---|
| `rapidfuzz` | 🔵 **Harus install** | `process.extractOne()` + `fuzz.token_set_ratio` untuk mencocokkan input dengan contoh dataset |
| `logging` | 🟢 Bawaan Python | Pencatatan log |

---

## Step 7: Post-Processing — Multi-Entry & Overrides

**File**: [nlp/processor.py](file:///c:/Users/FINN/Documents/BOT/nlp/processor.py) — **813 baris**

### 7a. Split Multi-Entry — `split_multi_entries()` (baris 8-58)

Jika user mengirim banyak transaksi sekaligus, dipecah dulu:

```
Input: "pak budi pesan permen 10 dus, meses 5 karton, brownis 3 box"
                    ↓
Split berdasarkan: koma (,) ; titik koma (;) | baris baru (\n) | pipe (|)
                    ↓
Output: ["pak budi pesan permen 10 dus", "meses 5 karton", "brownis 3 box"]
```

**Teknik**: `re.split(r'[,;\n|]+', text)` — regex split.

### 7b. Fungsi Utama `proses_nlp()` (baris 713-811)

Ini adalah **entry point** yang dipanggil oleh handler. Alur lengkapnya:

```
Input: teks dari user
          ↓
Step 0: Cek pola multi-item dengan mixed status (baris 718)
   → Jika cocok, langsung return hasil
          ↓
Step 1: Split teks menjadi entries (baris 755)
          ↓
Untuk SETIAP entry:
   ├── koreksi_teks(entry)        ← Step 4 (normalisasi)
   ├── ekstrak_entitas(...)       ← Step 5 (ekstraksi)
   ├── tentukan_intent(...)       ← Step 6 (identifikasi intent)
   └── Simpan ke results[]
          ↓
Step terakhir: _apply_multi_overrides(results) (baris 810)
   → Override global: "semua lunas transfer" berlaku ke semua item
   → Inheritance: tanggal & nama dari segmen pertama diterapkan ke semua
   → Recalculate intent setelah override
          ↓
Output: List of {intent, entitas, original_text}
```

### Library di Step 7

| Library | Tipe | Fungsi |
|---|---|---|
| `re` | 🟢 Bawaan Python | Split teks, deteksi pola tanggal/status |
| `datetime` | 🟢 Bawaan Python | Kalkulasi tanggal |

---

## Step 8: Handler Memanggil NLP

**File**: [handlers/text_handler.py](file:///c:/Users/FINN/Documents/BOT/handlers/text_handler.py) — **baris 14-15**
**File**: [handlers/photo_handler.py](file:///c:/Users/FINN/Documents/BOT/handlers/photo_handler.py) — **baris 18-19**

### Apa yang dilakukan

```python
from nlp.processor import proses_nlp
from nlp.normalizer import koreksi_teks

# Saat user kirim teks ke bot:
results = proses_nlp(teks_user, daftar_barang=daftar_barang, ...)

# results = [
#   {
#     "intent": "Catat_Penjualan_Lunas",
#     "entitas": {
#       "TANGGAL": "30-06-2026",
#       "NAMA": "Pak Budi",
#       "BARANG": "Permen Coklat",
#       "JUMLAH": "10 dus",
#       "STATUS": "Lunas",
#       ...
#     },
#     "original_text": "pak budi pesan permen 10 dus tunai hari ini"
#   }
# ]

# Berdasarkan intent, handler mengarahkan ke aksi yang sesuai
```

### Library di Step 8

**Tidak ada library NLP tambahan.** Handler hanya memanggil `proses_nlp()` dan menerima hasilnya.

---

## Rangkuman: Peran Fuzzy Matching & Regex

### 🎯 Fuzzy Matching (library `rapidfuzz`)

| Lokasi | File | Baris | Apa yang Di-fuzzy | Skor Min | Scorer |
|---|---|---|---|---|---|
| Koreksi typo kata | [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) | 125 | Status keyword vs {"lunas","hutang",...} | 80 | `fuzz.ratio` |
| Koreksi bigram | [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) | 135 | 2 kata vs `DAFTAR_KATA_KUNCI` | 90 | `fuzz.ratio` |
| Koreksi unigram | [normalizer.py](file:///c:/Users/FINN/Documents/BOT/nlp/normalizer.py) | 153 | 1 kata vs `DAFTAR_KATA_KUNCI` | 85 | `fuzz.ratio` |
| Match barang (master) | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) | 605 | Kata vs daftar barang DB | 80 | `fuzz.token_sort_ratio` |
| Match barang (alias) | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) | 653 | Kata vs `KAMUS_ALIAS` keys | 80 | `fuzz.token_sort_ratio` |
| Match satuan | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) | 119 | Kata vs `VALID_UNITS` | 80 | `fuzz.token_sort_ratio` |
| Match intent dataset | [intent_matcher.py](file:///c:/Users/FINN/Documents/BOT/nlp/intent_matcher.py) | 69 | Kalimat vs `INTENT_PATTERNS` | 80 | `fuzz.token_set_ratio` |
| Fallback dataset | [intent_matcher.py](file:///c:/Users/FINN/Documents/BOT/nlp/intent_matcher.py) | 104 | Kalimat vs contoh training | 80 | `fuzz.token_set_ratio` |

### 🔍 Regex (`re` — bawaan Python)

| Lokasi | File | Contoh Pattern | Apa yang Dideteksi |
|---|---|---|---|
| Slang preprocessing | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 148-201 | `r"\btf\b"` → "transfer" | 200+ singkatan gaul |
| Deteksi tanggal | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 318-390 | `r"\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b"` | Format DD/MM/YYYY |
| Deteksi nama | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 518 | `r"(pak\|bu\|mas) ([a-z]+)"` | Nama dengan prefix |
| Deteksi jumlah+satuan | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 683 | `r"(\d+)\s*([a-zA-Z]+)"` | "10 dus", "5 karton" |
| Deteksi harga | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 765 | `r"(?:harga).*?(\d[\d.,]*(?:\s*(?:k\|jt)))"` | "harga 15k", "rp 2.5jt" |
| Parse shorthand | [dictionaries.py](file:///c:/Users/FINN/Documents/BOT/nlp/dictionaries.py) baris 263-275 | `r"(\d+)\s*(?:juta\|jt)"` | "5jt" → 5.000.000 |
| Split multi-entry | [processor.py](file:///c:/Users/FINN/Documents/BOT/nlp/processor.py) baris 32 | `r"[,;\n\|]+"` | Pemisah koma/titik koma |
| Deteksi CRUD command | [extractor.py](file:///c:/Users/FINN/Documents/BOT/nlp/extractor.py) baris 841-863 | `r"\b(?:tambah\|input) (barang\|produk)"` | "tambah barang", "hapus produk" |

---

## Rangkuman: Semua Library NLP

### 🟢 Bawaan Python (Tidak Perlu Install)

| No | Library | Dipakai di Step | Fungsi |
|---|---|---|---|
| 1 | `re` | 4, 5, 7 | **50+ pola regex** untuk deteksi tanggal, nama, barang, harga, slang, split teks |
| 2 | `datetime` | 5, 7 | Kalkulasi tanggal relatif (kemarin, besok, X hari lalu) |
| 3 | `logging` | 4, 5, 6 | Pencatatan log error dan debug |
| 4 | `os` | 2 | Membaca environment variable |

### 🔵 Harus Install (Third-Party)

| No | Library | Versi | Dipakai di Step | Fungsi |
|---|---|---|---|---|
| 1 | `rapidfuzz` | `3.9.0` | 4, 5, 6 | **Satu-satunya library NLP external.** Digunakan untuk menghitung kemiripan kata (fuzzy matching) di koreksi typo, pencarian barang, satuan, dan intent |
| 2 | `thefuzz` | `0.20.0` | — | Ada di `pyproject.toml` tapi **tidak di-import** di modul NLP manapun. Kemungkinan warisan/cadangan |

---

## Diagram Alur Lengkap

```
User mengetik: "kmarin pk budi beli prmen 10 ctn tf"
                              ↓
┌─────────────────────────────────────────────────┐
│ Step 4: NORMALISASI (normalizer.py)             │
│                                                 │
│ ① Hapus angka menempel: prmen1 → prmen          │
│ ② Lowercase semua                               │
│ ③ KAMUS_ALIAS: wiilo → Willo                    │
│ ④ Typo dict: prmen → permen, ctn → karton       │
│ ⑤ Fuzzy match: kmarin → kemarin (skor 91)       │
│                                                 │
│ Hasil: "kemarin pak budi beli permen 10 karton   │
│         transfer"                               │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ Step 5: EKSTRAKSI ENTITAS (extractor.py)        │
│                                                 │
│ ① Slang: tf → transfer                         │
│ ② TANGGAL: "kemarin" → 29-06-2026              │
│ ③ NAMA: "pak budi" (regex prefix)  → Pak Budi  │
│ ④ AKSI: "beli" → Tambah Penjualan              │
│ ⑤ BARANG: "permen" (KAMUS_ALIAS) → Permen      │
│ ⑥ JUMLAH: "10 karton"                          │
│ ⑦ METODE: "transfer" → Transfer                │
│ ⑧ STATUS: (default) → Lunas                    │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ Step 6: IDENTIFIKASI INTENT                     │
│                                                 │
│ ① Fuzzy match dataset: skor 92                  │
│   → "tambah_transaksi_lunas_cash"               │
│ ② Mapping → "Catat_Penjualan_Lunas"            │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ Step 8: HANDLER mengeksekusi aksi               │
│                                                 │
│ Intent: Catat_Penjualan_Lunas                   │
│ → Simpan ke database:                           │
│   Tanggal: 29-06-2026                           │
│   Nama: Pak Budi                                │
│   Barang: Permen                                │
│   Jumlah: 10 karton                             │
│   Metode: Transfer                              │
│   Status: Lunas                                 │
└─────────────────────────────────────────────────┘
```
