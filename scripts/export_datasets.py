"""
Script untuk mengekspor dataset:
1. Sebelum normalisasi (text original + intent + entities)
2. Setelah normalisasi (text normalized + intent + entities)
3. Dataset intent (intent + patterns)
4. Dataset entities (entity type + examples)
"""
import csv
import json
from pathlib import Path

from analyze_dataset import load_nlp_dataset, load_normalization_dict, normalize_text

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "files"


def export_dataset_sebelum_normalisasi(dataset):
    """Ekspor dataset sebelum normalisasi ke CSV."""
    output_file = OUTPUT_DIR / "dataset_sebelum_normalisasi.csv"

    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["text_original", "intent", "entities"])

        for row in dataset:
            entities_str = (
                " | ".join([f"{k}: {v}" for k, v in row["entities"].items()])
                if row["entities"]
                else ""
            )
            writer.writerow([row["text_original"], row["intent"], entities_str])

    print(f"Berhasil ekspor: {output_file} (total {len(dataset)} baris)")


def export_dataset_setelah_normalisasi(dataset, norm_dict):
    """Ekspor dataset setelah normalisasi ke CSV."""
    output_file = OUTPUT_DIR / "dataset_setelah_normalisasi.csv"

    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["text_normalized", "intent", "entities"])

        for row in dataset:
            text_normalized = normalize_text(row["text_original"], norm_dict)
            entities_str = (
                " | ".join([f"{k}: {v}" for k, v in row["entities"].items()])
                if row["entities"]
                else ""
            )
            writer.writerow([text_normalized, row["intent"], entities_str])

    print(f"Berhasil ekspor: {output_file} (total {len(dataset)} baris)")


def export_dataset_intent(norm_dict):
    """Ekspor dataset intent ke JSON."""
    output_file = OUTPUT_DIR / "dataset_intent.json"

    intent_patterns = {}
    json_file = ROOT / "files" / "nlp_dataset.json"
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for intent_obj in data.get("intents", []):
            tag = intent_obj.get("tag", "")
            pats = intent_obj.get("patterns", [])
            if tag:
                intent_patterns[tag] = pats

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {"total_intent": len(intent_patterns), "intents": intent_patterns},
            f,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Berhasil ekspor: {output_file} (total {len(intent_patterns)} intent)")


def export_dataset_entities(dataset):
    """Ekspor dataset entities ke CSV (contoh setiap entity type)."""
    output_file = OUTPUT_DIR / "dataset_entities.csv"

    entity_examples = {}
    for row in dataset:
        for entity_type, entity_value in row["entities"].items():
            if entity_type not in entity_examples:
                entity_examples[entity_type] = []
            if entity_value not in entity_examples[entity_type]:
                entity_examples[entity_type].append(entity_value)

    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["entity_type", "total_examples", "examples"])

        for entity_type, examples in sorted(entity_examples.items()):
            examples_str = ", ".join(examples[:10])  # Show up to 10 examples
            writer.writerow([entity_type, len(examples), examples_str])

    print(f"Berhasil ekspor: {output_file} (total {len(entity_examples)} entity type)")


def main():
    print("=" * 80)
    print("MENGEKSPOR SEMUA DATASET")
    print("=" * 80)

    norm_dict = load_normalization_dict()
    dataset = load_nlp_dataset()

    print(f"\nTotal dataset: {len(dataset)} baris")
    print(f"Output directory: {OUTPUT_DIR}\n")

    export_dataset_sebelum_normalisasi(dataset)
    export_dataset_setelah_normalisasi(dataset, norm_dict)
    export_dataset_intent(norm_dict)
    export_dataset_entities(dataset)

    print("\n" + "=" * 80)
    print("SELESAI! Semua dataset berhasil diekspor ke folder 'files/'!")
    print("=" * 80)


if __name__ == "__main__":
    main()
