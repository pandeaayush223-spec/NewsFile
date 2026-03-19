import json
import os
from datetime import datetime
from logger import get_logger
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".env.development")
logger = get_logger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BACKUP_DIR = "backups"

def backup_table(client, table_name: str) -> list:
    logger.info(f"Backing up table: {table_name}")
    response = client.table(table_name).select("*").execute()
    return response.data

def run_backup() -> None:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{BACKUP_DIR}/newsfile_backup_{timestamp}.json"

    tables = ["articles"]  # add more table names here if you add them later
    backup_data = {}

    for table in tables:
        try:
            backup_data[table] = backup_table(client, table)
            logger.info(f"  → {len(backup_data[table])} rows from {table}")
        except Exception as e:
            logger.error(f"Failed to back up table {table}: {e}")

    with open(backup_filename, "w") as f:
        json.dump(backup_data, f, indent=2, default=str)

    logger.info(f"Backup saved to {backup_filename}")
    cleanup_old_backups()

def cleanup_old_backups(keep: int = 7) -> None:
    """Keep only the most recent N backups."""
    files = sorted([
        f for f in os.listdir(BACKUP_DIR) if f.startswith("newsfile_backup_")
    ])
    to_delete = files[:-keep]
    for f in to_delete:
        os.remove(os.path.join(BACKUP_DIR, f))
        logger.info(f"Deleted old backup: {f}")

if __name__ == "__main__":
    run_backup()