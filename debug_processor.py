from nlp.processor import proses_nlp, _apply_multi_overrides, split_multi_entries
from nlp.normalizer import koreksi_teks
from nlp.extractor import ekstrak_entitas
import pprint

input_test = "pak anDi Pesan prmen1 10 dus, mses 5 bks, will0 3 dus belum lunwas semua"

print("=" * 80)
print("INPUT:")
print(input_test)
print("\n" + "=" * 80)
print("SPLIT TO ENTRIES:")
entries = split_multi_entries(input_test)
pprint.pprint(entries)
print("\n" + "=" * 80)
print("EXTRACT ENTITAS PER ENTRY:")
results = []
for entry in entries:
    teks_koreksi = koreksi_teks(entry)
    print(f"\nEntry: {entry}")
    print(f"Koreksi: {teks_koreksi}")
    hasil = ekstrak_entitas(teks_koreksi, teks_asli=entry)
    pprint.pprint(hasil)
    results.append({
        "intent": hasil.get("intent"),
        "entitas": hasil["entitas"],
        "original_text": entry
    })

print("\n" + "=" * 80)
print("BEFORE _apply_multi_overrides:")
pprint.pprint(results)

print("\n" + "=" * 80)
print("AFTER _apply_multi_overrides:")
final = _apply_multi_overrides(results)
pprint.pprint(final)
