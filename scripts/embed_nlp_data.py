"""
Regenerate nlp/embedded_data.py from files/ (opsional, hanya untuk development).
Jalankan: python scripts/embed_nlp_data.py
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ROOT / "files"
OUT = ROOT / "nlp" / "embedded_data.py"


def _py_repr(obj, indent=0):
    sp = " " * indent
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for k, v in obj.items():
            lines.append(f"{sp}    {json.dumps(k, ensure_ascii=False)}: {_py_repr(v, indent + 4)},")
        lines.append(f"{sp}}}")
        return "\n".join(lines)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        if all(isinstance(x, str) for x in obj) and len(obj) > 8:
            # compact long string lists
            parts = [json.dumps(x, ensure_ascii=False) for x in obj]
            inner = ", ".join(parts)
            if len(inner) > 120:
                lines = ["["]
                for x in obj:
                    lines.append(f"{sp}    {json.dumps(x, ensure_ascii=False)},")
                lines.append(f"{sp}]")
                return "\n".join(lines)
        return "[" + ", ".join(_py_repr(x, 0) for x in obj) + "]"
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, bool):
        return "True" if obj else "False"
    if obj is None:
        return "None"
    return repr(obj)


def load_normalization():
    path = FILES / "nlp_normalization_dict.json"
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_intent_patterns():
    path = FILES / "nlp_dataset.json"
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    patterns = {}
    for intent_obj in data.get("intents", []):
        tag = intent_obj.get("tag", "")
        pats = intent_obj.get("patterns", [])
        if tag:
            patterns[tag] = pats
    return patterns


def load_csv_dataset():
    path = FILES / "nlp_dataset.csv"
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            entities_str = row.get("entities", "") or ""
            entities_dict = {}
            if entities_str:
                for pair in entities_str.split("|"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        entities_dict[k.strip()] = v.strip()
            rows.append(
                {
                    "text": row.get("text", "") or "",
                    "intent": row.get("intent", "") or "",
                    "entities": entities_dict,
                }
            )
    return rows


def main():
    norm = load_normalization()
    patterns = load_intent_patterns()
    dataset = load_csv_dataset()

    units = norm.get("entity_patterns", {}).get("satuan", {}).get("valid_units", [])

    body = f'''"""
Data NLP tertanam — dihasilkan dari files/ via scripts/embed_nlp_data.py
Jangan edit manual kecuali patch kecil; regenerate dengan skrip di atas.
"""

NORMALIZATION_DICT = {_py_repr(norm)}

INTENT_PATTERNS = {_py_repr(patterns)}

NLP_TRAINING_EXAMPLES = {_py_repr(dataset)}

VALID_UNITS = frozenset({_py_repr(list(units))})
'''

    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT} ({len(patterns)} intents, {len(dataset)} examples)")


if __name__ == "__main__":
    main()
