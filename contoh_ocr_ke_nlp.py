#!/usr/bin/env python3
"""
Contoh Sederhana: Alur OCR → NLP → Perhitungan Total
Tanpa merubah konfigurasi NLP apapun!
"""
import os
import sys

# Pastikan folder utama ada di sys.path
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("=" * 80)
print("CONTOH ALUR: OCR → NLP → PERHITUNGAN HARGA")
print("=" * 80)
print()

# 1. Inisialisasi OCR Service
from services.ocr_service import OCRService
print("1. Inisialisasi OCR Service...")
ocr_service = OCRService()
if not ocr_service.load_model():
    print(f"   ❌ Gagal: {ocr_service._disabled_reason}")
    sys.exit(1)
print("   ✅ OCR Service siap!")
print()

# 2. Load Master Data
print("2. Memuat Master Data dari Database...")
from core.master_data import get_all_barang, get_all_metode, muat_metode_keywords

semua_barang = get_all_barang()
daftar_nama_barang = [b["nama"] for b in semua_barang]
semua_metode = get_all_metode()
mapping_metode = muat_metode_keywords()

print(f"   ✅ Loaded: {len(semua_barang)} barang, {len(semua_metode)} metode pembayaran")
if semua_barang:
    print(f"      Contoh barang: {', '.join([b['nama'] for b in semua_barang[:3]])}")
print()

# 3. Tentukan gambar yang akan dibaca
gambar_path = os.path.join(os.path.dirname(__file__), "budis.jpg")
print(f"3. Memproses gambar: {gambar_path}")
if not os.path.exists(gambar_path):
    print(f"   ⚠️ File tidak ditemukan! Menggunakan contoh teks OCR...")
    teks_ocr = """Nota Penjualan
Tanggal: 29-06-2025
Kepada: Pak Budi
Barang: 2 dus Willo
Harga: Rp 100.000
Total: Rp 200.000
Metode: Tunai Lunas"""
else:
    teks_ocr = ocr_service.extract_text(gambar_path)
    if teks_ocr.startswith("Error OCR:"):
        print(f"   ❌ {teks_ocr}")
        print(f"   ⚠️ Menggunakan contoh teks OCR...")
        teks_ocr = """Nota Penjualan
Tanggal: 29-06-2025
Kepada: Pak Budi
Barang: 2 dus Willo
Harga: Rp 100.000
Total: Rp 200.000
Metode: Tunai Lunas"""
    else:
        print("   ✅ OCR berhasil!")

print()
print("=" * 80)
print("HASIL OCR:")
print("=" * 80)
print(teks_ocr)
print("=" * 80)
print()

# 4. Proses dengan NLP
print("4. Memproses teks dengan NLP Pipeline...")
from nlp.processor import proses_nlp

nlp_result = proses_nlp(
    teks_user=teks_ocr,
    db_metode=semua_metode,
    daftar_barang=daftar_nama_barang,
    mapping_metode=mapping_metode
)

if not nlp_result["valid_results"]:
    print("   ❌ Tidak ada transaksi yang bisa diekstrak!")
    if nlp_result["errors"]:
        print("   Errors:")
        for err in nlp_result["errors"]:
            print(f"   - {err}")
    sys.exit(1)

print(f"   ✅ Berhasil mengekstrak {len(nlp_result['valid_results'])} transaksi!")
print()

# 5. Hitung total harga
from core.master_data import cari_harga_default, parse_rupiah, format_rupiah
import re

print("=" * 80)
print("HASIL AKHIR:")
print("=" * 80)

for idx, transaksi in enumerate(nlp_result["valid_results"], 1):
    print(f"\nTransaksi #{idx}:")
    print(f"  Tanggal: {transaksi.get('TANGGAL', 'Tidak terdeteksi')}")
    print(f"  Nama Pelanggan: {transaksi.get('NAMA', 'Tidak terdeteksi')}")
    print(f"  Barang: {transaksi.get('BARANG', 'Tidak terdeteksi')}")
    print(f"  Jumlah: {transaksi.get('JUMLAH', 'Tidak terdeteksi')}")
    print(f"  Satuan: {transaksi.get('SATUAN', 'Tidak terdeteksi')}")
    print(f"  Status: {transaksi.get('STATUS', 'Tidak terdeteksi')}")
    print(f"  Metode: {transaksi.get('METODE_PEMBAYARAN', 'Tidak terdeteksi')}")
    
    # Hitung harga jika ada
    nama_barang = transaksi.get("BARANG")
    satuan = transaksi.get("SATUAN")
    jumlah_str = transaksi.get("JUMLAH")
    
    if nama_barang and semua_barang:
        harga_list = cari_harga_default(
            None,
            nama_barang,
            satuan_cari=satuan,
            semua_barang=semua_barang
        )
        
        if harga_list:
            harga_satuan = harga_list[0]["harga"]
            angka_jumlah_match = re.search(r"\d+", str(jumlah_str))
            jumlah = int(angka_jumlah_match.group()) if angka_jumlah_match else 1
            total = harga_satuan * jumlah
            
            print(f"  Harga Satuan: {format_rupiah(harga_satuan)}")
            print(f"  Total: {format_rupiah(total)}")
        else:
            print(f"  ⚠️ Harga barang '{nama_barang}' tidak ditemukan di master data!")

print()
print("=" * 80)
print("SELESAI!")
print("=" * 80)
