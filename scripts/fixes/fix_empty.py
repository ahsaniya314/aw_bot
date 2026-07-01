def fix_empty_try(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if line.strip() == "try:":
            # Check next non-empty line
            next_line = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip() != "":
                    next_line = lines[j]
                    break

            if next_line:
                indent_try = len(line) - len(line.lstrip())
                indent_next = len(next_line) - len(next_line.lstrip())
                if indent_next <= indent_try:
                    # The try block is empty!
                    out.append(" " * (indent_try + 4) + "pass\n")
            else:
                # EOF
                indent_try = len(line) - len(line.lstrip())
                out.append(" " * (indent_try + 4) + "pass\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(out))


fix_empty_try("handlers/callback_transaksi.py")
fix_empty_try("handlers/callback_pengaturan.py")
