"""
Unit Tests for Handlers
"""

import pytest
from unittest.mock import MagicMock, patch


class TestCommandHandlers:
    """Tests for command handlers."""

    def test_start_command(self, bot):
        """Test /start command."""
        from handlers.command.start import register
        register(bot)
        assert bot is not None

    def test_help_command(self, bot):
        """Test /help command."""
        from handlers.command.help import register
        register(bot)
        assert bot is not None


class TestCallbackHandlers:
    """Tests for callback handlers."""

    def test_barang_callbacks(self, bot):
        """Test product callbacks."""
        from handlers.callback.barang import register
        register(bot)
        assert bot is not None

    def test_transaksi_callbacks(self, bot):
        """Test transaction callbacks."""
        from handlers.callback.transaksi import register
        register(bot)
        assert bot is not None


class TestMessageHandlers:
    """Tests for message handlers."""

    def test_text_handler(self, bot):
        """Test text message handler."""
        from handlers.message.text import register
        register(bot)
        assert bot is not None

    def test_photo_handler(self, bot):
        """Test photo message handler."""
        from handlers.message.photo import register
        register(bot)
        assert bot is not None
