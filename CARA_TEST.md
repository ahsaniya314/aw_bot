# Cara Test Perbaikan Bug Siper Queen

## Masalah yang Diperbaiki
**Bug:** Ketika input `"siiper quuen 50 karton"`, sistem salah membaca harga Rp 250 atau angka 50 sebagai harga, padahal 50 adalah jumlah barang.

**Penyebab:** Regex untuk ekstraksi harga menangkap substring "per" dalam kata "siiper" sebagai keyword "per" (harga per satuan), sehingga angka setelahnya (50) dianggap sebagai harga.

**Solusi:** Menambahkan word boundary `\b` di depan keyword agar hanya menangkap "per" sebagai kata lengkap, bukan bagian dari kata lain.

## File yang Diperbaiki
- `nlp/extractor.py` (line 1574)

## Langkah Test

### 1. Stop Bot Telegram (jika sedang running)
Tekan Ctrl+C pada terminal yang menjalankan bot

### 2. Clear Cache (Optional tapi direkomendasikan)
```bash
python -c "from core.bot_context import ctx; ctx.gs_cache.invalidate(); print('Cache cleared')"
```

### 3. Jalankan Ulang Bot
```bash
python app.py
```

### 4. Test di Telegram
Kirim pesan berikut ke bot:

```
05 April 2026 Pak Edi pesan siiper quuen 50 karton, willo 20 karton, miksu 20 karton semua sudah lunas pembayaran transfer
```

### 5. Verifikasi Hasil yang Benar
Bot seharusnya mendeteksi **3 transaksi** dengan data:

**Entri #1 - Siper Queen:**
- Tanggal: 05-04-2026
- Nama: Pak Edi  
- Barang: Siper Queen (atau siiper quuen)
- Jumlah: 50 karton
- Harga: **Rp 504.000** (dari database, bukan 250!) ✅
- Status: Lunas
- Metode: Transfer

**Entri #2 - Willo:**
- Barang: Willo
- Jumlah: 20 karton
- Harga: **Rp 504.000** ✅
- (data lain sama dengan entri #1)

**Entri #3 - Miksu:**
- Barang: Miksu
- Jumlah: 20 karton
- Harga: **Rp 650.000** ✅
- (data lain sama dengan entri #1)

## Jika Masih Bermasalah

### Debug Mode
Jalankan script debug untuk melihat detail proses:

```bash
python debug_siper_queen.py
```

Hasil yang benar:
```
✅ TEST 1 PASSED: Correct price (Rp 504.000)
✅ TEST 2 PASSED: Fuzzy match works correctly  
✅ TEST 3 PASSED: 'karton' prioritized correctly
```

### Periksa Log
Cek file `logs/bot.log` untuk melihat proses ekstraksi harga:

```bash
tail -f logs/bot.log | grep -i "harga\|price\|lookup"
```

## Catatan Penting

1. **Nama Produk di Database**  
   Pastikan nama produk di database adalah **"siiper quuen"** (huruf kecil, dengan typo), karena normalizer akan otomatis memperbaikinya menjadi "Siper Queen" untuk matching.

2. **Harga di Database**
   - siiper quuen + karton = Rp 504.000 ✅
   - siiper quuen + toples = Rp 14.000 ✅

3. **Cache**
   Jika masih ada masalah setelah perbaikan, clear cache dengan:
   ```python
   from core.bot_context import ctx
   ctx.gs_cache.invalidate()
   ```

## Kontak Support
Jika masih ada masalah, screenshot hasil test dan kirim ke developer.
