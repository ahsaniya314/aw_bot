"""Auto-generated cleaned embedded data (removed flagged inconsistent waktu entries)."""
CLEANED_NLP_TRAINING_EXAMPLES = [
  {
    "text": "1 minggu lagi pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "1 minggu lagi"
    }
  },
  {
    "text": "Berapa harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "barang": "Permen"
    }
  },
  {
    "text": "Berapa total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Berapa total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "Berapa total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "Berapa total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "Berapa total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "Berapa total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "Cek harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "barang": "Permen"
    }
  },
  {
    "text": "Cek pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "Cek penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "Cek pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "Cek pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "Andi"
    }
  },
  {
    "text": "Cek pesanan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "Cek pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "Udin"
    }
  },
  {
    "text": "Cek/tampilkan harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "Cek/tampilkan pesanan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21-04-2026"
    }
  },
  {
    "text": "Edit harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "Ganti harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {
      "barang": "Brownis",
      "harga": "2000"
    }
  },
  {
    "text": "Ganti harga permen jadi 14.000",
    "intent": "edit_produk",
    "entities": {
      "barang": "Permen",
      "harga": "14000"
    }
  },
  {
    "text": "Hapus pesanan udin dengan status pembayaran belum lunas",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "Udin",
      "status": "Hutang"
    }
  },
  {
    "text": "Hapus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "Hapus/tampilkan semua data",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "Hari ini Udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "dus",
      "status": "Lunas"
    }
  },
  {
    "text": "Hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Naha",
      "barang": "Permen",
      "jumlah": "50",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Brownis",
      "jumlah": "100",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "1000000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Permen",
      "jumlah": "70",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "2000000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Serbuk",
      "jumlah": "100",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Agus",
      "barang": "Permen Coklat",
      "jumlah": "2",
      "satuan": "dus"
    }
  },
  {
    "text": "Hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "50",
      "satuan": "pcs"
    }
  },
  {
    "text": "Hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Rara",
      "barang": "Permen Coklat",
      "jumlah": "13",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Lunas"
    }
  },
  {
    "text": "Hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Supri",
      "barang": "Permen",
      "jumlah": "20",
      "satuan": "toples",
      "status": "Lunas"
    }
  },
  {
    "text": "Perbaharui pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "Naha"
    }
  },
  {
    "text": "Perbaharui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "Zio"
    }
  },
  {
    "text": "Pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "Ardi"
    }
  },
  {
    "text": "Siapa pembeli paling banyak hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Siapa pembeli terbanyak",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Siapa pembeli terbanyak hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Siapa transaksi terbangak hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Siapa tunggakan paking banyak",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "Siapa yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {}
  },
  {
    "text": "Siapa yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {}
  },
  {
    "text": "Siapa yang masih hutang",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "Siapa yang masih nyicil",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "Siapa yang pesan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "Tambah barang brownis harga 2500 per bungkus",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Brownis",
      "harga": "2500",
      "satuan": "bungkus"
    }
  },
  {
    "text": "Tambah barang brownis harga 2500 per toples",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Brownis",
      "harga": "2500",
      "satuan": "toples"
    }
  },
  {
    "text": "Tambah barang permen coklat",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Permen Coklat"
    }
  },
  {
    "text": "Tambah barang roti pia bulus",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Roti Pia Bulus"
    }
  },
  {
    "text": "Tampilan data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "Tampilkan daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "Tampilkan harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "barang": "Brownis"
    }
  },
  {
    "text": "Tampilkan jumlah pesanan dari pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "Andi"
    }
  },
  {
    "text": "Tampilkan semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "Tampilkan total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "Tampilkan transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "28"
    }
  },
  {
    "text": "Tampilkan uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "Total cicilan penjual hari ini",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "Update harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "Update pesanan naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "Naha"
    }
  },
  {
    "text": "Zio bayar hutang 27000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "Zio",
      "nominal_bayar": "27000000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Zio bayar tagihan 27 juta",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "Zio",
      "nominal_bayar": "27000000"
    }
  },
  {
    "text": "ada barang apa saja",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "ada berapa penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "add barang brownis",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "add produk permen",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "apa yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "apa yg blm lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "apakabar",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "assalamualaikum",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "barang apa saja yang ada",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "barang paling mahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "berapa banyak transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "berapa harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "berapa harga permen coklat",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "berapa harga produk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "berapa harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "berapa harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "serbuk"
    }
  },
  {
    "text": "berapa pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "berapa piutang hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total cicilan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "berapa total hutang pelanggan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "berapa total tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "berapa total transaksi",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "berapa total transaksi bulan ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "bulan ini"
    }
  },
  {
    "text": "berapa total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "berapa total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "berapa transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa transaksi kemarin",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "berapa transaksi pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "berapa tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "berapa uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "berapa yang masih tagihan",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "besok pak ardi ambil barang 100 buah brownis sudah dibayar",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "status": "lunas",
      "waktu": "besok"
    }
  },
  {
    "text": "brp harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "brp harga prduk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "buang semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "catat pelunasan pak zio 27 juta tf",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak zio",
      "nominal": "27000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "cek barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "cek harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek harga brg",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "cek harga permen",
    "intent": "tampilkan_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "cek harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "cek harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "serbuk"
    }
  },
  {
    "text": "cek hutang pelanggan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "cek hutang terbesar",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "cek pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "cek penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "cek penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "cek penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "cek penjulan hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "cek pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "cek pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "cek pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "cek pesanan pak hendra",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak hendra"
    }
  },
  {
    "text": "cek pesanan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "cek pesanan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21-04-2026"
    }
  },
  {
    "text": "cek pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "cek pesnan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "cek pesnan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "cek pesnan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "cek pesnan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21-04-2026"
    }
  },
  {
    "text": "cek pesnan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "cek piutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "cek pnjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "cek produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "cek semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "cek smua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "cek tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "cek transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "cek transaksi ibu maya",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "ibu maya"
    }
  },
  {
    "text": "cek transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "cek transaksi tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "cek transaksi tunai",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "tunai"
    }
  },
  {
    "text": "cek transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "cek transaksi via transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "cek tunggakan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "cek yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "tunai"
    }
  },
  {
    "text": "cek yang bayar via tf",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "cek yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "clear semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "customer terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "daftar barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "daftar hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "daftar penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "daftar penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "daftar penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "daftar prduk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "daftar produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "daftar tunggakan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "daftar yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "daftar yang bayar tf",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "daftarkan barang brownis",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "daftarkan produk permen",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "data pembelian pak rudi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak rudi"
    }
  },
  {
    "text": "data penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "data penjualan tanggal 5",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "5"
    }
  },
  {
    "text": "data pesanan mba rina",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "mba rina"
    }
  },
  {
    "text": "data tanggal 21 04",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21-04"
    }
  },
  {
    "text": "data transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "delete barang permen",
    "intent": "hapus_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "delete produk brownis",
    "intent": "hapus_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "delete semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "edit barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit data transaksi ibu maya",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "ibu maya"
    }
  },
  {
    "text": "edit harga brownis",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "edit harga produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit nama barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit order pak joko",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak joko"
    }
  },
  {
    "text": "edit pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak naha"
    }
  },
  {
    "text": "edit produk brownis",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "edit transaksi pak budi",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak budi"
    }
  },
  {
    "text": "ganti data transaksi pak soni",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak soni"
    }
  },
  {
    "text": "ganti harga brownis",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "ganti harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis",
      "harga_baru": "2000"
    }
  },
  {
    "text": "ganti harga brownis jdi 2000",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis",
      "harga_baru": "2000"
    }
  },
  {
    "text": "ganti harga permen coklat",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "ganti harga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen",
      "harga_baru": "14000"
    }
  },
  {
    "text": "ganti hrga prmen jdi 14000",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen",
      "harga_baru": "14000"
    }
  },
  {
    "text": "ganti nama barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "gimana penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "gmn penjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "hai",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hai bisa bantu saya",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hai bot",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hai kak",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hallo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hallo semuanya",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halloo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halo ada yang bisa bantu",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halo bot",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halo bro",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "haloo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "halooo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hapus barang brownis",
    "intent": "hapus_produk",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "hapus barang permen coklat",
    "intent": "hapus_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "hapus barang produk",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus data pak hendra",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak hendra"
    }
  },
  {
    "text": "hapus data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus harga barang",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus order pak rudi",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak rudi"
    }
  },
  {
    "text": "hapus pesanan pak budi",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak budi"
    }
  },
  {
    "text": "hapus pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "hapus pesanan udin dengan status pembayaran belum lunas",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "udin",
      "status": "belum lunas"
    }
  },
  {
    "text": "hapus pesnan udin",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "hapus pesnan udin dg status pembayaran blm lunas",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "udin",
      "status": "belum lunas"
    }
  },
  {
    "text": "hapus produk permen",
    "intent": "hapus_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "hapus produk roti pia",
    "intent": "hapus_produk",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "hapus produk serbuk",
    "intent": "hapus_produk",
    "entities": {
      "produk": "serbuk"
    }
  },
  {
    "text": "hapus rekap penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus riwayat pesanan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "hapus seluruh transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua data transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua order",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus smua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus smua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus transaksi pak andi",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "hapus transaksi pak joko",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "pak joko"
    }
  },
  {
    "text": "hapus transaksi udin",
    "intent": "hapus_transaksi",
    "entities": {
      "pelanggan": "udin"
    }
  },
  {
    "text": "harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "harga brownis diganti 2000",
    "intent": "edit_produk",
    "entities": {
      "produk": "brownis",
      "harga_baru": "2000"
    }
  },
  {
    "text": "harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "harga permen coklat",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "harga permen diubah 14000",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen",
      "harga_baru": "14000"
    }
  },
  {
    "text": "harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "serbuk"
    }
  },
  {
    "text": "harga terendah",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "terendah"
    }
  },
  {
    "text": "harga tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "hari ini ada order apa aja",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "hari ini ada transaksi apa",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "andi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "tunai"
    }
  },
  {
    "text": "hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "budi",
      "produk": "permen",
      "jumlah": "30",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "cash"
    }
  },
  {
    "text": "hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "naha",
      "produk": "permen",
      "jumlah": "50",
      "satuan": "dus",
      "bayar": "transfer",
      "status": "lunas"
    }
  },
  {
    "text": "hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "nala",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "bungkus",
      "dp": "1000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "nala",
      "produk": "permen",
      "jumlah": "70",
      "satuan": "dus",
      "dp": "2000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "nala",
      "produk": "serbuk",
      "jumlah": "100",
      "bayar": "transfer",
      "status": "lunas"
    }
  },
  {
    "text": "hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "pak agus",
      "produk": "permen coklat",
      "jumlah": "2",
      "satuan": "dus"
    }
  },
  {
    "text": "hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "pak andi",
      "produk": "permen",
      "jumlah": "50",
      "satuan": "pcs"
    }
  },
  {
    "text": "hari ini penjualan gimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "rara",
      "produk": "permen coklat",
      "jumlah": "13",
      "satuan": "dus",
      "bayar": "cash",
      "status": "lunas"
    }
  },
  {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "rudi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "langsung"
    }
  },
  {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "rudi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "cash"
    }
  },
  {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "rudi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "transfer"
    }
  },
  {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "rudi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "dp": "200000",
      "bayar": "transfer"
    }
  },
  {
    "text": "hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "rudi",
      "produk": "permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "lunas"
    }
  },
  {
    "text": "hari ini siapa yang beli",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "supri",
      "produk": "permen",
      "jumlah": "20",
      "satuan": "toples",
      "status": "lunas"
    }
  },
  {
    "text": "hari ini udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "udin",
      "produk": "permen",
      "jumlah": "30",
      "satuan": "dus",
      "status": "lunas"
    }
  },
  {
    "text": "hari minggu pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "hari minggu"
    }
  },
  {
    "text": "hei gan",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hello",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "helo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "helo bos",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hey",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hitung total transaksi",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "hlo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hlw",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hrga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "hrga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "hutang pelanggan berapa",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "hutang terbesar siapa",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "ibu sari lunasi hutang 1000000 tf",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "ibu sari",
      "nominal": "1000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "info penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "input barang brownis 2500",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis",
      "harga": "2500"
    }
  },
  {
    "text": "input produk permen coklat 13000",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat",
      "harga": "13000"
    }
  },
  {
    "text": "jumlah transaksi",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "jumlah transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "keluarkan data penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "kemarin ada order apa",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "kemarin pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "kemarin"
    }
  },
  {
    "text": "kemarin siapa yang beli",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "kemren ada order apa",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "laporan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "laporan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "laporan penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "laporan pnjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "lhat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "liatin semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "lihat data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat order pak doni",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak doni"
    }
  },
  {
    "text": "lihat penjualan tanggal 15",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "15"
    }
  },
  {
    "text": "lihat pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "lihat produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "lihat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "lihat transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "lihat yang belum bayar",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "list barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "list produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "list semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lusa pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "lusa"
    }
  },
  {
    "text": "masukkan produk baru permen coklat",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "mba rina bayar hutang 2000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "mba rina",
      "nominal": "2000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "met pagi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "met siang",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "minggu depan pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "minggu depan"
    }
  },
  {
    "text": "minggu depang pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
      "pelanggan": "pak ardi",
      "produk": "brownis",
      "jumlah": "100",
      "satuan": "buah",
      "bayar": "tunai",
      "status": "lunas",
      "waktu": "minggu depan"
    }
  },
  {
    "text": "order hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "order kemarin ada apa aja",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "order pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "order tanggal 14",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "14"
    }
  },
  {
    "text": "p kabar",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "pak andi bayar hutang 500000 cash",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak andi",
      "nominal": "500000",
      "bayar": "cash"
    }
  },
  {
    "text": "pak andi bayar hutng 500000 csh",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak andi",
      "nominal": "500000",
      "bayar": "cash"
    }
  },
  {
    "text": "pak andi beli apa saja",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "pak budi bayar cicilan 200000 tunai",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak budi",
      "nominal": "200000",
      "bayar": "tunai"
    }
  },
  {
    "text": "pak budi bayar ciciln 200000 tuni",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak budi",
      "nominal": "200000",
      "bayar": "tunai"
    }
  },
  {
    "text": "pak doni bayar 100000 cash",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak doni",
      "nominal": "100000",
      "bayar": "cash"
    }
  },
  {
    "text": "pak hendra bayar tagihan 750000 cash",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak hendra",
      "nominal": "750000",
      "bayar": "cash"
    }
  },
  {
    "text": "pak joko bayar cicilan 150000 langsung",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak joko",
      "nominal": "150000",
      "bayar": "langsung"
    }
  },
  {
    "text": "pak rudi bayar sisa 300000 transfer",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak rudi",
      "nominal": "300000",
      "bayar": "transfer"
    }
  },
  {
    "text": "pak soni bayar hutang 3000000 tf",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak soni",
      "nominal": "3000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "pak wahyu lunasi tagihan 500000 tunai",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak wahyu",
      "nominal": "500000",
      "bayar": "tunai"
    }
  },
  {
    "text": "pak zio udah bayar 27 juta transfer",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "pak zio",
      "nominal": "27000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "pelanggan paling banyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "pelanggan terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "pemasukan kemarin",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "pembeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "pembeli yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "pembeli yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "tunai"
    }
  },
  {
    "text": "pembelian hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "pembelian kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "penjualan 21 april 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21-04-2026"
    }
  },
  {
    "text": "penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "penjualan hari ini ada berapa",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "penjualan hari ini bagaimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "penjualan hari ini gimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "penjualan tanggal 25",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "25"
    }
  },
  {
    "text": "perbaharui harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "perbaharui order pak hendra",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak hendra"
    }
  },
  {
    "text": "perbaharui pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak naha"
    }
  },
  {
    "text": "perbaharui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "zio"
    }
  },
  {
    "text": "perbahrui pesnan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak naha"
    }
  },
  {
    "text": "perbahrui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "zio"
    }
  },
  {
    "text": "perbarui pesanan ibu sari",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "ibu sari"
    }
  },
  {
    "text": "permisi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "pesanan ibu sari",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "ibu sari"
    }
  },
  {
    "text": "pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "pesanan pak budi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak budi"
    }
  },
  {
    "text": "pesnan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak ardi"
    }
  },
  {
    "text": "piutang pelanggan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "produk apa saja",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "produk paling mahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "produk termahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "tertinggi"
    }
  },
  {
    "text": "produk termurah",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "filter": "terendah"
    }
  },
  {
    "text": "ranking pembeli",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "rekap hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "rekap kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "rekap penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "rekap pnjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "rekap semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "rekap tanggal 10",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "10"
    }
  },
  {
    "text": "rekap uang masuk",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "remove produk roti pia",
    "intent": "hapus_produk",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "ringkasan penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "riwayat penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "riwayat pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "salam",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "salam kenal",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "selamat malam",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "selamat pagi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "selamat siang",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "selamat sore",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "semua transaksi ada apa aja",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "show semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "siapa bayar di tempat",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "langsung"
    }
  },
  {
    "text": "siapa beli hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa cicilan terbesar",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa hutang terbanyak",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa hutng trbanyak",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa masih ada cicilan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa pembeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "siapa pembeli terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pembeli terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "siapa pembeli terbanyak kemarin",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "siapa pembeli terbesar",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pesan barang hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa punya hutang paling besar",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa tggakn paling banyak",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa transaksi terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "siapa tunggakan paling banyak",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang ambil barang hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "siapa yang bayar langsung",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "langsung"
    }
  },
  {
    "text": "siapa yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "siapa yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "tunai"
    }
  },
  {
    "text": "siapa yang beli hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa yang beli kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "siapa yang belum bayar",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang cicilan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang kontan",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "kontan"
    }
  },
  {
    "text": "siapa yang masih hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang masih nyicil",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang masih punya hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang order hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa yang order kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "siapa yang paling banyak cicilan",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak hutang",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak order",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak pesan",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak tunggakan",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang pesan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa yang tf",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "siapa yg bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "siapa yg bayar lgsung",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "langsung"
    }
  },
  {
    "text": "siapa yg bayar transfr",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "siapa yg bayar tuni",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "tunai"
    }
  },
  {
    "text": "siapa yg blm bayar",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yg msh hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yg msh nyicil",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yg order hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "siapa yg paling banyak order hri ini",
    "intent": "pembeli_terbanyak",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "siapa yg pesan hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "summary penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "tagihan hari ini berapa",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "tagihan pelanggan",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "tambah barang",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang baru",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang brownis harga 2500 per bungkus",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis",
      "harga": "2500",
      "satuan": "bungkus"
    }
  },
  {
    "text": "tambah barang brownis harga 2500 per toples",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis",
      "harga": "2500",
      "satuan": "toples"
    }
  },
  {
    "text": "tambah barang permen cokalat",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Permen Coklat"
    }
  },
  {
    "text": "tambah barang permen coklat",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "tambah barang prmen cklat harga 13.000",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat",
      "harga": "13000"
    }
  },
  {
    "text": "tambah barang produk permen coklat",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "tambah barang roti pia bulus",
    "intent": "tambah_produk",
    "entities": {
      "produk": "roti pia bulus"
    }
  },
  {
    "text": "tambah produk baru",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk brownis harga 2.500",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis",
      "harga": "2500"
    }
  },
  {
    "text": "tambah produk permen cokalat",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat"
    }
  },
  {
    "text": "tambah produk permen coklat harga 13.000",
    "intent": "tambah_produk",
    "entities": {
      "barang": "Permen Coklat",
      "harga": "13000"
    }
  },
  {
    "text": "tambah produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat",
      "harga": "13000"
    }
  },
  {
    "text": "tambahkan barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {
      "produk": "brownis",
      "harga": "2500"
    }
  },
  {
    "text": "tambahkan produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {
      "produk": "permen coklat",
      "harga": "13000"
    }
  },
  {
    "text": "tampil semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilan data penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "tampilan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilan semua transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "tampilan smua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilin data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilin semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilin transaksi hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "tampilin transaksi kmarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "tampilkan barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan daftar hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "tampilkan daftar transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan data penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "tampilkan harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
      "produk": "brownis"
    }
  },
  {
    "text": "tampilkan harga produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan hutang terbesar",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "tampilkan jumlah pesanan dari pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "tampilkan katalog produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "tampilkan penjualan tanggal 21 april",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21 april"
    }
  },
  {
    "text": "tampilkan pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "tampilkan piutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "tampilkan produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan rekap penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan riwayat transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan seluruh transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua data",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "tampilkan smua brg",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan smua prduk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan tagihan",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "tampilkan total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "tampilkan transaksi cash",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "tampilkan transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "tampilkan transaksi pak joko",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak joko"
    }
  },
  {
    "text": "tampilkan transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "28"
    }
  },
  {
    "text": "tampilkan transaksi tgl 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "28"
    }
  },
  {
    "text": "tampilkan transaksi transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "tampilkan tunggakan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "tampilkan uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "tampilkan yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "tampilkan yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "tampilkan yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "tamplkan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tanggal 21 ada transaksi apa",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "tanggal 28 ada order apa",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "28"
    }
  },
  {
    "text": "tgl 21 siapa yang beli",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21"
    }
  },
  {
    "text": "top pembeli",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "total cash masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini",
      "bayar": "cash"
    }
  },
  {
    "text": "total cicilan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "total cicilan penjualan hari ini",
    "intent": "total_tunggakan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total hutang",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "total order hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total pemasukan",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "total pembelian hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total pesanan pak budi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
      "pelanggan": "pak budi"
    }
  },
  {
    "text": "total piutang",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "total tagihan",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "total tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total transaksi",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total transaksi kemarin",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "total transaksi minggu ini",
    "intent": "total_transaksi",
    "entities": {
      "waktu": "minggu ini"
    }
  },
  {
    "text": "total transfer masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini",
      "bayar": "transfer"
    }
  },
  {
    "text": "total tunggakan",
    "intent": "total_tunggakan",
    "entities": {}
  },
  {
    "text": "total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "total uang masuk",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "transaksi hari ini apa saja",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "transaksi hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "transaksi tanggal 20",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "20"
    }
  },
  {
    "text": "transaksi tanggal 21 bulan 4",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "21 bulan 4"
    }
  },
  {
    "text": "transaksi tgl 20",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
      "tanggal": "20"
    }
  },
  {
    "text": "tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "tunggakan terbesar siapa",
    "intent": "hutang_terbanyak",
    "entities": {}
  },
  {
    "text": "uang masuk hari ini berapa",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "hari ini"
    }
  },
  {
    "text": "uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
      "waktu": "kemarin"
    }
  },
  {
    "text": "ubah data pesanan pak wahyu",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak wahyu"
    }
  },
  {
    "text": "ubah harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah harga permen",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "ubah harga produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah nama produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah order pak doni",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak doni"
    }
  },
  {
    "text": "ubah pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak naha"
    }
  },
  {
    "text": "ubah pesnan pak naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak naha"
    }
  },
  {
    "text": "ubah produk permen",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "ubah transaksi pak andi",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak andi"
    }
  },
  {
    "text": "update data pesnan naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "naha"
    }
  },
  {
    "text": "update harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update harga permen",
    "intent": "edit_produk",
    "entities": {
      "produk": "permen"
    }
  },
  {
    "text": "update harga produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update nama produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "update pesanan naha",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "naha"
    }
  },
  {
    "text": "update produk roti pia",
    "intent": "edit_produk",
    "entities": {
      "produk": "roti pia"
    }
  },
  {
    "text": "update transaksi pak rudi",
    "intent": "update_transaksi",
    "entities": {
      "pelanggan": "pak rudi"
    }
  },
  {
    "text": "yang bayar cash siapa",
    "intent": "filter_bayar_cash",
    "entities": {
      "bayar": "cash"
    }
  },
  {
    "text": "yang bayar transfer siapa",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "yang belum bayar siapa",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "yang paling sering beli siapa",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "yg bayar transfr siapa",
    "intent": "filter_bayar_transfer",
    "entities": {
      "bayar": "transfer"
    }
  },
  {
    "text": "zio bayar hutang 27000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "zio",
      "nominal": "27000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "zio bayar hutng 27000000 transfr",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "zio",
      "nominal": "27000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "zio bayar taghn 27 juta",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "zio",
      "nominal": "27000000"
    }
  },
  {
    "text": "zio bayar tagihan 27 juta",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "zio",
      "nominal": "27000000"
    }
  },
  {
    "text": "zio transfer 27 jt buat lunasin hutang",
    "intent": "bayar_hutang",
    "entities": {
      "pelanggan": "zio",
      "nominal": "27000000",
      "bayar": "transfer"
    }
  },
  {
    "text": "hari ini andi pesan l0lipop 10 dus",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "andi",
      "produk": "lolipop",
      "jumlah": "10",
      "satuan": "dus"
    }
  },
  {
    "text": "hari ini budi pesan loli pop 5 toples",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "budi",
      "produk": "lolipop",
      "jumlah": "5",
      "satuan": "toples"
    }
  },
  {
    "text": "hari ini nala pesan lolly pop 8 pack",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "nala",
      "produk": "lolipop",
      "jumlah": "8",
      "satuan": "pack"
    }
  },
  {
    "text": "hari ini rara pesan l0llip0p 12 pcs",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "rara",
      "produk": "lolipop",
      "jumlah": "12",
      "satuan": "pcs"
    }
  },
  {
    "text": "hari ini zio pesan lolypop 6 bungkus",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "zio",
      "produk": "lolipop",
      "jumlah": "6",
      "satuan": "bungkus"
    }
  },
  {
    "text": "berapa harga l0lipop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
      "produk": "lolipop"
    }
  },
  {
    "text": "berapa harga loli pop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
      "produk": "lolipop"
    }
  },
  {
    "text": "berapa harga lolly pop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
      "produk": "lolipop"
    }
  },
  {
    "text": "tambah barang l0lipop harga 15000 per pack",
    "intent": " tambah_produk",
    "entities": {
      "produk": "lolipop",
      "harga": "15000",
      "satuan": "pack"
    }
  },
  {
    "text": "edit harga l0lipop jadi 16000",
    "intent": " edit_produk",
    "entities": {
      "produk": "lolipop",
      "harga_baru": "16000"
    }
  },
  {
    "text": "hapus barang l0lipop",
    "intent": " hapus_produk",
    "entities": {
      "produk": "lolipop"
    }
  },
  {
    "text": "pak budi ambil willo 2 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "pak budi",
      "produk": "willo",
      "jumlah": "2",
      "satuan": "toples"
    }
  },
  {
    "text": "naha beli beem-beeng 1 karton",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "naha",
      "produk": "beem-beeng",
      "jumlah": "1",
      "satuan": "karton"
    }
  },
  {
    "text": "adangrow 5 pouch",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "adangrow",
      "jumlah": "5",
      "satuan": "pouch"
    }
  },
  {
    "text": "siperquuen 10 pack",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "siperquuen",
      "jumlah": "10",
      "satuan": "pack"
    }
  },
  {
    "text": "chocholetus 3 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "chocholetus",
      "jumlah": "3",
      "satuan": "toples",
      "status": "lunas"
    }
  },
  {
    "text": "miksu 1 paket",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "miksu",
      "jumlah": "1",
      "satuan": "paket"
    }
  },
  {
    "text": "lolipop 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "lolipop",
      "jumlah": "50",
      "satuan": "pcs"
    }
  },
  {
    "text": "coklat kubus 5 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "coklat kubus",
      "jumlah": "5",
      "satuan": "toples"
    }
  },
  {
    "text": "piramide 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "piramide",
      "jumlah": "2",
      "satuan": "dus"
    }
  },
  {
    "text": "mesis 10 bungkus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "mesis",
      "jumlah": "10",
      "satuan": "bungkus"
    }
  },
  {
    "text": "salju 1 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "salju",
      "jumlah": "1",
      "satuan": "toples"
    }
  },
  {
    "text": "serbuk jelli 5 pouch",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "serbuk jelli",
      "jumlah": "5",
      "satuan": "pouch"
    }
  },
  {
    "text": "pia bulus 2 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "pia bulus",
      "jumlah": "2",
      "satuan": "toples"
    }
  },
  {
    "text": "pia roda 1 ctn",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "produk": "pia roda",
      "jumlah": "1",
      "satuan": "karton"
    }
  },
  {
    "text": "hari ini andi ambil permen 3 dus lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "3",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini budi beli brownis 10 bungkus lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Brownis",
      "jumlah": "10",
      "satuan": "bungkus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "pak ardi pesan serbuk 2 karton sudah dibayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Ardi",
      "barang": "Serbuk",
      "jumlah": "2",
      "satuan": "karton",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "rara order permen coklat 5 dus dibayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Rara",
      "barang": "Permen Coklat",
      "jumlah": "5",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "QRIS"
    }
  },
  {
    "text": "udin ambil permen 1 dus lunas via qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Permen",
      "jumlah": "1",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "QRIS"
    }
  },
  {
    "text": "nala ambil roti pia 2 toples sudah lunas transfer bca",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Roti Pia",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "mas dodi beli mesis 4 bungkus bayar trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Dodi",
      "barang": "Mesis",
      "jumlah": "4",
      "satuan": "bungkus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "kak rina order salju 1 toples lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Rina",
      "barang": "Salju",
      "jumlah": "1",
      "satuan": "toples",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "zio ambil pia bulus 1 toples lunas qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Zio",
      "barang": "Pia Bulus",
      "jumlah": "1",
      "satuan": "toples",
      "status": "Lunas",
      "metode": "QRIS"
    }
  },
  {
    "text": "hari ini sinta beli lolipop 20 pcs dibayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Sinta",
      "barang": "Lolipop",
      "jumlah": "20",
      "satuan": "pcs",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini akbar pesan coklat kubus 2 toples lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Akbar",
      "barang": "Coklat Kubus",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini iwan ambil serbuk jelli 6 pouch lunas transfer bri",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Iwan",
      "barang": "Serbuk Jelli",
      "jumlah": "6",
      "satuan": "pouch",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "pak agus ambil permen 2 dus dibayar transfer mandiri",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Agus",
      "barang": "Permen",
      "jumlah": "2",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini dini beli permen 10 pcs lunas trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Dini",
      "barang": "Permen",
      "jumlah": "10",
      "satuan": "pcs",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini rudi pesan piramide 1 dus sudah dibayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Piramide",
      "jumlah": "1",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "QRIS"
    }
  },
  {
    "text": "hari ini andi order permen 30 toples dicicil 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini budi ambil brownis 20 bungkus dp 150000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Brownis",
      "jumlah": "20",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "150000",
      "metode": "Transfer"
    }
  },
  {
    "text": "nala pesan permen 10 dus dicicil 500000 dibayar transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Permen",
      "jumlah": "10",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "500000",
      "metode": "Transfer"
    }
  },
  {
    "text": "rara ambil permen coklat 4 dus uang muka 100000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Rara",
      "barang": "Permen Coklat",
      "jumlah": "4",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "100000",
      "metode": "Transfer"
    }
  },
  {
    "text": "udin order serbuk 2 karton nyicil 250000 trf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Serbuk",
      "jumlah": "2",
      "satuan": "karton",
      "status": "Cicil",
      "nominal_bayar": "250000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini zio ambil roti pia 3 toples dicicil 120000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Zio",
      "barang": "Roti Pia",
      "jumlah": "3",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "120000",
      "metode": "Transfer"
    }
  },
  {
    "text": "pak ardi pesan mesis 8 bungkus bayar dp 50000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Ardi",
      "barang": "Mesis",
      "jumlah": "8",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "50000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini sinta ambil salju 2 toples bayar sebagian 70000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Sinta",
      "barang": "Salju",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "70000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini iwan order permen 100 pcs dicicil 100000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Iwan",
      "barang": "Permen",
      "jumlah": "100",
      "satuan": "pcs",
      "status": "Cicil",
      "nominal_bayar": "100000",
      "metode": "Transfer"
    }
  },
  {
    "text": "akbar pesan pia bulus 5 toples dp 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Akbar",
      "barang": "Pia Bulus",
      "jumlah": "5",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Transfer"
    }
  },
  {
    "text": "dini ambil coklat kubus 2 toples dicicil 80000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Dini",
      "barang": "Coklat Kubus",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "80000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini rudi order piramide 3 dus dicicil 300000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Piramide",
      "jumlah": "3",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "300000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini agus order permen 40 pcs dicicil setengah 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Agus",
      "barang": "Permen",
      "jumlah": "40",
      "satuan": "pcs",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Transfer"
    }
  },
  {
    "text": "hari ini andi order permen 30 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "hari ini budi ambil brownis 20 bungkus dp 150000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Brownis",
      "jumlah": "20",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "150000",
      "metode": "Tunai"
    }
  },
  {
    "text": "nala pesan permen 10 dus dicicil 500000 dibayar tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Permen",
      "jumlah": "10",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "500000",
      "metode": "Tunai"
    }
  },
  {
    "text": "rara ambil permen coklat 4 dus uang muka 100000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rara",
      "barang": "Permen Coklat",
      "jumlah": "4",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "100000",
      "metode": "Tunai"
    }
  },
  {
    "text": "udin order serbuk 2 karton nyicil 250000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Serbuk",
      "jumlah": "2",
      "satuan": "karton",
      "status": "Cicil",
      "nominal_bayar": "250000",
      "metode": "Tunai"
    }
  },
  {
    "text": "hari ini zio ambil roti pia 3 toples dicicil 120000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Zio",
      "barang": "Roti Pia",
      "jumlah": "3",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "120000",
      "metode": "Tunai"
    }
  },
  {
    "text": "pak ardi pesan mesis 8 bungkus bayar dp 50000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Ardi",
      "barang": "Mesis",
      "jumlah": "8",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "50000",
      "metode": "Tunai"
    }
  },
  {
    "text": "hari ini sinta ambil salju 2 toples bayar sebagian 70000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Sinta",
      "barang": "Salju",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "70000",
      "metode": "Tunai"
    }
  },
  {
    "text": "hari ini iwan order permen 100 pcs dicicil 100000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Iwan",
      "barang": "Permen",
      "jumlah": "100",
      "satuan": "pcs",
      "status": "Cicil",
      "nominal_bayar": "100000",
      "metode": "Tunai"
    }
  },
  {
    "text": "akbar pesan pia bulus 5 toples dp 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Akbar",
      "barang": "Pia Bulus",
      "jumlah": "5",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "dini ambil coklat kubus 2 toples dicicil 80000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Dini",
      "barang": "Coklat Kubus",
      "jumlah": "2",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "80000",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 2 aqua bayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "barang": "Aqua",
      "jumlah": "2",
      "satuan": "botol",
      "status": "Lunas",
      "metode": "QRIS"
    }
  },
  {
    "text": "jual 3 permen bayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "barang": "Permen",
      "jumlah": "3",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "jual 1 brownis bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Brownis",
      "jumlah": "1",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 5 permen dicicil 20000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "barang": "Permen",
      "jumlah": "5",
      "status": "Cicil",
      "nominal_bayar": "20000",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 5 permen dicicil 20000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "barang": "Permen",
      "jumlah": "5",
      "status": "Cicil",
      "nominal_bayar": "20000",
      "metode": "Transfer"
    }
  },
  {
    "text": "jual 10 roti pia bayar cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Roti Pia",
      "jumlah": "10",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 1 serbuk bayar trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "barang": "Serbuk",
      "jumlah": "1",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "jual permen 2 dus bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Permen",
      "jumlah": "2",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual permen 2 dus bayar tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "barang": "Permen",
      "jumlah": "2",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "jual 2 permen dp 10000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "barang": "Permen",
      "jumlah": "2",
      "status": "Cicil",
      "nominal_bayar": "10000",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 2 aqua bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Aqua",
      "jumlah": "2",
      "satuan": "botol",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 1 aqua lunas tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Aqua",
      "jumlah": "1",
      "satuan": "botol",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 3 permen kontan",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Permen",
      "jumlah": "3",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 2 serbuk bayar cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Serbuk",
      "jumlah": "2",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 5 mesis bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Mesis",
      "jumlah": "5",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 1 piramide lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Piramide",
      "jumlah": "1",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 4 pia bulus dibayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Pia Bulus",
      "jumlah": "4",
      "satuan": "toples",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "jual 10 lolipop bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "barang": "Lolipop",
      "jumlah": "10",
      "satuan": "pcs",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "hari ini pak andi pesan permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini pak agus ngambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini rara ambil permen coklat 13 dus lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini udin ngambil permen 30 dus lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini naha ambil permen 50 dus lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {}
  },
  {
    "text": "hari ini nala ambil permen 70 dus cicil 2000000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {}
  },
  {
    "text": "hari ini nala ambil brownis 100 bungkus cicil 1000000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {}
  },
  {
    "text": "hari ini nala ambil serbuk 100 lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {}
  },
  {
    "text": "hari ini rudi order permen 600 toples cicil 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {}
  },
  {
    "text": "hari ini rudi order permen 600 toples cicil 200000 lunas",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {}
  },
  {
    "text": "hari ini rudi order permen 600 toples cicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {}
  },
  {
    "text": "hari ini budi order permen 30 toples cicil 200000 cash langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {}
  },
  {
    "text": "hari ini rudi order permen 600 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini andi order permen 600 toples cicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {}
  },
  {
    "text": "hari ini rudi order permen 600 toples cicil 200000 langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {}
  },
  {
    "text": "hari ini supri ambil permen 20 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "kemarin pak ardi beli brownis 100 buah lunas cash",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "kemarin ardi ambil brownis 100 udah bayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "besok ardi ambil brownis 100 buah lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "lusa ardi ambil brownis 100 buah lunas cash",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "3 hari lalu ardi ambil brownis 100 lunas tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "2 hari yang lalu budi ambil permen 50 dus lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "3 hari ke depan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "minggu dpan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "1 minggu ke depan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "hari selasa pak ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "hari rabu naha ambil permen 50 dus lunas transfer",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {}
  },
  {
    "text": "hari ini pak andi oredre permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hri ini pak andi order prmen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini paka andi order permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ni pak andi order permen 50 pcs lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hri ini rudi ordr permen 600 toples cicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {}
  },
  {
    "text": "hari ini budi ambl brownis 30 bungkus luans",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "kemrin ardi ambil brownis 100 udah bayar tnai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "minggu dpan ardi ambl brownis 100 lunas tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini supri ambil permen 20 topls sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "hari ini nala ambl srbuk 100 lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {}
  },
  {
    "text": "tadi andi beli permen 50 pcs lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "pak andi beli permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "pak agus pesan permen coklat 2 dus hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "pak agus beli permen coklat 2 dus hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "pak agus transaksi permen coklat 2 dus hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "catat pesanan pak andi permen 50 pcs hari ini lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "input transaksi pak andi permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "tambah transaksi pak andi permen 50 pcs hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "simpan transaksi pak andi permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "rekap pak andi beli permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {}
  },
  {
    "text": "tampil semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "tampilkan data penjualan lusa",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {}
  },
  {
    "text": "lihat pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "tampilkan pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "cek pesanan tanggal 21 april 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "tampilkan pesanan tanggal 21 april",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "lihat transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "data tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "pesanan tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "tampilkan semua transaksi/data/pembelian pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua data pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua pembelian pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan jumlah pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "riwayat pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "Cek pesanan/transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "lihat transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "riwayat udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "tampilkaan semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "liht semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan semua tranksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampilkan dat penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "pesanan pak ardi hari ini",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "tampiln transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {}
  },
  {
    "text": "liat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "liat transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {}
  },
  {
    "text": "liat pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "lht riwayat pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {}
  },
  {
    "text": "print semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tampung semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "daftar semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "list semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {}
  },
  {
    "text": "Hapus semua data penjualan/transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua data/daftar penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua data",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus seluruh data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua rekap penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pesanan udin belum lunas",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus transaksi udin belum lunas",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pesanan/transaksi udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus data udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pesanan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus data pak andi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pembelian pak andi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semwa data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semu transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus penjualan udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pesenan udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hpus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus pesanaan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hps semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus semua dat penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapus transaks udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "remove pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "clear semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "bersihkan semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hilangkan semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapusin semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "hapusin pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {}
  },
  {
    "text": "Update pesanan/transaksi naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "update transaksi naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "Perbaharui/ubah/edit pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "edit transaksi zio",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ubah transaksi zio",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "update data pak ardi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ubah data pesanan pak ardi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "edit data pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "perbarui pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ganti status pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ganti status bayar pak andi jadi lunas",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ubah status bayar naha jadi lunas",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "edit status pembayaran udin",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "zio bayar hutang 27 juta transfer",
    "intent": "Pelunasan_Hutang",
    "entities": {}
  },
  {
    "text": "zio bayar tagihan 27000000",
    "intent": "Pelunasan_Hutang",
    "entities": {}
  },
  {
    "text": "zio lunasin tagihan 27 juta",
    "intent": "Pelunasan_Hutang",
    "entities": {}
  },
  {
    "text": "zio bayar cicilan 27 juta transfer",
    "intent": "Pelunasan_Hutang",
    "entities": {}
  },
  {
    "text": "zio bayar 27000000 tf",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "updaet pesanan naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "update pesanaan naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "perbaharui pesenan pak naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "edti transaksi zio",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "edit transaks zio",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ubah transksi pak ardi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "update dat pak ardi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "zio byr hutang 27 juta tf",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "modify pesanan naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "revisi pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "koreksi transaksi zio",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "change data pesanan pak ardi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "ganti data transaksi pak andi",
    "intent": "update_transaksi",
    "entities": {}
  },
  {
    "text": "Cek/tampilkan harga barang/produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek harga produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampil semua barang/produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "lihat daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "lihat semua produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "harga brownis berapa",
    "intent": "cek_harga_produk_spesifik",
    "entities": {}
  },
  {
    "text": "lihat harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {}
  },
  {
    "text": "harga produk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {}
  },
  {
    "text": "harga termahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {}
  },
  {
    "text": "produk apa yang paling mahal",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek hraga permen",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan hrga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek hrga produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "berapa hraga permen",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "berapa hrga brownis",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkan semua barng",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "liat harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {}
  },
  {
    "text": "liat semua produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "tampilkn daftar harga",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "cek harga prmen",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "show harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "print daftar produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "info harga barang",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "info produk",
    "intent": "tampilkan_produk",
    "entities": {}
  },
  {
    "text": "Tambah barang/produk permen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk permen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang/produk",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang brownis harga 2500 toples",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk brownis 2500 per toples",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang brownis harga 2500 bungkus",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk roti pia bulus",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "input produk baru permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "input barang baru brownis 2500",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah item permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "daftarkan produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "masukkan barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambh barang permen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang premen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tamabah produk permen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tamabah barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah brg brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang bornwis harga 2500",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah produk rmeni coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tamabh barang roti pia",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "tambah barang/produk permen cokalat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "add barang permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "buat produk baru permen coklat",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "create produk permen coklat 13000",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "register barang brownis 2500 toples",
    "intent": "tambah_produk",
    "entities": {}
  },
  {
    "text": "edit barang/produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "Edit/update/ubah/hapus harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "Update/ubah/edti harga barang/produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edti harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update harga brownis 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit harga brownis 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah harga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update harga permen 14000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit harga permen 14000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah harga barang/produk",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit/ubah/ganti/update/perbaharui nama barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ganti nama brownis jadi brownies premium",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah nama permen jadi permen original",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edti barang permen",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ganti hraga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah hrga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "updaet harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edti harga prmen",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "ubah harga brownis jd 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "update hrga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "edit produk brwnis",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "modify harga brownis 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "change harga permen 14000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "revisi harga brownis 2000",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "koreksi harga barang",
    "intent": "edit_produk",
    "entities": {}
  },
  {
    "text": "hapus barang",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus produk",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus barang permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus produk brownis",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah nama barang/produk",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "buang produk permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "delete produk permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "remove barang brownis",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hilangkan barang roti",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus brang permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hpus produk permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus prdk permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus barang brwnis",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "hapus produk browni",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "remove produk brownis",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "buang produk brownis",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "clear barang permen",
    "intent": "hapus_produk",
    "entities": {}
  },
  {
    "text": "total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "Cek/tampilkan/berapa pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "total cicilan hari ini",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "berapa cicilan hari ini",
    "intent": "total_tagihan",
    "entities": {}
  },
  {
    "text": "berapa total transaks hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "total transakis hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "brp total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "total uang masuk hari ni",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "brp uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "total uang taagihan hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "total tunggakaan hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "berapa pemassukan hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "rekap transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "summary transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {}
  },
  {
    "text": "omzet hari ini",
    "intent": "total_uang_masuk",
    "entities": {}
  },
  {
    "text": "siapa yang masih cicil",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang punya hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang bayar dengan transfer",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang bayar cash/tunai/langsung",
    "intent": "filter_bayar_cash",
    "entities": {}
  },
  {
    "text": "siapa bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {}
  },
  {
    "text": "siapa bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {}
  },
  {
    "text": "siapa yang msh nyicil",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang masih nyicill",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang masih ntang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yg masih hutang",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa paling banyak hutng",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yg byr cash",
    "intent": "filter_bayar_cash",
    "entities": {}
  },
  {
    "text": "siapa yang byr transfer",
    "intent": "filter_bayar_transfer",
    "entities": {}
  },
  {
    "text": "siapa yang blm lunas",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang outstanding",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang kredit",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang debt",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang nunggak",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa yang punya tagihan",
    "intent": "filter_belum_lunas",
    "entities": {}
  },
  {
    "text": "siapa saja yang pesan hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak beli hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak transaksi hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling banyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "Siapa pembeli terbanyak hari ini/kemarin/tanggal sekian",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pembeli terbanyak tanggal 21",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang pesn hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa saja yg order hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pemeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pembeli trbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang paling bnyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa pmbeli terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "pelanggan terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "customer terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "pembeli top hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "siapa yang belanja terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {}
  },
  {
    "text": "pagi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "siang",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "sore",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "malam",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "assalamu'alaikum",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "wassalamu'alaikum",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "ada orang",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "helloo",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "haii",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hie",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "slmat pagi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "selamat apgi",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "helo bot",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "hai bott",
    "intent": "greeting",
    "entities": {}
  },
  {
    "text": "bantuan",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "help",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "tolong",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "cara pakai",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "cara menggunakan",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "perintah apa saja",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "apa saja yang bisa dilakukan",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "fitur apa saja",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "menu",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "panduan",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "tutorial",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "info",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "informasi",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "bantuaan",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "hlp",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "helpp",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "bantu dong",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "cara pake",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "cara nggunain",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "perintah apa aj",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "menu apa aj",
    "intent": "bantuan",
    "entities": {}
  },
  {
    "text": "Hari ini udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "dus",
      "status": "Lunas"
    }
  },
  {
    "text": "Hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Permen",
      "jumlah": "30",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Naha",
      "barang": "Permen",
      "jumlah": "50",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Brownis",
      "jumlah": "100",
      "satuan": "bungkus",
      "status": "Cicil",
      "nominal_bayar": "1000000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Permen",
      "jumlah": "70",
      "satuan": "dus",
      "status": "Cicil",
      "nominal_bayar": "2000000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
      "pelanggan": "Nala",
      "barang": "Serbuk",
      "jumlah": "100",
      "status": "Lunas",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Agus",
      "barang": "Permen Coklat",
      "jumlah": "2",
      "satuan": "dus"
    }
  },
  {
    "text": "Hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Andi",
      "barang": "Permen",
      "jumlah": "50",
      "satuan": "pcs"
    }
  },
  {
    "text": "Hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Rara",
      "barang": "Permen Coklat",
      "jumlah": "13",
      "satuan": "dus",
      "status": "Lunas",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Transfer"
    }
  },
  {
    "text": "Hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Rudi",
      "barang": "Permen",
      "jumlah": "600",
      "satuan": "toples",
      "status": "Lunas"
    }
  },
  {
    "text": "Hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
      "pelanggan": "Supri",
      "barang": "Permen",
      "jumlah": "20",
      "satuan": "toples",
      "status": "Lunas"
    }
  },
  {
    "text": "cek hutang",
    "intent": "cek_hutang",
    "entities": {}
  },
  {
    "text": "cek hutang pelanggan",
    "intent": "cek_hutang",
    "entities": {}
  },
  {
    "text": "cek piutang",
    "intent": "cek_hutang",
    "entities": {}
  },
  {
    "text": "cek tagihan",
    "intent": "cek_tagihan",
    "entities": {}
  },
  {
    "text": "cek tagihan pelanggan",
    "intent": "cek_tagihan",
    "entities": {}
  },
  {
    "text": "cek semua penjualan",
    "intent": "cek_semua_penjualan",
    "entities": {}
  },
  {
    "text": "cek semua transaksi",
    "intent": "cek_semua_penjualan",
    "entities": {}
  },
  {
    "text": "lihat semua transaksi",
    "intent": "lihat_semua_transaksi",
    "entities": {}
  },
  {
    "text": "lihat semua penjualan",
    "intent": "lihat_semua_transaksi",
    "entities": {}
  },
  {
    "text": "tanggal 19-06-2026 budi ambil bembeng 40 ctn dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_tanggal_spesifik",
    "entities": {
      "pelanggan": "Budi",
      "barang": "Bembeng",
      "jumlah": "40",
      "satuan": "ctn",
      "status": "Cicil",
      "nominal_bayar": "200000",
      "metode": "Tunai",
      "waktu": "tanggal 19-06-2026"
    }
  },
  {
    "text": "21 april 2026 udin ambil meses 20 ctn dicicil 150000 cash",
    "intent": "tambah_transaksi_cicilan_tanggal_spesifik",
    "entities": {
      "pelanggan": "Udin",
      "barang": "Meses",
      "jumlah": "20",
      "satuan": "ctn",
      "status": "Cicil",
      "nominal_bayar": "150000",
      "metode": "Tunai",
      "waktu": "21 april 2026"
    }
  },
  {
    "text": "hari ini pak andi order bembeng 10 ctn; meses 5 ctn; willo 12 ctn sudah lunas cash",
    "intent": "tambah_transaksi_multi_item",
    "entities": {
      "pelanggan": "Andi",
      "status": "Lunas",
      "metode": "Tunai"
    }
  }
]
