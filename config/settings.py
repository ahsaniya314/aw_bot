"""
Settings Module - Centralized Configuration Management
======================================================
Loads and validates all environment variables in one place.
Usage:
    from config.settings import get_settings
    config = get_settings()
    print(config.TELEGRAM_BOT_TOKEN)
"""

import os
import logging
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

logger = logging.getLogger("config")


class Config:
    """
    Centralized configuration container.
    All configuration is loaded from environment variables at startup.
    """

    # ==========================================
    # TELEGRAM BOT CONFIGURATION
    # ==========================================
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_BOT_ADMIN_IDS: List[int] = []
    TELEGRAM_WEBHOOK_URL: Optional[str] = os.getenv("TELEGRAM_WEBHOOK_URL")
    TELEGRAM_WEBHOOK_PATH_SECRET: Optional[str] = os.getenv("TELEGRAM_WEBHOOK_PATH_SECRET")
    TELEGRAM_WEBHOOK_SECRET_TOKEN: Optional[str] = os.getenv("TELEGRAM_WEBHOOK_SECRET_TOKEN")

    # ==========================================
    # SUPABASE CONFIGURATION
    # ==========================================
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_POSTGREST_TIMEOUT: int = int(os.getenv("SUPABASE_POSTGREST_TIMEOUT", "30"))
    SUPABASE_STORAGE_TIMEOUT: int = int(os.getenv("SUPABASE_STORAGE_TIMEOUT", "20"))

    # ==========================================
    # GOOGLE SHEETS CONFIGURATION (Legacy)
    # ==========================================
    GSPREAD_SHEET_NAME: str = os.getenv("GSPREAD_SHEET_NAME", "AW PRODUCTION")
    GSPREAD_CREDENTIALS_FILE: str = os.getenv("GSPREAD_CREDENTIALS_FILE", "credentials.json")
    GSPREAD_BACKUP_ENABLED: bool = os.getenv("GSPREAD_BACKUP_ENABLED", "true").lower() in ("true", "yes", "1")

    # ==========================================
    # DATABASE CONFIGURATION
    # ==========================================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///bot_data.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() in ("true", "yes", "1")

    # ==========================================
    # NLP CONFIGURATION
    # ==========================================
    NLP_MODEL_TYPE: str = os.getenv("NLP_MODEL_TYPE", "rule_based")  # rule_based, distilbert, indobert
    NLP_CONFIDENCE_THRESHOLD: float = float(os.getenv("NLP_CONFIDENCE_THRESHOLD", "0.7"))
    NLP_FUZZY_THRESHOLD: int = int(os.getenv("NLP_FUZZY_THRESHOLD", "85"))

    # ==========================================
    # OCR CONFIGURATION
    # ==========================================
    OCR_LANGUAGE: str = os.getenv("OCR_LANGUAGE", "en")
    OCR_ANGLE_DETECTION: bool = os.getenv("OCR_ANGLE_DETECTION", "true").lower() in ("true", "yes", "1")
    OCR_CONFIDENCE_THRESHOLD: float = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.5"))
    OCR_ENGINE: str = os.getenv("OCR_ENGINE", "paddleocr")  # "paddleocr" or "mistralocr"
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    OCR_RUNTIME_MAX_DIM: int = int(os.getenv("OCR_RUNTIME_MAX_DIM", "2200"))
    OCR_RUNTIME_JPEG_QUALITY: int = int(os.getenv("OCR_RUNTIME_JPEG_QUALITY", "88"))
    OCR_RUNTIME_PNG_COMPRESSION: int = int(os.getenv("OCR_RUNTIME_PNG_COMPRESSION", "3"))
    OCR_MISTRAL_MAX_DIM: int = int(os.getenv("OCR_MISTRAL_MAX_DIM", "1800"))
    OCR_MISTRAL_JPEG_QUALITY: int = int(os.getenv("OCR_MISTRAL_JPEG_QUALITY", "82"))
    OCR_MISTRAL_MAX_SOURCE_BYTES: int = int(os.getenv("OCR_MISTRAL_MAX_SOURCE_BYTES", "1500000"))
    OCR_RESULT_CACHE_TTL_SECONDS: int = int(os.getenv("OCR_RESULT_CACHE_TTL_SECONDS", "3600"))
    OCR_RESULT_CACHE_MAX_ITEMS: int = int(os.getenv("OCR_RESULT_CACHE_MAX_ITEMS", "64"))

    # ==========================================
    # LOGGING CONFIGURATION
    # ==========================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # text, json

    # ==========================================
    # RATE LIMITING
    # ==========================================
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() in ("true", "yes", "1")
    RATE_LIMIT_REQUESTS_PER_SECOND: int = int(os.getenv("RATE_LIMIT_REQUESTS_PER_SECOND", "10"))
    RATE_LIMIT_BURST_SIZE: int = int(os.getenv("RATE_LIMIT_BURST_SIZE", "20"))

    # ==========================================
    # CACHE CONFIGURATION
    # ==========================================
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))

    # ==========================================
    # UI CONFIGURATION
    # ==========================================
    ITEM_PER_PAGE: int = int(os.getenv("ITEM_PER_PAGE", "5"))
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))

    # ==========================================
    # FEATURE FLAGS
    # ==========================================
    ENABLE_OCR: bool = os.getenv("ENABLE_OCR", "true").lower() in ("true", "yes", "1")
    ENABLE_NLP: bool = os.getenv("ENABLE_NLP", "true").lower() in ("true", "yes", "1")
    ENABLE_AUTO_REMINDER: bool = os.getenv("ENABLE_AUTO_REMINDER", "true").lower() in ("true", "yes", "1")
    ENABLE_DASHBOARD: bool = os.getenv("ENABLE_DASHBOARD", "true").lower() in ("true", "yes", "1")

    # ==========================================
    # DEPLOYMENT CONFIGURATION
    # ==========================================
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # development, staging, production
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "yes", "1")
    BUILD_ID: str = os.getenv("BUILD_ID", "dev-local")
    SHOW_BUILD: bool = os.getenv("SHOW_BUILD", "true").lower() in ("true", "yes", "1")

    # ==========================================
    # API CONFIGURATION
    # ==========================================
    FLASK_HOST: str = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", "7860"))
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "yes", "1")

    def __init__(self):
        """Initialize and validate configuration."""
        self._parse_admin_ids()
        self._validate()

    def _parse_admin_ids(self):
        """Parse TELEGRAM_BOT_ADMIN_IDS from comma-separated string."""
        admin_ids_str = os.getenv("TELEGRAM_BOT_ADMIN_IDS", "")
        try:
            self.TELEGRAM_BOT_ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()]
        except ValueError:
            logger.warning(f"Invalid TELEGRAM_BOT_ADMIN_IDS format: {admin_ids_str}")
            self.TELEGRAM_BOT_ADMIN_IDS = []

    def _validate(self):
        """Validate critical configuration values."""
        if not self.TELEGRAM_BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN is not set")
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            logger.warning("Supabase credentials not fully configured")

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT.lower() == "development"

    def get_log_level(self):
        """Get logging level as logging constant."""
        import logging
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)

    def to_dict(self, include_secrets: bool = False) -> dict:
        """Convert config to dictionary (useful for debugging)."""
        result = {}
        for key in dir(self):
            if key.startswith("_") or callable(getattr(self, key)):
                continue
            value = getattr(self, key)
            # Mask sensitive values
            if not include_secrets and any(secret in key for secret in ["TOKEN", "KEY", "SECRET", "PASSWORD"]):
                value = "***REDACTED***"
            result[key] = value
        return result


# Global configuration instance (Singleton)
_config_instance: Optional[Config] = None


def get_settings() -> Config:
    """Get or create the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def reload_config() -> Config:
    """Reload configuration from environment (useful for testing)."""
    global _config_instance
    load_dotenv(override=True)
    _config_instance = Config()
    return _config_instance
