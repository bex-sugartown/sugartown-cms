import csv
import requests
import json
import base64
from datetime import datetime
import os
import config

# ==========================================
# CONFIGURATION
# ==========================================
WP_URL = config.BASE_URL
WP_USER = config.USER
WP_PASS = config.PASSWORD

# Endpoints
POSTS_ENDPOINT = f"{WP_URL}/wp-json/wp/v2/gem" 
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
    print("📊 SUGARTOWN GEM EXPORT v3.0 (Full Meta)")
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
        # Include 'status=any' to ensure we capture Drafts too
        url = f"{POSTS_ENDPOINT}?per_page=100&page={page}&status=any"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            if page == 1:
                print(f"❌ Error connecting to API: {response.status_code}")
            break
            
        data = response.json()
        if not data: break
        
        all_posts.extend(data)
        page += 1

    print(f"   📦 Retrieved {len(all_posts)} total items.")

    # 3. Prepare CSV Data
    csv_rows = []
    for post in all_posts:
        # Map IDs to Names for human readability
        cat_names = [cat_map.get(cid, str(cid)) for cid in post.get('categories', [])]
        tag_names = [tag_map.get(tid, str(tid)) for tid in post.get('tags', [])]
        
        # Extract Meta Fields
        meta = post.get('meta', {})
        if not isinstance(meta, dict): meta = {} 

        row = {
            'id': post['id'],
            'title': post['title']['rendered'],
            'status': post['status'],
            'modified': post['modified'].split('T')[0], # Easy to read date
            
            # Taxonomy (WordPress)
            'wp_categories': ", ".join(cat_names),
            'wp_tags': ", ".join(tag_names),
            
            # Meta (Sugartown Internal)
            'project_id': meta.get('gem_related_project', ''),
            'internal_category': meta.get('gem_category', ''), # The "ProductOps" tag
            'gem_status': meta.get('gem_status', ''),
            'action_item': meta.get('gem_action_item', ''),
            
            # Links
            'slug': post['slug'],
            'link': post['link']
        }
        csv_rows.append(row)

    # 4. Write to File
    os.makedirs('output/reports', exist_ok=True)
    # Timestamped filename for version control
    filename = f"output/reports/gems_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # Define Column Order
    keys = [
        'id', 'title', 'status', 'project_id', 'internal_category', 
        'gem_status', 'action_item', 'modified', 
        'wp_categories', 'wp_tags', 'slug', 'link'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\n✨ Export Complete: {filename}")
    print("   💡 Review this CSV to ensure your Project IDs mapped correctly.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()