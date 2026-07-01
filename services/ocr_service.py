import base64
import hashlib
import logging
import os
import tempfile
from collections import OrderedDict

import numpy as np
import requests

from config.settings import get_settings

logger = logging.getLogger("bot_logger")


class OCRService:
    def __init__(self, preprocessor_output_dir=None):
        self.settings = get_settings()
        self.ocr_engine = None
        self.mistral_client = None
        self._disabled_reason = None
        self._last_debug = None
        # OCRPreprocessor tidak digunakan (preprocessing disabled untuk Mistral OCR)
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
            import time

            if (time.time() - entry.get("time", 0.0)) > ttl_seconds:
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

    def _try_init_mistral(self):
        try:
            if not self.settings.MISTRAL_API_KEY:
                return (
                    None,
                    "MISTRAL_API_KEY is not set. Silakan setting MISTRAL_API_KEY di environment variables!",
                )
            # Just check that we have the API key, no need for SDK
            return True, None
        except Exception as e:
            return None, f"Failed to initialize Mistral OCR: {e}"

    def _sanitize_image_path(self, image_path):
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

        # Step 3: Remove any extra spaces
        sanitized = sanitized.replace(" ", "")

        # Step 4: Normalize the path
        sanitized = os.path.normpath(sanitized)

        return sanitized

    def _find_image_path(self, image_path):
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
                return base64.b64encode(image_file.read()).decode("utf-8")
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
            raise RuntimeError("Gagal encode gambar!")

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
            "Content-Type": "application/json",
        }
        payload = {
            "model": "pixtral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all text from this receipt or document. Return only the extracted text, no explanations.",
                        },
                        {"type": "image_url", "image_url": image_url},
                    ],
                }
            ],
            "temperature": 0,
            "max_tokens": 2048,
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
                logger.warning(f"[OCR] Mistral timeout attempt {attempt}/{max_attempts}")
                if attempt >= max_attempts:
                    raise RuntimeError(
                        f"Timeout OCR ke Mistral setelah {max_attempts}x percobaan (read timeout={read_timeout}s)!"
                    ) from e
                time.sleep(min(attempt, 3))
            except requests.exceptions.HTTPError as e:
                last_error = e
                logger.error(f"[OCR] Mistral HTTP Error: {e}")
                # Coba cek response.text
                try:
                    error_detail = response.json() if response else str(e)
                    raise RuntimeError(f"Mistral API Error: {error_detail}") from e
                except:
                    raise RuntimeError(f"Mistral API Error: {str(e)}") from e
            except Exception as e:
                raise RuntimeError(f"Kesalahan koneksi ke Mistral: {str(e)}") from e
        raise RuntimeError(f"Gagal koneksi ke Mistral setelah {max_attempts}x: {last_error}")

    def load_model(self):
        """Memuat model OCR (HANYA MISTRAL OCR!"""
        engine = self.settings.OCR_ENGINE.lower()

        if engine == "mistralocr":
            if self.mistral_client is None:
                client, err = self._try_init_mistral()
                if err:
                    self._disabled_reason = err
                    logger.error(f"[OCR] {self._disabled_reason}")
                    return False
                self.mistral_client = client
                logger.info("[OCR] Mistral OCR configured successfully!")
            return True
        else:
            return False

    def _prepare_image_for_runtime_ocr(self, image_path):
        # OpenCV preprocessing disabled – directly use original image
        final_path = self._find_image_path(image_path)
        # No resizing or re‑encoding is performed; the image will be sent as‑is to Mistral OCR
        return final_path, None

    def extract_text(self, image_path):
        temp_runtime_path = None
        try:
            final_path = self._find_image_path(image_path)
            final_path, temp_runtime_path = self._prepare_image_for_runtime_ocr(final_path)
            self._last_debug = None
            engine = self.settings.OCR_ENGINE.lower()
            cache_key = self._get_ocr_cache_key(final_path)
            cached_text = self._get_cached_ocr_result(cache_key)
            if cached_text:
                logger.info("[OCR] Result cache hit!")
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
                            {
                                "name": "mistralocr",
                                "quality": 1.0,
                                "lines": len(extracted_text.splitlines()),
                                "score": 1.0,
                            }
                        ],
                    }
                    if (os.getenv("OCR_DEBUG") or "").strip().lower() in ("1", "true", "yes", "on"):
                        logger.info(
                            f"[OCR][DEBUG] Ran Mistral OCR directly on image. Lines: {len(extracted_text.splitlines())}"
                        )
                    self._set_cached_ocr_result(cache_key, extracted_text)
                    return extracted_text
                except Exception as mistral_error:
                    logger.error(f"[OCR] Mistral OCR Error: {mistral_error}")
                    return f"Error OCR: Mistral gagal - {str(mistral_error)}"
            else:
                return f"Error OCR: Hanya mendukung Mistral OCR! Setting OCR_ENGINE='mistralocr'!"
        except Exception as e:
            logger.error(f"[OCR] Extraction Error: {e}")
            return f"Error OCR: {str(e)}"
        finally:
            if temp_runtime_path and os.path.exists(temp_runtime_path):
                try:
                    os.remove(temp_runtime_path)
                except Exception:
                    pass

    def get_last_debug(self):
        return self._last_debug
