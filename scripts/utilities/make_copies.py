import os

with open('handlers/callback_handler.py', 'r', encoding='utf-8') as f:
    content = f.read()

# callback_transaksi.py
content_trx = content.replace('def handle_semua_tombol(call):', 'def handle_transaksi_callbacks(call):')
with open('handlers/callback_transaksi.py', 'w', encoding='utf-8') as f:
    f.write(content_trx)

# callback_pengaturan.py
content_pg = content.replace('def handle_semua_tombol(call):', 'def handle_pengaturan_callbacks(call):')
with open('handlers/callback_pengaturan.py', 'w', encoding='utf-8') as f:
    f.write(content_pg)
