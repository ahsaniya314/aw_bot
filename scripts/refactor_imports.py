import os
import re

MAPPINGS = {
    r"(\b)import db_client(\b)": r"\1from database import db_client\2",
    r"(\b)from db_client import(\b)": r"\1from database.db_client import\2",
    r"(\b)import gspread_mock(\b)": r"\1from database import gspread_mock\2",
    r"(\b)from gspread_mock import(\b)": r"\1from database.gspread_mock import\2",
    r"(\b)import bot_context(\b)": r"\1from core import bot_context\2",
    r"(\b)from bot_context import(\b)": r"\1from core.bot_context import\2",
    r"(\b)import master_data(\b)": r"\1from core import master_data\2",
    r"(\b)from master_data import(\b)": r"\1from core.master_data import\2",
    r"(\b)import daily_dashboard(\b)": r"\1from services import daily_dashboard\2",
    r"(\b)from daily_dashboard import(\b)": r"\1from services.daily_dashboard import\2",
    r"(\b)import debt_tracker(\b)": r"\1from services import debt_tracker\2",
    r"(\b)from debt_tracker import(\b)": r"\1from services.debt_tracker import\2",
    r"(\b)import auto_reminder(\b)": r"\1from services import auto_reminder\2",
    r"(\b)from auto_reminder import(\b)": r"\1from services.auto_reminder import\2",
    r"(\b)import dashboard_api(\b)": r"\1from services import dashboard_api\2",
    r"(\b)from dashboard_api import(\b)": r"\1from services.dashboard_api import\2",
    r"(\b)import handler_dashboard(\b)": r"\1from handlers import handler_dashboard\2",
    r"(\b)from handler_dashboard import(\b)": r"\1from handlers.handler_dashboard import\2",
}


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, repl in MAPPINGS.items():
        new_content = re.sub(pattern, repl, new_content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {path}")


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if (
            ".venv" in dirpath
            or "node_modules" in dirpath
            or ".git" in dirpath
            or "__pycache__" in dirpath
        ):
            continue
        for filename in filenames:
            if filename.endswith(".py") and filename != "refactor_imports.py":
                file_path = os.path.join(dirpath, filename)
                process_file(file_path)


if __name__ == "__main__":
    main()
