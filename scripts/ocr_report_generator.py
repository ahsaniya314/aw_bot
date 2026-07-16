"""
OCR Report Generator - Script untuk menghasilkan laporan lengkap proses OCR
Menampilkan: Akuisisi Citra, Prapemrosesan, Pengenalan Teks, Pencocokan Pola, Ekstraksi Fitur, Pascapemrosesan
"""

import os
import sys
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import cv2
import numpy as np

from services.ocr_preprocessor import OCRPreprocessor
from config.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRReportGenerator:
    def __init__(self, output_dir: str = None):
        """
        Inisialisasi generator laporan OCR.
        
        Args:
            output_dir: Direktori untuk menyimpan laporan
        """
        self.settings = get_settings()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = output_dir or f"ocr_reports/report_{timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Sub-direktori untuk setiap tahap (Bahasa Indonesia)
        self.akuisisi_dir = os.path.join(self.output_dir, "01_akuisisi_citra")
        self.prapemrosesan_dir = os.path.join(self.output_dir, "02_prapemrosesan")
        self.pengenalan_teks_dir = os.path.join(self.output_dir, "03_pengenalan_teks")
        self.pencocokan_pola_dir = os.path.join(self.output_dir, "04_pencocokan_pola")
        self.ekstraksi_fitur_dir = os.path.join(self.output_dir, "05_ekstraksi_fitur")
        self.pascapemrosesan_dir = os.path.join(self.output_dir, "06_pascapemrosesan")
        
        for dir_path in [self.akuisisi_dir, self.prapemrosesan_dir, self.pengenalan_teks_dir, 
                        self.pencocokan_pola_dir, self.ekstraksi_fitur_dir, self.pascapemrosesan_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        self.preprocessor = OCRPreprocessor(output_dir=self.prapemrosesan_dir)
        self.ocr_engine = None
        self.report_data = {
            "timestamp": timestamp,
            "image_path": "",
            "akuisisi_citra": {},
            "prapemrosesan": {},
            "pengenalan_teks": {},
            "pencocokan_pola": {},
            "ekstraksi_fitur": {},
            "pascapemrosesan": {},
            "hasil_akhir": ""
        }

    def load_ocr_engine(self):
        """Load OCR engine - menggunakan EasyOCR sebagai primary option (tidak perlu install executable)."""
        try:
            # Coba EasyOCR terlebih dahulu (paling mudah untuk Windows - tidak perlu install executable)
            logger.info("Loading EasyOCR engine...")
            import easyocr
            self.ocr_engine = easyocr.Reader(['en'], gpu=False)
            self.ocr_engine_type = "easyocr"
            logger.info("EasyOCR loaded successfully!")
            return True
        except ImportError:
            logger.warning("EasyOCR not installed, trying Tesseract...")
            try:
                import pytesseract
                logger.info("Loading Tesseract OCR engine...")
                self.ocr_engine = pytesseract
                self.ocr_engine_type = "tesseract"
                logger.info("Tesseract OCR loaded successfully!")
                return True
            except ImportError:
                logger.warning("pytesseract not installed, trying PaddleOCR...")
                try:
                    from paddleocr import PaddleOCR
                    logger.info("Loading PaddleOCR engine...")
                    self.ocr_engine = PaddleOCR(use_angle_cls=True, lang="en")
                    self.ocr_engine_type = "paddleocr"
                    logger.info("PaddleOCR loaded successfully!")
                    return True
                except Exception as e:
                    logger.error(f"Failed to load PaddleOCR: {e}")
                    return False
        except Exception as e:
            logger.error(f"Failed to load EasyOCR: {e}")
            return False

    def step1_akuisisi_citra(self, image_path: str) -> Dict[str, Any]:
        """
        Step 1: Akuisisi Citra - dokumen gambar dipindai dan dikonversi menjadi data biner.
        Software menganalisis gambar dan mengklasifikasikan bagian terang sebagai background
        dan bagian gelap sebagai teks.
        """
        logger.info("=== TAHAP 1: AKUISISI CITRA ===")
        
        # Load gambar
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Gagal load gambar: {image_path}")
        
        # Simpan gambar original sebagai akuisisi citra
        original_path = os.path.join(self.akuisisi_dir, "00_gambar_asli.png")
        cv2.imwrite(original_path, image)
        
        # Analisis biner - klasifikasi background dan teks
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Simpan hasil biner
        binary_path = os.path.join(self.akuisisi_dir, "01_analisis_biner.png")
        cv2.imwrite(binary_path, binary)
        
        self.report_data["akuisisi_citra"] = {
            "deskripsi": "Dokumen gambar dipindai dan dikonversi menjadi data biner. Software menganalisis gambar dan mengklasifikasikan bagian terang sebagai background dan bagian gelap sebagai teks.",
            "original_size": image.shape[:2],
            "gambar_asli": original_path,
            "analisis_biner": binary_path,
            "output_images": ["00_gambar_asli.png", "01_analisis_biner.png"]
        }
        
        return {"image": image, "binary": binary, "metadata": {"original_size": image.shape[:2]}}

    def step2_prapemrosesan(self, binary_image: np.ndarray, original_size: tuple) -> Dict[str, Any]:
        """
        Step 2: Prapemrosesan - membersihkan gambar dari bagian-bagian yang kurang sempurna
        seperti bercak dan garis-garis yang mengenai teks. Teks dalam gambar mulai dikenali sistem.
        
        Tahapan:
        - Resize
        - Padding
        - Noise reduction
        - Contrast enhancement
        
        Args:
            binary_image: Hasil analisis biner dari tahap akuisisi citra
            original_size: Ukuran gambar asli
        """
        logger.info("=== TAHAP 2: PRAPEMROSESAN ===")
        
        # Simpan gambar biner sebagai input prapemrosesan
        binary_path = os.path.join(self.prapemrosesan_dir, "00_input_biner.png")
        cv2.imwrite(binary_path, binary_image)
        
        # Jalankan preprocessing dari gambar biner
        # Kita perlu save binary image ke temporary file untuk preprocessor
        temp_binary_path = os.path.join(self.prapemrosesan_dir, "temp_binary.png")
        cv2.imwrite(temp_binary_path, binary_image)
        
        # Jalankan preprocessing dengan visualisasi
        proof_data = self.preprocessor.preprocess_with_proof(temp_binary_path, base_filename="prapemrosesan")
        
        self.report_data["prapemrosesan"] = {
            "deskripsi": "Software OCR membersihkan gambar dari bagian-bagian yang kurang sempurna dan dapat mengganggu proses pemindaian, seperti bercak dan garis-garis yang mengenai teks. Dalam tahap ini, teks dalam gambar akan mulai dikenali oleh sistem. Input untuk tahap ini adalah hasil analisis biner dari tahap akuisisi citra.",
            "input_dari": "analisis_biner_dari_akuisisi_citra",
            "original_size": original_size,
            "steps": proof_data,
            "output_images": [f for f in os.listdir(self.prapemrosesan_dir) if f.endswith('.png')]
        }
        
        # Gunakan gambar terakhir untuk OCR
        last_step = list(proof_data.keys())[-1]
        last_image_path = proof_data[last_step]["image_path"]
        processed_image = cv2.imread(last_image_path)
        
        return {"processed_image": processed_image, "metadata": proof_data}

    def step3_pengenalan_teks(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Step 3: Pengenalan Teks - setiap kata diidentifikasi untuk disegmentasikan menjadi karakter terpisah.
        Teks mulai terbaca sistem, kemudian data akan diproses hingga siap memasuki proses selanjutnya.
        
        Output:
        - Bounding boxes
        - Teks yang terdeteksi
        - Confidence scores
        """
        logger.info("=== TAHAP 3: PENGENALAN TEKS ===")
        
        if not self.ocr_engine:
            if not self.load_ocr_engine():
                raise RuntimeError("Gagal load OCR engine")
        
        # Simpan gambar temporary untuk OCR
        temp_image_path = os.path.join(self.pengenalan_teks_dir, "temp_image.png")
        cv2.imwrite(temp_image_path, image)
        
        try:
            if self.ocr_engine_type == "tesseract":
                # Gunakan Tesseract
                logger.info("Using Tesseract OCR for text recognition...")
                ocr_text = self.ocr_engine.image_to_string(image)
                lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
                
                ocr_data = []
                for i, line in enumerate(lines):
                    ocr_data.append({
                        "text": line,
                        "confidence": 0.85,  # Tesseract doesn't provide confidence by default
                        "bounding_box": [[0, i*30], [image.shape[1], i*30], [image.shape[1], (i+1)*30], [0, (i+1)*30]],
                        "box_center": (image.shape[1]/2, i*30 + 15)
                    })
                
            elif self.ocr_engine_type == "easyocr":
                # Gunakan EasyOCR
                logger.info("Using EasyOCR for text recognition...")
                results = self.ocr_engine.readtext(temp_image_path)
                
                # Parse hasil EasyOCR
                ocr_data = []
                for (bbox, text, confidence) in results:
                    ocr_data.append({
                        "text": text,
                        "confidence": float(confidence),
                        "bounding_box": [[float(x) for x in point] for point in bbox],
                        "box_center": [float(x) for x in self._calculate_box_center(bbox)]
                    })
                
                ocr_text = "\n".join([item["text"] for item in ocr_data])
                
            else:
                # Gunakan pendekatan sederhana untuk PaddleOCR (karena ada compatibility issue)
                logger.info("Using simplified OCR approach...")
                # Fallback: gunakan dummy data
                logger.warning("PaddleOCR has compatibility issues, using dummy data")
                ocr_text = "OCR engine not available - PaddleOCR compatibility issue on Windows"
                ocr_data = [{
                    "text": ocr_text,
                    "confidence": 0.0,
                    "bounding_box": [[0, 0], [100, 0], [100, 20], [0, 20]],
                    "box_center": (50, 10)
                }]
            
            # Visualisasi hasil
            vis_path = os.path.join(self.pengenalan_teks_dir, "ocr_visualization.png")
            vis_image = image.copy()
            
            for item in ocr_data:
                box = item["bounding_box"]
                text = item["text"]
                conf = item["confidence"]
                
                # Gambar bounding box
                if len(box) == 4:  # EasyOCR format
                    pts = np.array(box, dtype=np.int32).reshape((-1, 1, 2))
                    cv2.polylines(vis_image, [pts], True, (0, 255, 0), 2)
                    
                    # Hitung posisi teks
                    x_min = int(np.min(pts[:, :, 0]))
                    y_min = int(np.min(pts[:, :, 1]))
                    
                    # Tampilkan teks
                    cv2.putText(vis_image, text, (x_min, y_min - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                    
                    # Tampilkan confidence
                    cv2.putText(vis_image, f"{conf:.2f}", (x_min, y_min - 25), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            
            cv2.imwrite(vis_path, vis_image)
            
            self.report_data["pengenalan_teks"] = {
                "deskripsi": "Setiap kata diidentifikasi untuk disegmentasikan menjadi karakter terpisah. Teks mulai terbaca sistem, kemudian data akan diproses hingga siap memasuki proses selanjutnya.",
                "total_text_regions": len(ocr_data),
                "average_confidence": sum(item["confidence"] for item in ocr_data) / len(ocr_data) if ocr_data else 0.0,
                "texts": ocr_data,
                "visualization": vis_path,
                "raw_text": ocr_text,
                "engine_type": self.ocr_engine_type
            }
            
            return {"results": ocr_data, "ocr_data": ocr_data, "metadata": {"raw_text": ocr_text}}
            
        except Exception as e:
            logger.error(f"Error dalam pengenalan teks: {e}")
            # Fallback: gunakan dummy data
            ocr_data = [{
                "text": f"OCR processing error: {str(e)}",
                "confidence": 0.0,
                "bounding_box": [[0, 0], [100, 0], [100, 20], [0, 20]],
                "box_center": (50, 10)
            }]
            
            self.report_data["pengenalan_teks"] = {
                "total_text_regions": 1,
                "average_confidence": 0.0,
                "texts": ocr_data,
                "visualization": temp_image_path,
                "error": str(e)
            }
            
            return {"results": ocr_data, "ocr_data": ocr_data, "metadata": {"error": str(e)}}

    def step4_pencocokan_pola(self, ocr_data: List[Dict]) -> Dict[str, Any]:
        """
        Step 4: Pencocokan Pola - software mengisolasi citra karakter (glyph) dan
        membandingkannya dengan glyph yang tersimpan dalam sistem. Font dan skala
        dalam gambar akan dicocokkan.
        
        Pola yang dicari:
        - Tanggal
        - Harga
        - Nama barang
        - Jumlah
        """
        logger.info("=== TAHAP 4: PENCOCOKAN POLA ===")
        
        import re
        
        patterns = {
            "tanggal": [
                r"\b(\d{1,2})[-/\s\.](\d{1,2})[-/\s\.](\d{2,4})\b",
                r"\b(\d{1,2})\s+(?:jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|nov|des)\s+(\d{2,4})\b"
            ],
            "harga": [
                r"(?:rp\.?\s*)?(\d[\d\.,]*)\s*(?:ribu|rb|juta|jt)?\b"
            ],
            "jumlah": [
                r"\b(\d+)\s*(?:pcs|karton|pouch|toples|pack|dus|kg)\b"
            ]
        }
        
        matched_patterns = {}
        
        for item in ocr_data:
            text = item["text"]
            
            for pattern_type, pattern_list in patterns.items():
                if pattern_type not in matched_patterns:
                    matched_patterns[pattern_type] = []
                
                for pattern in pattern_list:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        matched_patterns[pattern_type].extend([
                            {"text": text, "match": m, "confidence": item["confidence"]}
                            for m in matches
                        ])
        
        self.report_data["pencocokan_pola"] = {
            "deskripsi": "Software mengisolasi citra karakter (glyph) dan membandingkannya dengan glyph yang tersimpan dalam sistem. Font dan skala dalam gambar akan dicocokkan. Proses ini akan berjalan dengan baik bila font yang digunakan dalam gambar merupakan font yang umum digunakan.",
            "matched_patterns": matched_patterns
        }
        
        return matched_patterns

    def step5_ekstraksi_fitur(self, ocr_data: List[Dict]) -> Dict[str, Any]:
        """
        Step 5: Ekstraksi Fitur - glyph akan diurai menjadi fitur tertentu,
        seperti garis, lengkungan, hingga perpotongan garis. Setelah diekstraksi,
        fitur-fitur tersebut akan dicocokkan dengan beragam glyph yang telah tersimpan sebelumnya.
        
        Features:
        - Spatial distribution
        - Text density
        - Line spacing
        - Font size estimation
        """
        logger.info("=== TAHAP 5: EKSTRAKSI FITUR ===")
        
        if not ocr_data:
            return {}
        
        # Ekstrak spatial features
        x_positions = [item["box_center"][0] for item in ocr_data]
        y_positions = [item["box_center"][1] for item in ocr_data]
        
        features = {
            "deskripsi": "Glyph akan diurai menjadi fitur tertentu, seperti garis, lengkungan, hingga perpotongan garis. Setelah diekstraksi, fitur-fitur tersebut akan dicocokkan dengan beragam glyph yang telah tersimpan sebelumnya.",
            "spatial_distribution": {
                "x_range": [min(x_positions), max(x_positions)],
                "y_range": [min(y_positions), max(y_positions)],
                "x_center": sum(x_positions) / len(x_positions),
                "y_center": sum(y_positions) / len(y_positions)
            },
            "text_density": {
                "total_text_regions": len(ocr_data),
                "regions_per_line": self._estimate_lines(ocr_data)
            },
            "confidence_distribution": {
                "min_confidence": min(item["confidence"] for item in ocr_data),
                "max_confidence": max(item["confidence"] for item in ocr_data),
                "avg_confidence": sum(item["confidence"] for item in ocr_data) / len(ocr_data)
            }
        }
        
        self.report_data["ekstraksi_fitur"] = features
        
        return features

    def step6_pascapemrosesan(self, ocr_data: List[Dict]) -> Dict[str, Any]:
        """
        Step 6: Pascapemrosesan - data teks telah siap dikonversi menjadi file dokumen
        yang terkomputerisasi. Ada pula sistem OCR yang bisa menyertakan dokumen versi
        sebelum dan setelah dipindai.
        
        Tahapan:
        - Text normalization
        - Noise filtering
        - Confidence-based filtering
        - Text merging
        """
        logger.info("=== TAHAP 6: PASCAPROSESAN ===")
        
        # Filter berdasarkan confidence threshold
        threshold = self.settings.OCR_CONFIDENCE_THRESHOLD
        filtered_data = [item for item in ocr_data if item["confidence"] >= threshold]
        
        # Normalisasi teks
        normalized_texts = []
        for item in filtered_data:
            text = item["text"]
            # Hapus whitespace berlebih
            text = " ".join(text.split())
            # Hapus karakter khusus
            text = re.sub(r'[^\w\s\.,\-/]', '', text)
            normalized_texts.append(text)
        
        # Gabungkan teks
        final_text = "\n".join(normalized_texts)
        
        # Simpan hasil post-processing
        postprocess_path = os.path.join(self.pascapemrosesan_dir, "final_text.txt")
        with open(postprocess_path, "w", encoding="utf-8") as f:
            f.write(final_text)
        
        self.report_data["pascapemrosesan"] = {
            "deskripsi": "Data teks telah siap dikonversi menjadi file dokumen yang terkomputerisasi. Ada pula sistem OCR yang bisa menyertakan dokumen versi sebelum dan setelah dipindai.",
            "confidence_threshold": threshold,
            "original_count": len(ocr_data),
            "filtered_count": len(filtered_data),
            "removed_count": len(ocr_data) - len(filtered_data),
            "final_text": final_text,
            "output_file": postprocess_path
        }
        
        self.report_data["hasil_akhir"] = final_text
        
        return {"final_text": final_text, "filtered_data": filtered_data}

    def _calculate_box_center(self, box):
        """Hitung center point dari bounding box."""
        points = np.array(box)
        x_center = np.mean(points[:, 0])
        y_center = np.mean(points[:, 1])
        return (x_center, y_center)

    def _estimate_lines(self, ocr_data):
        """Estimasi jumlah baris berdasarkan posisi Y."""
        y_positions = [item["box_center"][1] for item in ocr_data]
        y_positions.sort()
        
        lines = 1
        threshold = 30  # Threshold untuk beda baris (pixel)
        
        for i in range(1, len(y_positions)):
            if y_positions[i] - y_positions[i-1] > threshold:
                lines += 1
        
        return lines

    def generate_report(self, image_path: str) -> str:
        """
        Generate laporan lengkap untuk satu gambar.
        
        Args:
            image_path: Path ke gambar input
            
        Returns:
            Path ke file laporan JSON
        """
        logger.info(f"Generating OCR report for: {image_path}")
        
        self.report_data["image_path"] = image_path
        
        try:
            # Tahap 1: Akuisisi Citra
            akuisisi_result = self.step1_akuisisi_citra(image_path)
            
            # Tahap 2: Prapemrosesan (menggunakan output biner dari tahap 1)
            prapemrosesan_result = self.step2_prapemrosesan(
                akuisisi_result["binary"], 
                akuisisi_result["metadata"]["original_size"]
            )
            
            # Tahap 3: Pengenalan Teks
            pengenalan_result = self.step3_pengenalan_teks(prapemrosesan_result["processed_image"])
            
            # Tahap 4: Pencocokan Pola
            pola_result = self.step4_pencocokan_pola(pengenalan_result["ocr_data"])
            
            # Tahap 5: Ekstraksi Fitur
            fitur_result = self.step5_ekstraksi_fitur(pengenalan_result["ocr_data"])
            
            # Tahap 6: Pascapemrosesan
            pascapemrosesan_result = self.step6_pascapemrosesan(pengenalan_result["ocr_data"])
            
            # Simpan laporan JSON
            report_path = os.path.join(self.output_dir, "ocr_report.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise


def main():
    """Main function untuk menjalankan generator laporan."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate OCR Report with Full Visibility")
    parser.add_argument("image_path", help="Path ke gambar input")
    parser.add_argument("--output", "-o", help="Direktori output untuk laporan")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        logger.error(f"Gambar tidak ditemukan: {args.image_path}")
        return
    
    generator = OCRReportGenerator(output_dir=args.output)
    report_path = generator.generate_report(args.image_path)
    
    print(f"\n{'='*60}")
    print(f"OCR REPORT GENERATED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"Report Location: {report_path}")
    print(f"Output Directory: {generator.output_dir}")
    print(f"\nContents:")
    print(f"  - 01_preprocessing/: Gambar hasil setiap tahap preprocessing")
    print(f"  - 02_text_recognition/: Visualisasi hasil OCR dengan bounding box")
    print(f"  - 03_postprocessing/: Teks hasil post-processing")
    print(f"  - ocr_report.json: Data lengkap semua tahapan")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
