def fix_orphaned_try(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = []
    try_stack = [] # stores (indent_level, line_index_in_out)
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
        
    for i, line in enumerate(lines):
        indent = get_indent(line)
        
        # If we dedented, we might need to close a try block
        while try_stack and indent <= try_stack[-1][0] and line.strip() != '' and not line.strip().startswith('except') and not line.strip().startswith('finally') and not line.strip().startswith('elif') and not line.strip().startswith('else'):
            # Close the try block!
            try_indent = try_stack.pop()[0]
            out.append(' ' * try_indent + 'except Exception:\n')
            out.append(' ' * (try_indent + 4) + 'pass\n')
            
        if line.strip() == 'try:':
            try_stack.append((indent, len(out)))
            out.append(line)
        elif line.strip().startswith('except ') or line.strip() == 'except:':
            if try_stack:
                try_stack.pop()
            out.append(line)
        else:
            out.append(line)
            
    while try_stack:
        try_indent = try_stack.pop()[0]
        out.append(' ' * try_indent + 'except Exception:\n')
        out.append(' ' * (try_indent + 4) + 'pass\n')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("".join(out))

fix_orphaned_try('handlers/callback_transaksi.py')
fix_orphaned_try('handlers/callback_pengaturan.py')
