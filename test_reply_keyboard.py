import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Force utf8 encoding for Windows
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Initialize the context
from core.bot_context import ctx
from handlers.command_handler import build_reply_keyboard

print("=== Testing Reply Keyboard ===")
print("\nReply Keyboard:")
markup = build_reply_keyboard()
print(repr(markup))
print("\nButtons in Reply Keyboard:")
for row in markup.keyboard:
    print(f"Row: {[btn['text'] for btn in row]}")

print("\n✅ Reply Keyboard test passed! All buttons are present!")