# [OPEN] Debug Session: save-dashboard-mismatch

## Ringkasan Masalah
- Gejala: data OCR/NLP sudah terbaca, tetapi setelah dikirim pengguna tidak melihat data di database maupun dashboard web.
- Ekspektasi: setelah tombol kirim ditekan, data masuk ke tabel `transaksi` dan muncul di dashboard web.

## Hipotesis
1. Callback tombol simpan tidak benar-benar memanggil alur `tangani_simpan_transaksi` atau `tangani_simpan_multi`.
2. Insert ke tabel relasional (`pelanggan` / `pesanan` / `pesanan_item`) berhasil, tetapi insert ke tabel flat `transaksi` gagal atau kosong.
3. Insert ke `transaksi` berhasil, tetapi dashboard web tidak menampilkan karena parsing tanggal / cache / filter rentang tanggal.
4. Session state atau `entitas` yang dikirim ke fungsi simpan tidak lengkap saat tombol kirim ditekan, sehingga data yang disimpan tidak sesuai atau gagal.
5. Ada exception runtime saat simpan, tetapi pesan sukses tetap terkirim karena jalur validasi response insert belum cukup ketat.

## Rencana Bukti
- Tambah instrumentation pada callback kirim, fungsi simpan tunggal/batch, dan API dashboard recent/summary.
- Reproduksi alur kirim data dan kumpulkan bukti runtime dari log.
- Cocokkan bukti insert database vs hasil query dashboard.

## Status
- Session dibuat.
- Menunggu instrumentation awal.
