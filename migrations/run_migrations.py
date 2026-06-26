import os
import sys
from database import db_client
from dotenv import load_dotenv

# Fix Unicode output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

def run_migrations():
    load_dotenv()
    supabase = db_client.get_supabase()
    
    try:
        # Check if master_satuan table exists
        response = supabase.table("master_satuan").select("id").limit(1).execute()
        print("✓ master_satuan table already exists!")
    except Exception as e:
        print("[WARNING] master_satuan table does not exist!")
        print("Please run the following SQL in Supabase SQL Editor:")
        print("-" * 50)
        sql_path = os.path.join(os.path.dirname(__file__), "001_create_master_satuan.sql")
        with open(sql_path, "r", encoding="utf-8") as f:
            print(f.read())
        print("-" * 50)

if __name__ == "__main__":
    run_migrations()
