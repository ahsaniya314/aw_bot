# Message Handlers Module
# Handles text messages, photos, documents, etc.

import logging

from telebot import TeleBot

logger = logging.getLogger(__name__)


def register_message_handlers(bot: TeleBot):
    """Register all message handlers."""
    try:
        from . import text

        text.register(bot)
    except Exception as e:
        logger.warning(f"Could not register text message handler: {e}")

    try:
        from . import photo

        photo.register(bot)
    except Exception as e:
        logger.warning(f"Could not register photo message handler: {e}")

    logger.info("Message handlers registered")


__all__ = ["register_message_handlers"]
