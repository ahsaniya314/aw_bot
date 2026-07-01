import os
import sys

import numpy as np


def get_box_metrics(box):
    """Menghitung x_min, y_min, y_max, dan y_center dari bounding box PaddleOCR."""
    points = np.array(box)
    x_min = np.min(points[:, 0])
    y_min = np.min(points[:, 1])
    y_max = np.max(points[:, 1])
    y_center = (y_min + y_max) / 2
    height = y_max - y_min
    return x_min, y_min, y_max, y_center, height


def sort_ocr_results(results):
    """
    Menyortir hasil OCR secara spatial dengan logika pengelompokan baris yang lebih fleksibel:
    1. Kelompokkan teks berdasarkan kedekatan vertikal (Y center).
    2. Urutkan tiap baris dari kiri ke kanan (X min).
    3. Menggunakan toleransi dinamis berdasarkan tinggi rata-rata karakter.
    """
    if not results or not results[0]:
        return []

    extracted_data = []
    for line in results[0]:
        box = line[0]
        text = line[1][0]
        x_min, y_min, y_max, y_center, height = get_box_metrics(box)
        extracted_data.append(
            {
                "text": text,
                "y_min": y_min,
                "y_max": y_max,
                "y_center": y_center,
                "x_min": x_min,
                "height": height,
            }
        )

    # 1. Urutkan berdasarkan koordinat Y center (Atas ke Bawah)
    extracted_data.sort(key=lambda x: x["y_center"])

    rows = []
    if not extracted_data:
        return rows

    current_row = [extracted_data[0]]

    for i in range(1, len(extracted_data)):
        item = extracted_data[i]

        # Hitung rata-rata center dan height dari baris saat ini
        avg_y_center = sum(x["y_center"] for x in current_row) / len(current_row)
        avg_height = sum(x["height"] for x in current_row) / len(current_row)

        # Toleransi: Jika jarak vertikal center < 45% dari tinggi baris, anggap baris yang sama
        # Ini lebih toleran terhadap tulisan tangan yang sedikit naik/turun
        if abs(item["y_center"] - avg_y_center) < (avg_height * 0.45):
            current_row.append(item)
        else:
            # Baris selesai, urutkan KIRI ke KANAN
            current_row.sort(key=lambda x: x["x_min"])
            rows.append(current_row)
            current_row = [item]

    # Tambahkan baris terakhir
    if current_row:
        current_row.sort(key=lambda x: x["x_min"])
        rows.append(current_row)

    return rows


def _normalize_predict_result(raw):
    """
    Mengkonversi output predict() PaddleOCR v5 ke format legacy:
    [ [ [box, [text, score]], ... ] ]
    agar kompatibel dengan sort_ocr_results.
    """
    # Jika sudah dalam format legacy (list of list), kembalikan langsung
    if isinstance(raw, list) and raw and isinstance(raw[0], list):
        # Periksa apakah ini benar-benar format legacy [[box, [text, score]], ...]
        if raw[0] and isinstance(raw[0][0], list):
            return raw

    if not isinstance(raw, list) or not raw:
        return [[]]

    first = raw[0]
    res = None
    if isinstance(first, dict):
        res = first.get("res") or first
    else:
        res = getattr(first, "res", None)

    if not isinstance(res, dict):
        return [[]]

    polys = res.get("rec_polys") or res.get("dt_polys")
    texts = res.get("rec_texts") or []
    scores = res.get("rec_scores") or []

    if polys is None or not len(texts):
        return [[]]

    lines = []
    n = min(len(polys), len(texts))
    for i in range(n):
        t = texts[i]
        if t is None or not str(t).strip():
            continue
        sc = None
        try:
            if i < len(scores):
                sc = float(scores[i])
        except Exception:
            sc = None
        box = polys[i]
        try:
            box = np.array(box).tolist()
        except Exception:
            pass
        lines.append([box, [t, sc]])

    return [lines]


def run_ocr(image_path):
    try:
        from paddleocr import PaddleOCR

        try:
            ocr_engine = PaddleOCR(
                text_detection_model_name="PP-OCRv5_mobile_det",
                text_recognition_model_name="PP-OCRv5_mobile_rec",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=True,
                lang="latin",
                device="cpu",
            )
        except Exception:
            try:
                ocr_engine = PaddleOCR(use_angle_cls=True, lang="en")
            except Exception:
                ocr_engine = PaddleOCR(lang="en")

        input_data = image_path
        raw = ocr_engine.predict(input_data)

        # Normalize predict() output ke format legacy [[box, [text, score]], ...]
        result = _normalize_predict_result(raw)

        # 2. Sort secara spatial untuk mempertahankan tata letak baris & kolom
        sorted_rows = sort_ocr_results(result)

        # 3. Susun teks per baris (satu baris teks per baris receipt)
        extracted_text = []
        for row in sorted_rows:
            row_text = " ".join([item["text"] for item in row])
            if row_text.strip():
                extracted_text.append(row_text.strip())

        if extracted_text:
            print("\n".join(extracted_text))
        else:
            print("")
    except Exception as e:
        sys.stderr.write(f"OCR Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python ocr_runner.py <image_path>\n")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        sys.stderr.write(f"Error: File not found {img_path}\n")
        sys.exit(1)

    run_ocr(img_path)
