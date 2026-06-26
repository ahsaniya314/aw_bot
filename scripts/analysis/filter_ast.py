import ast

def filter_ast(file_in, file_out, keep_keywords, exclude_keywords, new_func_name):
    with open(file_in, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
        
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'handle_semua_tombol':
            node.name = new_func_name
            new_body = []
            for stmt in node.body:
                if isinstance(stmt, ast.If):
                    # We convert the condition to string to check if it matches keywords
                    cond_str = ast.unparse(stmt.test)
                    
                    # If this is not a condition based on call.data, keep it as common logic
                    if 'call.data' not in cond_str and 'cmd' not in cond_str and 'chat_id' not in cond_str:
                        new_body.append(stmt)
                        continue
                        
                    # Check if it should be kept
                    should_keep = False
                    
                    if keep_keywords:
                        if any(kw in cond_str for kw in keep_keywords):
                            should_keep = True
                    else:
                        should_keep = True
                        
                    if exclude_keywords:
                        if any(kw in cond_str for kw in exclude_keywords):
                            should_keep = False
                            
                    # Some common checks like session validation should always be kept
                    if "chat_id not in ctx.user_sessions" in cond_str or "cmd = call.data" in cond_str:
                        should_keep = True
                        
                    if should_keep:
                        new_body.append(stmt)
                else:
                    new_body.append(stmt)
                    
            node.body = new_body
            
    with open(file_out, 'w', encoding='utf-8') as f:
        f.write(ast.unparse(tree))

# We need the original callback_handler.py. But wait, I already overwrote it!
# I will grab the original one from git or just read it from callback_transaksi.py since I copied it earlier.
# Wait, I didn't overwrite the copies I made in the previous step? No, make_copies.py was overwritten by split_logic.py.
