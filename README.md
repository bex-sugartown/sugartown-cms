# 💎 Sugartown Content Engine

**The Headless "Brain" for Sugartown.io**

This repository is the **Source of Truth** for the Sugartown digital ecosystem. It decouples content from presentation, managing "Golden Records" for blog posts (Gems), career history (Resume), and portfolio data.

---

## 📂 Architecture

We follow strict separation of concerns: **Data** (this repo) vs. **Code** (Theme repo).

```
sugartown-cms/
├── content_store.py       # THE DATABASE. All Gems & metadata
├── publish_gem.py         # THE PUBLISHER. Syncs to WordPress API
├── build_resume.py        # THE FACTORY. Generates resumes from JSON
├── export_gems.py         # THE AUDITOR. Exports WP → CSV
├── config.py              # SECRETS. API keys (not in Git)
├── data/
│   └── json/
│       └── master_resume_data.json  # Resume source of truth
├── output/
│   ├── resumes/           # Generated resume artifacts
│   └── reports/           # CSV exports and logs
├── scripts/               # Utilities (graph viz, helpers)
├── docs/                  # Project documentation
│   └── knowledge-graph-project/  # Knowledge Graph redesign plans
└── README.md              # This file
```

CHANGELOG.md is the canonical source of release history.
Changelog entries are imported automatically during publish; do not edit them manually.

---

## 🚀 Core Workflows

### 1. Publishing Content (Gems)

**Principle:** Python is the "Bully" — it enforces `content_store.py` state onto WordPress.

```bash
# 1. Edit content_store.py
# 2. Add new gem to all_gems list
# 3. Set status: 'draft' or 'publish'
# 4. Run publisher
python3 publish_gem.py
```

**How it works:**
- Uses MD5 hashing to skip unchanged posts
- Fuzzy matching prevents duplicates
- Never manually edit gems in WordPress — script will overwrite

---

### 2. Building Resumes

**Principle:** Resume is a dataset, not a document.

```bash
# 1. Edit golden record
vim data/json/master_resume_data.json

# 2. Generate resumes
python3 build_resume.py

# 3. Find output
ls output/resumes/
```

**See also:** [Resume Factory v3.0 PRD](docs/sugartown_resume_factory_PRD_v3.md)

---

### 3. Auditing Taxonomy

Verify tags/categories sync between Local ↔ Prod:

```bash
# Export WordPress state to CSV
python3 export_gems.py

# Check results
open output/reports/gems_report_$(date +%Y-%m-%d).csv
```

---

## 🛠 Setup & Configuration

### 1. Dependencies

```bash
pip3 install requests
```

### 2. Authentication

Create `config.py` in root (ignored by Git):

```python
# Local WordPress (via LocalWP)
# BASE_URL = "http://localhost:10003"

# Production (Pair hosting)
BASE_URL = "https://sugartown.io"

USER = "your_username"
PASSWORD = "your_application_password"  # From WP Admin > Users > Profile
```

---

## 🌍 Environment Details

### Local Development
- **WordPress:** LocalWP at `http://localhost:10003`
- **Theme:** `/Users/beckyalice/SUGARTOWN_DEV/wordpress/localwp/sugartown-local/app/public/wp-content/themes/sugartown-pink`
- **CMS Repo:** `/Users/beckyalice/Documents/01 PORTFOLIO/sugartown-cms`

### Production
- **Hosting:** Pair Networks (SSH + Filezilla)
- **Web Root:** `/usr/home/bhead/public_html/sugartown.io`
- **URL:** https://sugartown.io

### GitHub Repositories
- **CMS (this repo):** https://github.com/bex-sugartown/sugartown-cms
- **Theme:** https://github.com/bex-sugartown/2025-sugartown-pink

---

## 📜 Governance Rules

### 🔴 Code is King
**Never manually edit a Gem's title, content, or tags in WordPress.**  
The script will overwrite your changes on next run.

### 🔵 Taxonomy Flows Down
Create Categories/Tags in WordPress first (or import XML).  
The script reads them to assign IDs.

### 🟢 One Repo, One Job
- **This repo (sugartown-cms):** Owns DATA (content, structure)
- **Theme repo (2025-sugartown-pink):** Owns CODE (CSS, templates, PHP)
- **Do not mix concerns.**

---

## 🎯 Active Projects

### PROJ-001: Sugartown Headless CMS
**Status:** Active  
**Gems:** 21  
**Focus:** Content architecture, governance, Python automation

### PROJ-002: Resume Factory
**Status:** Active → Planning v3.0  
**Gems:** 5  
**Focus:** Resume variants, JSON → Markdown/PDF pipeline  
**Next:** Migration to Sanity CMS (see PRD in `docs/`)

### PROJ-003: Atomic Design System (Pink)
**Status:** Shipped  
**Gems:** 3  
**Focus:** Sugartown Pink™ design tokens, CSS architecture
**Next:** Design System framework in progress (see PRD in `docs/`)

### PROJ-004: Knowledge Graph Visualization
**Status:** 🟡 Phase 1 Complete, Visualization Pending  
**Gems:** 3  
**Focus:** Interactive graph of gems by project/category/tag  
**Shipped:** Landing page architecture, content model separation  
**Next:** Force-directed graph visualization (v4.3)  
**See:** `docs/knowledge-graph-project/`

---

## 📊 Knowledge Graph Project

**Goal:** Transform static gem cards into interactive, filterable knowledge graph.

**Planning Documents:**
- `docs/knowledge-graph-project/knowledge_graph_improvement_plan.md` — Master plan
- `docs/knowledge-graph-project/visualization_options_comparison.md` — Graph viz options

**Phase 1: Landing Page & Content Model (✅ Shipped v2025.12.24)**
1. ✅ Migrated from generic CPT archive (`/gem/`) to intentional section landing (`/knowledge-graph/`)
2. ✅ Established content model rule: narrative content lives as Gems, not templates
3. ✅ Routing: `/knowledge-graph/` shows landing + grid; `?tag=X` shows filtered cards
4. ✅ Fixed template integration (Block Theme parts render correctly in archive)

**Phase 2: Enhanced Filtering (Planned v4.3)**
1. ⏳ Clickable project/category/tag filters on cards
2. ⏳ Dynamic archive state updates without page reload
3. ⏳ Filter persistence via URL parameters

**Phase 3: Graph Visualization (Planned v4.3+)**
1. ⏳ Force-directed graph layout (D3.js or Python → SVG)
2. ⏳ Interactive node exploration
3. ⏳ Visual relationship mapping (project ↔ gems ↔ tags)

**Current Status:** Landing page architecture complete; visualization implementation deferred to v4.3

---

## 🔄 Deployment Workflow

### Local → Production

```bash
# 1. Test locally (LocalWP)
python3 publish_gem.py  # with BASE_URL = localhost

# 2. Switch to production
vim config.py  # Update BASE_URL to https://sugartown.io

# 3. Deploy to production
python3 publish_gem.py

# 4. Verify
python3 export_gems.py
open output/reports/gems_report_*.csv
```

### Theme Updates

```bash
# Theme changes go to separate repo
cd /path/to/2025-sugartown-pink

# Deploy via FTP/SSH to Pair hosting
# Or commit to GitHub and pull on server
```

---

## 📚 Documentation Index

### Core System Docs
- `README.md` — This file (overview, workflows, setup)
- `content_store.py` — Gem definitions (inline comments)
- `config.py.example` — Sample config (create your own)

### Project Plans (docs/)
- Resume Factory v3.0 PRD
- Knowledge Graph redesign plans
- Architecture decision records

### Reports (output/reports/)
- `gems_report_YYYY-MM-DD.csv` — WordPress state exports
- Taxonomy audits
- Content inventories

---

## 🐛 Troubleshooting

### "Script won't publish my gem"
- Check `status: 'publish'` in `content_store.py`
- Verify credentials in `config.py`
- Check WordPress user has "Author" role minimum

### "Tags/categories not syncing"
- Create taxonomy in WordPress first
- Run `export_gems.py` to see current state
- Script reads WP taxonomy IDs, doesn't create them

### "Local vs. Prod out of sync"
- Run `export_gems.py` on both environments
- Compare CSVs
- Identify drifts in `content_store.py`

### "Resume won't build"
- Check JSON syntax in `master_resume_data.json`
- Validate schema (all required fields present)
- Check Python traceback for specific error

---

## 🎨 Philosophy

### Topology Over Chronology
Gems are organized by **relationships** (projects, tags, themes), not by date.

### Structured Content Over Documents
Every piece of content is **data-first**: queryable, reusable, exportable.

### Source of Truth Over Sync
This repo is canonical. WordPress is a presentation layer.

---

## 🚧 Roadmap

### Near-term (Q1 2026)
- [ ] Complete Knowledge Graph visualization
- [ ] Add `display_order` field to gems (replace date-sort)
- [ ] Implement archive page filters (by project/category/tag)
- [ ] Add status badges to gem cards

### Mid-term (Q2 2026)
- [ ] Resume Factory v3.0 migration to Sanity
- [ ] Add `gem_status` visibility on homepage
- [ ] Implement graph-based navigation
- [ ] Create project landing pages

### Long-term (Q3+ 2026)
- [ ] Multi-format resume export (PDF, HTML, JSON)
- [ ] AI-powered content suggestions
- [ ] Collaborative editing workflows
- [ ] Portfolio case study integration

---

## 🤝 Contributing

This is a personal portfolio project, but if you're interested in the architecture or want to fork for your own use:

1. Fork the repo
2. Adapt `content_store.py` to your content model
3. Update `config.py` with your WordPress credentials
4. Customize resume JSON schema as needed

**Questions?** Open an issue or contact via [sugartown.io](https://sugartown.io)

---

## 📄 License

Proprietary — for portfolio demonstration purposes.  
Code architecture may be referenced with attribution.

---

## 🎓 Learn More

- **Live site:** https://sugartown.io
- **Knowledge Graph:** https://sugartown.io/gems/
- **Resume Factory:** https://sugartown.io/cv-resume/
- **GitHub (CMS):** https://github.com/bex-sugartown/sugartown-cms
- **GitHub (Theme):** https://github.com/bex-sugartown/2025-sugartown-pink

---

**Last Updated:** December 2025  
**Version:** 2.0 (Headless CMS Era)

---

## License

This project is source-available but not open source.

The code and assets are provided for reference and educational purposes only.

See the [LICENSE](./LICENSE) file for full terms.
# Git workflow configured
