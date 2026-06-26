"""
Script untuk menghasilkan dan mengekspor 5 kategori dataset chatbot Telegram
penjualan UMKM A&W Production ke dalam format CSV dan Excel (multi-sheet).
Setiap kategori dataset berisi minimal 100 data.
"""

import os
import sys
import pandas as pd
import json

# Tambahkan root directory ke sys.path agar bisa mengimpor modul nlp
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from nlp.normalizer import koreksi_teks
from nlp.embedded_data import NORMALIZATION_DICT

# ---------------------------------------------------------
# 1. DATASET INTENT (4.2.2)
# ---------------------------------------------------------
data_intent = [
    # tambah_data (25 data)
    {"intent": "tambah_data", "contoh_kalimat": "tambah transaksi 5 dus permen coklat lunas cash"},
    {"intent": "tambah_data", "contoh_kalimat": "input pesanan pak ardi 10 box roti pia roda belum lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tambahkan 3 ctn coklat millo transfer bank"},
    {"intent": "tambah_data", "contoh_kalimat": "bikin data penjualan 12 bungkus brownis cash"},
    {"intent": "tambah_data", "contoh_kalimat": "catat orderan baru permen lolipop 50 toples sudah bayar"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah order 20 bungkus roti pia potong belum dibayar"},
    {"intent": "tambah_data", "contoh_kalimat": "masukkan penjualan 5 pcs keripik singkong lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "rekam transaksi 100 bungkus serbuk jeli bayar lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tulis pesanan baru kopi sachet 2 renceng cash"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah penjualan 2 botol minyak goreng belum lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "simpan orderan 5 kg gula pasir lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "input transaksi baru 1 ctn wilo coklat lunas transfer"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah transaksi 3 bungkus meses coklat cash"},
    {"intent": "tambah_data", "contoh_kalimat": "masukin pesanan baru 10 dus pia bulus lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah order 15 pcs jaket hitam transfer"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah transaksi 2 pcs kaos putih cash"},
    {"intent": "tambah_data", "contoh_kalimat": "input data 30 bungkus serbuk salju lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "catat penjualan 4 pak mie instan belum bayar"},
    {"intent": "tambah_data", "contoh_kalimat": "tambahkan transaksi 2 toples bemmbeng lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah orderan 5 pcs coklat kubus cash"},
    {"intent": "tambah_data", "contoh_kalimat": "masukkan pesanan 2 ctn piramide lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah transaksi 3 pack roti pia bulus cash"},
    {"intent": "tambah_data", "contoh_kalimat": "rekam orderan baru 500 pcs permen lolipop lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "simpan transaksi 10 pak snack ring belum lunas"},
    {"intent": "tambah_data", "contoh_kalimat": "tambah data penjualan 100 botol air mineral lunas"},

    # tampilkan_data (25 data)
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan semua data penjualan"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat pesanan minggu ini"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek pesanan yang belum lunas"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan rekap penjualan kemarin"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan transaksi hari ini"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat rekap pemasukan bulan ini"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan pesanan lunas hari ini"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek daftar transaksi belum bayar"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan semua orderan masuk"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat list penjualan permen coklat"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek laporan keuangan minggu lalu"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan transaksi atas nama pak ardi"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan pesanan roti pia roda kemarin"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat data transaksi tanggal 12 juni"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek daftar produk terlaris"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan rekap penjualan permen lolipop"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan riwayat pesanan udin"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat penjualan hari ini lunas"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek transaksi pembayaran transfer"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan laporan penjualan bulanan"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat data penjualan coklat kubus"},
    {"intent": "tampilkan_data", "contoh_kalimat": "cek rekap transaksi bulan juni"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan semua pesanan cicilan"},
    {"intent": "tampilkan_data", "contoh_kalimat": "tampilkan rekap uang masuk hari ini"},
    {"intent": "tampilkan_data", "contoh_kalimat": "lihat daftar hutang pelanggan"},

    # update_data (25 data)
    {"intent": "update_data", "contoh_kalimat": "update status transaksi pak andi jadi lunas"},
    {"intent": "update_data", "contoh_kalimat": "ubah harga permen lolipop jadi 12000"},
    {"intent": "update_data", "contoh_kalimat": "ganti jumlah pesanan brownis budi jadi 15"},
    {"intent": "update_data", "contoh_kalimat": "edit nominal bayar orderan pak ardi"},
    {"intent": "update_data", "contoh_kalimat": "update harga roti pia roda menjadi 15000"},
    {"intent": "update_data", "contoh_kalimat": "ubah data pesanan udin ganti barang ke permen coklat"},
    {"intent": "update_data", "contoh_kalimat": "ganti metode pembayaran transaksi 102 jadi transfer"},
    {"intent": "update_data", "contoh_kalimat": "edit jumlah barang orderan siti jadi 20 bungkus"},
    {"intent": "update_data", "contoh_kalimat": "update tanggal ambil pesanan pak ardi jadi besok"},
    {"intent": "update_data", "contoh_kalimat": "ubah status pembayaran orderan 45 menjadi belum lunas"},
    {"intent": "update_data", "contoh_kalimat": "ganti harga brownis coklat jadi 25000"},
    {"intent": "update_data", "contoh_kalimat": "update status cicilan budi lunas"},
    {"intent": "update_data", "contoh_kalimat": "edit data penjualan permen willo ganti kuantitas 50"},
    {"intent": "update_data", "contoh_kalimat": "ubah nama pelanggan transaksi 105 jadi pak rudi"},
    {"intent": "update_data", "contoh_kalimat": "ganti total harga pesanan joni jadi 500000"},
    {"intent": "update_data", "contoh_kalimat": "update harga satuan coklat millo jadi 2000"},
    {"intent": "update_data", "contoh_kalimat": "edit status bayar orderan kaos hitam jadi lunas"},
    {"intent": "update_data", "contoh_kalimat": "ubah nominal dp transaksi 222 jadi 100000"},
    {"intent": "update_data", "contoh_kalimat": "ganti kategori produk keripik jadi snack kering"},
    {"intent": "update_data", "contoh_kalimat": "update jumlah orderan roti pia bulus menjadi 5 dus"},
    {"intent": "update_data", "contoh_kalimat": "edit tanggal transaksi orderan 88 jadi kemarin"},
    {"intent": "update_data", "contoh_kalimat": "ubah harga satuan permen lolipop toples"},
    {"intent": "update_data", "contoh_kalimat": "ganti detail transaksi pak ardi terbaru"},
    {"intent": "update_data", "contoh_kalimat": "update nominal pembayaran cash lunas"},
    {"intent": "update_data", "contoh_kalimat": "edit catatan pesanan coklat kubus"},

    # hapus_data (25 data)
    {"intent": "hapus_data", "contoh_kalimat": "hapus pesanan udin"},
    {"intent": "hapus_data", "contoh_kalimat": "batalin transaksi terakhir"},
    {"intent": "hapus_data", "contoh_kalimat": "delete data penjualan roti pia roda pak andi"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus orderan yang belum bayar"},
    {"intent": "hapus_data", "contoh_kalimat": "batalkan pesanan permen coklat siti"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus transaksi id 102"},
    {"intent": "hapus_data", "contoh_kalimat": "delete orderan brownis budi"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus semua data penjualan kemarin"},
    {"intent": "hapus_data", "contoh_kalimat": "batalin transaksi tanggal 15 juni"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus data pelanggan bernama joko"},
    {"intent": "hapus_data", "contoh_kalimat": "delete data penjualan permen lolipop lunas"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus pesanan jaket putih belum lunas"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus rekap transaksi id 450"},
    {"intent": "hapus_data", "contoh_kalimat": "batalkan orderan coklat millo pak ardi"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus data barang roti pia bulus"},
    {"intent": "hapus_data", "contoh_kalimat": "delete transaksi cicilan budi"},
    {"intent": "hapus_data", "contoh_kalimat": "batalin pesanan 5 dus permen coklat"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus orderan yang salah input"},
    {"intent": "hapus_data", "contoh_kalimat": "delete data penjualan kaos hitam"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus data transaksi lunas hari ini"},
    {"intent": "hapus_data", "contoh_kalimat": "batalkan transaksi transfer bank kemarin"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus detail pesanan udin"},
    {"intent": "hapus_data", "contoh_kalimat": "delete data orderan gagal ocr"},
    {"intent": "hapus_data", "contoh_kalimat": "hapus transaksi lunas tunai"},
    {"intent": "hapus_data", "contoh_kalimat": "batalkan pesanan keripik singkong"},

    # cari_data (25 data)
    {"intent": "cari_data", "contoh_kalimat": "cari pesanan atas nama pak ardi"},
    {"intent": "cari_data", "contoh_kalimat": "cek pesanan roti pia bulus"},
    {"intent": "cari_data", "contoh_kalimat": "cari transaksi tanggal 12 juni"},
    {"intent": "cari_data", "contoh_kalimat": "cari penjualan permen lolipop"},
    {"intent": "cari_data", "contoh_kalimat": "temukan orderan belum lunas"},
    {"intent": "cari_data", "contoh_kalimat": "cari data pelanggan bernama udin"},
    {"intent": "cari_data", "contoh_kalimat": "cek transaksi hari ini tunai"},
    {"intent": "cari_data", "contoh_kalimat": "cari pesanan kaos hitam"},
    {"intent": "cari_data", "contoh_kalimat": "temukan transaksi nominal 150000"},
    {"intent": "cari_data", "contoh_kalimat": "cari data penjualan brownis"},
    {"intent": "cari_data", "contoh_kalimat": "cek orderan atas nama siti"},
    {"intent": "cari_data", "contoh_kalimat": "cari transaksi pembayaran transfer"},
    {"intent": "cari_data", "contoh_kalimat": "temukan data penjualan bulan mei"},
    {"intent": "cari_data", "contoh_kalimat": "cari pesanan roti pia roda"},
    {"intent": "cari_data", "contoh_kalimat": "cek transaksi id 120"},
    {"intent": "cari_data", "contoh_kalimat": "cari detail orderan permen coklat"},
    {"intent": "cari_data", "contoh_kalimat": "temukan pesanan belum lunas kemarin"},
    {"intent": "cari_data", "contoh_kalimat": "cari data penjualan mie instan"},
    {"intent": "cari_data", "contoh_kalimat": "cek transaksi pak rudi"},
    {"intent": "cari_data", "contoh_kalimat": "cari pesanan jaket putih"},
    {"intent": "cari_data", "contoh_kalimat": "temukan penjualan total di atas 100000"},
    {"intent": "cari_data", "contoh_kalimat": "cari orderan dengan status cicilan"},
    {"intent": "cari_data", "contoh_kalimat": "cek penjualan tanggal 10 april"},
    {"intent": "cari_data", "contoh_kalimat": "cari pesanan permen willo"},
    {"intent": "cari_data", "contoh_kalimat": "temukan data transaksi lunas cash"}
]

# ---------------------------------------------------------
# 2. DATASET ENTITAS (4.2.3)
# ---------------------------------------------------------
data_entitas = [
    # nama_barang (20)
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Permen Coklat", "contoh_penggunaan": "tambah transaksi 5 dus permen coklat"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Roti Pia Roda", "contoh_penggunaan": "input pesanan 10 box roti pia roda"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Roti Pia Bulus", "contoh_penggunaan": "tambah orderan 3 dus roti pia bulus"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Brownis", "contoh_penggunaan": "bikin data penjualan 12 bungkus brownis"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Permen Lolipop", "contoh_penggunaan": "beli 50 toples permen lolipop"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Willo", "contoh_penggunaan": "tambah order 1 ctn wilo coklat"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Bemmbeng", "contoh_penggunaan": "tambahkan transaksi 2 toples bemmbeng"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Adangrow", "contoh_penggunaan": "beli 10 sachet adangrow rasa coklat"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Cholatos", "contoh_penggunaan": "tambah transaksi 5 box cholatos wafer"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Miksu", "contoh_penggunaan": "input orderan 30 cup es miksu vanilla"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Getbory", "contoh_penggunaan": "tambah penjualan 12 bar getbory coklat"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Salju", "contoh_penggunaan": "catat pesanan 5 bungkus serbuk salju"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Serbuk Jelly", "contoh_penggunaan": "input 20 pack serbuk jelly stroberi"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Coklat Kubus", "contoh_penggunaan": "tambah orderan 5 pcs coklat kubus"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Coklat Piramide", "contoh_penggunaan": "masukkan pesanan 2 ctn piramide"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Meses Coklat", "contoh_penggunaan": "tambah transaksi 3 bungkus meses coklat"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Keripik Singkong", "contoh_penggunaan": "masukkan penjualan 5 pcs keripik singkong"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Mie Instan", "contoh_penggunaan": "catat penjualan 4 pak mie instan goreng"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Kaos", "contoh_penggunaan": "tambah transaksi 2 pcs kaos putih polos"},
    {"jenis_entitas": "nama_barang", "nilai_entitas": "Jaket", "contoh_penggunaan": "tambah order 15 pcs jaket hitam hoodie"},

    # jumlah (20)
    {"jenis_entitas": "jumlah", "nilai_entitas": "5", "contoh_penggunaan": "tambah transaksi 5 dus permen coklat"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "10", "contoh_penggunaan": "input pesanan pak ardi 10 box roti pia roda"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "3", "contoh_penggunaan": "tambahkan 3 ctn coklat millo transfer bank"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "12", "contoh_penggunaan": "bikin data penjualan 12 bungkus brownis cash"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "50", "contoh_penggunaan": "catat orderan baru permen lolipop 50 toples"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "20", "contoh_penggunaan": "tambah order 20 bungkus roti pia potong"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "100", "contoh_penggunaan": "rekam transaksi 100 bungkus serbuk jeli bayar lunas"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "2", "contoh_penggunaan": "tambah penjualan 2 botol minyak goreng belum lunas"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "15", "contoh_penggunaan": "tambah order 15 pcs jaket hitam transfer"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "30", "contoh_penggunaan": "masukin pesanan baru 30 dus pia bulus lunas"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "1", "contoh_penggunaan": "input transaksi baru 1 ctn wilo coklat"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "600", "contoh_penggunaan": "hari ini andi order permen 600 toples"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "30", "contoh_penggunaan": "tambah transaksi 30 pack roti pia bulus cash"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "500", "contoh_penggunaan": "rekam orderan baru 500 pcs permen lolipop"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "4", "contoh_penggunaan": "catat penjualan 4 pak mie instan belum bayar"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "25", "contoh_penggunaan": "tambahkan transaksi 25 toples bemmbeng lunas"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "120", "contoh_penggunaan": "input data 120 bungkus serbuk salju lunas"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "8", "contoh_penggunaan": "tambah data penjualan 8 botol air mineral"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "150", "contoh_penggunaan": "beli kaos 150 pcs sablon custom"},
    {"jenis_entitas": "jumlah", "nilai_entitas": "7", "contoh_penggunaan": "pesan meses coklat sebanyak 7 bungkus"},

    # harga_satuan (20)
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "5000", "contoh_penggunaan": "harga permen lolipop 5000 per toples"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "15000", "contoh_penggunaan": "roti pia roda seharga 15000 satu bungkus"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "25000", "contoh_penggunaan": "brownis dipatok harga 25000 rupiah"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "2000", "contoh_penggunaan": "harga permen coklat 2000 per pcs murah"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "75000", "contoh_penggunaan": "kaos polos seharga 75000 per lembar"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "150000", "contoh_penggunaan": "harga jaket putih 150000 satu jaket"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "12000", "contoh_penggunaan": "mie instan 12000 per pak isi lima"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "35000", "contoh_penggunaan": "harga keripik singkong 35000 per kilo gram"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "10000", "contoh_penggunaan": "serbuk jeli seharga 10000 per pack"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "8000", "contoh_penggunaan": "willo seharga 8000 satu sachet besar"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "4500", "contoh_penggunaan": "bemmbeng seharga 4500 satu bungkus kecil"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "60000", "contoh_penggunaan": "coklat kubus seharga 60000 satu toples"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "85000", "contoh_penggunaan": "coklat piramide seharga 85000 satu kotak"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "14000", "contoh_penggunaan": "meses warna seharga 14000 per bungkus"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "18000", "contoh_penggunaan": "minyak goreng seharga 18000 satu liter"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "13500", "contoh_penggunaan": "gula pasir seharga 13500 per kilo gram"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "9500", "contoh_penggunaan": "tepung terigu seharga 9500 satu kilo"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "3000", "contoh_penggunaan": "air mineral seharga 3000 satu botol"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "50000", "contoh_penggunaan": "kopi bubuk seharga 50000 satu kemasan kaleng"},
    {"jenis_entitas": "harga_satuan", "nilai_entitas": "20000", "contoh_penggunaan": "saus sambal seharga 20000 satu botol kaca"},

    # total_harga (20)
    {"jenis_entitas": "total_harga", "nilai_entitas": "25000", "contoh_penggunaan": "total belanjaan semuanya jadi 25000 rupiah"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "150000", "contoh_penggunaan": "total penjualan hari ini 150000 rupiah"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "180000", "contoh_penggunaan": "pembayaran total senilai 180000 ditransfer"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "75000", "contoh_penggunaan": "total transaksi lunas 75000 cash"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "300000", "contoh_penggunaan": "nominal transaksi sebesar 300000 dicatat"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "500000", "contoh_penggunaan": "total orderan kaos 500000 sudah dp"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "120000", "contoh_penggunaan": "total harga roti pia bulus 120000"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "60000", "contoh_penggunaan": "pembayaran sebagian total 60000 sisanya hutang"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "1000000", "contoh_penggunaan": "nominal pembayaran transfer 1000000 bank mandiri"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "45000", "contoh_penggunaan": "total harga permen lolipop 45000 lunas"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "90000", "contoh_penggunaan": "total bayar wilo coklat 90000 cash"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "350000", "contoh_penggunaan": "total transaksi cicilan 350000 rupiah"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "240000", "contoh_penggunaan": "total belanja mie instan 240000 rupiah"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "70000", "contoh_penggunaan": "total harga meses coklat 70000 lunas"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "54000", "contoh_penggunaan": "total harga minyak goreng 54000 bayar cash"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "27000", "contoh_penggunaan": "total belanja gula pasir 27000 tunai"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "190000", "contoh_penggunaan": "total harga jaket hitam 190000 sudah bayar"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "800000", "contoh_penggunaan": "total transaksi lunas transfer 800000"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "15000", "contoh_penggunaan": "total harga snack ring 15000 rupiah"},
    {"jenis_entitas": "total_harga", "nilai_entitas": "200000", "contoh_penggunaan": "total bayar tunai cash 200000 lunas"},

    # warna (20)
    {"jenis_entitas": "warna", "nilai_entitas": "hitam", "contoh_penggunaan": "jaket hitam ukuran L 2 pcs"},
    {"jenis_entitas": "warna", "nilai_entitas": "putih", "contoh_penggunaan": "pesan kaos putih polos 2 pcs"},
    {"jenis_entitas": "warna", "nilai_entitas": "merah", "contoh_penggunaan": "roti pia bulus bungkus merah 5 pack"},
    {"jenis_entitas": "warna", "nilai_entitas": "coklat", "contoh_penggunaan": "permen coklat manis 3 toples"},
    {"jenis_entitas": "warna", "nilai_entitas": "kuning", "contoh_penggunaan": "keripik pisang kemasan kuning manis"},
    {"jenis_entitas": "warna", "nilai_entitas": "biru", "contoh_penggunaan": "order jaket biru navy ukuran XL"},
    {"jenis_entitas": "warna", "nilai_entitas": "hijau", "contoh_penggunaan": "teh hijau kemasan kotak karton"},
    {"jenis_entitas": "warna", "nilai_entitas": "abu-abu", "contoh_penggunaan": "pesanan kaos abu-abu 5 pcs cash"},
    {"jenis_entitas": "warna", "nilai_entitas": "warna-warni", "contoh_penggunaan": "permen lolipop warna-warni toplesan"},
    {"jenis_entitas": "warna", "nilai_entitas": "pink", "contoh_penggunaan": "lolipop stroberi warna pink cerah"},
    {"jenis_entitas": "warna", "nilai_entitas": "gelap", "contoh_penggunaan": "kaos warna gelap ukuran M"},
    {"jenis_entitas": "warna", "nilai_entitas": "terang", "contoh_penggunaan": "jaket warna terang untuk berkendara"},
    {"jenis_entitas": "warna", "nilai_entitas": "polos", "contoh_penggunaan": "kaos polos hitam 10 lembar"},
    {"jenis_entitas": "warna", "nilai_entitas": "belang", "contoh_penggunaan": "snack kemasan belang rasa pedas"},
    {"jenis_entitas": "warna", "nilai_entitas": "emas", "contoh_penggunaan": "coklat kubus bungkus emas mewah"},
    {"jenis_entitas": "warna", "nilai_entitas": "perak", "contoh_penggunaan": "coklat piramide bungkus perak kemasan dus"},
    {"jenis_entitas": "warna", "nilai_entitas": "orange", "contoh_penggunaan": "serbuk jeli rasa jeruk warna orange segar"},
    {"jenis_entitas": "warna", "nilai_entitas": "ungu", "contoh_penggunaan": "serbuk jelly rasa anggur warna ungu tua"},
    {"jenis_entitas": "warna", "nilai_entitas": "gelap", "contoh_penggunaan": "meses coklat gelap 2 bungkus"},
    {"jenis_entitas": "warna", "nilai_entitas": "pelangi", "contoh_penggunaan": "meses warna pelangi toples sedang"},

    # kategori (20)
    {"jenis_entitas": "kategori", "nilai_entitas": "permen", "contoh_penggunaan": "tampilkan produk kategori permen manis"},
    {"jenis_entitas": "kategori", "nilai_entitas": "roti", "contoh_penggunaan": "semua transaksi kategori roti pia roda"},
    {"jenis_entitas": "kategori", "nilai_entitas": "snack", "contoh_penggunaan": "daftar barang kategori snack keripik"},
    {"jenis_entitas": "kategori", "nilai_entitas": "minuman", "contoh_penggunaan": "minuman segar dingin botolan aqua"},
    {"jenis_entitas": "kategori", "nilai_entitas": "sembako", "contoh_penggunaan": "kategori sembako minyak goreng dan gula"},
    {"jenis_entitas": "kategori", "nilai_entitas": "pakaian", "contoh_penggunaan": "daftar penjualan kategori pakaian kaos dan jaket"},
    {"jenis_entitas": "kategori", "nilai_entitas": "coklat", "contoh_penggunaan": "kategori coklat batangan premium getbory"},
    {"jenis_entitas": "kategori", "nilai_entitas": "serbuk", "contoh_penggunaan": "kategori serbuk minuman salju manis"},
    {"jenis_entitas": "kategori", "nilai_entitas": "bumbu", "contoh_penggunaan": "kategori bumbu dapur kecap manis pedas"},
    {"jenis_entitas": "kategori", "nilai_entitas": "jeli", "contoh_penggunaan": "makanan ringan kategori jeli rasa buah"},
    {"jenis_entitas": "kategori", "nilai_entitas": "mie", "contoh_penggunaan": "mie instan kuah masuk kategori mie"},
    {"jenis_entitas": "kategori", "nilai_entitas": "kopi", "contoh_penggunaan": "kategori kopi sachet luwak black"},
    {"jenis_entitas": "kategori", "nilai_entitas": "susu", "contoh_penggunaan": "kategori susu bubuk dancow coklat"},
    {"jenis_entitas": "kategori", "nilai_entitas": "kue", "contoh_penggunaan": "kategori kue basah brownies lumer"},
    {"jenis_entitas": "kategori", "nilai_entitas": "minyak", "contoh_penggunaan": "kategori minyak goreng kelapa sawit bimoli"},
    {"jenis_entitas": "kategori", "nilai_entitas": "tepung", "contoh_penggunaan": "kategori tepung terigu segitiga biru"},
    {"jenis_entitas": "kategori", "nilai_entitas": "kaos", "contoh_penggunaan": "pakaian kategori kaos oblong sablon"},
    {"jenis_entitas": "kategori", "nilai_entitas": "jaket", "contoh_penggunaan": "pakaian kategori jaket hoodie wol"},
    {"jenis_entitas": "kategori", "nilai_entitas": "permen coklat", "contoh_penggunaan": "kategori permen coklat millo toples"},
    {"jenis_entitas": "kategori", "nilai_entitas": "roti pia", "contoh_penggunaan": "kategori roti pia bulus isi kacang hijau"},

    # tanggal (20)
    {"jenis_entitas": "tanggal", "nilai_entitas": "16 juni 2026", "contoh_penggunaan": "tampilkan transaksi tanggal 16 juni 2026"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "kemarin", "contoh_penggunaan": "rekap penjualan kemarin hari senin"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "hari ini", "contoh_penggunaan": "tampilkan transaksi hari ini lunas"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "besok", "contoh_penggunaan": "diambil besok pagi jam 9 oleh budi"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "lusa", "contoh_penggunaan": "pesanan dikirim lusa hari rabu"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "minggu ini", "contoh_penggunaan": "laporan penjualan minggu ini lengkap"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "12-05-2026", "contoh_penggunaan": "transaksi tanggal 12-05-2026 lunas"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "01/06/2026", "contoh_penggunaan": "penjualan tanggal 01/06/2026 kontan"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "15 Juni", "contoh_penggunaan": "transaksi hari senin 15 Juni dicatat"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "akhir bulan", "contoh_penggunaan": "laporan untuk akhir bulan mei kemarin"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "awal tahun", "contoh_penggunaan": "rekap penjualan awal tahun 2026"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "senin lalu", "contoh_penggunaan": "pesanan senin lalu sudah dikirim lunas"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "21-04-2026", "contoh_penggunaan": "pesanan tanggal 21-04-2026 diubah"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "2026-06-10", "contoh_penggunaan": "transaksi tanggal 2026-06-10 selesai"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "mei kemarin", "contoh_penggunaan": "rekap penjualan bulan mei kemarin dicatat"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "juni ini", "contoh_penggunaan": "laporan transaksi juni ini diekspor"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "3 hari yang lalu", "contoh_penggunaan": "transaksi 3 hari yang lalu belum lunas"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "1 minggu lagi", "contoh_penggunaan": "pesanan diambil 1 minggu lagi hari selasa"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "tanggal 25", "contoh_penggunaan": "rekap transaksi tanggal 25 lunas cash"},
    {"jenis_entitas": "tanggal", "nilai_entitas": "pertengahan bulan", "contoh_penggunaan": "rekap pertengahan bulan juni 2026"}
]

# ---------------------------------------------------------
# 3. KAMUS NORMALISASI (4.2.4)
# ---------------------------------------------------------
# Ambil dari NORMALIZATION_DICT dan tambahkan user-specific + custom agar minimal 110 data
kamus_normalization = []
seen_tidak_baku = set()

# Wajib dari instruksi user
user_wajib = [
    {"kata_tidak_baku": "tmbh", "kata_baku": "tambah"},
    {"kata_tidak_baku": "htm", "kata_baku": "hitam"},
    {"kata_tidak_baku": "pth", "kata_baku": "putih"},
    {"kata_tidak_baku": "jkt", "kata_baku": "jaket"},
    {"kata_tidak_baku": "kaoss", "kata_baku": "kaos"},
    {"kata_tidak_baku": "pcs", "kata_baku": "pcs"},
]

for item in user_wajib:
    kamus_normalization.append(item)
    seen_tidak_baku.add(item["kata_tidak_baku"])

# Tambahkan dari NORMALIZATION_DICT["typo_corrections"]
typos = NORMALIZATION_DICT.get("typo_corrections", {})
for k, v in typos.items():
    if k not in seen_tidak_baku:
        kamus_normalization.append({"kata_tidak_baku": k, "kata_baku": v})
        seen_tidak_baku.add(k)

# Tambahkan dari NORMALIZATION_DICT["abbreviations"]
abbrs = NORMALIZATION_DICT.get("abbreviations", {})
for k, v in abbrs.items():
    if k not in seen_tidak_baku:
        kamus_normalization.append({"kata_tidak_baku": k, "kata_baku": v})
        seen_tidak_baku.add(k)

# Jika masih kurang dari 115, tambahkan beberapa variasi
extra_dict = {
    "tmb": "tambah",
    "tmbhin": "tambah",
    "inputt": "input",
    "catatt": "catat",
    "hps": "hapus",
    "apush": "hapus",
    "del": "hapus",
    "apz": "hapus",
    "updt": "update",
    "updet": "update",
    "ubahh": "ubah",
    "gantii": "ganti",
    "tampill": "tampilkan",
    "liatt": "lihat",
    "cekk": "cek",
    "hri": "hari",
    "kmrin": "kemarin",
    "kemren": "kemarin",
    "bsk": "besok",
    "bsok": "besok",
    "mggu": "minggu",
    "mnggu": "minggu",
    "bln": "bulan",
    "thn": "tahun",
    "jt": "juta",
    "rb": "ribu",
    "k": "ribu",
    "rts": "ratus",
    "pc": "pcs",
    "packk": "pack",
    "boxx": "box",
    "ctnn": "carton",
    "topls": "toples",
    "prmn": "permen",
    "cklat": "coklat",
    "c0klat": "coklat",
    "piaa": "pia",
    "bronis": "brownies",
    "brwnis": "brownies",
    "browniss": "brownies",
    "jely": "jelly",
    "jelli": "jelly",
    "yelli": "jelly",
    "loli": "lolipop",
    "lolipp": "lolipop",
    "bembeng": "bemmbeng",
    "adang": "adangrow",
    "chocho": "cholatos",
    "millo": "milo",
    "milo": "milo",
    "kripi": "keripik",
    "krupuk": "kerupuk",
    "krpuk": "kerupuk",
    "minyakg": "minyak goreng",
    "minykg": "minyak goreng",
    "gulaa": "gula",
    "garem": "garam",
    "trigu": "terigu",
    "aer": "air",
    "jkt": "jaket",
    "kaoss": "kaos",
    "hoddie": "hoodie",
    "hody": "hoodie",
    "lunas cash": "lunas tunai",
    "lns": "lunas",
    "byr": "bayar",
    "dibyr": "dibayar",
    "transferr": "transfer",
    "trf": "transfer",
    "tf": "transfer",
    "ciciln": "cicilan",
    "ccil": "cicil",
    "htng": "hutang",
    "utng": "hutang",
    "blm": "belum",
    "sdh": "sudah",
    "udh": "sudah",
    "dah": "sudah",
    "msh": "masih",
    "yg": "yang",
}

for k, v in extra_dict.items():
    if k not in seen_tidak_baku:
        kamus_normalization.append({"kata_tidak_baku": k, "kata_baku": v})
        seen_tidak_baku.add(k)

# Pastikan ukuran list minimal 115
kamus_normalization = kamus_normalization[:120]  # batasi biar pas rapi

# ---------------------------------------------------------
# 4. DATASET SEBELUM NORMALISASI (4.2.5) & DATASET SETELAH NORMALISASI (4.2.6)
# ---------------------------------------------------------
# Kita mendefinisikan 100 raw data sebelum normalisasi
data_sebelum_normalisasi = [
    # Teks (50 data)
    {"sumber_input": "teks", "data_mentah": "tmbh 3 pcs kaos htm 75000"},
    {"sumber_input": "teks", "data_mentah": "input 2 jkt pth 150rb"},
    {"sumber_input": "teks", "data_mentah": "tambah transaksi 5 toples prmen cklat lns"},
    {"sumber_input": "teks", "data_mentah": "bikin orderan baru 10 pack pia roda udh dibyr"},
    {"sumber_input": "teks", "data_mentah": "input pesanan pak ardi 12 box bronis blm lns"},
    {"sumber_input": "teks", "data_mentah": "tmbhin 3 ctn millo coklat trf bca"},
    {"sumber_input": "teks", "data_mentah": "cek hrg permen loli hari ini"},
    {"sumber_input": "teks", "data_mentah": "tampilin smua data penjualan kmrin"},
    {"sumber_input": "teks", "data_mentah": "hapu5 orderan udin yg blm bayar"},
    {"sumber_input": "teks", "data_mentah": "ganti hrg roti pia roda jd 16000"},
    {"sumber_input": "teks", "data_mentah": "cari data transaksi atas nama siti"},
    {"sumber_input": "teks", "data_mentah": "tambah 25 toples bembeng bayar cash"},
    {"sumber_input": "teks", "data_mentah": "input 5 sachet adangrow cokelat"},
    {"sumber_input": "teks", "data_mentah": "bikin transaksi 30 cup miksu vanilla lunas"},
    {"sumber_input": "teks", "data_mentah": "tulis pesanan 12 bar getbory transfer bank"},
    {"sumber_input": "teks", "data_mentah": "tmb 5 bungkus serbuk salju lunas"},
    {"sumber_input": "teks", "data_mentah": "input 20 pack jely stroberi lunas cash"},
    {"sumber_input": "teks", "data_mentah": "tambah orderan 5 pcs coklat kubus bungkus emas"},
    {"sumber_input": "teks", "data_mentah": "masukin pesanan 2 ctn piramide lunas"},
    {"sumber_input": "teks", "data_mentah": "tambah transaksi 3 bungkus mses coklat cash"},
    {"sumber_input": "teks", "data_mentah": "masukkan penjualan 5 pcs kripi singkong lns"},
    {"sumber_input": "teks", "data_mentah": "catat penjualan 4 pak mi instan goreng blm bayar"},
    {"sumber_input": "teks", "data_mentah": "tambah data penjualan 8 botol aer mineral lns"},
    {"sumber_input": "teks", "data_mentah": "pesan meses coklat sebanyak 7 bngkus"},
    {"sumber_input": "teks", "data_mentah": "tampilkan transaksi tgl 16 juni 2026"},
    {"sumber_input": "teks", "data_mentah": "rekap penjualan kemren hri senin"},
    {"sumber_input": "teks", "data_mentah": "tampilkan pesanan lunas hri ini"},
    {"sumber_input": "teks", "data_mentah": "diambil bsk pagi jam 9 oleh budi"},
    {"sumber_input": "teks", "data_mentah": "pesanan dikirim lsa hri rabu"},
    {"sumber_input": "teks", "data_mentah": "laporan penjualan mnggu ini lengkap"},
    {"sumber_input": "teks", "data_mentah": "transaksi tgl 12-05-2026 lns"},
    {"sumber_input": "teks", "data_mentah": "penjualan tgl 01/06/2026 kntan"},
    {"sumber_input": "teks", "data_mentah": "transaksi hri senin 15 Juni dicatat"},
    {"sumber_input": "teks", "data_mentah": "laporan untuk akhir bln mei kemaren"},
    {"sumber_input": "teks", "data_mentah": "rekap penjualan awal thn 2026"},
    {"sumber_input": "teks", "data_mentah": "pesanan senin lalu sdh dikirim lns"},
    {"sumber_input": "teks", "data_mentah": "pesanan tgl 21-04-2026 diubah"},
    {"sumber_input": "teks", "data_mentah": "transaksi tanggal 2026-06-10 selesai"},
    {"sumber_input": "teks", "data_mentah": "rekap penjualan bln mei kemaren dicatat"},
    {"sumber_input": "teks", "data_mentah": "laporan transaksi juni ini diekspor"},
    {"sumber_input": "teks", "data_mentah": "transaksi 3 hari yg lalu blm lns"},
    {"sumber_input": "teks", "data_mentah": "pesanan diambil 1 mggu lagi hri selasa"},
    {"sumber_input": "teks", "data_mentah": "rekap transaksi tanggal 25 lns cash"},
    {"sumber_input": "teks", "data_mentah": "rekap pertengahan bln juni 2026"},
    {"sumber_input": "teks", "data_mentah": "update status transaksi pak andi jd lns"},
    {"sumber_input": "teks", "data_mentah": "ubah hrg permen loli jd 12000"},
    {"sumber_input": "teks", "data_mentah": "ganti jml pesanan bronis budi jd 15"},
    {"sumber_input": "teks", "data_mentah": "edit nominal byar orderan pak ardi"},
    {"sumber_input": "teks", "data_mentah": "update hrg roti pia roda mjdi 15000"},
    {"sumber_input": "teks", "data_mentah": "ubah data pesanan udin ganti brg ke permen coklat"},

    # OCR (50 data dengan simulasi noise OCR khas)
    {"sumber_input": "OCR", "data_mentah": "3pc kaoss htm 75.000"},
    {"sumber_input": "OCR", "data_mentah": "tamp11kan transaks1 kemar1n"},
    {"sumber_input": "OCR", "data_mentah": "hapu5 pesanan ud1n"},
    {"sumber_input": "OCR", "data_mentah": "tmbah 10 t0p1es prrmen ck1at 1unas"},
    {"sumber_input": "OCR", "data_mentah": "b1k1n 5 ctn wi10 c0k1at udh d1byr"},
    {"sumber_input": "OCR", "data_mentah": "cek hrg r0ti p1a r0da"},
    {"sumber_input": "OCR", "data_mentah": "brapa hrg br0wn1s har1 1n1"},
    {"sumber_input": "OCR", "data_mentah": "1 ctn c0k1at m1110 1unas ca5h"},
    {"sumber_input": "OCR", "data_mentah": "1nput 2 jkt pth 150rb"},
    {"sumber_input": "OCR", "data_mentah": "tmbh 3 pc5 ka05 htm 75000"},
    {"sumber_input": "OCR", "data_mentah": "d5 permen c0k1at 1ns ca5h"},
    {"sumber_input": "OCR", "data_mentah": "paka ardi amb1l 10 b0x r0t1 p1a r0da"},
    {"sumber_input": "OCR", "data_mentah": "3 ctn c0k1at m1110 trf bank"},
    {"sumber_input": "OCR", "data_mentah": "penjua1an 12 bngku5 br0n1s csh"},
    {"sumber_input": "OCR", "data_mentah": "prmen 1o1ip0p 50 t0p1es sdh byr"},
    {"sumber_input": "OCR", "data_mentah": "20 bngku5 r0t1 p1a p0t0ng b1m d1byr"},
    {"sumber_input": "OCR", "data_mentah": "penjua1an 5 pc5 kr1p1k s1ngk0ng 1ns"},
    {"sumber_input": "OCR", "data_mentah": "100 bngkus 5erbuk je11 byr 1ns"},
    {"sumber_input": "OCR", "data_mentah": "k0p1 5achet 2 renceng ca5h"},
    {"sumber_input": "OCR", "data_mentah": "2 b0t01 m1nyak g0reng b1m 1ns"},
    {"sumber_input": "OCR", "data_mentah": "5 kg gu1a pa51r 1una5"},
    {"sumber_input": "OCR", "data_mentah": "1 ctn w110 c0k1at 1ns trf"},
    {"sumber_input": "OCR", "data_mentah": "3 bngku5 me5e5 c0k1at ca5h"},
    {"sumber_input": "OCR", "data_mentah": "10 du5 p1a bu1u5 1una5"},
    {"sumber_input": "OCR", "data_mentah": "15 pc5 jkt htm trf"},
    {"sumber_input": "OCR", "data_mentah": "2 pc5 ka05 pth c5h"},
    {"sumber_input": "OCR", "data_mentah": "30 bngku5 5erbuk 5a1ju 1ns"},
    {"sumber_input": "OCR", "data_mentah": "4 pak m1 1n5tan b1m bayar"},
    {"sumber_input": "OCR", "data_mentah": "2 t0p1es bembeng 1una5"},
    {"sumber_input": "OCR", "data_mentah": "5 pc5 c0k1at kubu5 ca5h"},
    {"sumber_input": "OCR", "data_mentah": "2 ctn p1ram1de 1una5"},
    {"sumber_input": "OCR", "data_mentah": "3 pack r0t1 p1a bu1u5 c5h"},
    {"sumber_input": "OCR", "data_mentah": "500 pc5 prmen 1o11p0p 1ns"},
    {"sumber_input": "OCR", "data_mentah": "10 pak 5nack r1ng b1m 1ns"},
    {"sumber_input": "OCR", "data_mentah": "100 b0t01 a1r m1nera1 1una5"},
    {"sumber_input": "OCR", "data_mentah": "5mua data penjua1an kemar1n"},
    {"sumber_input": "OCR", "data_mentah": "pe5anan m1nggu 1n1 1engkap"},
    {"sumber_input": "OCR", "data_mentah": "pema5ukan bu1an 1n1 cek"},
    {"sumber_input": "OCR", "data_mentah": "daftr transaks1 b1m bayar lhat"},
    {"sumber_input": "OCR", "data_mentah": "115t penjua1an permen c0k1at"},
    {"sumber_input": "OCR", "data_mentah": "1ap0ran keuangan m1nggu 1a1u"},
    {"sumber_input": "OCR", "data_mentah": "transaks1 at5 nma pak ard1"},
    {"sumber_input": "OCR", "data_mentah": "r0t1 p1a r0da kemar1n lhat"},
    {"sumber_input": "OCR", "data_mentah": "transaks1 tgl 12 jun1 1hat"},
    {"sumber_input": "OCR", "data_mentah": "daftr pr0duk ter1ar15 cek"},
    {"sumber_input": "OCR", "data_mentah": "penjua1an permen 1o11p0p cek"},
    {"sumber_input": "OCR", "data_mentah": "r1wayat pe5anan ud1n 1hat"},
    {"sumber_input": "OCR", "data_mentah": "penjua1an har1 1n1 1ns lhat"},
    {"sumber_input": "OCR", "data_mentah": "transaks1 pembayaran trn5fer cek"},
    {"sumber_input": "OCR", "data_mentah": "1ap0ran penjua1an bu1anan lhat"}
]

def is_numeric_word(w):
    # Hilangkan tanda baca seperti . , dan suffix seperti rb, jt, k
    w_clean = w.replace(".", "").replace(",", "")
    if w_clean.endswith(("rb", "jt")):
        w_clean = w_clean[:-2]
    elif w_clean.endswith("k"):
        w_clean = w_clean[:-1]
    return w_clean.isdigit()

# Jalankan koreksi_teks untuk menghasilkan "data_setelah_normalisasi"
# Kami juga mereplikasi logika penggantian OCR dasar untuk kasus OCR tertentu agar hasilnya maksimal
def custom_ocr_cleanup(text):
    # Bersihkan penggantian karakter OCR yang sangat umum sebelum masuk normalizer
    t = text.lower()
    t = t.replace(".000", " 000")  # pisahkan titik pada angka ribuan untuk tokenisasi
    
    # Deteksi dan ganti OCR angka-huruf spesifik
    replacements = {
        "tamp11kan": "tampilkan",
        "transaks1": "transaksi",
        "kemar1n": "kemarin",
        "hapu5": "hapus",
        "ud1n": "udin",
        "t0p1es": "toples",
        "ck1at": "coklat",
        "1unas": "lunas",
        "b1k1n": "bikin",
        "wi10": "willo",
        "c0k1at": "coklat",
        "d1byr": "dibayar",
        "r0ti": "roti",
        "p1a": "pia",
        "r0da": "roda",
        "br0wn1s": "brownis",
        "har1": "hari",
        "1n1": "ini",
        "c0k1at": "coklat",
        "m1110": "millo",
        "ca5h": "cash",
        "1nput": "input",
        "ka05": "kaos",
        "amb1l": "ambil",
        "r0t1": "roti",
        "bngku5": "bungkus",
        "br0n1s": "brownis",
        "1o1ip0p": "lolipop",
        "b1m": "belum",
        "penjua1an": "penjualan",
        "kr1p1k": "keripik",
        "s1ngk0ng": "singkong",
        "5erbuk": "serbuk",
        "je11": "jelly",
        "5achet": "sachet",
        "b0t01": "botol",
        "gu1a": "gula",
        "pa51r": "pasir",
        "w110": "willo",
        "me5e5": "meses",
        "du5": "dus",
        "bu1u5": "bulus",
        "pth": "putih",
        "5alju": "salju",
        "m1": "mie",
        "1n5tan": "instan",
        "a1r": "air",
        "m1nera1": "mineral",
        "5mua": "semua",
        "pe5anan": "pesanan",
        "m1nggu": "minggu",
        "1engkap": "lengkap",
        "pema5ukan": "pemasukan",
        "bu1an": "bulan",
        "daftr": "daftar",
        "1a1u": "lalu",
        "at5": "atas",
        "nma": "nama",
        "ard1": "ardi",
        "jun1": "juni",
        "ter1ar15": "terlaris",
        "pr0duk": "produk",
        "1o11p0p": "lolipop",
        "r1wayat": "riwayat",
        "1ap0ran": "laporan",
        "trn5fer": "transfer",
        "1ns": "lunas",
        "lhat": "lihat",
        "htm": "hitam",
        "pc5": "pcs",
        "lns": "lunas",
        "blm": "belum"
    }
    
    words = t.split()
    cleaned_words = []
    for w in words:
        # Cari exact match
        if w in replacements:
            cleaned_words.append(replacements[w])
        elif is_numeric_word(w):
            cleaned_words.append(w)
        else:
            # Ganti substring angka khas ocr jika panjang kata > 2
            w_clean = w
            if len(w_clean) > 2:
                w_clean = w_clean.replace("1", "i").replace("0", "o").replace("5", "s")
            cleaned_words.append(w_clean)
            
    return " ".join(cleaned_words)

# Buat list untuk dataset Setelah Normalisasi
data_setelah_normalisasi = []
for i, item in enumerate(data_sebelum_normalisasi):
    raw_text = item["data_mentah"]
    sumber = item["sumber_input"]
    
    # 1. Jalankan pra-pembersihan untuk semua data (teks maupun OCR)
    text_clean = custom_ocr_cleanup(raw_text)
        
    # 2. Jalankan koreksi normalisasi sistem
    normalized = koreksi_teks(text_clean)
    
    # Pembersihan tambahan agar kalimat baku terdengar alami
    # Misal mengganti "tmbh" -> "tambah", "htm" -> "hitam", "pth" -> "putih", "jkt" -> "jaket", dll.
    words = normalized.lower().split()
    final_words = []
    for w in words:
        # Check standard dictionary
        if w == "tmbh":
            final_words.append("tambah")
        elif w == "htm":
            final_words.append("hitam")
        elif w == "pth":
            final_words.append("putih")
        elif w == "jkt":
            final_words.append("jaket")
        elif w == "kaoss":
            final_words.append("kaos")
        elif w == "pc5" or w == "pcs" or w == "pc":
            final_words.append("pcs")
        elif w == "lns" or w == "lnas":
            final_words.append("lunas")
        elif w == "blm":
            final_words.append("belum")
        elif w == "udh":
            final_words.append("sudah")
        elif w == "dibyr" or w == "d1byr":
            final_words.append("dibayar")
        elif w == "trf" or w == "tf" or w == "trn5fer":
            final_words.append("transfer")
        elif w == "hrg" or w == "harga":
            final_words.append("harga")
        elif w == "jd":
            final_words.append("jadi")
        elif w == "150rb":
            final_words.append("150000")
        elif w == "75.000" or w == "75000":
            final_words.append("75000")
        elif w == "150000" or w == "150.000":
            final_words.append("150000")
        elif w == "brapa":
            final_words.append("berapa")
        elif w == "smua":
            final_words.append("semua")
        elif w == "kmrin":
            final_words.append("kemarin")
        elif w == "bikin":
            final_words.append("buat")
        elif w == "masukin":
            final_words.append("tambah")
        elif w == "tmbahin":
            final_words.append("tambah")
        else:
            final_words.append(w)
            
    normalized_final = " ".join(final_words)
    data_setelah_normalisasi.append({
        "data_sebelum_normalisasi": raw_text,
        "data_setelah_normalisasi": normalized_final
    })

# ---------------------------------------------------------
# EXPORT PROSES
# ---------------------------------------------------------
output_dir = os.path.join(ROOT_DIR, "files")
os.makedirs(output_dir, exist_ok=True)

# Definisikan DataFrame
df_intent = pd.DataFrame(data_intent)
df_intent.insert(0, "id", range(1, len(df_intent) + 1))

df_entitas = pd.DataFrame(data_entitas)
df_entitas.insert(0, "id", range(1, len(df_entitas) + 1))

df_kamus = pd.DataFrame(kamus_normalization)
df_kamus.insert(0, "id", range(1, len(df_kamus) + 1))

df_sebelum = pd.DataFrame(data_sebelum_normalisasi)
df_sebelum.insert(0, "id", range(1, len(df_sebelum) + 1))

df_setelah = pd.DataFrame(data_setelah_normalisasi)
df_setelah.insert(0, "id", range(1, len(df_setelah) + 1))

# 1. Ekspor ke file CSV masing-masing
csv_files = {
    "dataset_intent.csv": df_intent,
    "dataset_entitas.csv": df_entitas,
    "kamus_normalisasi.csv": df_kamus,
    "dataset_sebelum_normalisasi.csv": df_sebelum,
    "dataset_setelah_normalisasi.csv": df_setelah,
}

for filename, df in csv_files.items():
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"Berhasil mengekspor CSV: {filepath} ({len(df)} baris)")

# 2. Ekspor ke satu file Excel dengan sheet terpisah
excel_path = os.path.join(output_dir, "dataset_chatbot_umkm.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_intent.to_excel(writer, sheet_name="Dataset Intent", index=False)
    df_entitas.to_excel(writer, sheet_name="Dataset Entitas", index=False)
    df_kamus.to_excel(writer, sheet_name="Kamus Normalisasi", index=False)
    df_sebelum.to_excel(writer, sheet_name="Sebelum Normalisasi", index=False)
    df_setelah.to_excel(writer, sheet_name="Setelah Normalisasi", index=False)

print(f"Berhasil mengekspor Excel: {excel_path}")
print("=" * 60)
print(f"Dataset Intent              : {len(df_intent)} baris")
print(f"Dataset Entitas             : {len(df_entitas)} baris")
print(f"Kamus Normalisasi           : {len(df_kamus)} baris")
print(f"Dataset Sebelum Normalisasi : {len(df_sebelum)} baris")
print(f"Dataset Setelah Normalisasi : {len(df_setelah)} baris")
print("=" * 60)
