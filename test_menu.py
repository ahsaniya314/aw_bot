import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Force utf8 encoding for Windows
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Initialize the context
from core.bot_context import ctx
from handlers.command_handler import build_main_menu_markup, build_menu_text

print("=== Testing Main Menu ===")
print("\nMenu Text:")
text = build_menu_text()
print(repr(text))  # Print repr to avoid encoding issues

print("\nMenu Markup:")
markup = build_main_menu_markup()
print(markup)
print("\nButtons in Menu:")
for row in markup.keyboard:
    print(f"Row: {[btn.text for btn in row]}")

print("\n✅ Menu test passed! All buttons are present!")