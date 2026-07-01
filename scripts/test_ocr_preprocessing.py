import os
import sys

# Tambahkan direktori root ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import logging

from services.ocr_preprocessor import OCRPreprocessor
from services.ocr_service import OCRService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    print("=" * 80)
    print("DEMO LENGKAP: PREPROCESSING + OCR DENGAN BUKTI")
    print("=" * 80)
    
    # Cari gambar contoh di direktori files
    files_dir = os.path.join(os.path.dirname(__file__), "..", "files")
    example_image = None
    
    # Cari gambar dengan ekstensi umum
    for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        for f in os.listdir(files_dir):
            if f.lower().endswith(ext):
                example_image = os.path.join(files_dir, f)
                break
        if example_image:
            break
    
    if not example_image:
        print("\n[!] Tidak menemukan gambar contoh di direktori files")
        print("[!] Silakan letakkan gambar dengan ekstensi .jpg/.jpeg/.png di direktori files")
        print("[!] Atau ubah path di bawah ini secara manual")
        return
    
    print(f"\n[*] Menggunakan gambar contoh: {example_image}")
    
    # Jalankan OCRService dengan bukti lengkap
    print("\n" + "=" * 80)
    print("MENJALANKAN PREPROCESSING + OCR...")
    print("=" * 80)
    
    ocr = OCRService()
    text, proof_data = ocr.extract_text_with_preprocessing_proof(example_image, "demo_lengkap")
    
    print("\n" + "=" * 80)
    print("RINGKASAN BUKTI YANG DIHASILKAN")
    print("=" * 80)
    
    for step, data in proof_data.items():
        print(f"\n  • {step.upper()}:")
        if "image_path" in data:
            print(f"    - Gambar: {os.path.basename(data['image_path'])}")
        if "metadata" in data:
            print(f"    - Metadata: {data['metadata']}")
    
    print("\n" + "=" * 80)
    print("HASIL EKSTRAKSI TEKS OCR:")
    print("=" * 80)
    print(text)
    print("=" * 80)
    
    print("\nSELESAI!")
    print(f"[✓] Semua bukti disimpan di: {ocr.preprocessor.output_dir}")
    print("\nDaftar file bukti:")
    for filename in sorted(os.listdir(ocr.preprocessor.output_dir)):
        if filename.startswith("demo_lengkap_"):
            print(f"  - {filename}")
    print("=" * 80)


if __name__ == "__main__":
    main()
