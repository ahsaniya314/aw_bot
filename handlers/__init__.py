# Handlers Module
# Organizes all Telegram event handlers (commands, callbacks, messages)

import logging

logger = logging.getLogger(__name__)


def register_all_handlers(bot):
    """Register all handlers with the bot."""
    try:
        from .command import register_command_handlers

        register_command_handlers(bot)
    except Exception as e:
        logger.warning(f"Error registering command handlers: {e}")

    try:
        from .callback import register_callback_handlers

        register_callback_handlers(bot)
    except Exception as e:
        logger.warning(f"Error registering callback handlers: {e}")

    try:
        from .message import register_message_handlers

        register_message_handlers(bot)
    except Exception as e:
        logger.warning(f"Error registering message handlers: {e}")

    logger.info("All handlers registered successfully")


__all__ = ["register_all_handlers"]
