import logging
import os
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger("bot_logger")


class OCRPreprocessor:
    def __init__(self, output_dir: Optional[str] = None):
        """
        Inisialisasi preprocessor OCR dengan direktori output untuk bukti preprocessing.

        Args:
            output_dir: Direktori untuk menyimpan gambar hasil setiap langkah preprocessing
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), "ocr_preprocessing_proof")
        os.makedirs(self.output_dir, exist_ok=True)

    def resize_image(
        self, image: np.ndarray, target_size: Tuple[int, int] = None, scale_factor: float = None
    ) -> Tuple[np.ndarray, Dict]:
        """
        Langkah 1: Resize gambar.

        Args:
            image: Gambar input (numpy array BGR)
            target_size: Ukuran target (width, height) - opsional
            scale_factor: Faktor skala (misal 0.5 untuk setengah ukuran) - opsional

        Returns:
            Tuple (gambar_resize, metadata)
        """
        h, w = image.shape[:2]
        metadata = {"original_size": (w, h), "method": "resize"}

        if target_size:
            resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
            metadata["target_size"] = target_size
        elif scale_factor:
            new_w = int(w * scale_factor)
            new_h = int(h * scale_factor)
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            metadata["scale_factor"] = scale_factor
            metadata["new_size"] = (new_w, new_h)
        else:
            # Default: Resize agar lebar tidak lebih dari 2000px (menjaga rasio aspek)
            max_width = 2000
            if w > max_width:
                scale = max_width / w
                new_w = max_width
                new_h = int(h * scale)
                resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
                metadata["scale_factor"] = scale
                metadata["new_size"] = (new_w, new_h)
            else:
                resized = image.copy()
                metadata["new_size"] = (w, h)

        return resized, metadata

    def pad_image(
        self,
        image: np.ndarray,
        padding_size: int = 50,
        padding_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> Tuple[np.ndarray, Dict]:
        """
        Langkah 2: Menambahkan padding pada gambar.

        Args:
            image: Gambar input
            padding_size: Ukuran padding di setiap sisi (pixel)
            padding_color: Warna padding (BGR)

        Returns:
            Tuple (gambar_padded, metadata)
        """
        h, w = image.shape[:2]
        padded = cv2.copyMakeBorder(
            image,
            top=padding_size,
            bottom=padding_size,
            left=padding_size,
            right=padding_size,
            borderType=cv2.BORDER_CONSTANT,
            value=padding_color,
        )
        metadata = {
            "original_size": (w, h),
            "padding_size": padding_size,
            "padding_color": padding_color,
            "new_size": (padded.shape[1], padded.shape[0]),
            "method": "padding",
        }
        return padded, metadata

    def convert_and_normalize_color(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Langkah 3: Konversi warna dan normalisasi.

        Args:
            image: Gambar input (BGR)

        Returns:
            Tuple (gambar_normalized, metadata)
        """
        metadata = {"method": "color_conversion_normalization"}

        # Konversi ke grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            metadata["color_space_conversion"] = "BGR -> GRAY"
        else:
            gray = image.copy()
            metadata["color_space_conversion"] = "Already GRAY"

        # Normalisasi kontras (CLAHE - Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        normalized = clahe.apply(gray)

        # Opsional: Thresholding atau denoising
        # normalized = cv2.GaussianBlur(normalized, (3, 3), 0)

        metadata["enhancement"] = "CLAHE"

        return normalized, metadata

    def deskew_image(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Langkah 4: De-skewing ( Koreksi kemiringan gambar ).

        Args:
            image: Gambar input (grayscale atau BGR)

        Returns:
            Tuple (gambar_deskewed, metadata)
        """
        metadata = {"method": "deskewing"}

        # Pastikan gambar grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Thresholding untuk mendapatkan binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Temukan contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            metadata["angle"] = 0.0
            metadata["status"] = "No contours found, no rotation applied"
            return image.copy(), metadata

        # Ambil contour terbesar
        largest_contour = max(contours, key=cv2.contourArea)

        # Hitung bounding rectangle dengan rotasi
        rect = cv2.minAreaRect(largest_contour)
        angle = rect[-1]

        # Koreksi sudut
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        metadata["angle"] = angle

        # Rotasi gambar jika sudut > 0.5 derajat
        if abs(angle) > 0.5:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            deskewed = cv2.warpAffine(
                image if len(image.shape) == 3 else gray,
                M,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )
            metadata["status"] = f"Rotated by {angle:.2f} degrees"
        else:
            deskewed = image.copy()
            metadata["status"] = "Angle < 0.5 degrees, no rotation applied"

        return deskewed, metadata

    def _sanitize_image_path(self, image_path):
        """Sanitize image path to fix issues like '. ./contoh.jpeg' or '.contoh.jpeg'."""
        import os
        import re

        sanitized = image_path.strip()

        # Step 1: Handle cases with spaces between dots and slashes
        while True:
            old_sanitized = sanitized
            sanitized = re.sub(r"\.\s+\.", r"..", sanitized)
            sanitized = re.sub(r"\.\s+([/\\])", r".\1", sanitized)
            sanitized = re.sub(r"([/\\])\s+\.", r"\1.", sanitized)
            sanitized = re.sub(r"\.\s+([^\./\\])", r"./\1", sanitized)
            if sanitized == old_sanitized:
                break

        # Step 2: Fix missing slash: ".contoh" → "./contoh"
        sanitized = re.sub(r"^\.([^\./\\])", r"./\1", sanitized)

        # Step 3: Remove any extra spaces that are left
        sanitized = sanitized.replace(" ", "")

        # Step 4: Normalize the path
        sanitized = os.path.normpath(sanitized)

        return sanitized

    def _find_image_path(self, image_path):
        """Find the actual image path, trying multiple fallbacks."""
        import os

        sanitized_path = self._sanitize_image_path(image_path)

        # Try 1: The path as-is
        if os.path.exists(sanitized_path):
            return sanitized_path

        # Try 2: Parent directory (for notebooks/)
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fallback1 = os.path.join(parent_dir, sanitized_path)
        if os.path.exists(fallback1):
            return fallback1

        # Try 3: Just filename in parent directory
        filename = os.path.basename(sanitized_path)
        fallback2 = os.path.join(parent_dir, filename)
        if os.path.exists(fallback2):
            return fallback2

        # If none found, return sanitized path
        return sanitized_path

    def preprocess_with_proof(self, image_path: str, base_filename: str = "preprocessing") -> Dict:
        """
        Jalankan semua langkah preprocessing dan simpan bukti berupa gambar.

        Args:
            image_path: Path ke gambar input
            base_filename: Nama dasar untuk file output

        Returns:
            Dictionary berisi metadata setiap langkah dan path ke gambar bukti
        """
        # Find the actual image path
        image_path = self._find_image_path(image_path)

        proof_data = {}
        steps = [
            ("01_original", None),
            ("02_resized", self.resize_image),
            ("03_padded", self.pad_image),
            ("04_color_normalized", self.convert_and_normalize_color),
            ("05_deskewed", self.deskew_image),
        ]

        # Baca gambar asli
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Gambar tidak dapat dibaca: {image_path}")

        current_image = image.copy()

        for step_name, step_func in steps:
            step_output_path = os.path.join(self.output_dir, f"{base_filename}_{step_name}.png")

            if step_func is None:
                # Simpan gambar asli
                cv2.imwrite(step_output_path, current_image)
                proof_data[step_name] = {
                    "image_path": step_output_path,
                    "metadata": {"note": "Original image"},
                }
                continue

            # Jalankan langkah preprocessing
            processed, metadata = step_func(current_image)

            # Simpan gambar hasil
            if len(processed.shape) == 2:  # Grayscale
                cv2.imwrite(step_output_path, processed)
            else:  # BGR
                cv2.imwrite(step_output_path, processed)

            proof_data[step_name] = {"image_path": step_output_path, "metadata": metadata}

            # Update current_image untuk langkah selanjutnya (kecuali untuk color normalized)
            if step_name != "04_color_normalized":
                current_image = processed

        logger.info(
            f"[OCR Preprocessor] Preprocessing selesai. Bukti disimpan di: {self.output_dir}"
        )

        return proof_data

    def visualize_ocr_results(
        self,
        image: np.ndarray,
        ocr_results: List,
        output_path: str,
        draw_text: bool = True,
        draw_confidence: bool = True,
    ) -> Dict:
        """
        Memvisualisasikan hasil OCR dengan bounding box, teks, dan skor akurasi.

        Args:
            image: Gambar input (BGR atau grayscale)
            ocr_results: Hasil OCR mentah dari PaddleOCR
            output_path: Path untuk menyimpan gambar visualisasi
            draw_text: Apakah menampilkan teks yang terdeteksi
            draw_confidence: Apakah menampilkan skor akurasi

        Returns:
            Dictionary metadata visualisasi
        """
        # Pastikan gambar berwarna (BGR)
        if len(image.shape) == 2:
            vis_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            vis_image = image.copy()

        metadata = {
            "total_text_boxes": 0,
            "average_confidence": 0.0,
            "confidences": [],
            "texts": [],
        }

        total_conf = 0.0
        count = 0

        # Warna untuk bounding box (BGR)
        box_color = (0, 255, 0)  # Hijau
        text_color = (255, 0, 0)  # Biru
        conf_color = (0, 0, 255)  # Merah

        # Parse dan gambar hasil OCR
        if ocr_results and len(ocr_results) > 0:
            for line in ocr_results[0]:
                box = line[0]
                text = line[1][0]
                conf = None
                try:
                    conf = float(line[1][1])
                except Exception:
                    pass

                if not text or not str(text).strip():
                    continue

                metadata["total_text_boxes"] += 1
                metadata["texts"].append(text)
                if conf is not None:
                    metadata["confidences"].append(conf)
                    total_conf += conf
                    count += 1

                # Gambar bounding box
                box_points = np.array(box, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(vis_image, [box_points], True, box_color, 2)

                # Hitung posisi untuk teks
                x_min = int(np.min(box_points[:, :, 0]))
                y_min = int(np.min(box_points[:, :, 1]))

                # Tampilkan teks yang terdeteksi
                if draw_text:
                    cv2.putText(
                        vis_image,
                        text,
                        (x_min, y_min - 20 if y_min > 30 else y_min + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        text_color,
                        2,
                    )

                # Tampilkan skor akurasi
                if draw_confidence and conf is not None:
                    conf_text = f"{conf:.2f}"
                    cv2.putText(
                        vis_image,
                        conf_text,
                        (x_min, y_min - 5 if y_min > 30 else y_min + 55),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        conf_color,
                        1,
                    )

        if count > 0:
            metadata["average_confidence"] = total_conf / count

        # Tambahkan legend/info di sudut kiri atas
        legend_y = 30
        cv2.putText(
            vis_image,
            f"Total: {metadata['total_text_boxes']} boxes",
            (10, legend_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        legend_y += 30
        if count > 0:
            cv2.putText(
                vis_image,
                f"Avg Conf: {metadata['average_confidence']:.2f}",
                (10, legend_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

        # Simpan gambar
        cv2.imwrite(output_path, vis_image)
        metadata["image_path"] = output_path

        logger.info(f"[OCR Preprocessor] Visualisasi OCR disimpan: {output_path}")

        return metadata


# Contoh penggunaan
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Contoh: Preprocess gambar dengan bukti
    preprocessor = OCRPreprocessor()

    # Ganti dengan path gambar Anda
    test_image = "test_image.jpg"
    if os.path.exists(test_image):
        proof = preprocessor.preprocess_with_proof(test_image, "contoh_preprocessing")
        print("Bukti preprocessing:")
        for step, data in proof.items():
            print(f"- {step}: {data['image_path']}")
            print(f"  Metadata: {data['metadata']}")
    else:
        print(f"Gambar uji tidak ditemukan: {test_image}")
        print("Silakan letakkan gambar dengan nama 'test_image.jpg' di direktori saat ini.")
