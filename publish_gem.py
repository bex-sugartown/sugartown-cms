import requests
import base64
import sys
import html
from datetime import datetime
from content_store import all_gems
import config 

# --- CONFIGURATION ---
BASE_URL = config.BASE_URL
USER = config.USER
PASSWORD = config.PASSWORD

# --- AUTHENTICATION ---
credentials = f"{USER}:{PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# --- LOGGING ---
def log_change(action, title, gem_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{action.upper()}] {title} (ID: {gem_id})\n"
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

# --- FIND ID ---
def find_gem_id(gem):
    # 1. PRIMARY KEY CHECK (The Fix)
    # If the file has an ID, trust it implicitly.
    if 'id' in gem:
        return gem['id']

    # 2. FALLBACK: Title Search
    title = gem['title']
    search_url = f"{BASE_URL}?search={title}&status=any"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        for item in results:
            wp_title = item['title']['rendered']
            decoded_wp_title = html.unescape(wp_title)
            normalized_wp = decoded_wp_title.replace('“', '"').replace('”', '"').replace("’", "'")
            normalized_local = title.replace('“', '"').replace('”', '"').replace("’", "'")
            
            if normalized_wp == normalized_local:
                return item['id']
    return None

# --- MAIN LOOP ---
print(f"🚀 Processing {len(all_gems)} Gems from Content Store...")

for gem in all_gems:
    existing_id = find_gem_id(gem) # Pass the whole gem object now
    gem_id = existing_id
    action = ""
    target_status = gem.get('status', 'draft')

    if existing_id:
        print(f"🔄 Updating Gem {existing_id}: {gem['title']}...")
        gem['status'] = target_status 
        update_url = f"{BASE_URL}/{existing_id}"
        response = requests.post(update_url, headers=headers, json=gem)
        action = f"Updated ({target_status})"
    else:
        print(f"✨ Creating New Gem ({target_status}): {gem['title']}...")
        gem['status'] = target_status
        response = requests.post(BASE_URL, headers=headers, json=gem)
        action = f"Created ({target_status})"
        if response.status_code == 201:
            gem_id = response.json().get('id')

    if response.status_code in [200, 201]:
        print(f"   ✅ Success: {response.json()['link']}")
        log_change(action, gem['title'], gem_id)
    else:
        print(f"   ❌ ERROR: {response.status_code} - {response.text}")
        log_error(gem['title'], response.status_code, response.text)

print("✨ Done!")
