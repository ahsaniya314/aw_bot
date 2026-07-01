import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ocr_service import OCRService

ocr = OCRService()
ocr.load_model()

# User's exact path
image_path = ".contoh.jpeg"

text = ocr.extract_text(image_path)

print("="*60)
print("Extracted Text from:", image_path)
print("="*60)
print(text)
print("="*60)
