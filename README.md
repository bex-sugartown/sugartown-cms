# 🧠 Sugartown "Second Brain" Pipeline

This repository contains the automation scripts for the Sugartown.io Headless CMS architecture. It decouples content creation (local Python/AI) from presentation (WordPress Knowledge Graph).

## 🛠 Tech Stack
* **Source:** Python 3 (Scripts) + Gemini 3 (Content Gen)
* **Destination:** WordPress (Sugartown.io) via REST API
* **Data Model:** Custom Post Type `gem` with Native Meta Fields
* **Frontend:** Block Themes with Custom Templates (Headless Style)

## ⚙️ Configuration
**⚠️ IMPORTANT:** This repo ignores `config.py` to protect credentials.

1.  Create a file named `config.py` in the root folder.
2.  Add the following variables:
    BASE_URL = "https://sugartown.io/wp-json/wp/v2/gems"
    USER = "your_wp_username"
    PASSWORD = "xxxx xxxx xxxx xxxx" # WP Application Password

## 🚀 Scripts

### 1. `publish_gem.py` (The Engine)
**Purpose:** The main logic script. Reads content from the store and pushes it to WordPress.
* **Features:**
    * **Upsert Logic:** Checks if a Gem exists by title. Updates it if found; creates it if new.
    * **Logging:** Writes successes to `changelog.txt` and failures to `errorlog.txt`.
    * **Safety:** Imports content and config externally; contains no hardcoded secrets.

**Usage:**
python3 publish_gem.py

### 2. `content_store.py` (The Fuel)
**Purpose:** A pure Python list of dictionaries containing your Gem data.
* **Workflow:** Edit this file to add new Gems or update existing ones.
* **Status:** Set `status: 'draft'` for new ideas, `status: 'publish'` for live updates.

### 3. `export_gems.py` (The Audit)
**Purpose:** Pulls all data from WordPress and saves it as a CSV.
* **Use Case:** Periodic audits to check for data integrity issues (missing meta, orphans) that aren't visible in the WP Admin.

**Usage:**
python3 export_gems.py

### 4. `prep_resume.py`
**Purpose:** Standardizes resume file naming for recruiters vs. internal archives.
* **Input:** Google Doc exported as `MASTER_RESUME.pdf`.
* **Output:** `Becky-Head_Product-Leader_2026.pdf` (Clean SEO name).

## 🐛 Troubleshooting
* **Duplicate Posts?** The script matches by Title. If smart quotes (“) don't match straight quotes ("), it creates a duplicate. *Fix:* The script now uses `html.unescape` to handle this.
* **404 Error?** The Post Type `gem` isn't registered. Check WPCode snippet.
* **"Written by" on frontend?** CSS issue. Use the custom "Hide Meta" CSS in Customizer or the Custom Template.
* **Import Error?** Ensure `config.py` and `content_store.py` exist in the same folder.
