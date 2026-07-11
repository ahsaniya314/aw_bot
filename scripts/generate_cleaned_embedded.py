import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nlp.embedded_data import NLP_TRAINING_EXAMPLES

# Load inconsistent list
inc_path = Path('reports/embedded_waktu_inconsistent.json')
inc_texts = set()
if inc_path.exists():
    with open(inc_path, 'r', encoding='utf8') as f:
        inc = json.load(f)
        for e in inc:
            inc_texts.add(e.get('text'))

cleaned = [e for e in NLP_TRAINING_EXAMPLES if e.get('text') not in inc_texts]

out_json = Path('reports/embedded_data_cleaned.json')
with open(out_json, 'w', encoding='utf8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

# Produce a python module
out_py = Path('nlp/embedded_data_cleaned.py')
with open(out_py, 'w', encoding='utf8') as f:
    f.write('"""Auto-generated cleaned embedded data (removed flagged inconsistent waktu entries)."""\n')
    f.write('CLEANED_NLP_TRAINING_EXAMPLES = ')
    json.dump(cleaned, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f'Cleaned examples: {len(cleaned)} (removed {len(NLP_TRAINING_EXAMPLES)-len(cleaned)} entries)')
print(f'Wrote {out_json} and {out_py}')
