"""
Command Handler - /help
Shows available commands
"""


def register(bot):
    @bot.message_handler(commands=["help"])
    def handle_help(message):
        help_text = """
Available commands:
/start - Show greeting
/help - Show this message
/dashboard - Show dashboard
"""
        bot.reply_to(message, help_text)


__all__ = ["register"]
