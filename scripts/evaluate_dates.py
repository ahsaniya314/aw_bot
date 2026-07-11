"""
Evaluate date extraction accuracy using `nlp.embedded_data.NLP_TRAINING_EXAMPLES`.
Skip examples where the dataset `waktu` label does not literally appear in the example `text`.
"""
import io
import sys
from pathlib import Path
from collections import defaultdict
import json
import re

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Set encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    # Prefer cleaned dataset if available
    from nlp.embedded_data_cleaned import CLEANED_NLP_TRAINING_EXAMPLES as NLP_TRAINING_EXAMPLES
    print('Using cleaned embedded dataset: nlp.embedded_data_cleaned.CLEANED_NLP_TRAINING_EXAMPLES')
except Exception:
    from nlp.embedded_data import NLP_TRAINING_EXAMPLES
from nlp.extractor import ekstrak_entitas
from core.master_data import normalisasi_tanggal_gs


def evaluate_dates():
    if not NLP_TRAINING_EXAMPLES:
        print("No training examples found.")
        return

    total = 0
    evaluated = 0
    correct = 0
    skipped = 0
    details = []

    for ex in NLP_TRAINING_EXAMPLES:
        text = ex.get("text", "")
        waktu = None
        entities = ex.get("entities") or {}
        # waktu may be nested in entities
        if isinstance(entities, dict):
            waktu = entities.get("waktu") or entities.get("waktu")
        if not text or not waktu:
            continue
        total += 1

        # Only evaluate when waktu literal appears in text (to avoid dataset hints)
        if not waktu or waktu.lower() not in text.lower():
            skipped += 1
            continue

        evaluated += 1
        expected = normalisasi_tanggal_gs(waktu)
        pred = ekstrak_entitas(text)["entitas"].get("TANGGAL")
        ok = bool(expected and pred == expected)
        if ok:
            correct += 1
        details.append({"text": text, "waktu": waktu, "expected": expected, "predicted": pred, "match": ok})

    accuracy = (correct / evaluated * 100) if evaluated else 0.0

    print(f"Total examples in dataset: {total}")
    print(f"Evaluated (waktu literal present): {evaluated}")
    print(f"Skipped (waktu not present): {skipped}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

    # Write detailed report
    out = Path("reports")
    out.mkdir(exist_ok=True)
    with open(out / "date_evaluation_details.json", "w", encoding="utf8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    print(f"Detailed results written to {out / 'date_evaluation_details.json'}")


if __name__ == "__main__":
    evaluate_dates()
