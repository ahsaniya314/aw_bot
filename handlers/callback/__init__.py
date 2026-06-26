# Callback Handlers Module
# Handles inline button callbacks and menu interactions

from telebot import TeleBot
import logging

logger = logging.getLogger(__name__)

def register_callback_handlers(bot: TeleBot):
    """Register callback handlers using the existing callback_handler.py."""
    try:
        # Use the existing register_handlers from the main callback_handler.py
        from handlers.callback_handler import register_handlers
        register_handlers(bot)
        logger.info("Callback handlers registered (using callback_handler.py router)")
    except Exception as e:
        logger.error(f"Could not register callback handlers: {e}", exc_info=True)

__all__ = ["register_callback_handlers"]
