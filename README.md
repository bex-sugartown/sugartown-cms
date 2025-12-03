# 🧠 Sugartown "Second Brain" Pipeline

This repository contains the automation scripts for the Sugartown.io Headless CMS architecture. It decouples content creation (local Python/AI) from presentation (WordPress Knowledge Graph) and treats personal branding as a CI/CD pipeline.

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

---

## 🚀 Core Workflow Scripts

### 1. `publish_gem.py` (The Engine)
**Purpose:** The main logic script. Reads content from the store and pushes it to WordPress.
* **Safety First:** Automatically backs up `content_store.py` (Data) and `publish_gem.py` (Logic) to the `/backups` folder before execution.
* **Smart Updates (Diff Check):** Uses MD5 hashing to detect changes. If a Gem hasn't changed since the last run, it skips the API call (`💤 Skipped`), reducing API load and noise.
* **System Integrity:** Self-aware checks that log any modifications to the script itself.
* **Usage:** `python3 publish_gem.py`

### 2. `revert_changes.py` (The Panic Button)
**Purpose:** Disaster recovery. Restores the system to the "Last Known Good" state.
* **Menu System:** Prompts the user to fix the **Data** (Content Store) or the **Engine** (Publish Script).
* **Logic:** Overwrites the broken live file with the timestamped backup created by the engine.
* **Usage:** `python3 revert_changes.py`

### 3. `content_store.py` (The Source of Truth)
**Purpose:** A pure Python list of dictionaries containing your Gem data.
* **Workflow:** Edit this file to add new Gems or update existing ones.
* **Status:** Set `status: 'draft'` for new ideas, `status: 'publish'` for live updates.

---

## 💼 Resume Engineering Scripts

### 4. `prep_resume.py` (Standardization)
**Purpose:** Standardizes resume file naming for external recruiters vs. internal archives.
* **Input:** Google Doc exported as `MASTER_RESUME.pdf`.
* **Output:** `Becky-Head_Product-Leader_2026.pdf` (Clean SEO name).

### 5. `ingest_resume.py` (The ETL)
**Purpose:** Parses the PDF resume and extracts structured data.
* **Output:** Generates `resume_data.csv` for analysis or prompt engineering context.

---

## 📊 Audit & Reporting Scripts

### 6. `export_gems.py` (The Audit)
**Purpose:** Pulls all data from WordPress and saves it as a CSV.
* **Use Case:** Periodic audits to check for data integrity issues (missing meta, orphans) that aren't visible in the WP Admin.
* **Output:** `gems_report_YYYY-MM-DD.csv`.

---

## 📂 Logs & Artifacts
* **`changelog.txt`**: A chronological record of every successful API update (Draft/Publish) and System Code update.
* **`errorlog.txt`**: Captures API failures (400/500 errors) for debugging.
* **`.content_state.json`**: (Hidden) Stores MD5 hashes of content to enable smart diffing.
* **`/backups/`**: Directory containing `.last_good.py` snapshots.

## 🐛 Troubleshooting
* **Duplicate Posts?** The script matches by Title. If smart quotes (“) don't match straight quotes ("), it creates a duplicate. *Fix:* The script now uses `html.unescape` to handle this.
* **Script crashes?** Run `python3 revert_changes.py` to restore the previous working version.
* **"Skipped" messages?** This is normal. The script only updates Gems that have changed content.
* **404 Error?** The Post Type `gem` isn't registered. Check WPCode snippet.
