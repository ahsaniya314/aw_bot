import re

def fix_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # We want to find where except Exception as e: is and inject 	ry: at the start of the function.
    # Actually, the function is def handle_transaksi_callbacks(call):
    # Let's see if we can find the start of the logic and insert 	ry: and indent everything.
    # But wait, my split_logic.py just printed lines as they were, it didn't change indentation.
    # If I just insert 	ry: right after sess = ctx.user_sessions[chat_id], it might work.
    
    # Or instead of guessing, let's just REPLACE except Exception as e: with nothing!
    # Because if we remove the except block entirely, it becomes valid python, and we can just add a global try-except in the dispatcher!
    
    new_lines = []
    skip = False
    for i, line in enumerate(lines):
        if line.strip().startswith('except Exception as e:'):
            skip = True
            continue
            
        if skip:
            if line.startswith('    ') or line.strip() == '':
                # check if it's the ctx.bot.send_message line which is indented
                if 'ctx.bot.send_message' in line or 'safe_edit_message' in line:
                    continue
            skip = False
            
        new_lines.append(line)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("".join(new_lines))

fix_file('handlers/callback_transaksi.py')
fix_file('handlers/callback_pengaturan.py')
