import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test various problematic paths
test_paths = [
    ".contoh.jpeg",      # User's case 1 (missing slash)
    ". contoh.jpeg",     # Dot + space + filename
    ". /contoh.jpeg",    # Dot + space + slash + filename → should become ./contoh.jpeg
    ". \\contoh.jpeg",   # Dot + space + backslash + filename
    ".. /contoh.jpeg",   # Two dots + space + slash + filename
    "./contoh.jpeg",     # Normal path
    " . /contoh.jpeg ",  # Leading/trailing spaces
    ". ./contoh.jpeg",   # User's original case - this probably means ./contoh.jpeg, not ../contoh.jpeg? Because the file is in current directory!
]

for test_path in test_paths:
    print(f"\nOriginal path: '{test_path}'")
    
    # Test from ocr_service
    from services.ocr_service import OCRService
    ocr = OCRService()
    sanitized_ocr = ocr._sanitize_image_path(test_path)
    print(f"OCR service sanitized: '{sanitized_ocr}'")

    # Test from ocr_preprocessor
    from services.ocr_preprocessor import OCRPreprocessor
    prep = OCRPreprocessor()
    sanitized_prep = prep._sanitize_image_path(test_path)
    print(f"Preprocessor sanitized: '{sanitized_prep}'")


