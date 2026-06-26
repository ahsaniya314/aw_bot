# Debug Session: dashboard-date-no-response

Status: OPEN

Bug:

- Dashboard menampilkan prompt `Pilih Tanggal`, tetapi setelah user mengirim tanggal, bot tidak memberi balasan.

Symptoms:

- Prompt tanggal muncul normal.
- Input tanggal manual seperti `19-06-2026` terlihat masuk dari user.
- Tidak ada respons lanjutan dari bot.

Initial Hypotheses:

- H1: Pesan tanggal tidak pernah masuk ke `handle_dashboard_date_input()`.
- H2: Pesan masuk, tetapi state sesi `awaiting_dashboard_date` hilang atau tertimpa sebelum dicek.
- H3: Pesan tanggal ditangkap `next_step_handler` lain, sehingga flow dashboard tidak sempat memprosesnya.
- H4: Parser `normalisasi_tanggal_gs()` gagal pada input yang user kirim, tetapi balasan error juga tidak terkirim.
- H5: Handler dashboard berhasil dipanggil, tetapi gagal saat render dashboard custom date dan error-nya tertelan.

Plan:

- Tambahkan log instrumentasi pada callback dashboard, text handler, dan handler input tanggal dashboard.
- Reproduksi alur `Pilih Tanggal` -> kirim tanggal.
- Bandingkan event runtime untuk menentukan hipotesis yang benar.
- Setelah penyebab terbukti, lakukan fix minimal dan verifikasi ulang.

Evidence Collected:

- `handle_dashboard_date_input()` dipanggil dari `handlers/text_handler.py` di bagian bawah flow text.
- Sebelum titik itu, `handlers/text_handler.py` memiliki blok skip yang menolak hampir semua state `awaiting_*`.
- State dashboard yang dipakai adalah `awaiting_dashboard_date`, sehingga pesan tanggal berisiko di-return lebih awal sebelum sampai ke handler dashboard.
- Instrumentasi runtime tetap dipertahankan untuk verifikasi setelah fix.

Fix Applied:

- Kecualikan `awaiting_dashboard_date` dari blok skip di `handlers/text_handler.py`.
- Ubah prompt dashboard agar memakai tombol `Batal` saja, bukan instruksi teks `ketik batal`.
- Tambahkan callback `dashboard_cancel_date_input` untuk membatalkan input tanggal.

Pending Verification:

- Restart bot/app.
- Uji `/dashboard` -> `Pilih Tanggal` -> kirim `19-06-2026`.

Additional Symptom:
- User melaporkan kirim foto tidak mendapat respons sama sekali.

Evidence:
- Import langsung `handlers.photo_handler` gagal dengan `SyntaxError: invalid character '📅' (U+1F4C5)` pada `handlers/photo_handler.py:230`.
- Penyebabnya adalah sisipan teks prompt dashboard mentah di tengah source file Python.
- Jika modul ini gagal di-import saat startup, handler foto tidak akan terpasang.

Fix Applied:
- Hapus sisipan teks non-Python dari `handlers/photo_handler.py`.

Next Verification:
- Restart bot/app.
- Kirim satu foto nota untuk memastikan handler foto kembali merespons.
