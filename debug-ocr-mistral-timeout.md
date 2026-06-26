# Debug Session: ocr-mistral-timeout

Status: OPEN

Bug:
- OCR gagal dengan error `HTTPSConnectionPool(host='api.mistral.ai', port=443): Read timed out. (read timeout=60)`.

Symptoms:
- User mengirim foto.
- Proses OCR memanggil API `api.mistral.ai`.
- Request berhenti pada batas waktu baca 60 detik dan melempar exception timeout.

Initial Hypotheses:
- H1: File gambar terlalu besar atau payload terlalu berat, sehingga respons Mistral lewat dari 60 detik.
- H2: Jalur OCR tidak memakai retry/backoff, jadi timeout tunggal langsung menggagalkan seluruh proses.
- H3: Ada perlambatan jaringan atau koneksi keluar ke `api.mistral.ai` dari environment bot.
- H4: Model/endpoint OCR Mistral yang dipakai sedang lambat atau responsnya tidak stabil untuk jenis input tertentu.
- H5: Timeout 60 detik di client terlalu agresif dibanding waktu proses OCR aktual pada gambar nota tertentu.

Plan:
- Temukan implementasi service OCR dan titik pemanggilan Mistral.
- Tambahkan instrumentasi runtime untuk mencatat ukuran file, durasi request, timeout yang dipakai, dan jenis exception.
- Reproduksi atau analisis jalur timeout berdasarkan bukti log.
- Terapkan fix minimal hanya setelah hipotesis terkonfirmasi oleh bukti runtime.

Evidence:
- Error aktual dari user: `HTTPSConnectionPool(host='api.mistral.ai', port=443): Read timed out. (read timeout=60)`.
- Kode di `services/ocr_service.py` sebelumnya hardcode `timeout=(10, 60)` pada request ke `https://api.mistral.ai/v1/chat/completions`.
- Jalur request sebelumnya tidak memiliki retry untuk timeout.
- `extract_text()` mengembalikan string `Error OCR: ...` saat exception, dan `handlers/photo_handler.py` sebelumnya memperlakukan string non-kosong itu sebagai hasil OCR sukses.

Confirmed / Rejected:
- H2 confirmed: tidak ada retry/backoff untuk timeout.
- H5 confirmed: timeout baca 60 detik memang berasal dari client lokal.
- H1/H3/H4 belum terpisah secara final; bisa ikut berkontribusi, tetapi fix minimal tetap perlu membuat client lebih tahan timeout.

Fix Applied:
- Tambahkan timeout OCR Mistral yang bisa diatur via env:
  - `MISTRAL_OCR_CONNECT_TIMEOUT_SECONDS` default `10`
  - `MISTRAL_OCR_READ_TIMEOUT_SECONDS` default `120`
  - `MISTRAL_OCR_MAX_ATTEMPTS` default `2`
- Tambahkan retry pada timeout di `services/ocr_service.py`.
- Ubah `photo_handler.py` agar hasil `Error OCR: ...` tidak diteruskan sebagai teks OCR sukses ke NLP, tetapi ditampilkan sebagai pesan gagal yang ramah.
- Pertahankan instrumentasi `post-fix` untuk verifikasi runtime berikutnya.

Pending Verification:
- Restart bot/app.
- Kirim ulang foto yang sama.
- Cek apakah OCR berhasil, atau minimal error yang tampil sekarang menjadi pesan timeout yang lebih ramah tanpa meneruskan teks error ke NLP.
