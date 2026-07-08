from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
response = supabase.table('master_barang').select('*').execute()

items_250 = [b for b in response.data if b['harga'] == 250]
items_250k = [b for b in response.data if b['harga'] == 250000]

print('Barang dengan harga EXACTLY 250:')
if items_250:
    for b in items_250:
        print(f"  - {b['nama_barang']:25s} | {b['satuan']}")
else:
    print('  (tidak ada)')

print('\nBarang dengan harga 250.000:')
if items_250k:
    for b in items_250k:
        print(f"  - {b['nama_barang']:25s} | {b['satuan']}")
else:
    print('  (tidak ada)')
