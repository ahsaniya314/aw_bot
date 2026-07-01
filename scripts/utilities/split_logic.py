import re

with open("handlers/callback_handler.py", "r", encoding="utf-8") as f:
    lines = f.readlines()


def get_indent(line):
    return len(line) - len(line.lstrip())


start_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def handle_semua_tombol(call):"):
        start_idx = i
        break

prelude = "".join(lines[:start_idx])
main_lines = lines[start_idx + 1 :]

blocks = []
current_block = []
current_condition = ""

for line in main_lines:
    indent = get_indent(line)
    if (
        indent == 4
        and line.lstrip().startswith("if call.data")
        or line.lstrip().startswith("if chat_id not in ctx.user_sessions")
    ):
        if current_block:
            blocks.append((current_condition, current_block))
        current_block = [line]
        current_condition = line.strip()
    elif indent == 4 and line.lstrip().startswith("cmd = call.data"):
        if current_block:
            blocks.append((current_condition, current_block))
        current_block = [line]
        current_condition = line.strip()
    elif indent == 4 and line.lstrip().startswith("if cmd"):
        if current_block:
            blocks.append((current_condition, current_block))
        current_block = [line]
        current_condition = line.strip()
    else:
        # if indent < 4 and line.strip(): # end of func
        #     break
        if current_block:
            current_block.append(line)
        else:
            # variables before ifs
            current_block.append(line)

if current_block:
    blocks.append((current_condition, current_block))

# Now categorize
trx_blocks = []
pg_blocks = []
dash_blocks = []
common_blocks = []

for cond, block in blocks:
    if (
        "mb_" in cond
        or "mm_" in cond
        or "btn_batal_edit" in cond
        or "pick_del" in cond
        or "pick_metode" in cond
    ):
        pg_blocks.append("".join(block))
    elif "dashboard" in cond:
        dash_blocks.append("".join(block))
    elif (
        "cmd =" in cond
        or "chat_id =" in cond
        or "msg_idx =" in cond
        or "chat_id not in ctx" in cond
    ):
        common_blocks.append("".join(block))
    else:
        trx_blocks.append("".join(block))

with open("handlers/callback_transaksi.py", "w", encoding="utf-8") as f:
    f.write(prelude)
    f.write("def handle_transaksi_callbacks(call):\n")
    for b in common_blocks:
        f.write(b)
    for b in trx_blocks:
        f.write(b)

with open("handlers/callback_pengaturan.py", "w", encoding="utf-8") as f:
    f.write(prelude)
    f.write("def handle_pengaturan_callbacks(call):\n")
    for b in common_blocks:
        f.write(b)
    for b in pg_blocks:
        f.write(b)

print(
    f"Total blocks: {len(blocks)}, Trx: {len(trx_blocks)}, Pg: {len(pg_blocks)}, Dash: {len(dash_blocks)}, Common: {len(common_blocks)}"
)
