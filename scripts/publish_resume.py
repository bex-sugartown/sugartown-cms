#!/usr/bin/env python3
import markdown
import requests
import base64
import re
from pathlib import Path
import sys

# --- PATH SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# --- IMPORT CONFIG ---
try:
    import config
except ImportError:
    print("❌ ERROR: Could not find 'config.py'.")
    sys.exit(1)

# --- CONFIGURATION ---
PAGE_ID = 207  # https://sugartown.io/cv-resume/
WP_URL = f"{config.BASE_URL}/wp-json/wp/v2"

# ⚠️ UPDATE THIS: The link to your new Resume Gem
GEM_URL = "/architecture-update-the-resume-factory-v2-0" 

RESUME_FILE = BASE_DIR / "output" / "resumes" / "Resume_CMS-DS-PDM-01.md"

# --- REDACTION LIST ---
# These strings will be stripped from the public web version
SENSITIVE_DATA = [
    ("bex@sugartown.io", "[Email Available on Request]"), # Replace Email
    ("(510) 679-4580", ""), # Remove Phone entirely
]

def publish_to_wordpress():
    print(f"🚀 SUGARTOWN PUBLISHER: Targeting Page ID {PAGE_ID}")

    if not RESUME_FILE.exists():
        print(f"❌ ERROR: File not found: {RESUME_FILE}")
        return

    # 1. Read Markdown
    with open(RESUME_FILE, 'r') as f:
        md_text = f.read()

    # 2. REDACTION STEP (Security)
    print("🛡️  Redacting sensitive data for public web...")
    for secret, replacement in SENSITIVE_DATA:
        # Use simple string replacement
        md_text = md_text.replace(secret, replacement)
    
    # Clean up double pipes " | | " if phone removal left a gap
    # (Regex finds ' | ' followed optionally by whitespace and another pipe)
    md_text = re.sub(r'\|\s+\|\s+', '| ', md_text)
    # Clean up trailing pipes at end of lines
    md_text = re.sub(r'\|\s+$', '', md_text, flags=re.MULTILINE)

    # 3. Convert to HTML
    html_body = markdown.markdown(md_text, extensions=['extra'])

    # 4. Inject Blurb
    blurb_html = f"""
    <div class="wp-block-group has-background" style="background-color: #fff0f5; border-left: 4px solid #d63384; padding: 20px; margin-bottom: 40px; border-radius: 4px;">
        <p style="margin: 0; font-size: 0.9em; color: #555;">
            <strong>⚡️ Live Demo:</strong> This CV is dynamically generated from a Python/CSV pipeline. 
            <a href="{GEM_URL}" style="text-decoration: underline; color: #d63384;">Read the "Resume Factory v2.0" architecture case study.</a>
        </p>
    </div>
    """

    final_html = f"""
    <div class="resume-container">
        {blurb_html}
        {html_body}
    </div>
    """

    # 5. Auth & Send
    credentials = f"{config.USER}:{config.PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    endpoint = f"{WP_URL}/pages/{PAGE_ID}"
    print(f"📡 Pushing content to {endpoint}...")
    
    response = requests.post(endpoint, headers=headers, json={"content": final_html})

    if response.status_code == 200:
        print("✅ SUCCESS: Resume updated (Redacted for Privacy)!")
        print(f"   View live: {config.BASE_URL}/cv-resume/")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    publish_to_wordpress()