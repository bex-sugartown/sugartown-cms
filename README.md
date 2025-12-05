🚀 Workflows
1. Publishing Content (Gems)
The Python script is the "Bully." It enforces the state of content_store.py onto the WordPress database.

Open content_store.py.

Add a new dictionary entry to the all_gems list.

Set status: 'draft' to preview or 'publish' to go live.

Run the engine:

Bash

python3 publish_gem.py
Note: The script uses MD5 hashing to skip unchanged posts and "Fuzzy Matching" to prevent duplicates.

2. Building Resumes
We treat the Resume as a dataset, not a document.

Edit the Golden Record: data/json/master_resume_data.json.

Run the builder:

Bash

python3 build_resume.py
Find your formatted Markdown files in output/resumes/.

3. Auditing Taxonomy
To verify that tags and categories are syncing correctly between Local/Prod:

Run the exporter:

Bash

python3 export_gems.py
Check the CSV in output/reports/ to see exactly what is live.

🛠 Setup & Config
1. Dependencies

Bash

pip3 install requests
2. Authentication (config.py) Create a file named config.py in the root (it is ignored by Git).

Python

# UNCOMMENT ONE ENVIRONMENT
# BASE_URL = "http://localhost:10003"  # Local
BASE_URL = "[https://sugartown.io](https://sugartown.io)"    # Prod

USER = "your_username"
PASSWORD = "your_application_password" # Get this from WP Admin > Users > Profile
📜 Governance Rules
Code is King: Never manually edit a Gem's title, content, or tags in WordPress. The script will overwrite your changes on the next run.

Taxonomy flows Down: Create Categories/Tags in WordPress (or import XML) first. The script reads them to assign IDs.

One Repo, One Job: This repo owns Data. The 2025-sugartown-pink repo owns Theme/CSS. Do not mix them. """

with open('README.md', 'w') as f: f.write(readme_content)

print("README.md created successfully.")

```python?code_reference&code_event_index=6
readme_content = """# 💎 Sugartown Content Engine

**The Headless "Brain" for Sugartown.io**

This repository acts as the **Source of Truth** for the Sugartown digital ecosystem. It decouples content from presentation, managing the "Golden Records" for blog posts (Gems), career history (Resume), and portfolio data.

## 📂 Architecture

We follow a strict separation of concerns between **Data** (this repo) and **Code** (the Theme repo).

text sugartown_cms/ ├── content_store.py # THE DATABASE. All Gems & Metadata live here. ├── publish_gem.py # THE PUBLISHER. Syncs content_store -> WordPress API. ├── build_resume.py # THE FACTORY. Generates PDF-ready Markdown from JSON. ├── export_gems.py # THE AUDITOR. Exports WP database to CSV for analysis. ├── config.py # SECRETS. API keys and Auth (Not in Git). ├── data/ │ └── json/ # Source JSON for Resume & Structured Data. ├── output/ │ ├── resumes/ # Generated Resume artifacts. │ └── reports/ # CSV exports and logs. └── scripts/ # Helper utilities (Graph viz, ingestors).


---

## 🚀 Core Workflows

### 1. Publishing Content (Gems)
The Python script is the "Bully." It enforces the state of `content_store.py` onto the WordPress database.

1.  Open `content_store.py`.
2.  Add a new dictionary entry to the `all_gems` list.
3.  Set `status: 'draft'` to preview or `'publish'` to go live.
4.  Run the engine:
    ```bash
    python3 publish_gem.py
    ```
    * **Note:** The script uses MD5 hashing to skip unchanged posts and "Fuzzy Matching" to prevent duplicates.

### 2. Building Resumes
We treat the Resume as a dataset, not a document.

1.  Edit the Golden Record: `data/json/master_resume_data.json`.
2.  Run the builder:
    ```bash
    python3 build_resume.py
    ```
3.  Find your formatted Markdown files in `output/resumes/`.

### 3. Auditing Taxonomy
To verify that tags and categories are syncing correctly between Local/Prod:

1.  Run the exporter:
    ```bash
    python3 export_gems.py
    ```
2.  Check the CSV in `output/reports/` to see exactly what is live.

---

## 🛠 Setup & Config

**1. Dependencies**
```bash
pip3 install requests
2. Authentication (config.py) Create a file named config.py in the root (it is ignored by Git).

Python

# UNCOMMENT ONE ENVIRONMENT
# BASE_URL = "http://localhost:10003"  # Local
BASE_URL = "[https://sugartown.io](https://sugartown.io)"    # Prod

USER = "your_username"
PASSWORD = "your_application_password" # Get this from WP Admin > Users > Profile
📜 Governance Rules
Code is King: Never manually edit a Gem's title, content, or tags in WordPress. The script will overwrite your changes on the next run.

Taxonomy flows Down: Create Categories/Tags in WordPress (or import XML) first. The script reads them to assign IDs.

One Repo, One Job: This repo owns Data. The 2025-sugartown-pink repo owns Theme/CSS. Do not mix them. """

with open('README.md', 'w') as f: f.write(readme_content)

print("README.md file created.")

Here is the corrected, complete `README.md` file ready for download. This version cleans up the "munged" text and aligns perfectly with the new folder structure (`scripts/`, `data/`, etc.).

[README.md]

And here is the raw text block if you prefer to copy/paste:

```markdown
# 💎 Sugartown Content Engine

**The Headless "Brain" for Sugartown.io**

This repository acts as the **Source of Truth** for the Sugartown digital ecosystem. It decouples content from presentation, managing the "Golden Records" for blog posts (Gems), career history (Resume), and portfolio data.

## 📂 Architecture

We follow a strict separation of concerns between **Data** (this repo) and **Code** (the Theme repo).

```text
sugartown_cms/
├── content_store.py       # THE DATABASE. All Gems & Metadata live here.
├── publish_gem.py         # THE PUBLISHER. Syncs content_store -> WordPress API.
├── build_resume.py        # THE FACTORY. Generates PDF-ready Markdown from JSON.
├── export_gems.py         # THE AUDITOR. Exports WP database to CSV for analysis.
├── config.py              # SECRETS. API keys and Auth (Not in Git).
├── data/
│   └── json/              # Source JSON for Resume & Structured Data.
├── output/
│   ├── resumes/           # Generated Resume artifacts.
│   └── reports/           # CSV exports and logs.
└── scripts/               # Helper utilities (Graph viz, ingestors).
🚀 Workflows
1. Publishing Content (Gems)
The Python script is the "Bully." It enforces the state of content_store.py onto the WordPress database.

Open content_store.py.

Add a new dictionary entry to the all_gems list.

Set status: 'draft' to preview or 'publish' to go live.

Run the engine:

Bash

python3 publish_gem.py
Note: The script uses MD5 hashing to skip unchanged posts and "Fuzzy Matching" to prevent duplicates.

2. Building Resumes
We treat the Resume as a dataset, not a document.

Edit the Golden Record: data/json/master_resume_data.json.

Run the builder:

Bash

python3 build_resume.py
Find your formatted Markdown files in output/resumes/.

3. Auditing Taxonomy
To verify that tags and categories are syncing correctly between Local/Prod:

Run the exporter:

Bash

python3 export_gems.py
Check the CSV in output/reports/ to see exactly what is live.

🛠 Setup & Config
1. Dependencies

Bash

pip3 install requests
2. Authentication (config.py) Create a file named config.py in the root (it is ignored by Git).

Python

# UNCOMMENT ONE ENVIRONMENT
# BASE_URL = "http://localhost:10003"  # Local
BASE_URL = "[https://sugartown.io](https://sugartown.io)"    # Prod

USER = "your_username"
PASSWORD = "your_application_password" # Get this from WP Admin > Users > Profile
📜 Governance Rules
Code is King: Never manually edit a Gem's title, content, or tags in WordPress. The script will overwrite your changes on the next run.

Taxonomy flows Down: Create Categories/Tags in WordPress (or import XML) first. The script reads them to assign IDs.

One Repo, One Job: This repo owns Data. The 2025-sugartown-pink repo owns Theme/CSS. Do not mix them.
