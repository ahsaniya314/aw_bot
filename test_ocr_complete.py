import os
import sys
# Pastikan direktori root ada di path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import OCRService
from services.ocr_service import OCRService

# Inisialisasi OCR Service
ocr = OCRService()
ocr.load_model()  # Memuat model OCR (penting!)
print("OCR Service initialized successfully!")

# Path gambar yang ingin diproses (pastikan file ini ada di direktori Anda!)
image_path = "./contoh.jpeg"  # Atau "contoh.jpeg" tanpa "./"

# Jalankan OCR
text = ocr.extract_text(image_path)

# Tampilkan hasil
print("="*60)
print("Extracted Text from:", image_path)
print("="*60)
print(text)
print("="*60)
