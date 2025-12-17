import content_store
import layout_engine  # <--- NEW: Import your layout engine
import requests
import json
import base64
import html
import hashlib
import os
import re
import config

# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = config.BASE_URL
USER = config.USER
PASSWORD = config.PASSWORD
STATE_FILE = ".content_state.json" 

API_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/gem" 
CATS_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/categories"
TAGS_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/tags"

# Auth
creds = f"{USER}:{PASSWORD}"
token = base64.b64encode(creds.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# ==========================================
# CACHE & FUZZY MATCHING
# ==========================================
CATEGORY_MAP = {}
TAG_MAP = {}
GEM_MAP = {} 

def simplify_key(text):
    """Strips all punctuation/spaces/html for robust matching."""
    if not text: return ""
    text = html.unescape(text).lower()
    return re.sub(r'[^a-z0-9]', '', text)

def build_cache(endpoint, target_map, label="items"):
    print(f"   🔄 Caching {label}...")
    page = 1
    while True:
        try:
            url = f"{endpoint}?per_page=100&page={page}&status=any"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200: break
            data = response.json()
            if not data: break
            
            for item in data:
                raw_name = item.get('name') or item.get('title', {}).get('rendered')
                if raw_name:
                    key = simplify_key(raw_name)
                    target_map[key] = item['id']
            page += 1
        except: break
        
    print(f"      ✅ OK: Found {len(target_map)} {label}.")

# ==========================================
# HELPERS
# ==========================================
def get_term_id(name, endpoint, target_map):
    key = simplify_key(name)
    if key in target_map: return target_map[key]
    
    print(f"      ✨ Creating missing term: '{name}'...")
    try:
        response = requests.post(endpoint, headers=headers, json={'name': name})
        if response.status_code == 201:
            new_id = response.json()['id']
            target_map[key] = new_id
            return new_id
    except: pass
    return None

def calculate_hash(gem_data):
    s = json.dumps(gem_data, sort_keys=True).encode('utf-8')
    return hashlib.md5(s).hexdigest()

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f: return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f: json.dump(state, f, indent=2)

# ==========================================
# MAIN LOOP
# ==========================================

def main():
    print("\n💎 SUGARTOWN PUBLISHER v3.8 (Layout Engine Ready)")
    print(f"🎯 Target: {BASE_URL}\n")

    state = load_state()
    
    gems = content_store.all_gems 

    # GOVERNANCE CHECK: Validate Project IDs
    print("🔍 Running Governance Check...")
    valid_projects = content_store.projects.keys()
    
    for gem in gems:
        proj_id = gem.get('meta', {}).get('gem_related_project')
        if proj_id and proj_id not in valid_projects:
             print(f"   ⚠️  WARNING: Gem '{gem['title']}' references invalid Project ID: '{proj_id}'")

    print("-" * 40)
    
    # 1. PRE-FETCH
    build_cache(CATS_ENDPOINT, CATEGORY_MAP, "Categories")
    build_cache(TAGS_ENDPOINT, TAG_MAP, "Tags")
    build_cache(API_ENDPOINT, GEM_MAP, "Existing Gems")
    print("-" * 40)

    gems = content_store.all_gems

    for gem in gems:
        # 1. RESOLVE ID
        my_key = simplify_key(gem['title'])
        target_id = GEM_MAP.get(my_key)
        
        if not target_id and 'id' in gem:
             if gem['id'] in GEM_MAP.values():
                 target_id = gem['id']

        # 2. PREPARE DATA
        cat_ids = []
        if 'categories' in gem:
            for c in gem['categories']:
                cid = get_term_id(c, CATS_ENDPOINT, CATEGORY_MAP)
                if cid: cat_ids.append(cid)

        tag_ids = []
        if 'tags' in gem:
            for t in gem['tags']:
                tid = get_term_id(t, TAGS_ENDPOINT, TAG_MAP)
                if tid: tag_ids.append(tid)

        # ==========================================
        # ✨ CONTENT PRE-PROCESSING (The Hook)
        # ==========================================
        final_content = gem.get('content', '')

        # Check if this Gem has a grid definition
        if 'card_grid_data' in gem:
            print(f"      🎨 Generating Grid Layout for '{gem['title']}'...")
            try:
                grid_html = layout_engine.generate_pink_card_grid(gem['card_grid_data'])
                # Append grid to the bottom of existing content
                final_content += f"\n{grid_html}"
            except Exception as e:
                print(f"      ❌ Layout Engine Error: {e}")

        # 3. BUILD PAYLOAD
        meta_data = gem.get('meta', {})
        
        payload = {
            'title': gem['title'],
            'content': final_content, # <--- Uses the processed content
            'status': gem['status'],
            'categories': cat_ids,
            'tags': tag_ids,
            'meta': {
                'gem_category': meta_data.get('gem_category', ''),
                'gem_status': meta_data.get('gem_status', ''),
                'gem_action_item': meta_data.get('gem_action_item', ''),
                'gem_related_project': meta_data.get('gem_related_project', '')
            }
        }

        # 4. SPEED CHECK
        current_hash = calculate_hash(payload)
        if target_id and str(target_id) in state and state[str(target_id)] == current_hash:
            print(f"💤 Skipped: {gem['title']}")
            continue

        # 5. PUSH
        print(f"Processing: {gem['title']}...")
        
        if target_id:
            url = f"{API_ENDPOINT}/{target_id}"
            response = requests.post(url, headers=headers, json=payload)
            action = "Updated"
            icon = "🔹"
        else:
            response = requests.post(API_ENDPOINT, headers=headers, json=payload)
            action = "Created"
            icon = "✨"

        if response.status_code in [200, 201]:
            real_id = response.json()['id']
            print(f"   {icon} {action} (ID: {real_id})")
            
            state[str(real_id)] = current_hash
            GEM_MAP[my_key] = real_id
            save_state(state)
        else:
            print(f"   ❌ {action} Failed: {response.status_code}")
            print(f"      {response.text[:200]}")

if __name__ == "__main__":
    main()