import os
import json
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "ocr_results"

    if not results_dir.exists():
        print(f"Error: Folder {results_dir} tidak ditemukan! Jalankan terlebih dahulu test_ocr_single.py untuk setiap gambar.")
        return

    # Baca semua file result
    all_results = []
    for i in range(1, 10):
        result_file = results_dir / f"result_{i}.json"
        if result_file.exists():
            with open(result_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_results.append(data)
                print(f"[OK] Memuat hasil untuk {data['filename']}")
        else:
            print(f"[WARN] Hasil untuk {i}.jpg belum ditemukan!")

    if not all_results:
        print("\nTidak ada hasil yang bisa diolah!")
        return

    # Hitung total dan rata-rata
    total_cer = sum(r["cer"] for r in all_results)
    total_wer = sum(r["wer"] for r in all_results)
    avg_cer = total_cer / len(all_results)
    avg_wer = total_wer / len(all_results)

    # Cari performa terbaik dan terburuk
    best_cer = min(all_results, key=lambda x: x["cer"])
    worst_cer = max(all_results, key=lambda x: x["cer"])
    best_wer = min(all_results, key=lambda x: x["wer"])
    worst_wer = max(all_results, key=lambda x: x["wer"])

    # Tampilkan ringkasan
    print("\n" + "=" * 100)
    print("RINGKASAN AKHIR PENGUJIAN OCR MISTRAL (9 GAMBAR)".center(100))
    print("=" * 100)
    print(f"\n1. JUMLAH GAMBAR YANG DIUJI: {len(all_results)} dari 9")
    print("\n2. DETAIL HASIL PER GAMBAR:")
    print("-" * 100)
    print(f"{'NAMA FILE':<15} {'CER':<12} {'WER':<12}")
    print("-" * 100)
    for r in all_results:
        print(f"{r['filename']:<15} {r['cer']:>8.2%}   {r['wer']:>8.2%}")
    print("-" * 100)
    print(f"\n3. RATA-RATA:")
    print(f"   - Rata-rata CER: {avg_cer:.2%}")
    print(f"   - Rata-rata WER: {avg_wer:.2%}")
    print("\n4. PERFORMA TERBAIK:")
    print(f"   - CER Terendah: {best_cer['filename']} ({best_cer['cer']:.2%})")
    print(f"   - WER Terendah: {best_wer['filename']} ({best_wer['wer']:.2%})")
    print("\n5. PERFORMA TERBURUK:")
    print(f"   - CER Tertinggi: {worst_cer['filename']} ({worst_cer['cer']:.2%})")
    print(f"   - WER Tertinggi: {worst_wer['filename']} ({worst_wer['wer']:.2%})")
    print("\n" + "=" * 100)
    print("KESIMPULAN".center(100))
    print("=" * 100)
    print(f"\nBerdasarkan pengujian {len(all_results)} gambar dari folder 'tes gambar':")
    if avg_cer < 0.30:
        print("[SANGAT BAIK] Performa OCR Mistral SANGAT BAIK dengan rata-rata CER di bawah 30%")
    elif avg_cer < 0.50:
        print("[CUKUP BAIK] Performa OCR Mistral CUKUP BAIK dengan rata-rata CER di bawah 50%")
    elif avg_cer < 0.70:
        print("[CUKUP] Performa OCR Mistral CUKUP dengan rata-rata CER di bawah 70%")
    else:
        print("[PERLU DIPERBAIKI] Performa OCR Mistral PERLU DIPERBAIKI dengan rata-rata CER di atas 70%")
    print("\n" + "=" * 100)


if __name__ == "__main__":
    main()
