import requests
import base64
import csv
import sys
from datetime import datetime
import config # <--- IMPORT CONFIG

# --- CONFIGURATION (Loaded from config.py) ---
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

# --- FETCH ALL GEMS ---
def fetch_all_gems():
    all_gems = []
    page = 1
    
    print("🚀 Fetching Gems from WordPress...")
    
    while True:
        # Fetch 100 at a time to be safe
        response = requests.get(f"{BASE_URL}?per_page=100&page={page}&status=any", headers=headers)
        
        if response.status_code != 200:
            break
            
        data = response.json()
        if not data:
            break
            
        for post in data:
            # Extract Core Data
            gem = {
                'ID': post['id'],
                'Title': post['title']['rendered'],
                'Status': post['status'],
                'Date': post['date'].split('T')[0],
                'Link': post['link']
            }
            
            # Extract Meta Data (Handle missing fields gracefully)
            meta = post.get('meta', {})
            gem['Category'] = meta.get('gem_category', '')
            gem['Project'] = meta.get('gem_related_project', '')
            gem['Gem Status'] = meta.get('gem_status', '')
            gem['Action Item'] = meta.get('gem_action_item', '')
            
            all_gems.append(gem)
        
        print(f"   Batch {page} done ({len(data)} gems found)...")
        page += 1

    return all_gems

# --- SAVE TO CSV ---
def save_csv(gems):
    if not gems:
        print("❌ No gems found.")
        return

    filename = f"gems_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # Get headers from the first dictionary keys
    headers = gems[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(gems)
        
    print(f"\n✅ SUCCESS! Exported {len(gems)} gems to: {filename}")

# --- EXECUTE ---
gems_data = fetch_all_gems()
save_csv(gems_data)
