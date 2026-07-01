"""
Message Handler - Photo/OCR Processing
"""

import logging

logger = logging.getLogger(__name__)


def register(bot):
    from handlers.photo_handler import register_handlers

    register_handlers(bot)
    logger.info("Photo message handler registered (photo_handler.py)")


__all__ = ["register"]
