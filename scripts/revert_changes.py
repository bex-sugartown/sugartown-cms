import shutil
import os
import time
from datetime import datetime

# --- CONFIGURATION ---
BACKUP_DIR = "backups"
LOG_FILE = "changelog.txt"

# Map the live file to its backup counterpart
FILES = {
    "1": {"live": "content_store.py", "backup": "content_store.last_good.py", "name": "Content Store (Data)"},
    "2": {"live": "publish_gem.py", "backup": "publish_gem.last_good.py", "name": "Publish Script (Engine)"}
}

def log_revert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [ROLLBACK] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

def main():
    print("🛑 INITIATING ROLLBACK PROTOCOL...")
    print("Which component is broken?")
    
    for key, info in FILES.items():
        print(f"   [{key}] {info['name']}")
    
    choice = input("Select option (1/2): ")
    
    if choice not in FILES:
        print("🚫 Invalid selection.")
        return

    target = FILES[choice]
    live_file = target["live"]
    backup_path = os.path.join(BACKUP_DIR, target["backup"])

    # 1. Check if backup exists
    if not os.path.exists(backup_path):
        print(f"❌ Error: No backup found at {backup_path}")
        return

    # 2. Check timestamp
    backup_time = os.path.getmtime(backup_path)
    human_time = time.ctime(backup_time)
    
    print(f"\nℹ️  Found backup from: {human_time}")
    confirm = input(f"❓ Overwrite {live_file} with this backup? (y/n): ")

    if confirm.lower() != 'y':
        print("🚫 Rollback aborted.")
        return

    # 3. Perform Restore
    try:
        shutil.copy2(backup_path, live_file)
        print(f"✅ Success: {live_file} restored.")
        log_revert(f"Restored {live_file} from backup ({human_time})")
    except Exception as e:
        print(f"❌ Critical Failure: {e}")

if __name__ == "__main__":
    main()
