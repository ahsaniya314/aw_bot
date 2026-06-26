
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from services.ocr_service import OCRService

ocr = OCRService()
ocr.load_model()

text = ocr.extract_text("dashboard-web\\public\\logo.png")

print("=" * 60)
print("Extracted Text:")
print("=" * 60)
print(text)
