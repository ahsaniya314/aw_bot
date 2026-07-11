#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze confusion matrix improvements
Comparing before and after fixes
"""

# Before fixes
before = {
    "04-04-2026": {"04-04-2026": 3, "11-07-2026": 0},
    "05-04-2026": {"05-04-2026": 2, "11-07-2026": 1},  # 1 false positive to 11-07-2026
    "07-07-2026": {"10-07-2026": 2, "others": 0},
    "08-07-2026": {"08-07-2026": 11, "others": 0},  # But many mismatches in other rows
    "10-04-2026": {"10-04-2026": 2},
    "10-07-2026": {"10-07-2026": 0},
    "11-07-2026": {"11-07-2026": 0},
}

# After fixes (from new confusion matrix)
after = {
    "04-04-2026": {"04-04-2026": 3},  # Same
    "05-04-2026": {"05-04-2026": 3},  # IMPROVED: +1 correct (from 2 → 3)
    "07-07-2026": {"10-07-2026": 2},  # Same issue remains
    "08-07-2026": {"08-07-2026": 11},  # Same
    "10-04-2026": {"10-04-2026": 2},  # Same
    "10-07-2026": {},  # No entries
    "11-07-2026": {},  # No entries - CRITICAL: no more false positives!
}

print("="*80)
print("CONFUSION MATRIX IMPROVEMENT ANALYSIS")
print("="*80)

print("\n1. IMPROVEMENT in 05-04-2026:")
print(f"   BEFORE: 2 correct, 1 false positive to 11-07-2026")
print(f"   AFTER:  3 correct, 0 false positives")
print(f"   Status: [FIXED] ✅")

print("\n2. IMPROVEMENT in 11-07-2026 false positives:")
print(f"   BEFORE: 1 instance of 05-04-2026 misclassified as 11-07-2026")
print(f"   AFTER:  No false positives to 11-07-2026")
print(f"   Status: [FIXED] ✅ - Main fallback issue resolved!")

print("\n3. REMAINING ISSUE in 07-07-2026:")
print(f"   Status: 2 instances mispredicted as 10-07-2026")
print(f"   Issue:  NOT fixed by our changes")
print(f"   Cause:  Likely a different date calculation issue (off by 3 days)")

print("\n4. DIAGONAL ELEMENTS (Correct predictions):")
diagonal_before = 3 + 2 + 2 + 11 + 2 + 0 + 0  # = 20
diagonal_after = 3 + 3 + 2 + 11 + 2 + 0 + 0   # = 21
print(f"   BEFORE: {diagonal_before} correct predictions")
print(f"   AFTER:  {diagonal_after} correct predictions")
print(f"   Improvement: +{diagonal_after - diagonal_before} ✅")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("\nOur fixes successfully resolved the main issue:")
print("  ✅ FALLBACK TO HARI INI (11-07-2026) - FIXED")
print("  ✅ 05-04-2026 misclassification - FIXED")
print("  ⚠️  07-07-2026 → 10-07-2026 mismatch - NEEDS INVESTIGATION")
print("\nCRITICAL SUCCESS: No more 11-07-2026 false positives!")
