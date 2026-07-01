import re

from nlp.processor import _apply_multi_overrides, split_multi_entries

user_input = "Pak Andi pesan permen 10 dus, meses 5 bungkus, willo 3 dus, belum lunas semua."
print("split_multi_entries:")
segments = split_multi_entries(user_input)
print(segments)
print("\n---\n")

# Debug the second segment's match_satuan!
test_seg = "meses 5 bungkus"
print(f"Testing match_satuan on: {test_seg}")
teks_qty = test_seg.lower()
match_satuan = re.search(r"(\d+)\s*(dus|pcs|toples|pack|buah|botol|karton|ctn|etn|crn|krtn|katon|katron|krton|kerton|kartom|kg|butir|bal|kantong|lusin|koli|roll|meter|lembar|box|dusan|balan|pak|ikat|ikat\s*kecil|ikat\s*besar|dus\s*kecil|dus\s*besar|dus\s*sedang|renceng|pouch|kaleng|slop|sak|liter|biji|tablet|kapsul)\b", teks_qty)
print(f"match_satuan: {match_satuan}")
if match_satuan:
    print(f"group 1: {match_satuan.group(1)}, group 2: {match_satuan.group(2)}")
else:
    print("NO MATCH!")

print("\n---\n")


# Now let's simulate what happens in proses_nlp:
from nlp.extractor import ekstrak_entitas

results = []
for seg in segments:
    res = ekstrak_entitas(seg, teks_asli=seg)
    results.append({"intent": "Catat_Penjualan_Lunas", "entitas": res["entitas"], "original_text": seg})

print("After ekstrak_entitas:")
for r in results:
    print(r)
print("\n---\n")

print("After _apply_multi_overrides:")
final = _apply_multi_overrides(results)
for f in final:
    print(f)
