# 🧠 Sugartown "Second Brain" Pipeline

This repository contains the automation scripts for the Sugartown.io Headless CMS architecture. It decouples content creation (local Python/AI) from presentation (WordPress Knowledge Graph).

## 🛠 Tech Stack
* **Source:** Python 3 (Scripts) + Gemini 3 (Content Gen)
* **Destination:** WordPress (Sugartown.io) via REST API
* **Data Model:** Custom Post Type `gem` with Native Meta Fields

## ⚙️ Configuration
**Do not commit credentials to Git!**
Scripts rely on variables hardcoded in the `CONFIGURATION` block (or `.env` if upgraded):
* `URL`: `https://sugartown.io/wp-json/wp/v2/gems`
* `USER`: [Your WP Username]
* **Auth:** Uses WordPress Application Passwords (NOT login password).
    * *To generate new key:* WP Admin > Users > Profile > Application Passwords.

## 🚀 Scripts

### 1. `publish_gem.py`
**Purpose:** Publishes structured "Gems" (Knowledge Nodes) to the site.
* **Bulk Mode:** Edit the `all_gems` list inside the script to upload multiple nodes.
* **Single Mode:** (Legacy) Can be modified to accept CLI arguments.
* **Default Status:** `draft` (Safety first!).

**Usage:**
```bash
python3 publish_gem.py
