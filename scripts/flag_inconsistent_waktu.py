import inspect
import re
import json
from nlp import embedded_data
from nlp.extractor import ekstrak_entitas
from core.master_data import normalisasi_tanggal_gs

src = inspect.getsource(embedded_data)
lines = src.splitlines()
entries = []
for i, line in enumerate(lines):
    if '"waktu"' in line:
        start = max(0, i-6)
        end = min(len(lines), i+6)
        block = '\n'.join(lines[start:end])
        m_w = re.search(r'"waktu"\s*:\s*"([^"\\]+)"', block)
        m_t = re.search(r'"text"\s*:\s*"([^"\\]+)"', block)
        if m_w and m_t:
            text = m_t.group(1)
            waktu = m_w.group(1)
            pred = ekstrak_entitas(text)['entitas'].get('TANGGAL')
            norm = normalisasi_tanggal_gs(waktu)
            entries.append({
                'text': text,
                'waktu': waktu,
                'normalized_waktu': norm,
                'predicted': pred,
                'waktu_in_text': waktu.lower() in text.lower(),
            })

inconsistent = []
consistent = []
for e in entries:
    # Consider consistent if waktu literal appears in text, or predicted matches normalized waktu
    if e['waktu_in_text'] or (e['normalized_waktu'] and e['normalized_waktu'] == e['predicted']):
        consistent.append(e)
    else:
        inconsistent.append(e)

print(f'Total entries with waktu: {len(entries)}')
print(f'Consistent: {len(consistent)}; Inconsistent: {len(inconsistent)}')

with open('reports/embedded_waktu_inconsistent.json', 'w', encoding='utf8') as f:
    json.dump(inconsistent, f, ensure_ascii=False, indent=2)
with open('reports/embedded_waktu_consistent.json', 'w', encoding='utf8') as f:
    json.dump(consistent, f, ensure_ascii=False, indent=2)

print('Reports written to reports/embedded_waktu_inconsistent.json and reports/embedded_waktu_consistent.json')
