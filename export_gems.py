import csv
import requests
import json
import base64
from datetime import datetime
import config  # <--- SECURE IMPORT

# ==========================================
# CONFIGURATION
# ==========================================
# Pull from the secure config.py file
WP_URL = config.BASE_URL
WP_USER = config.USER
WP_PASS = config.PASSWORD

# Endpoints
# Check if your custom post type is 'gem' or 'gems' based on previous success
POSTS_ENDPOINT = f"{WP_URL}/wp-json/wp/v2/gems" 
CATS_ENDPOINT = f"{WP_URL}/wp-json/wp/v2/categories"
TAGS_ENDPOINT = f"{WP_URL}/wp-json/wp/v2/tags"

# Auth
creds = f"{WP_USER}:{WP_PASS}"
token = base64.b64encode(creds.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}'
}

# ==========================================
# HELPER: FETCH TAXONOMY MAPS
# ==========================================
def get_taxonomy_map(endpoint):
    """Returns a dictionary mapping ID -> Name (e.g. {14: 'Engineering'})"""
    print(f"🔄 Fetching taxonomy terms from {endpoint}...")
    mapping = {}
    page = 1
    while True:
        try:
            response = requests.get(f"{endpoint}?per_page=100&page={page}", headers=headers)
            if response.status_code != 200: break
            data = response.json()
            if not data: break
            
            for term in data:
                mapping[term['id']] = term['name']
            page += 1
        except Exception as e:
            print(f"   ⚠️ Error fetching taxonomy: {e}")
            break
            
    return mapping

# ==========================================
# MAIN EXPORT LOOP
# ==========================================
def main():
    print("------------------------------------------------")
    print("📊 SUGARTOWN GEM EXPORT v2.1 (Secure + Taxonomy)")
    print(f"   🎯 Target: {WP_URL}")
    print("------------------------------------------------")

    # 1. Build lookup maps
    cat_map = get_taxonomy_map(CATS_ENDPOINT)
    tag_map = get_taxonomy_map(TAGS_ENDPOINT)
    print(f"   ✅ Mapped {len(cat_map)} categories and {len(tag_map)} tags.\n")

    # 2. Fetch all Gems
    print("🚀 Fetching Gems from WordPress...")
    all_posts = []
    page = 1
    while True:
        url = f"{POSTS_ENDPOINT}?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            if page == 1:
                print(f"❌ Error connecting to API: {response.status_code}")
                print(f"   Check URL: {url}")
            break
            
        data = response.json()
        if not data: break
        
        all_posts.extend(data)
        page += 1

    print(f"   📦 Retrieved {len(all_posts)} total items.")

    # 3. Prepare CSV Data
    csv_rows = []
    for post in all_posts:
        cat_names = [cat_map.get(cid, str(cid)) for cid in post.get('categories', [])]
        tag_names = [tag_map.get(tid, str(tid)) for tid in post.get('tags', [])]

        # Handle cases where 'content' is protected or empty
        content_snippet = ""
        if 'content' in post and 'rendered' in post['content']:
             content_snippet = post['content']['rendered'][:100] + "..."

        row = {
            'id': post['id'],
            'title': post['title']['rendered'],
            'status': post['status'],
            'date': post['date'].split('T')[0],
            'categories': ", ".join(cat_names),
            'tags': ", ".join(tag_names),
            'slug': post['slug'],
            'link': post['link']
        }
        csv_rows.append(row)

    # 4. Write to File
    # Old:
    # filename = f"gems_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

    # New:
    import os
    os.makedirs('output/reports', exist_ok=True)
    filename = f"output/reports/gems_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

    keys = ['id', 'title', 'status', 'date', 'categories', 'tags', 'slug', 'link']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\n✨ Export Complete: {filename}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
