# Command Handlers Module
# Handles /start, /help, /dashboard, /master_barang, etc.

import logging

from telebot import TeleBot

logger = logging.getLogger(__name__)


def register_command_handlers(bot: TeleBot):
    """Register all command handlers using the old command_handler.py."""
    try:
        # Use the existing register_handlers from command_handler.py
        from handlers.command_handler import register_handlers as legacy_register

        legacy_register(bot)
        logger.info("Legacy command handlers registered")
    except Exception as e:
        logger.error(f"Could not register legacy command handlers: {e}")


__all__ = ["register_command_handlers"]
