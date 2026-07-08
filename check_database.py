"""
Script untuk mengecek data master barang Siper Queen di database
"""
from core.bot_context import ctx
from core.master_data import get_all_barang

def check_database():
    print("="*70)
    print("CEK DATABASE: Master Barang untuk 'Siper Queen'")
    print("="*70)
    
    if not ctx.IS_DB_CONNECTED:
        print("\n❌ Database tidak terkoneksi!")
        print("   Pastikan file .env sudah diisi dengan benar")
        return
    
    print("\n✅ Database terkoneksi")
    print("\nMencari semua data 'Siper Queen' di database...")
    print("-"*70)
    
    try:
        # Ambil semua barang
        all_barang = get_all_barang(ctx.db_barang)
        
        # Filter hanya Siper Queen
        siper_items = [b for b in all_barang if 'siper' in b['nama'].lower() or 'siiper' in b['nama'].lower()]
        
        if not siper_items:
            print("❌ MASALAH: Tidak ada data 'Siper Queen' di database!")
            print("\nSILAHKAN TAMBAHKAN DATA BERIKUT:")
            print("  Nama Barang: Siper Queen")
            print("  Satuan: karton")
            print("  Harga: (sesuai harga asli, misalnya Rp 5.000)")
        else:
            print(f"\nDitemukan {len(siper_items)} data Siper Queen:")
            print("-"*70)
            for i, item in enumerate(siper_items, 1):
                print(f"\n[Data #{i}]")
                print(f"  ID         : {item.get('row_idx')}")
                print(f"  Nama       : {item.get('nama')}")
                print(f"  Harga      : Rp {item.get('harga'):,}".replace(',', '.'))
                print(f"  Satuan     : {item.get('satuan')}")
                
                # Analisis
                if item.get('satuan') == 'karton':
                    if item.get('harga') <= 0:
                        print(f"  ⚠️  MASALAH: Harga 0 atau negatif!")
                    elif item.get('harga') == 250:
                        print(f"  ⚠️  KEMUNGKINAN SALAH: Harga terlalu kecil untuk karton")
                        print(f"      (Apakah ini seharusnya untuk satuan 'toples'?)")
                    else:
                        print(f"  ✅ Data terlihat OK")
                elif item.get('satuan') == 'toples' and item.get('harga') == 250:
                    print(f"  ✅ Data untuk toples terlihat OK")
        
        print("\n" + "="*70)
        print("REKOMENDASI:")
        print("="*70)
        
        has_karton = any(item.get('satuan') == 'karton' and item.get('harga') > 0 for item in siper_items)
        
        if not has_karton:
            print("\n⚠️  TIDAK ADA DATA VALID untuk 'Siper Queen' satuan 'karton'!")
            print("\nLANGKAH PERBAIKAN:")
            print("1. Buka bot Telegram Anda")
            print("2. Ketik: /menu")
            print("3. Pilih: ⚙️ Pengaturan")
            print("4. Pilih: 📦 Master Barang")
            print("5. Pilih: ➕ Tambah Data")
            print("6. Masukkan:")
            print("   - Nama: Siper Queen")
            print("   - Harga: (misalnya 5000)")
            print("   - Satuan: karton")
            print("\nATAU via command line:")
            print("   Ketik: tambah barang Siper Queen 5000 karton")
        else:
            print("\n✅ Data sudah ada dan valid!")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
