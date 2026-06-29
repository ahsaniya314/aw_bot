import os
import base64
import requests
import numpy as np
import logging
import tempfile
import hashlib
from collections import OrderedDict
from .ocr_preprocessor import OCRPreprocessor
from config.settings import get_settings

logger = logging.getLogger("bot_logger")

class OCRService:
    def __init__(self, preprocessor_output_dir=None):
        self.settings = get_settings()
        self.ocr_engine = None
        self.mistral_client = None
        self._disabled_reason = None
        self._last_debug = None
        self.preprocessor = OCRPreprocessor(output_dir=preprocessor_output_dir)
        self.http = requests.Session()
        self._ocr_result_cache = OrderedDict()
        logger.info("[OCR] Initializing OCR Service...")

    def _env_int(self, name, default):
        try:
            value = os.getenv(name)
            return int(value) if value is not None else int(default)
        except Exception:
            return int(default)

    def _get_ocr_cache_key(self, image_path):
        try:
            final_path = self._find_image_path(image_path)
            h = hashlib.sha1()
            with open(final_path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            return f"{self.settings.OCR_ENGINE.lower()}:{h.hexdigest()}"
        except Exception as e:
            logger.debug(f"[OCR] Cache key skipped: {e}")
            return None

    def _get_cached_ocr_result(self, cache_key):
        if not cache_key:
            return None
        entry = self._ocr_result_cache.get(cache_key)
        if not entry:
            return None

        ttl_seconds = self._env_int("OCR_RESULT_CACHE_TTL_SECONDS", 3600)
        if ttl_seconds > 0:
            age = max(0.0, entry.get("time", 0.0))
            import time
            if (time.time() - age) > ttl_seconds:
                self._ocr_result_cache.pop(cache_key, None)
                return None

        self._ocr_result_cache.move_to_end(cache_key)
        return entry.get("text")

    def _set_cached_ocr_result(self, cache_key, text):
        if not cache_key or text is None:
            return
        import time
        self._ocr_result_cache[cache_key] = {"text": text, "time": time.time()}
        self._ocr_result_cache.move_to_end(cache_key)

        max_items = self._env_int("OCR_RESULT_CACHE_MAX_ITEMS", 64)
        while len(self._ocr_result_cache) > max_items:
            self._ocr_result_cache.popitem(last=False)

    def _try_import_paddleocr(self):
        try:
            os.environ.setdefault("FLAGS_use_mkldnn", "0")
            os.environ.setdefault("FLAGS_use_onednn", "0")
            os.environ.setdefault("FLAGS_use_oneDNN", "0")
            from paddleocr import PaddleOCR
            try:
                import paddle
                paddle.set_flags({
                    "FLAGS_use_mkldnn": 0,
                    "FLAGS_use_onednn": 0,
                    "FLAGS_use_oneDNN": 0,
                })
            except Exception:
                pass
            return PaddleOCR, None
        except Exception as e:
            return None, e

    def _try_init_mistral(self):
        try:
            if not self.settings.MISTRAL_API_KEY:
                return None, "MISTRAL_API_KEY is not set"
            # Just check that we have the API key, no need for SDK
            return True, None
        except Exception as e:
            return None, f"Failed to initialize Mistral OCR: {e}"

    def _sanitize_image_path(self, image_path):
        """Sanitize image path to fix issues like '. ./contoh.jpeg' or '.contoh.jpeg'."""
        import os
        import re
        
        sanitized = image_path.strip()
        
        # Step 1: Handle cases with spaces between dots and slashes
        # Replace any sequence of dots followed by spaces followed by slash/backslash/dot
        # with the correct sequence
        # E.g., ". ./file" → "../file", ". /file" → "./file", ". /file" → "./file"
        # Use non-greedy regex
        while True:
            old_sanitized = sanitized
            # Replace ". " with "..", or ". /" → "./"
            sanitized = re.sub(r'\.\s+\.', r'..', sanitized)
            sanitized = re.sub(r'\.\s+([/\\])', r'.\1', sanitized)
            sanitized = re.sub(r'([/\\])\s+\.', r'\1.', sanitized)
            # Replace ". " followed by non-slash → "./" + the character
            sanitized = re.sub(r'\.\s+([^\./\\])', r'./\1', sanitized)
            if sanitized == old_sanitized:
                break
        
        # Step 2: Fix missing slash: ".contoh" → "./contoh"
        sanitized = re.sub(r'^\.([^\./\\])', r'./\1', sanitized)
        
        # Step 3: Remove any extra spaces that are left
        sanitized = sanitized.replace(' ', '')
        
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
        
        # If none found, return the sanitized path anyway (will fail later)
        return sanitized_path
    
    def _encode_image_to_base64(self, image_path):
        try:
            final_path = self._find_image_path(image_path)
            with open(final_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"[OCR] Failed to encode image: {e}")
            return None

    def _extract_markdown_from_mistral_response(self, response_json):
        try:
            extracted_text = ""
            if "choices" in response_json and len(response_json["choices"]) > 0:
                message = response_json["choices"][0].get("message", {})
                extracted_text = message.get("content", "")
            return extracted_text.strip()
        except Exception as e:
            logger.error(f"[OCR] Failed to parse Mistral OCR response: {e}")
            return ""

    def _call_mistral_ocr_api(self, image_path):
        # Meningkatkan default timeout untuk stabilitas di deployment
        connect_timeout = max(3, self._env_int("MISTRAL_OCR_CONNECT_TIMEOUT_SECONDS", 30))
        read_timeout = max(30, self._env_int("MISTRAL_OCR_READ_TIMEOUT_SECONDS", 180))
        max_attempts = max(1, self._env_int("MISTRAL_OCR_MAX_ATTEMPTS", 3))
        import time
        base64_image = self._encode_image_to_base64(image_path)
        if not base64_image:
            raise RuntimeError("Failed to encode image")
        
        # Determine image type from extension
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = "image/jpeg"
        if ext in [".png"]:
            mime_type = "image/png"
        elif ext in [".gif"]:
            mime_type = "image/gif"
        elif ext in [".webp"]:
            mime_type = "image/webp"
            
        image_url = f"data:{mime_type};base64,{base64_image}"
        
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "pixtral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this receipt or document. Return only the extracted text, no explanations."},
                        {"type": "image_url", "image_url": image_url}
                    ]
                }
            ],
            "temperature": 0,
            "max_tokens": 2048
        }
        
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        last_error = None
        for attempt in range(1, max_attempts + 1):
            _started_at = time.perf_counter()
            try:
                response = self.http.post(
                    url,
                    json=payload,
                    headers=headers,
                    verify=False,
                    timeout=(connect_timeout, read_timeout),
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout as e:
                last_error = e
                if attempt >= max_attempts:
                    raise RuntimeError(f"Timeout OCR ke Mistral setelah {max_attempts} percobaan (read timeout={read_timeout}s)") from e
                time.sleep(min(attempt, 3))
            except Exception as e:
                raise
        raise RuntimeError(f"Timeout OCR ke Mistral: {last_error}")


    def _env_bool(self, name, default=False):
        v = os.getenv(name)
        if v is None:
            return default
        return str(v).strip().lower() in ("1", "true", "yes", "on")

    def _build_paddleocr_kwargs(self, ocr_lang):
        series = (os.getenv("OCR_MODEL_SERIES") or "ppocrv5_mobile").strip().lower()

        base = {"lang": ocr_lang}

        if series in ("ppocrv5_mobile", "pp-ocrv5_mobile", "v5_mobile"):
            base.update({
                "text_detection_model_name": "PP-OCRv5_mobile_det",
                "text_recognition_model_name": "PP-OCRv5_mobile_rec",
                "use_doc_orientation_classify": False,
                "use_doc_unwarping": False,
                "use_textline_orientation": self._env_bool("OCR_USE_TEXTLINE_ORIENTATION", True),
                "device": "cpu",
            })
            return base

        if series in ("ppocrv5_server", "pp-ocrv5_server", "v5_server"):
            base.update({
                "text_detection_model_name": "PP-OCRv5_server_det",
                "text_recognition_model_name": "PP-OCRv5_server_rec",
                "use_doc_orientation_classify": False,
                "use_doc_unwarping": False,
                "use_textline_orientation": self._env_bool("OCR_USE_TEXTLINE_ORIENTATION", True),
                "device": "cpu",
            })
            return base

        base.update({
            "use_gpu": False,
            "use_angle_cls": True,
        })
        return base

    def load_model(self):
        """Memuat model OCR (PaddleOCR atau MistralOCR) ke RAM (Single Initialization)"""
        engine = self.settings.OCR_ENGINE.lower()
        
        if engine == "mistralocr":
            if self.mistral_client is None:
                client, err = self._try_init_mistral()
                if err:
                    self._disabled_reason = err
                    logger.error(f"[OCR] {self._disabled_reason}")
                    return False
                self.mistral_client = client
                logger.info("[OCR] Mistral OCR configured successfully")
            return True
        elif engine == "paddleocr":
            if self.ocr_engine is None:
                try:
                    PaddleOCR, err = self._try_import_paddleocr()
                    if not PaddleOCR:
                        self._disabled_reason = f"PaddleOCR import gagal: {err}"
                        logger.error(f"[OCR] {self._disabled_reason}")
                        return False

                    ocr_lang = (os.getenv("OCR_LANG") or "latin").strip()
                    kwargs = self._build_paddleocr_kwargs(ocr_lang)
                    import re
                    while True:
                        try:
                            self.ocr_engine = PaddleOCR(**kwargs)
                            break
                        except (TypeError, ValueError) as e:
                            err_msg = str(e)
                            match = re.search(r"Unknown argument:\s*(\w+)", err_msg) or re.search(r"unexpected keyword argument\s*'(\w+)'", err_msg)
                            if match:
                                unknown_arg = match.group(1)
                                if unknown_arg in kwargs:
                                    logger.warning(f"[OCR] Removing unsupported argument: {unknown_arg}")
                                    kwargs.pop(unknown_arg)
                                    continue
                            kwargs.pop("device", None)
                            kwargs.pop("text_detection_model_name", None)
                            kwargs.pop("text_recognition_model_name", None)
                            kwargs.pop("use_doc_orientation_classify", None)
                            kwargs.pop("use_doc_unwarping", None)
                            kwargs.pop("use_textline_orientation", None)
                            kwargs.pop("show_log", None)
                            if "use_gpu" not in kwargs:
                                kwargs["use_gpu"] = False
                            if "use_angle_cls" not in kwargs:
                                kwargs["use_angle_cls"] = True
                            try:
                                self.ocr_engine = PaddleOCR(**kwargs)
                                break
                            except Exception as inner_e:
                                raise inner_e
                    logger.info("[OCR] PaddleOCR Model loaded successfully to RAM")
                    return True
                except Exception as e:
                    self._disabled_reason = f"Load model gagal: {e}"
                    logger.error(f"[OCR] Failed to load PaddleOCR model: {e}")
                    return False
            return True
        else:
            self._disabled_reason = f"Unsupported OCR engine: {engine}. Use 'paddleocr' or 'mistralocr'."
            logger.error(f"[OCR] {self._disabled_reason}")
            return False

    def _ensure_paddle_fallback_engine(self):
        if self.ocr_engine is not None:
            return True
        PaddleOCR, err = self._try_import_paddleocr()
        if not PaddleOCR:
            raise RuntimeError(f"PaddleOCR import gagal: {err}")

        ocr_lang = (os.getenv("OCR_LANG") or "latin").strip()
        kwargs = self._build_paddleocr_kwargs(ocr_lang)
        import re
        while True:
            try:
                self.ocr_engine = PaddleOCR(**kwargs)
                return True
            except (TypeError, ValueError) as e:
                err_msg = str(e)
                match = re.search(r"Unknown argument:\s*(\w+)", err_msg) or re.search(r"unexpected keyword argument\s*'(\w+)'", err_msg)
                if match:
                    unknown_arg = match.group(1)
                    if unknown_arg in kwargs:
                        logger.warning(f"[OCR] Removing unsupported fallback argument: {unknown_arg}")
                        kwargs.pop(unknown_arg)
                        continue
                kwargs.pop("device", None)
                kwargs.pop("text_detection_model_name", None)
                kwargs.pop("text_recognition_model_name", None)
                kwargs.pop("use_doc_orientation_classify", None)
                kwargs.pop("use_doc_unwarping", None)
                kwargs.pop("use_textline_orientation", None)
                kwargs.pop("show_log", None)
                if "use_gpu" not in kwargs:
                    kwargs["use_gpu"] = False
                if "use_angle_cls" not in kwargs:
                    kwargs["use_angle_cls"] = True
                self.ocr_engine = PaddleOCR(**kwargs)
                return True

    def _extract_text_with_paddle_fallback(self, final_path):
        self._ensure_paddle_fallback_engine()
        if not hasattr(self.ocr_engine, "predict"):
            raise RuntimeError("Paddle fallback tidak mendukung method predict")
        raw = self.ocr_engine.predict(final_path)
        normalized = self._normalize_ocr_result(raw)
        extracted_lines, avg_score = self._build_lines_and_score(normalized)
        extracted_text = "\n".join(extracted_lines)
        self._last_debug = {
            "chosen": "paddle_fallback",
            "chosen_quality": avg_score,
            "best_candidate": "paddle_fallback",
            "best_quality": avg_score,
            "line_regions_quality": -1.0,
            "candidates": [
                {"name": "paddle_fallback", "quality": avg_score, "lines": len(extracted_lines), "score": avg_score}
            ],
        }
        return extracted_text


    def _get_box_metrics(self, box):
        points = np.array(box)
        x_min = np.min(points[:, 0])
        y_min = np.min(points[:, 1])
        y_max = np.max(points[:, 1])
        y_center = (y_min + y_max) / 2
        height = y_max - y_min
        return x_min, y_min, y_max, y_center, height

    def _sort_ocr_results(self, results):
        if not results or not results[0]:
            return []
        
        boxes = []
        for line in results[0]:
            box = line[0]
            text = line[1][0]
            score = None
            try:
                score = float(line[1][1])
            except Exception:
                score = None
            points = np.array(box)
            x_min = np.min(points[:, 0])
            x_max = np.max(points[:, 0])
            y_min = np.min(points[:, 1])
            y_max = np.max(points[:, 1])
            height = y_max - y_min
            if not text or not str(text).strip():
                continue
            boxes.append({
                "text": text,
                "score": score,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "height": height,
                "y_center": (y_min + y_max) / 2
            })
        
        if not boxes:
            return []

        heights = [b["height"] for b in boxes if b["height"] and b["height"] > 0]
        median_h = float(np.median(heights)) if heights else 10.0
        y_threshold = max(median_h * 0.7, 10.0)

        boxes.sort(key=lambda b: (b["y_center"], b["x_min"]))
        lines = []
        for b in boxes:
            best_i = None
            best_d = None
            for i, ln in enumerate(lines):
                d = abs(b["y_center"] - ln["y"])
                if d <= y_threshold and (best_d is None or d < best_d):
                    best_d = d
                    best_i = i
            if best_i is None:
                lines.append({"y": b["y_center"], "items": [b]})
            else:
                ln = lines[best_i]
                n = len(ln["items"])
                ln["y"] = (ln["y"] * n + b["y_center"]) / (n + 1)
                ln["items"].append(b)

        lines.sort(key=lambda ln: ln["y"])
        final_rows = []
        for ln in lines:
            ln["items"].sort(key=lambda b: b["x_min"])
            final_rows.append(ln["items"])
        return final_rows

    def _build_lines_and_score(self, ocr_result):
        sorted_rows = self._sort_ocr_results(ocr_result)
        extracted_lines = []
        total_score = 0.0
        score_count = 0
        for row in sorted_rows:
            line_text = " ".join([item["text"] for item in row]).strip()
            if line_text:
                extracted_lines.append(line_text)
            for item in row:
                s = item.get("score")
                if s is None:
                    continue
                total_score += float(s)
                score_count += 1
        avg_score = (total_score / score_count) if score_count else 0.0
        return extracted_lines, avg_score

    def _quality(self, lines, score):
        if not lines:
            return -1e18
        text_len = sum(len(x) for x in lines)
        line_count = len(lines)
        return (float(score) * 1000.0) + (line_count * 40.0) + text_len

    def _normalize_ocr_result(self, raw_result):
        if isinstance(raw_result, list) and raw_result and isinstance(raw_result[0], list):
            return raw_result

        if not isinstance(raw_result, list) or not raw_result:
            return []

        first = raw_result[0]
        res = None
        if isinstance(first, dict):
            res = first.get("res") or first
        else:
            res = getattr(first, "res", None)

        if not isinstance(res, dict):
            return []

        polys = res.get("rec_polys") or res.get("dt_polys")
        texts = res.get("rec_texts") or []
        scores = res.get("rec_scores") or []

        if polys is None or not len(texts):
            return []

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

    def _run_ocr(self, img):
        engine = self.settings.OCR_ENGINE.lower()
        
        if engine == "mistralocr":
            if self.mistral_client is None:
                ok = self.load_model()
                if not ok:
                    raise RuntimeError(self._disabled_reason or "OCR tidak tersedia")
            
            response_json = self._call_mistral_ocr_api(img)
            extracted_text = self._extract_markdown_from_mistral_response(response_json)
            return extracted_text
        elif engine == "paddleocr":
            if self.ocr_engine is None:
                ok = self.load_model()
                if not ok:
                    raise RuntimeError(self._disabled_reason or "OCR tidak tersedia")

            if hasattr(self.ocr_engine, "predict"):
                raw = self.ocr_engine.predict(img)
                return self._normalize_ocr_result(raw)

            raise RuntimeError("OCR engine tidak mendukung method predict")
        else:
            raise RuntimeError(f"Unsupported OCR engine: {engine}")

    def _prepare_image_for_runtime_ocr(self, image_path):
        """
        Ringankan gambar sangat besar sebelum OCR untuk mengurangi waktu decode,
        inferensi CPU, dan ukuran payload API tanpa mengubah alur fitur.
        """
        try:
            import cv2

            final_path = self._find_image_path(image_path)
            image = cv2.imread(final_path)
            if image is None:
                return final_path, None

            h, w = image.shape[:2]
            max_dim = max(w, h)
            engine = self.settings.OCR_ENGINE.lower()
            src_ext = (os.path.splitext(final_path)[1] or ".jpg").lower()
            file_size = os.path.getsize(final_path) if os.path.exists(final_path) else 0

            if engine == "mistralocr":
                target_max_dim = self._env_int("OCR_MISTRAL_MAX_DIM", 1800)
                jpeg_quality = self._env_int("OCR_MISTRAL_JPEG_QUALITY", 82)
                max_source_bytes = self._env_int("OCR_MISTRAL_MAX_SOURCE_BYTES", 1500000)

                needs_resize = max_dim > target_max_dim
                needs_reencode = src_ext not in (".jpg", ".jpeg") or file_size > max_source_bytes
                if not needs_resize and not needs_reencode:
                    return final_path, None

                resized = image
                if needs_resize:
                    scale = target_max_dim / float(max_dim)
                    resized, _ = self.preprocessor.resize_image(image, scale_factor=scale)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    temp_path = tmp.name

                cv2.imwrite(temp_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                try:
                    out_size = os.path.getsize(temp_path)
                except Exception:
                    out_size = 0
                logger.info(
                    f"[OCR] Mistral runtime optimize: {w}x{h} -> {resized.shape[1]}x{resized.shape[0]}, "
                    f"{file_size}B -> {out_size}B"
                )
                return temp_path, temp_path

            target_max_dim = self._env_int("OCR_RUNTIME_MAX_DIM", 2200)
            if max_dim <= target_max_dim:
                return final_path, None

            scale = target_max_dim / float(max_dim)
            resized, _ = self.preprocessor.resize_image(image, scale_factor=scale)
            suffix = os.path.splitext(final_path)[1] or ".jpg"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                temp_path = tmp.name

            ext = suffix.lower()
            if ext in (".jpg", ".jpeg"):
                cv2.imwrite(temp_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), self._env_int("OCR_RUNTIME_JPEG_QUALITY", 88)])
            elif ext == ".png":
                cv2.imwrite(temp_path, resized, [int(cv2.IMWRITE_PNG_COMPRESSION), self._env_int("OCR_RUNTIME_PNG_COMPRESSION", 3)])
            else:
                cv2.imwrite(temp_path, resized)

            logger.info(f"[OCR] Runtime resize applied: {w}x{h} -> {resized.shape[1]}x{resized.shape[0]}")
            return temp_path, temp_path
        except Exception as e:
            logger.warning(f"[OCR] Runtime image optimization skipped: {e}")
            return self._find_image_path(image_path), None

    def extract_text(self, image_path):
        """Fungsi utama ekstraksi teks (PaddleOCR atau MistralOCR)"""
        temp_runtime_path = None
        try:
            final_path = self._find_image_path(image_path)
            final_path, temp_runtime_path = self._prepare_image_for_runtime_ocr(final_path)
            self._last_debug = None
            engine = self.settings.OCR_ENGINE.lower()
            cache_key = self._get_ocr_cache_key(final_path)
            cached_text = self._get_cached_ocr_result(cache_key)
            if cached_text:
                logger.info("[OCR] Result cache hit")
                return cached_text
            
            if engine == "mistralocr":
                if self.mistral_client is None:
                    ok = self.load_model()
                    if not ok:
                        return f"Error OCR: {self._disabled_reason or 'OCR tidak tersedia'}"
                try:
                    response_json = self._call_mistral_ocr_api(final_path)
                    extracted_text = self._extract_markdown_from_mistral_response(response_json)
                    self._last_debug = {
                        "chosen": "mistralocr",
                        "chosen_quality": 1.0,
                        "best_candidate": "mistralocr",
                        "best_quality": 1.0,
                        "line_regions_quality": -1.0,
                        "candidates": [
                            {"name": "mistralocr", "quality": 1.0, "lines": len(extracted_text.splitlines()), "score": 1.0}
                        ],
                    }
                    if (os.getenv("OCR_DEBUG") or "").strip().lower() in ("1", "true", "yes", "on"):
                        logger.info(f"[OCR][DEBUG] Ran Mistral OCR directly on image. Lines: {len(extracted_text.splitlines())}")
                    self._set_cached_ocr_result(cache_key, extracted_text)
                    return extracted_text
                except Exception as mistral_error:
                    # TIDAK ADA FALLBACK! Langsung return error Mistral
                    logger.error(f"[OCR] Mistral OCR Error: {mistral_error}")
                    return f"Error OCR: Mistral gagal - {str(mistral_error)}"
            elif engine == "paddleocr":
                if self.ocr_engine is None:
                    ok = self.load_model()
                    if not ok:
                        return f"Error OCR: {self._disabled_reason or 'OCR tidak tersedia'}"

                # Jalankan OCR langsung pada file asli
                r = self._run_ocr(final_path)
                extracted_lines, avg_score = self._build_lines_and_score(r)

                self._last_debug = {
                    "chosen": "raw_image",
                    "chosen_quality": avg_score,
                    "best_candidate": "raw_image",
                    "best_quality": avg_score,
                    "line_regions_quality": -1.0,
                    "candidates": [
                        {"name": "raw_image", "quality": avg_score, "lines": len(extracted_lines), "score": avg_score}
                    ],
                }

                if (os.getenv("OCR_DEBUG") or "").strip().lower() in ("1", "true", "yes", "on"):
                    logger.info(f"[OCR][DEBUG] Ran pure PaddleOCR directly on image. Lines: {len(extracted_lines)}, Score: {avg_score:.4f}")
                extracted_text = "\n".join(extracted_lines)
                self._set_cached_ocr_result(cache_key, extracted_text)
                return extracted_text
            else:
                return f"Error OCR: Unsupported engine {engine}"
        except Exception as e:
            logger.error(f"[OCR] Extraction Error: {e}")
            return f"Error OCR: {e}"
        finally:
            if temp_runtime_path and os.path.exists(temp_runtime_path):
                try:
                    os.remove(temp_runtime_path)
                except Exception:
                    pass

    def extract_text_with_preprocessing_proof(self, image_path, base_filename="ocr_process", 
                                              save_ocr_visualization: bool = True):
        """
        Ekstrak teks dengan preprocessing lengkap dan bukti visual setiap langkah + bukti proses OCR.
        
        Args:
            image_path: Path ke gambar input
            base_filename: Nama dasar untuk file bukti preprocessing
            save_ocr_visualization: Apakah menyimpan visualisasi proses OCR (bounding box dll) - Hanya untuk PaddleOCR
            
        Returns:
            Tuple (teks_ekstraksi, dict_bukti_lengkap)
        """
        try:
            final_path = self._find_image_path(image_path)
            logger.info(f"[OCR] Memulai preprocessing dengan bukti untuk: {final_path}")
            engine = self.settings.OCR_ENGINE.lower()
            
            # Jalankan preprocessing dan simpan bukti
            proof_data = self.preprocessor.preprocess_with_proof(final_path, base_filename)
            
            # Dapatkan gambar yang sudah di-preprocess (langkah terakhir: deskewed)
            deskewed_image_path = proof_data["05_deskewed"]["image_path"]
            
            if engine == "mistralocr":
                if self.mistral_client is None:
                    ok = self.load_model()
                    if not ok:
                        return f"Error OCR: {self._disabled_reason or 'OCR tidak tersedia'}", proof_data
                
                response_json = self._call_mistral_ocr_api(deskewed_image_path)
                extracted_text = self._extract_markdown_from_mistral_response(response_json)
                proof_data["ocr_result"] = {
                    "text": extracted_text,
                    "source_image": deskewed_image_path,
                    "average_score": 1.0,
                    "raw_response": response_json
                }
                
                self._last_debug = {
                    "chosen": "mistralocr",
                    "chosen_quality": 1.0,
                    "best_candidate": "mistralocr",
                    "best_quality": 1.0,
                    "proof_data": proof_data
                }
                
                logger.info(f"[OCR] Ekstraksi dengan bukti selesai (MistralOCR). Lines: {len(extracted_text.splitlines())}")
                
                return extracted_text, proof_data
            
            elif engine == "paddleocr":
                # Baca gambar yang sudah di-preprocess
                import cv2
                processed_image = cv2.imread(deskewed_image_path)
                
                # Jalankan OCR dan dapatkan hasil mentah
                raw_ocr_result = self._run_ocr(deskewed_image_path)
                extracted_lines, avg_score = self._build_lines_and_score(raw_ocr_result)
                ocr_text = "\n".join(extracted_lines)
                
                # Tambahkan bukti proses OCR
                proof_data["ocr_result"] = {
                    "text": ocr_text,
                    "source_image": deskewed_image_path,
                    "average_score": avg_score,
                    "raw_result": raw_ocr_result
                }
                
                # Simpan visualisasi OCR jika diminta
                if save_ocr_visualization:
                    ocr_vis_path = os.path.join(self.preprocessor.output_dir, f"{base_filename}_06_ocr_visualization.png")
                    ocr_vis_metadata = self.preprocessor.visualize_ocr_results(
                        image=processed_image,
                        ocr_results=raw_ocr_result,
                        output_path=ocr_vis_path
                    )
                    proof_data["06_ocr_visualization"] = {
                        "image_path": ocr_vis_path,
                        "metadata": ocr_vis_metadata
                    }
                
                self._last_debug = {
                    "chosen": "preprocessed_image",
                    "chosen_quality": avg_score,
                    "best_candidate": "preprocessed_image",
                    "best_quality": avg_score,
                    "proof_data": proof_data
                }
                
                logger.info(f"[OCR] Ekstraksi dengan bukti selesai (PaddleOCR). Teks: {len(extracted_lines)} baris")
                
                return ocr_text, proof_data
            
            else:
                return f"Error OCR: Unsupported engine {engine}", proof_data
            
        except Exception as e:
            logger.error(f"[OCR] Error pada extract_text_with_preprocessing_proof: {e}")
            return f"Error: {e}", {}
    
    def get_last_debug(self):
        return self._last_debug
