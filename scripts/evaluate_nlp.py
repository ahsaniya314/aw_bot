"""
Script untuk mengevaluasi performa model NLP (fuzzy matching) Anda!
Cara jalankan: python scripts/evaluate_nlp.py
"""

import io
import sys
from collections import defaultdict
from pathlib import Path

# Set encoding untuk console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Tambahkan root ke path agar bisa import module proyek
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nlp.embedded_data import NLP_TRAINING_EXAMPLES
from nlp.intent_matcher import DATASET_TO_SYSTEM_INTENT, match_intent_from_dataset


def evaluate_nlp():
    print("=" * 70)
    print("EVALUASI MODEL NLP (FUZZY MATCHING)")
    print("=" * 70)

    if not NLP_TRAINING_EXAMPLES:
        print("Dataset NLP_TRAINING_EXAMPLES kosong!")
        return

    total = 0
    correct = 0
    wrong = []
    confusion = defaultdict(lambda: defaultdict(int))  # actual -> predicted

    print(f"\nTotal contoh data: {len(NLP_TRAINING_EXAMPLES)}")
    print("-" * 70)

    for example in NLP_TRAINING_EXAMPLES:
        text = example.get("text", "")
        actual_tag = example.get("intent", "")

        if not text or not actual_tag:
            continue

        # Map dataset tag ke system intent (sesuai DATASET_TO_SYSTEM_INTENT)
        actual_intent = DATASET_TO_SYSTEM_INTENT.get(actual_tag, actual_tag)

        total += 1
        predicted_intent, score = match_intent_from_dataset(text)

        # Catat untuk confusion matrix
        confusion[actual_intent][predicted_intent or "Unknown"] += 1

        if predicted_intent == actual_intent:
            correct += 1
        else:
            wrong.append(
                {
                    "text": text,
                    "actual_tag": actual_tag,
                    "actual_intent": actual_intent,
                    "predicted": predicted_intent,
                    "score": score,
                }
            )

    # Hitung metrik
    accuracy = (correct / total) * 100 if total > 0 else 0

    # Tampilkan hasil
    print(f"\nHasil Evaluasi:")
    print(f"   Total data uji     : {total}")
    print(f"   Prediksi benar     : {correct}")
    print(f"   Prediksi salah     : {len(wrong)}")
    print(f"   Akurasi            : {accuracy:.2f}%")

    # Tampilkan contoh salah prediksi
    if wrong:
        print("\n" + "=" * 70)
        print("CONTOH PREDIKSI SALAH:")
        print("=" * 70)
        for i, w in enumerate(wrong[:10], 1):  # Tampilkan 10 contoh pertama
            print(f"\n{i}. Teks: {w['text']}")
            print(f"   Actual Intent: {w['actual_intent']}")
            print(f"   Predicted Intent: {w['predicted']}")
            print(f"   Score: {w['score']}")

    # Tampilkan confusion matrix ringkas
    print("\n" + "=" * 70)
    print("CONFUSION MATRIX RINGKAS:")
    print("=" * 70)
    print(f"{'Actual Intent':<30} | {'Prediksi Salah Sebagai':<30} | {'Jumlah':<10}")
    print("-" * 70)
    for actual_intent, preds in confusion.items():
        for pred_intent, count in preds.items():
            if actual_intent != pred_intent:
                print(f"{actual_intent:<30} | {pred_intent:<30} | {count:<10}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    evaluate_nlp()
