import requests
import json
import base64

# --- CONFIGURATION ---
BASE_URL = "https://sugartown.io/wp-json/wp/v2/gems"
USER = "bhead" # The username you use to login to WP
PASSWORD = "2vf9 WvM1 ygJa EkbM PMVk X92O" # The Application Password you just generated (NOT your login password)

# --- AUTHENTICATION ---
# We encode the username and password into a format the API understands
credentials = f"{USER}:{PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# --- HELPER FUNCTION: FIND ID ---
def find_gem_id(title):
    # Ask WP if a post with this text exists (search in drafts AND published)
    search_url = f"{BASE_URL}?search={title}&status=any"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        # Double check for exact match because search is fuzzy
        for item in results:
            if item['title']['rendered'] == title:
                return item['id']
    return None

# --- THE CONTENT PAYLOAD ---
all_gems = [
    # GEM: Defense of the Blog
    {
        'title': 'Confession: I Don\'t Hate Blogs, I Just Hate Unstructured Data',
        'status': 'draft', 
        'content': """
        <p>My AI architect recently pointed out a flaw in my new site strategy: <em>"Why are you so down on blogs?"</em></p>
        <p>It’s a fair question. I’ve spent the last week rigorously separating my "Field Notes" from my "Blog," treating the latter like a second-class citizen. But I want to clarify: I don't hate blogs. I hate <strong>Flat Content Models</strong>.</p>
        <h3>The Problem with "The Feed"</h3>
        <p>In a standard CMS, a Blog Post is designed to decay. It is sorted <strong>Chronologically</strong>. Its primary metadata is <em>Time</em>. This is great for news ("We raised Series A!"), but it is terrible for Knowledge ("How to configure Webpack").</p>
        <p>If I write a technical guide today, and you visit my site in 2027, you won't find it. It will be on Page 47 of the pagination abyss.</p>
        <h3>The Solution: The Node</h3>
        <p>By moving my technical insights into a <strong>Knowledge Graph</strong> (Custom Post Type), I am sorting them <strong>Topologically</strong> (by Topic and Relevance), not Chronologically.</p>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Feature</th><th>The Blog Post</th><th>The Knowledge Node</th></tr></thead>
        <tbody>
        <tr><td><strong>Primary Metric</strong></td><td>Recency (When?)</td><td>Relevance (What?)</td></tr>
        <tr><td><strong>Data Structure</strong></td><td>Blob (Title + Body)</td><td>Structured (Status, Project, Tech Stack)</td></tr>
        <tr><td><strong>Lifespan</strong></td><td>Decays over time</td><td>Evergreen (Updated via API)</td></tr>
        <tr><td><strong>User Intent</strong></td><td>"Entertain me."</td><td>"I need an answer."</td></tr>
        </tbody></table></figure>
        <h3>The Verdict</h3>
        <p>I still write blog posts. I use them for <strong>Narrative</strong>—stories about my career, culture, and opinion. But I use my Knowledge Graph for <strong>Assets</strong>—proof of my technical competence.</p>
        <p><strong>Recruiters:</strong> If you want to know who I <em>am</em>, read the Blog. If you want to know what I can <em>build</em>, search the Graph.</p>
        """,
        'meta': {'gem_category': 'Content Strategy', 'gem_status': 'Active', 'gem_action_item': 'Make peace with the blog', 'gem_related_project': 'Sugartown.io v2'}
    }
]

# --- THE SMART LOOP ---
print(f"🚀 Processing {len(all_gems)} Gems...")

for gem in all_gems:
    existing_id = find_gem_id(gem['title'])
    
    if existing_id:
        # --- UPDATE MODE ---
        print(f"🔄 Updating Existing Gem: {gem['title']} (ID: {existing_id})...")
        update_url = f"{BASE_URL}/{existing_id}"
        response = requests.post(update_url, headers=headers, json=gem)
    else:
        # --- CREATE MODE ---
        print(f"✨ Creating New Gem: {gem['title']}...")
        response = requests.post(BASE_URL, headers=headers, json=gem)

    if response.status_code in [200, 201]:
        print(f"   ✅ Success: {response.json()['link']}")
    else:
        print(f"   ❌ ERROR: {response.status_code} - {response.text}")

print("✨ Done!")
