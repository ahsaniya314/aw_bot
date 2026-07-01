import re


def clean_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "except Exception:\n                        pass\n                    except: pass",
        "except: pass",
    )
    content = content.replace(
        "except Exception:\n                    pass\n                except: pass", "except: pass"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


clean_file("handlers/callback_transaksi.py")
clean_file("handlers/callback_pengaturan.py")
