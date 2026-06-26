import sys

def fix_try_except(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = []
    for line in lines:
        if line.strip() == 'try:':
            # keep it
            out.append(line)
        elif line.strip() == '# try:':
            out.append(line.replace('# try:', 'try:'))
        elif line.strip() == 'except Exception as e:':
            out.append(line)
        else:
            out.append(line)
            
    # Now we just need to ensure every try has an except and vice versa. 
    # Actually, let's just use st to parse. If it fails, we know we have a syntax error.
    # But it's easier to just do it manually. Let's print out lines with 	ry: and except
    for i, line in enumerate(out):
        if 'try:' in line or 'except' in line:
            print(f"{i+1}: {line.rstrip()}")

fix_try_except('handlers/callback_transaksi.py')
