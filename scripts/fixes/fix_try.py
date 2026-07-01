import re


def fix_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip() == "try:":
            # Just comment out the try block
            new_lines.append(line.replace("try:", "# try:"))
        else:
            new_lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(new_lines))


fix_file("handlers/callback_transaksi.py")
fix_file("handlers/callback_pengaturan.py")
