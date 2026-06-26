"""
Config Module - Centralized Configuration Management
====================================================
Import the config instance from here:
    from config import get_config
    
Or for direct settings access:
    from config.settings import Config, get_settings
"""

from .settings import Config, get_settings

def get_config() -> Config:
    """Get the global configuration instance."""
    return get_settings()

__all__ = ["get_config", "Config", "get_settings"]
