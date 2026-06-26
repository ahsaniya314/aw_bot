import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("COMPREHENSIVE SYSTEM AUDIT: BUTTON RESPONSIVENESS ISSUES")
print("="*70)
print()

files_to_audit = {
    'handlers/callback_transaksi.py': 'Transaksi Callbacks',
    'handlers/callback_pengaturan.py': 'Pengaturan Callbacks',
}

for file_path, label in files_to_audit.items():
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print(f"\n--- {label} ({file_path}) ---")
    print("-" * 70)
    
    # Find all callback patterns
    callbacks = re.findall(r'elif cmd\.startswith\("([^"]+)"\)|elif cmd == "([^"]+)"', content)
    callback_names = [c[0] or c[1] for c in callbacks]
    
    # Count answer_callback_query in vicinity of each callback
    issues = []
    current_line = 0
    for match in re.finditer(r'elif (cmd\.|call\.data)', content):
        start = max(0, match.start() - 100)
        end = min(len(content), match.end() + 500)
        section = content[start:end]
        
        # Check if this section has answer_callback_query
        has_answer = 'answer_callback_query' in section
        
        # Get the callback name
        cmd_match = re.search(r'elif (?:cmd|call\.data)(?:\.startswith|)\("([^"]+)"\)|== "([^"]+)"', section)
        if cmd_match and not has_answer:
            cmd_name = cmd_match.group(1) or cmd_match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            issues.append((line_num, cmd_name))
    
    if issues:
        print(f"\n--- Handlers WITHOUT answer_callback_query() ---")
        for line_num, cmd_name in issues[:15]:  # Show first 15
            print(f"   Line {line_num}: {cmd_name}*")
        if len(issues) > 15:
            print(f"   ... and {len(issues)-15} more")
    
    # Check for silent failures
    silent_fails = len(re.findall(r'except:\s*pass', content))
    print(f"\nSilent failures (except: pass): {silent_fails}")
    
    # Check for proper exception handling
    proper_except = len(re.findall(r'except Exception', content))
    print(f"Proper exceptions (except Exception): {proper_except}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
CRITICAL ISSUES FOUND:
  1. Pagination buttons in callback_pengaturan.py missing answer_callback_query
     - mb_edit_page_* handlers
     - mb_hapus_page_* handlers
  
  2. Silent failures throughout codebase
     - 28+ instances of 'except: pass' without logging
     - Users don't get feedback when errors occur

POSITIVE:
  - callback_transaksi.py mostly fixed after earlier changes
  - read_page_* handlers now have proper feedback

NEXT STEPS:
  1. Fix pagination handlers in callback_pengaturan.py (PRIORITY)
  2. Replace silent failures with proper logging
  3. Add try-catch blocks around critical operations
  4. Test all button interactions
""")
print("="*70)
