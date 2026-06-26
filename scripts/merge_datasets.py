import os
import json
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from nlp.embedded_data import NORMALIZATION_DICT, INTENT_PATTERNS, NLP_TRAINING_EXAMPLES, VALID_UNITS

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
    if isinstance(obj, set) or isinstance(obj, frozenset):
        return _py_repr(list(obj))
    return repr(obj)

def parse_rasa_yaml(path):
    data = []
    text = path.read_text(encoding="utf-8")
    blocks = text.split("- intent:")
    for block in blocks[1:]:
        lines = block.splitlines()
        intent = lines[0].strip()
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("- "):
                example = line[2:].strip()
                if example:
                    data.append({"text": example, "intent": intent})
    return data

def main():
    new_examples = []
    
    csv_path = FILES / "dataset_flat.csv"
    if csv_path.exists():
        with open(csv_path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("text") and row.get("intent"):
                    new_examples.append({"text": row["text"], "intent": row["intent"]})
                    
    flat_json_path = FILES / "dataset_flat.json"
    if flat_json_path.exists():
        with open(flat_json_path, encoding="utf-8") as f:
            jdata = json.load(f)
            for item in jdata:
                if item.get("text") and item.get("intent"):
                    new_examples.append({"text": item["text"], "intent": item["intent"]})
                    
    chatbot_json_path = FILES / "dataset_chatbot_nlp.json"
    if chatbot_json_path.exists():
        with open(chatbot_json_path, encoding="utf-8") as f:
            jdata = json.load(f)
            for intent_obj in jdata.get("intents", []):
                intent = intent_obj.get("intent")
                for ex in intent_obj.get("examples", []):
                    new_examples.append({"text": ex, "intent": intent})
                    
    yaml_path = FILES / "dataset_rasa_nlu.yml"
    if yaml_path.exists():
        new_examples.extend(parse_rasa_yaml(yaml_path))

    existing_texts = {ex["text"].lower().strip() for ex in NLP_TRAINING_EXAMPLES}
    
    added_count = 0
    for ex in new_examples:
        txt = ex["text"].strip()
        txt_low = txt.lower()
        if txt_low not in existing_texts:
            existing_texts.add(txt_low)
            intent = ex["intent"]
            
            NLP_TRAINING_EXAMPLES.append({
                "text": txt,
                "intent": intent,
                "entities": {}
            })
            
            if intent not in INTENT_PATTERNS:
                INTENT_PATTERNS[intent] = []
            INTENT_PATTERNS[intent].append(txt)
            added_count += 1
            
    print(f"Added {added_count} new examples.")
    
    body = f'''"""\nData NLP tertanam — dihasilkan dari files/ via scripts/embed_nlp_data.py / merge_datasets.py\nJangan edit manual kecuali patch kecil; regenerate dengan skrip di atas.\n"""\n\nNORMALIZATION_DICT = {_py_repr(NORMALIZATION_DICT)}\n\nINTENT_PATTERNS = {_py_repr(INTENT_PATTERNS)}\n\nNLP_TRAINING_EXAMPLES = {_py_repr(NLP_TRAINING_EXAMPLES)}\n\nVALID_UNITS = frozenset({_py_repr(list(VALID_UNITS))})\n'''
    
    OUT.write_text(body, encoding="utf-8")
    print(f"Successfully wrote {OUT}")

if __name__ == "__main__":
    main()
