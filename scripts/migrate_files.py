"""
Migration Script - Organize Root Scripts into Subdirectories
Moves utility scripts from project root to organized scripts/ folders
Run: python scripts/migrate_files.py
"""

import os
import shutil
from pathlib import Path

# Define mappings: (source_file, target_folder)
SCRIPT_MAPPINGS = {
    # Analysis scripts
    "analyze_syntax.py": "scripts/analysis",
    "check_ast.py": "scripts/analysis",
    "filter_ast.py": "scripts/analysis",
    # Fix scripts
    "fix_all.py": "scripts/fixes",
    "fix_syntax.py": "scripts/fixes",
    "fix_try.py": "scripts/fixes",
    "fix_empty.py": "scripts/fixes",
    "fix_excepts.py": "scripts/fixes",
    "auto_fix_try.py": "scripts/fixes",
    "unfix_try.py": "scripts/fixes",
    # Utility scripts
    "make_copies.py": "scripts/utilities",
    "rewrite_dispatcher.py": "scripts/utilities",
    "split_callbacks.py": "scripts/utilities",
    "split_logic.py": "scripts/utilities",
    "ocr_runner.py": "scripts/utilities",
}


def migrate_scripts():
    """Migrate scripts from root to organized folders."""
    project_root = Path(__file__).parent.parent

    print("🚀 Starting script migration...\n")

    moved_count = 0
    skipped_count = 0

    for script_file, target_folder in SCRIPT_MAPPINGS.items():
        source_path = project_root / script_file
        target_path = project_root / target_folder / script_file

        if not source_path.exists():
            print(f"⏭️  SKIP: {script_file} (not found)")
            skipped_count += 1
            continue

        # Create target directory if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Move file
        try:
            shutil.move(str(source_path), str(target_path))
            print(f"✅ MOVED: {script_file} → {target_folder}/")
            moved_count += 1
        except Exception as e:
            print(f"❌ ERROR: {script_file} - {e}")

    print(f"\n📊 Migration Summary:")
    print(f"   ✅ Moved: {moved_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"\n✨ Migration completed!")


if __name__ == "__main__":
    migrate_scripts()
