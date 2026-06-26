"""
Command Handler - /start
Registers greeting command
"""

def register(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "Hello! I'm AW Production Bot. Use /help for available commands.")

__all__ = ["register"]
