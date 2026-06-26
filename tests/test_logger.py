"""
Unit Tests for Logger
"""

import pytest
import logging
from utils.logger import get_logger, setup_logging, get_bot_logger


class TestLogger:
    """Tests for logging module."""

    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_get_bot_logger(self):
        """Test bot logger creation (legacy)."""
        logger = get_bot_logger()
        assert isinstance(logger, logging.Logger)

    def test_setup_logging(self, tmp_path):
        """Test logging setup."""
        log_file = tmp_path / "test.log"
        setup_logging(
            log_level="DEBUG",
            log_file=str(log_file),
            log_format="text"
        )
        
        logger = get_logger("test")
        logger.info("Test message")
        
        assert log_file.exists()

    def test_setup_logging_json_format(self, tmp_path):
        """Test JSON logging format."""
        log_file = tmp_path / "test.log"
        setup_logging(
            log_level="INFO",
            log_file=str(log_file),
            log_format="json"
        )
        
        logger = get_logger("test_json")
        logger.info("Test JSON message")
        
        assert log_file.exists()
