
import sys
from pathlib import Path
from datetime import datetime
import re

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all required modules
from nlp.processor import proses_nlp
from core.master_data import cari_harga_default, format_rupiah, parse_rupiah
from services.ui_transaksi import susun_balasan_multi_resume
from services.ui_common import _missing_keys_multi
from core.master_data import get_all_barang

print("=== TESTING FULL PIPELINE ===")

print("\n=== MASTER DATA IS ===")
for item in get_all_barang():
    print(f"  {item}")

test_input = "Pak Andi pesan permen 10 dus, meses 5 bungkus, willo 3 dus, belum lunas semua"
print(f"\n1. Testing NLP dengan input: {test_input}")
results = proses_nlp(test_input)
print(f"2. proses_nlp returned {len(results)} items:")
for i, item in enumerate(results):
    print(f"\n   Item {i+1}:")
    print(f"   - original_text: {item['original_text']}")
    print(f"   - entitas: {item['entitas']}")


print("\n3. Simulating context inheritance and price lookup:")
if results and len(results) >0:
    # Step 1: Inherit context from first item (like handlers/text_handler.py does)
    context_lama = {}
    context_pesan = {}
    ent0 = results[0].get("entitas", {}) or {}
    for k in ["TANGGAL", "NAMA", "METODE_PEMBAYARAN"]:
        if ent0.get(k):
            context_pesan[k] = ent0.get(k)
    # Process each result like handlers/text_handler.py does:
    for item in results:
        gabungan = context_lama.copy()
        for k, v in context_pesan.items():
            if v and not gabungan.get(k):
                gabungan[k] = v
        for k, v in item["entitas"].items():
            if v:
                gabungan[k] = v

        aksi = gabungan.get("AKSI")
        if not gabungan.get("TANGGAL") and not gabungan.get("SEMUA") and not (aksi == "Read Data" and gabungan.get("NAMA")):
            gabungan["TANGGAL"] = datetime.now().strftime("%d-%m-%Y")
        # Try extract satuan like handlers/text_handler.py:
        if not gabungan.get("SATUAN") and gabungan.get("JUMLAH"):
            m_sat = re.search(
                r"\d+\s*(dus|pcs|toples|pack|bungkus|karton|bks|buah|botol|kg|bal|kantong|lusin|koli|roll|meter|lembar|box|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul|gelas|cup|can|sachet|pak)\b",
                str(gabungan.get("JUMLAH")),
                re.IGNORECASE,
            )
            if m_sat:
                gabungan["SATUAN"] = m_sat.group(1).lower()

        item["entitas"] = gabungan
        print(f"\n   After context inheritance (item {results.index(item)+1}): {item['entitas']}")

        print("   Running cari_harga_default:")
        matches = cari_harga_default(None, item["entitas"]["BARANG"], satuan_cari=item["entitas"].get("SATUAN"))
        print(f"   cari_harga_default returned {matches}")
        if matches:
            print(f"   Using first match: {matches[0]}")
            item["entitas"]["HARGA"] = format_rupiah(matches[0]["harga"])
            if item["entitas"].get("JUMLAH"):
                j_match = re.search(r"\d+", item["entitas"]["JUMLAH"])
                if j_match:
                    j_num = int(j_match.group())
                    item["entitas"]["TOTAL"] = format_rupiah(j_num * matches[0]["harga"])
                    print(f"   Calculated TOTAL = {item['entitas']['TOTAL']}")

    print("\n4. Running _missing_keys_multi for each item:")
    for i, item in enumerate(results):
        missing = _missing_keys_multi(item["entitas"])
        item["missing_fields"] = missing
        print(f"   Item {i+1} missing keys: {missing}")

    print("\n5. Summary of all entitas:")
    for i, item in enumerate(results):
        print(f"\n   Item {i+1}: {item['entitas']}")

else:
    print("proses_nlp returned no results")

print("\n=== TESTING DONE ===")
