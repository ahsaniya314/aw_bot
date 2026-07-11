#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test date extraction after fixes"""
import sys
from datetime import datetime
from nlp.extractor import ekstrak_entitas

test_cases = [
    ("hari ini budi pesan bembeng 40 ctn", "11-07-2026"),
    ("munculkan semua transaksi", None),
    ("3 hari yang lalu pak ardi ambil barang", "08-07-2026"),
]

print("Testing date extraction...")
for text, expected in test_cases:
    result = ekstrak_entitas(text)
    predicted = result.get("entitas", {}).get("TANGGAL")
    status = "PASS" if predicted == expected else "FAIL"
    print(f"[{status}] '{text}'")
    print(f"      Expected: {expected}, Got: {predicted}")
