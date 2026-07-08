"""
Script evaluasi intent otomatis dengan data uji kustom.
Cara jalankan: python scripts/evaluate_intent_manual.py
Hasil akan disimpan ke folder "ekstrak tabel".
"""

import io
import sys
from pathlib import Path

# Set encoding untuk console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Tambahkan root proyek ke path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

from nlp.intent_matcher import match_intent_from_dataset


def evaluate_intent():
    print("=" * 70)
    print("EVALUASI IDENTIFIKASI INTENT (DATA UJI KUSTOM)")
    print("=" * 70)

    # Data uji dan ground truth
    test_data = [
        {"text": "Halo", "ground_truth": "Chit_Chat"},
        {"text": "Budi ambil bembeng 40 karton lunas", "ground_truth": "Catat_Penjualan_Lunas"},
        {"text": "Andi pesan willo 10 karton dicicil", "ground_truth": "Catat_Penjualan_Cicil"},
        {"text": "Tampilkan semua transaksi", "ground_truth": "Read_Transaksi_Spesifik"},
        {"text": "Cek transaksi hari ini.", "ground_truth": "Read_Transaksi_Spesifik"},
        {"text": "Total uang masuk hari ini", "ground_truth": "Read_Analitik_Penjualan"},
        {"text": "Total transaksi hari ini.", "ground_truth": "Read_Analitik_Penjualan"},
        {"text": "Siapa yang masih hutang?", "ground_truth": "Read_Analitik_Hutang"},
        {"text": "Tampilkan tagihan.", "ground_truth": "Read_Analitik_Hutang"},
        {"text": "budi bayar hutang 10 jt", "ground_truth": "Pelunasan_Hutang"},
        {"text": "Pak Andi bayar tagihan 10 juta.", "ground_truth": "Pelunasan_Hutang"},
        {"text": "Tambah barang", "ground_truth": "CRUD_Barang"},
        {"text": "Edit harga barang", "ground_truth": "CRUD_Barang"},
        {"text": "Tampilkan harga barang.", "ground_truth": "CRUD_Barang"},
        {"text": "Update transaksi Udin", "ground_truth": "Update_Delete_Transaksi"},
        {"text": "Edit transaksi Pak Ardi.", "ground_truth": "Update_Delete_Transaksi"},
        {"text": "Hapus transaksi Udin", "ground_truth": "Update_Delete_Transaksi"},
    ]

    # Jalankan prediksi
    results = []
    for item in test_data:
        text = item["text"]
        ground_truth = item["ground_truth"]
        predicted, score = match_intent_from_dataset(text)
        
        results.append({
            "text": text,
            "ground_truth": ground_truth,
            "predicted": predicted or "Unknown",
            "score": score,
            "correct": predicted == ground_truth
        })

    # Buat DataFrame
    df_results = pd.DataFrame(results)

    # Hitung metrik
    total = len(df_results)
    correct = df_results["correct"].sum()
    wrong = total - correct
    accuracy = (correct / total) * 100 if total > 0 else 0

    # Tampilkan hasil
    print(f"\nHasil Evaluasi:")
    print(f"   Total data uji     : {total}")
    print(f"   Prediksi benar     : {correct}")
    print(f"   Prediksi salah     : {wrong}")
    print(f"   Akurasi            : {accuracy:.2f}%")

    # Tampilkan semua hasil prediksi
    print("\n" + "=" * 70)
    print("DETAIL PREDIKSI:")
    print("=" * 70)
    for idx, row in df_results.iterrows():
        status = "✓ BENAR" if row["correct"] else "✗ SALAH"
        print(f"\n{idx+1}. {row['text']}")
        print(f"   Ground Truth: {row['ground_truth']}")
        print(f"   Prediksi    : {row['predicted']} (score: {row['score']})")
        print(f"   Status      : {status}")

    # Tampilkan classification report
    print("\n" + "=" * 70)
    print("CLASSIFICATION REPORT:")
    print("=" * 70)
    y_true = df_results["ground_truth"]
    y_pred = df_results["predicted"]
    print(classification_report(y_true, y_pred, zero_division=0))

    # Buat confusion matrix
    all_intents = sorted(list(set(y_true) | set(y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=all_intents)
    cm_df = pd.DataFrame(cm, index=all_intents, columns=all_intents)

    print("\n" + "=" * 70)
    print("CONFUSION MATRIX:")
    print("=" * 70)
    print(cm_df)

    # Simpan hasil ke folder "ekstrak tabel"
    output_dir = ROOT / "ekstrak tabel"
    output_dir.mkdir(exist_ok=True)

    cm_path = output_dir / "confusion_matrix_intent.csv"
    results_path = output_dir / "hasil_evaluasi_intent.csv"
    report_path = output_dir / "classification_report_intent.txt"

    cm_df.to_csv(cm_path)
    df_results.to_csv(results_path, index=False)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(classification_report(y_true, y_pred, zero_division=0))

    # Simpan gambar confusion matrix
    img_path = output_dir / "confusion_matrix_intent.png"
    plt.figure(figsize=(12, 8))
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.title('Confusion Matrix - Identifikasi Intent')
    plt.ylabel('Ground Truth')
    plt.xlabel('Prediksi')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    plt.close()

    print("\n" + "=" * 70)
    print("Hasil disimpan ke folder \"ekstrak tabel\":")
    print("=" * 70)
    print(f"  - {cm_path.name}")
    print(f"  - {results_path.name}")
    print(f"  - {report_path.name}")
    print(f"  - {img_path.name}")
    print("=" * 70)


if __name__ == "__main__":
    evaluate_intent()

