import re


def clean_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove any except Exception: followed by pass that was injected after an except:
    content = re.sub(r"except:\s*pass\s*except Exception:\s*pass", "except: pass", content)

    # Also clean up empty try blocks which cause indentation error
    content = re.sub(r"try:\s*except", "try:\n    pass\nexcept", content)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


clean_file("handlers/callback_transaksi.py")
clean_file("handlers/callback_pengaturan.py")
