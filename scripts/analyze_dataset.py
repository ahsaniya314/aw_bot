"""
Script untuk melihat dataset sebelum dan sesudah normalisasi,
serta bagaimana data dibagi menjadi bagian-bagiannya (text, intent, entities).
"""

import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_normalization_dict():
    """Memuat kamus normalisasi dari file JSON."""
    norm_file = ROOT / "files" / "nlp_normalization_dict.json"
    with open(norm_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_nlp_dataset():
    """Memuat dataset NLP dari file CSV."""
    csv_file = ROOT / "files" / "nlp_dataset.csv"
    data = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse entities string into a dictionary
            entities_str = row.get("entities", "")
            entities = {}
            if entities_str:
                for part in entities_str.split("|"):
                    if "=" in part:
                        key, value = part.split("=", 1)
                        entities[key.strip()] = value.strip()
            
            data.append({
                "text_original": row["text"],
                "intent": row["intent"],
                "entities": entities
            })
    return data


def normalize_text(text, norm_dict):
    """Melakukan normalisasi teks menggunakan kamus normalisasi (hanya whole words)."""
    text_lower = text.lower().strip()
    tokens = text_lower.split()
    
    normalized_tokens = []
    for token in tokens:
        # 1. Cek typo
        if token in norm_dict.get("typo_corrections", {}):
            token = norm_dict["typo_corrections"][token]
        
        # 2. Cek singkatan
        elif token in norm_dict.get("abbreviations", {}):
            token = norm_dict["abbreviations"][token]
        
        # 3. Cek sinonim
        else:
            for group, synonyms in norm_dict.get("synonyms", {}).items():
                if isinstance(synonyms, list) and token in synonyms:
                    base_word = group.split("_")[-1]
                    token = base_word
                    break
        
        normalized_tokens.append(token)
    
    return " ".join(normalized_tokens).capitalize()


def main():
    print("=" * 80)
    print("ANALISIS DATASET NLP - SEBELUM & SESUDAH NORMALISASI")
    print("=" * 80)
    
    # Load data
    norm_dict = load_normalization_dict()
    dataset = load_nlp_dataset()
    
    print(f"\nTotal dataset: {len(dataset)} baris\n")
    
    # Tampilkan 5 contoh pertama
    print("=" * 80)
    print("CONTOH DATA SEBELUM & SESUDAH NORMALISASI (5 Baris Pertama)")
    print("=" * 80)
    
    for i, row in enumerate(dataset[:5], 1):
        text_original = row["text_original"]
        text_normalized = normalize_text(text_original, norm_dict)
        
        print(f"\n{'=' * 80}")
        print(f"DATA KE-{i}")
        print(f"{'=' * 80}")
        
        print(f"\n1. TEXT ORIGINAL (Sebelum Normalisasi):")
        print(f"   {text_original}")
        
        print(f"\n2. TEXT NORMALIZED (Sesudah Normalisasi):")
        print(f"   {text_normalized}")
        
        print(f"\n3. INTENT (Label Intent):")
        print(f"   {row['intent']}")
        
        print(f"\n4. ENTITIES (Informasi yang Diekstrak):")
        if row["entities"]:
            for key, value in row["entities"].items():
                print(f"   - {key}: {value}")
        else:
            print(f"   (tidak ada entity)")
    
    # Tampilkan struktur dataset
    print("\n" + "=" * 80)
    print("STRUKTUR DATASET")
    print("=" * 80)
    print("\nDataset dibagi menjadi 3 bagian utama:")
    print("1. 'text'          : Kalimat input pengguna (original)")
    print("2. 'intent'        : Label intent (kategori maksud pengguna)")
    print("3. 'entities'      : Informasi detail yang diekstrak dari teks")
    
    print("\n" + "=" * 80)
    print("DAFTAR SEMUA INTENT YANG ADA")
    print("=" * 80)
    intents = list(set([row["intent"] for row in dataset]))
    for j, intent in enumerate(sorted(intents), 1):
        print(f"{j}. {intent}")


if __name__ == "__main__":
    main()
