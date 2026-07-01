import re

with open("handlers/callback_handler.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find def handle_semua_tombol
start_idx = 0
for i, line in enumerate(lines):
    if line.startswith("def handle_semua_tombol(call):"):
        start_idx = i
        break

pre_code = "".join(lines[:start_idx])
main_func_lines = lines[start_idx:]

with open("handlers/callback_handler_split_debug.txt", "w", encoding="utf-8") as f:
    f.write(f"Found handle_semua_tombol at line {start_idx}")
