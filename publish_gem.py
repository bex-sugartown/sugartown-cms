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

# --- LOGGING FUNCTIONS ---
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

# --- HELPER: GET FULL REMOTE DATA ---
def get_remote_gem(gem_id):
    # We use context=edit to get the RAW content (not rendered HTML) for comparison
    url = f"{BASE_URL}/{gem_id}?context=edit"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# --- HELPER: COMPARE LOCAL VS REMOTE ---
def has_changes(local, remote):
    # 1. Compare Title
    if local['title'] != remote['title']['raw']:
        return True
    
    # 2. Compare Content (Strip whitespace to avoid false positives)
    if local['content'].strip() != remote['content']['raw'].strip():
        return True
    
    # 3. Compare Metadata
    remote_meta = remote.get('meta', {})
    local_meta = local.get('meta', {})
    
    for key, value in local_meta.items():
        # If key missing in remote OR value is different
        if key not in remote_meta or remote_meta[key] != value:
            return True
            
    return False

# --- HELPER: FIND ID ---
def find_gem_id(title):
    search_url = f"{BASE_URL}?search={title}&status=any"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        for item in results:
            wp_title = item['title']['rendered']
            decoded_wp_title = html.unescape(wp_title)
            normalized_wp = decoded_wp_title.replace('“', '"').replace('”', '"')
            normalized_local = title.replace('“', '"').replace('”', '"')
            
            if normalized_wp == normalized_local:
                return item['id']
    return None

# --- THE SMART LOOP (DIFF CHECK) ---
print(f"🚀 Processing {len(all_gems)} Gems from Content Store...")

for gem in all_gems:
    existing_id = find_gem_id(gem['title'])
    
    if existing_id:
        # Step 1: Fetch the current live data
        remote_gem = get_remote_gem(existing_id)
        
        # Step 2: Check if anything actually changed
        if remote_gem and not has_changes(gem, remote_gem):
            print(f"⏩ Skipping (No Changes): {gem['title']}")
            continue # Skip to next gem, do NOT update or log

        # Step 3: If changed, proceed with Update
        print(f"🔄 Updating Existing Gem: {gem['title']} (ID: {existing_id})...")
        gem['status'] = 'publish' 
        update_url = f"{BASE_URL}/{existing_id}"
        response = requests.post(update_url, headers=headers, json=gem)
        action = "Updated"
        gem_id = existing_id

    else:
        # Step 4: If new, Create
        print(f"✨ Creating New Gem (Draft): {gem['title']}...")
        gem['status'] = 'draft'
        response = requests.post(BASE_URL, headers=headers, json=gem)
        action = "Created (Draft)"
        if response.status_code == 201:
            gem_id = response.json().get('id')

    # --- FINAL LOGGING ---
    if response.status_code in [200, 201]:
        print(f"   ✅ Success: {response.json()['link']}")
        log_change(action, gem['title'], gem_id)
    else:
        print(f"   ❌ ERROR: {response.status_code} - {response.text}")
        log_error(gem['title'], response.status_code, response.text)

print("✨ Done!")
