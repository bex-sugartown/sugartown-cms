import requests
import base64

# --- CONFIGURATION ---
URL = "https://sugartown.io/wp-json/wp/v2/gems" # Confirmed Plural
USER = "bhead"
PASSWORD = "2vf9 WvM1 ygJa EkbM PMVk X92O" 

# --- AUTHENTICATION ---
credentials = f"{USER}:{PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# --- THE CONTENT PAYLOAD (With Builder.io Added) ---
html_content = """
<p>As we move into 2026, the Headless CMS market has calcified into three distinct segments: the Developer Tools, the Marketer Suites, and the Visual Composers. Here is the breakdown of the top players.</p>
<figure class="wp-block-table is-style-stripes"><table><thead><tr><th>Platform</th><th>Founded</th><th>Free Tier?</th><th>Paid Start</th></tr></thead><tbody>
<tr><td><strong>Contentful</strong></td><td>2013</td><td>✅ Yes</td><td>$300/mo</td></tr>
<tr><td><strong>Sanity</strong></td><td>2018</td><td>✅ Yes</td><td>$15/seat</td></tr>
<tr><td><strong>Strapi</strong></td><td>2016</td><td>✅ Yes (Self-Hosted)</td><td>$99/mo</td></tr>
<tr><td><strong>Storyblok</strong></td><td>2017</td><td>✅ Yes</td><td>$108/mo</td></tr>
<tr><td><strong>Ghost</strong></td><td>2013</td><td>✅ Yes (Self-Hosted)</td><td>$9/mo</td></tr>
<tr><td><strong>Directus</strong></td><td>2015</td><td>✅ Yes (Self-Hosted)</td><td>$15/mo</td></tr>
<tr><td><strong>Contentstack</strong></td><td>2018</td><td>⚠️ Limited</td><td>~$995/mo</td></tr>
<tr><td><strong>Prismic</strong></td><td>2013</td><td>✅ Yes</td><td>$7/mo</td></tr>
<tr><td><strong>Hygraph</strong></td><td>2017</td><td>✅ Yes</td><td>$299/mo</td></tr>
<tr><td><strong>ButterCMS</strong></td><td>2014</td><td>❌ No</td><td>$99/mo</td></tr>
<tr><td><strong>Builder.io</strong></td><td>2018</td><td>✅ Yes</td><td>$24/user</td></tr>
</tbody></table></figure>
<p><strong>The Product Manager's Take:</strong> If you need a "Visual Page Builder" that plugs into your existing stack, <strong>Builder.io</strong> is the category leader. If you need pure data modeling, stick to <strong>Sanity</strong> or <strong>Contentful</strong>.</p>
"""

gem_data = {
    'title': 'Market Scan: Top Headless CMS Platforms (2025)',
    'content': html_content,
    'status': 'publish' 
}

# --- SEND IT ---
print(f"🚀 Publishing Table to {URL}...")
response = requests.post(URL, headers=headers, json=gem_data)

if response.status_code == 201:
    print("✅ SUCCESS! Table published.")
    print(f"View it here: {response.json()['link']}")
else:
    print("❌ ERROR:")
    print(response.status_code)
    print(response.text)
