"""
Message Handler - Text Messages
Routes natural-language input to the main text handler.
"""

import logging

logger = logging.getLogger(__name__)


def register(bot):
    from handlers.text_handler import register_handlers

    register_handlers(bot)
    logger.info("Text message handler registered (text_handler.py)")


__all__ = ["register"]
