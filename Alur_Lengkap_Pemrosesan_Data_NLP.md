# Alur Lengkap Pemrosesan Data NLP dan Penyimpanan Transaksi

## 1. Alur Normalisasi & Ekstraksi Entitas (Preprocessing)

File terkait: `nlp/normalizer.py`, `nlp/extractor.py`, `nlp/processor.py`

### 1.1. Preprocessing Normalisasi Teks

1. User mengirim teks (misal: "pak andi ambil 5 dus willo lunas tunai")
2. Teks dikoreksi oleh `koreksi_teks()` di `nlp/normalizer.py`:
   - Koreksi typo
   - Normalisasi kata (misal: "udah" → "sudah")
   - Menggunakan daftar barang sebagai referensi koreksi nama produk

### 1.2. Pemisah Multi-Entry (Jika Ada)

1. `split_multi_entries()` di `nlp/processor.py` memisahkan teks panjang menjadi beberapa transaksi (misal: koma, ";", kata "dan" diikuti waktu, dsb.)

### 1.3. Deteksi Pola Khusus (Multi-Item with Status)

1. Sistem cek apakah input cocok pola `parse_multi_item_with_status()` (contoh: daftar barang + "yang lunas..." atau sejenisnya)
2. Jika cocok, parsing dilakukan dengan parser khusus ini (lebih akurat untuk kasus bulk status)

### 1.4. Ekstraksi Entitas untuk Setiap Entry

`ekstrak_entitas()` di `nlp/extractor.py` bekerja:

- **TANGGAL**: Regex untuk pola DD-MM-YYYY, DD/MM, atau kata relative ("hari ini", "kemarin")
- **NAMA PELANGGAN**: Regex pola "Pak/Nama/Bu/Mas [Nama]" + blacklist kata yang bukan nama
- **JUMLAH & SATUAN**: Regex `\d+\s*[satuan]` (contoh: "5 dus"), normalisasi satuan (misal: "bks" → "bungkus")
- **HARGA & TOTAL & NOMINAL BAYAR**: Regex untuk mata uang + singkatan (misal: "100k" → 100000, "5jt" → 5000000)
- **STATUS & METODE PEMBAYARAN**: Deteksi keyword ("lunas", "hutang", "tunai", "transfer")

### 1.5. Post-Processing Override (Multi-Entry Konteks)

`_apply_multi_overrides()` di `nlp/processor.py`:

- **Konteks Inheritance**: Tanggal/Nama/Metode dari segmen pertama diwariskan ke segmen selanjutnya yang tidak punya data tsb
- **Global Override**: Frasa "semua lunas" / "semua hutang" diterapkan ke semua item
- **Per-Item Override**: Frasa status yang mengacu ke barang tertentu diterapkan ke item tersebut
- Menetapkan `intent` dengan `tentukan_intent()`

---

## 2. Alur Pencarian Harga & Perhitungan Total Transaksi

File terkait: `handlers/text_handler.py`, `core/master_data.py`

### 2.1. Single Entry (Satu Transaksi)

1. `handle_text_message()` di `text_handler.py` mengambil cache master barang & metode
2. **Cari Harga Default**: Fungsi `cari_harga_default()` di `core/master_data.py` mencari harga barang dari master barang, berdasarkan nama barang (dan satuan jika ada)
3. **Hitung Total**: Jika `HARGA` dan `JUMLAH` ada:
   - Ekstrak angka jumlah (dengan regex `\d+`)
   - Parse harga (dengan `parse_rupiah()`)
   - Hitung: `TOTAL = JUMLAH × HARGA`
   - Format hasil ke Rupiah (`format_rupiah()`)
4. **Tanggal Default**: Jika tidak ada tanggal, gunakan hari ini (`%d-%m-%Y`)

### 2.2. Multi Entry (Lebih dari Satu Transaksi)

1. Proses sama seperti single entry, tapi untuk **setiap item di list `valid_results`**:
   - Terapkan konteks inheritance (Tanggal/Nama/Metode/Status)
   - Lookup harga dan hitung total otomatis untuk setiap item
2. Hasil disimpan ke `user_sessions` dengan state `pending_multi_insert`

---

## 3. Alur Konfirmasi & Penyusunan Data Transaksi Final

File terkait: `handlers/text_handler.py`, `handlers/crud_transaksi.py`, `services/ui_transaksi.py`

### 3.1. Susun Balasan Resume

1. Fungsi `susun_balasan_resume()` (dipanggil dari `text_handler.py`) menampilkan rangkuman transaksi ke user (dengan Inline Keyboard untuk "✅ Konfirmasi" atau "✏️ Edit")
2. Untuk multi-entry, menampilkan daftar semua transaksi sekaligus

### 3.2. Tangani Konfirmasi User

1. User klik "✅ Konfirmasi"
2. Handler callback di `handlers/callback_transaksi.py` / `handlers/crud_transaksi.py` memproses penyimpanan
3. **Validasi Data**: Pastikan semua field wajib diisi
4. **Persiapkan Data Transaksi**:
   - `tanggal`: Sudah dalam format `%d-%m-%Y`
   - `nama_pelanggan`: Nama customer
   - `barang`: Nama barang
   - `jumlah_satuan`: Gabungan jumlah + satuan (misal: "5 dus")
   - `harga`: Harga satuan (sudah diformat Rupiah)
   - `total`: Total transaksi (sudah diformat Rupiah)
   - `status`: "Lunas", "Hutang", atau "Dicicil"
   - `metode_pembayaran`: "Tunai", "Transfer", dsb
   - `tagihan`: Total (untuk hutang/cicilan)
   - `uang_masuk`: Nominal bayar (untuk dicicil)

---

## 4. Alur Penyimpanan ke Database (Supabase)

File terkait: `database/db_client.py`, `handlers/crud_transaksi.py`

### 4.1. Simpan Transaksi

1. Fungsi `insert_transaksi_db()` di `database/db_client.py`:
   - Membuat koneksi singleton ke Supabase
   - Memasukkan data transaksi ke tabel `transaksi`
   - Mengembalikan `row_idx` dari transaksi yang baru disimpan

### 4.2. Catat Pelunasan (Jika Ada / Status Dicicil)

1. Jika statusnya "Dicicil" dan ada nominal bayar, catat ke `histori_pelunasan` dengan `insert_histori_pelunasan_db()`

### 4.3. Refresh Cache

1. Setelah penyimpanan berhasil, refresh cache transaksi agar dashboard menampilkan data terbaru

---

## 5. Alur untuk Input Foto Nota (OCR)

File terkait: `handlers/photo_handler.py`, `services/ocr_service.py`

Alur hampir sama dengan teks, tapi:

1. User upload foto → bot ambil file
2. **Resizing & Encoding**: Gambar diresize dan diencode Base64
3. **Kirim ke Mistral OCR API**: Dapatkan teks OCR
4. **Clean Noise OCR**: Hilangkan teks yang tidak relevan (header, footer)
5. **Normalisasi & Ekstraksi Entitas**: Proses teks OCR seperti alur teks normal
6. **Kadang Minta Input Tambahan**: Jika nama/tanggal tidak terbaca, bot akan bertanya ke user
7. **Resume & Simpan**: Sama dengan alur teks normal
