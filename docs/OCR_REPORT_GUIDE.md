# Panduan Laporan OCR dengan Visibility Penuh

## Overview

Script `scripts/ocr_report_generator.py` menyediakan visibility penuh ke semua tahapan proses OCR untuk keperluan laporan dan dokumentasi.

## Tahapan yang Ditampilkan

### 1. **Preprocessing**
- Resize gambar
- Padding
- Grayscale conversion
- Noise reduction
- Contrast enhancement
- Visualisasi setiap tahap

### 2. **Text Recognition**
- Bounding boxes untuk setiap teks
- Teks yang terdeteksi
- Confidence scores
- Visualisasi dengan warna

### 3. **Pattern Matching**
- Deteksi tanggal
- Deteksi harga
- Deteksi jumlah
- Pola khusus lainnya

### 4. Feature Extraction**
- Spatial distribution
- Text density
- Confidence distribution
- Layout analysis

### 5. **Post-processing**
- Text normalization
- Confidence-based filtering
- Noise removal
- Text merging

## Cara Penggunaan

### 1. Install Dependencies

```bash
pip install paddlepaddle paddleocr opencv-python numpy
```

### 2. Konfigurasi Environment

```bash
# Di .env file
OCR_ENGINE=paddleocr
OCR_CONFIDENCE_THRESHOLD=0.5
```

### 3. Jalankan Script

```bash
# Basic usage
python scripts/ocr_report_generator.py path/to/image.jpg

# Dengan direktori output custom
python scripts/ocr_report_generator.py path/to/image.jpg --output reports/my_report
```

### 4. Output yang Dihasilkan

```
ocr_reports/report_20260717_120000/
├── 01_preprocessing/
│   ├── 00_original.png
│   ├── 01_resized.png
│   ├── 02_padded.png
│   ├── 03_grayscale.png
│   ├── 04_denoised.png
│   └── 05_contrast_enhanced.png
├── 02_text_recognition/
│   └── ocr_visualization.png
├── 03_postprocessing/
│   └── final_text.txt
└── ocr_report.json
```

## Contoh Output JSON

```json
{
  "timestamp": "20260717_120000",
  "image_path": "receipt.jpg",
  "preprocessing": {
    "original_size": [1920, 1080],
    "steps": {
      "01_resized": {
        "method": "resize",
        "new_size": [1200, 675]
      },
      "02_padded": {
        "method": "padding",
        "padding_size": 50
      }
    }
  },
  "text_recognition": {
    "total_text_regions": 25,
    "average_confidence": 0.92,
    "texts": [
      {
        "text": "TOTAL: Rp 150.000",
        "confidence": 0.95,
        "bounding_box": [[100, 200], [300, 200], [300, 220], [100, 220]]
      }
    ]
  },
  "pattern_matching": {
    "harga": [
      {
        "text": "Rp 150.000",
        "match": ["150.000"],
        "confidence": 0.95
      }
    ]
  },
  "feature_extraction": {
    "spatial_distribution": {
      "x_range": [50, 1150],
      "y_range": [100, 600]
    },
    "text_density": {
      "total_text_regions": 25,
      "regions_per_line": 8
    }
  },
  "postprocessing": {
    "confidence_threshold": 0.5,
    "original_count": 25,
    "filtered_count": 24,
    "final_text": "TOTAL: Rp 150.000\nTANGGAL: 17/07/2026"
  }
}
```

## Integrasi dengan Sistem

### Menggunakan dalam Handler

```python
from scripts.ocr_report_generator import OCRReportGenerator

# Dalam photo_handler.py
def handle_photo_with_report(message, photo_path):
    generator = OCRReportGenerator()
    report_path = generator.generate_report(photo_path)
    
    # Kirim laporan ke user
    with open(report_path, 'r') as f:
        report_data = json.load(f)
    
    bot.reply_to(message, f"OCR Report Generated!\n\n"
                        f"Text Regions: {report_data['text_recognition']['total_text_regions']}\n"
                        f"Avg Confidence: {report_data['text_recognition']['average_confidence']:.2f}\n"
                        f"Final Text:\n{report_data['postprocessing']['final_text']}")
```

## Perbandingan: Mistral OCR vs PaddleOCR

| Fitur | Mistral OCR | PaddleOCR |
|-------|-------------|-----------|
| **Preprocessing Visibility** | ❌ Tidak ada | ✅ Full visibility |
| **Text Recognition Process** | ❌ Black box | ✅ Visible |
| **Bounding Boxes** | ❌ Tidak ada | ✅ Available |
| **Confidence Scores** | ❌ Tidak ada | ✅ Per character/word |
| **Pattern Matching** | ❌ Tidak ada | ✅ Customizable |
| **Feature Extraction** | ❌ Tidak ada | ✅ Available |
| **Post-processing** | ❌ Minimal | ✅ Full control |
| **Performance** | ⚡ Cepat (cloud) | 🐢 Lebih lambat (local) |
| **Cost** | 💰 API costs | 🆓 Gratis |

## Rekomendasi

### Gunakan PaddleOCR untuk:
- ✅ Laporan dan dokumentasi
- ✅ Debugging OCR
- ✅ Custom preprocessing
- ✅ Offline processing
- ✅ Cost optimization

### Gunakan Mistral OCR untuk:
- ✅ Production dengan high performance
- ✅ Gambar kompleks yang butuh AI canggih
- ✅ Tidak butuh visibility ke proses

## Troubleshooting

### Error: Failed to load PaddleOCR
```bash
# Install dependencies
pip install paddlepaddle paddleocr

# Untuk CPU
pip install paddlepaddle

# Untuk GPU (NVIDIA)
pip install paddlepaddle-gpu
```

### Error: Gambar tidak ditemukan
Pastikan path gambar benar dan file ada.

### Output kosong
Cek confidence threshold di `.env`:
```bash
OCR_CONFIDENCE_THRESHOLD=0.3  # Lower threshold untuk lebih banyak hasil
```

## Tips untuk Laporan

1. **Gunakan gambar berkualitas tinggi** untuk hasil OCR terbaik
2. **Adjust confidence threshold** sesuai kebutuhan
3. **Review visualisasi preprocessing** untuk optimasi
4. **Gunakan pattern matching custom** untuk domain spesifik
5. **Simpan laporan untuk dokumentasi** dan audit trail
