import requests
import base64
import sys
import html
import shutil
import os
import hashlib
import json
from datetime import datetime
from content_store import all_gems
import config 

# --- CONFIGURATION ---
BASE_URL = config.BASE_URL
USER = config.USER
PASSWORD = config.PASSWORD
STATE_FILE = ".content_state.json" # Stores hashes of content to detect changes

# --- AUTHENTICATION ---
credentials = f"{USER}:{PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# --- HELPERS ---
def get_content_hash(gem_data):
    """Generates a fingerprint of the gem's title, content, and status."""
    # We combine key fields to create a unique ID for the content state
    unique_string = f"{gem_data['title']}{gem_data['content']}{gem_data.get('status', 'draft')}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

def load_content_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_content_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

# --- LOGGING ---
def log_change(action, title, gem_id, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format: [TIMESTAMP] [ACTION (STATUS)] Title (ID: X)
    entry = f"[{timestamp}] [{action.upper()} ({status.upper()})] {title} (ID: {gem_id})\n"
    try:
        with open("changelog.txt", "a") as f:
            f.write(entry)
    except Exception as e:
        print(f"   ⚠️ Warning: Could not write to changelog: {e}")

def log_error(title, status_code, error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [ERROR] {title} - Status: {status_code} - Message: {error_message}\n"
    try:
        with open("errorlog.txt", "a") as f:
            f.write(entry)
    except Exception as e:
        print(f"   ⚠️ Warning: Could not write to errorlog: {e}")

# --- BACKUP SYSTEM ---
def create_backup():
    # 🛠 UPDATED: Now backing up both the Data and the Engine
    files_to_backup = ["content_store.py", "publish_gem.py"]
    backup_dir = "backups"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for filename in files_to_backup:
        # Creates: content_store.last_good.py AND publish_gem.last_good.py
        destination = os.path.join(backup_dir, filename.replace(".py", ".last_good.py"))
        
        try:
            shutil.copy2(filename, destination)
            print(f"💾 Backup created: {destination}")
        except Exception as e:
            print(f"⚠️ Warning: Backup failed for {filename}: {e}")

# --- SYSTEM INTEGRITY CHECK ---
def check_code_changes():
    tracked_files = ["publish_gem.py", "content_store.py"]
    sys_state_file = ".system_state.json"
    
    if os.path.exists(sys_state_file):
        try:
            with open(sys_state_file, "r") as f:
                last_state = json.load(f)
        except:
            last_state = {}
    else:
        last_state = {}

    current_state = {}
    changes = []

    for filename in tracked_files:
        try:
            with open(filename, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                current_state[filename] = file_hash
                if last_state.get(filename) != file_hash:
                    changes.append(filename)
        except Exception as e:
            print(f"   ⚠️ Warning: Could not hash {filename}: {e}")

    if changes:
        pretty_list = ", ".join(changes)
        print(f"🛠  System Update Detected: {pretty_list}")
        log_change("CODE UPDATE", f"Modified files: {pretty_list}", "SYSTEM", "N/A")
        with open(sys_state_file, "w") as f:
            json.dump(current_state, f)

# --- FIND ID ---
def find_gem_id(gem):
    if 'id' in gem:
        return gem['id']
    
    # Fallback: Search by title
    title = gem['title']
    search_url = f"{BASE_URL}?search={title}&status=any"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        for item in results:
            # Normalize smart quotes for comparison
            wp_title = item['title']['rendered']
            decoded_wp_title = html.unescape(wp_title)
            normalized_wp = decoded_wp_title.replace('“', '"').replace('”', '"').replace("’", "'")
            normalized_local = title.replace('“', '"').replace('”', '"').replace("’", "'")
            
            if normalized_wp == normalized_local:
                return item['id']
    return None

# --- MAIN LOOP ---
create_backup()       # 1. Back up data + engine
check_code_changes()  # 2. Check if code changed
content_state = load_content_state() # 3. Load content fingerprints

print(f"🚀 Processing {len(all_gems)} Gems from Content Store...")

for gem in all_gems:
    existing_id = find_gem_id(gem)
    gem_id = existing_id
    current_hash = get_content_hash(gem)
    target_status = gem.get('status', 'draft')
    
    # Check if content has actually changed (Skip if identical)
    # We only skip if we have an ID AND the hash matches the last run
    if existing_id and content_state.get(str(existing_id)) == current_hash:
        print(f"   💤 Skipped (No Changes): {gem['title']}")
        continue

    # Logic for API Call
    if existing_id:
        print(f"   🔄 Updating [{target_status.upper()}]: {gem['title']}...")
        update_url = f"{BASE_URL}/{existing_id}"
        response = requests.post(update_url, headers=headers, json=gem)
        action = "Updated"
    else:
        print(f"   ✨ Creating [{target_status.upper()}]: {gem['title']}...")
        response = requests.post(BASE_URL, headers=headers, json=gem)
        action = "Created"
        if response.status_code == 201:
            gem_id = response.json().get('id')

    # Handle Response
    if response.status_code in [200, 201]:
        print(f"      ✅ Success: {response.json()['link']}")
        log_change(action, gem['title'], gem_id, target_status)
        
        # Update local state so we don't re-upload next time
        if gem_id:
            content_state[str(gem_id)] = current_hash
            save_content_state(content_state)
    else:
        print(f"      ❌ ERROR: {response.status_code} - {response.text}")
        log_error(gem['title'], response.status_code, response.text)

print("✨ Done!")
