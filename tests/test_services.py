"""
Unit Tests for Services
"""

from unittest.mock import MagicMock, patch

import pytest


class TestOCRService:
    """Tests for OCR service."""

    def test_ocr_service_initialization(self):
        """Test OCR service initializes without errors."""
        from services.ocr_service import OCRService
        service = OCRService()
        assert service is not None

    @pytest.mark.skip(reason="Requires PaddleOCR dependency")
    def test_ocr_process_image(self):
        """Test OCR image processing."""
        from services.ocr_service import OCRService
        service = OCRService()
        # Test would require actual image file
        pass


class TestCacheManager:
    """Tests for cache manager."""

    def test_cache_set_get(self):
        """Test cache set and get operations."""
        from services.cache_manager import GSpreadCache
        cache = GSpreadCache()
        
        cache.set("test_key", "test_value", ttl=60)
        result = cache.get("test_key")
        assert result == "test_value"

    def test_cache_invalidate(self):
        """Test cache invalidation."""
        from services.cache_manager import GSpreadCache
        cache = GSpreadCache()
        
        cache.set("test_key", "test_value")
        cache.invalidate("test_key")
        result = cache.get("test_key")
        assert result is None


class TestSessionManager:
    """Tests for session manager."""

    def test_session_create(self):
        """Test session creation."""
        from services.session_manager import UserSessions
        sessions = UserSessions()
        
        user_id = 123
        sessions.create_session(user_id)
        assert sessions.get_session(user_id) is not None

    def test_session_clear(self):
        """Test session clearing."""
        from services.session_manager import UserSessions
        sessions = UserSessions()
        
        user_id = 123
        sessions.create_session(user_id)
        sessions.clear_session(user_id)
        assert sessions.get_session(user_id) is None
