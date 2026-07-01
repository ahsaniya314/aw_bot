"""
Centralized Logging Module
==========================
Provides consistent logging configuration across all modules.

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Starting bot...")
"""

import json
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """Text formatter for human-readable logging."""

    def __init__(self):
        super().__init__(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


_loggers = {}
_log_directory = None


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "text",
) -> None:
    """
    Setup global logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_format: Log format (text, json)
    """
    global _log_directory

    # Create log directory if needed
    if log_file:
        log_path = Path(log_file)
        _log_directory = log_path.parent
        _log_directory.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Choose formatter
    if log_format.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # File handler (if specified)
    if log_file:
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            root_logger.warning(f"Could not setup file logging to {log_file}: {e}")


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)
        level: Optional logging level override

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Cache logger for later reference
    _loggers[name] = logger

    return logger


def get_all_loggers() -> dict:
    """Get all registered loggers."""
    return _loggers.copy()


def configure_from_config(config) -> None:
    """
    Configure logging from Config object.

    Args:
        config: Configuration instance with LOG_LEVEL, LOG_FILE, LOG_FORMAT
    """
    setup_logging(
        log_level=config.LOG_LEVEL,
        log_file=config.LOG_FILE,
        log_format=config.LOG_FORMAT,
    )


# Legacy compatibility: bot_logger
def get_bot_logger() -> logging.Logger:
    """Get logger for bot module (legacy)."""
    return get_logger("bot_logger")
