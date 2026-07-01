"""
Unit Tests for Configuration
"""

import os

import pytest

from config.settings import Config, get_settings, reload_config


class TestConfigSettings:
    """Tests for configuration settings."""

    def test_config_singleton(self):
        """Test config singleton pattern."""
        config1 = get_settings()
        config2 = get_settings()
        assert config1 is config2

    def test_config_defaults(self):
        """Test default configuration values."""
        config = get_settings()
        assert config.LOG_LEVEL == "INFO"
        assert config.CACHE_TTL_SECONDS == 60
        assert config.ITEM_PER_PAGE == 5

    def test_config_environment_override(self):
        """Test environment variable override."""
        os.environ["LOG_LEVEL"] = "DEBUG"
        config = reload_config()
        # Reset to avoid affecting other tests
        if "LOG_LEVEL" in os.environ:
            del os.environ["LOG_LEVEL"]
        assert config.LOG_LEVEL == "DEBUG"

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = get_settings()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "LOG_LEVEL" in config_dict

    def test_config_mask_secrets(self):
        """Test that secrets are masked."""
        config = get_settings()
        config_dict = config.to_dict(include_secrets=False)
        # Check if sensitive values are masked
        assert config_dict.get("TELEGRAM_BOT_TOKEN") == "***REDACTED***" or config_dict.get("TELEGRAM_BOT_TOKEN") == ""

    def test_is_production(self):
        """Test production check."""
        os.environ["ENVIRONMENT"] = "production"
        config = reload_config()
        assert config.is_production() is True

    def test_is_development(self):
        """Test development check."""
        os.environ["ENVIRONMENT"] = "development"
        config = reload_config()
        assert config.is_development() is True
