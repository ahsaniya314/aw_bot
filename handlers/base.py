"""
Base Handler Classes
Provides common functionality for all handlers
"""

import logging
from typing import Callable

from telebot import TeleBot

logger = logging.getLogger(__name__)


class BaseHandler:
    """Base class for all handlers."""

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def register_handlers(self):
        """Override to register specific handlers."""
        raise NotImplementedError


class CommandHandler(BaseHandler):
    """Base class for command handlers."""

    def register_command(self, command: str, callback: Callable):
        """Register a command handler."""

        @self.bot.message_handler(commands=[command])
        def handler(message):
            return callback(message)


class CallbackHandler(BaseHandler):
    """Base class for callback query handlers."""

    def register_callback(self, pattern: str, callback: Callable):
        """Register a callback query handler."""

        @self.bot.callback_query_handler(func=lambda call: pattern in call.data)
        def handler(call):
            return callback(call)


class MessageHandler(BaseHandler):
    """Base class for message handlers."""

    def register_message(self, content_types: list, callback: Callable):
        """Register a message handler."""

        @self.bot.message_handler(content_types=content_types)
        def handler(message):
            return callback(message)
