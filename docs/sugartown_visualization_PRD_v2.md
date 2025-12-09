# Product Requirements Document (PRD)
## Sugartown Visualization Engine (Phase 2)

---

## 1. Overview

The **Visualization Engine** is a suite of Python scripts designed to transform the static data in the Content Store (Gems, Resume) into dynamic visual artifacts (Charts, Graphs, Timelines).

**Philosophy:** "Data Art as Code."
* **Source:** All visuals are generated from the "Golden Record" CSVs or JSONs.
* **Automation:** Visuals are regenerated on every build, ensuring they never drift from the underlying data.
* **Aesthetic:** Enforces the "Pink Stink" / "Subtle Tech" design language (Dark Mode, Monospace, Neon Accents).

---

## 2. Problem Statement

**The Friction:**
* **Stale Diagrams:** Manually updating a Roadmap graphic or Skills Cloud in Figma every time a date changes is unsustainable.
* **Invisible Data:** We have rich metadata (Tags, Categories, Dates) trapped in CSVs that visitors cannot see or explore.
* **Text Heavy:** The current site is text-dominant. We need "scannable" visual proof of the system's complexity.

---

## 3. Goals & Non-Goals

### 3.1 Goals

| Goal | Description |
| :--- | :--- |
| **Zero-Touch Updates** | Changing a date in `content_store.py` automatically updates the Roadmap visualization on the live site. |
| **Strict Styling** | All charts must inherit the "Pink Stink" palette (Pink/Cyan/Gold on Midnight) defined in the Design System. |
| **Idempotency** | Scripts must output to a stable filename (e.g., `roadmap_latest.html`) so WordPress links never break. |
| **Interactive SVG** | Prioritize SVG over PNG where possible to allow for hover states, crisp scaling, and text selection. |

### 3.2 Non-Goals

| Non-Goal | Description |
| :--- | :--- |
| **Real-Time Dashboards** | We are not building a Grafana/Tableau clone. These are static artifacts generated at build time. |
| **User Customization** | Visitors cannot toggle chart parameters (e.g., "Sort by Date"). The view is opinionated. |

---

## 4. User Stories

| Story ID | Title | User Story | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **VIZ-001** | **The Roadmap** | As a stakeholder, I want to see the project timeline. | Mermaid Gantt chart generated from `content_store.py` status tags. | **Done** |
| **VIZ-002** | **The Knowledge Graph** | As a visitor, I want to see how concepts connect. | Force-directed Network Graph (SVG) generated from Gem Tags/Categories. | **Done** |
| **VIZ-003** | **Skills Cloud** | As a recruiter, I want to see a weighted view of tech skills. | Word/Tag Cloud generated from `master_resume_data.json`, weighted by frequency. | **P0** |
| **VIZ-004** | **Experience Timeline** | As a recruiter, I want to visualize career progression. | Vertical or Horizontal Timeline generated from Resume "Start/End Dates". | **P1** |
| **VIZ-005** | **Category Distribution** | As the author, I want to audit my content balance. | Bar chart showing Gems per Category (Engineering vs. Strategy). | **P2** |

---

## 5. Technical Architecture

### 5.1 The Data Pipeline
1.  **Extract:** `export_gems.py` dumps WordPress data to `output/reports/gems_report_LATEST.csv`.
2.  **Transform:** Individual Viz Scripts read the latest CSV or JSON.
3.  **Load:** Scripts generate artifacts into `output/visuals/`.
4.  **Publish:** `publish_gem.py` pushes the HTML/SVG code into the relevant Gem.

### 5.2 The Script Library (`scripts/`)

| Script | Source Data | Output Type | Status |
| :--- | :--- | :--- | :--- |
| `viz_roadmap.py` | `content_store.py` (Hardcoded for now) | HTML (Mermaid) | ✅ Prod |
| `viz_smart_graph.py` | `gems_report_*.csv` | SVG (NetworkX) | ✅ Prod |
| `viz_skills.py` | `resume_data_complete.json` | SVG (WordCloud) | 🟡 To Do |
| `viz_timeline.py` | `resume_data_complete.json` | HTML/CSS | 🔴 Backlog |
| `viz_category_dist.py`| `gems_report_*.csv` | PNG (Matplotlib) | 🔴 Backlog |

---

## 6. Design Specs ("The Pink Stink")

All visualizations must adhere to the **Tier 2 Semantic Tokens** defined in the Design System PRD.

* **Background:** `#0D1226` (Deep Void)
* **Primary Data:** `#FE1295` (Sugartown Pink)
* **Secondary Data:** `#00E5FF` (Electric Cyan)
* **Tertiary Data:** `#FFD700` (Hard Gold)
* **Typography:** `Menlo`, `Consolas`, or `Fira Sans` (No generic serifs).

---

## 7. Success Criteria

| Area | Metric | Target |
| :--- | :--- | :--- |
| **Automation** | Manual steps to update a chart | **0** (Script run only) |
| **Legibility** | Text contrast ratio | **AA** (White on Midnight) |
| **Performance** | File size of generated SVGs | **< 100KB** |

---

## 8. Dependencies & Risks

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **WordPress Stripping Tags** | SVGs or Scripts break on render. | Use `<pre>` blocks or Custom HTML blocks; validated via `viz_roadmap.py`. |
| **Data Gaps** | Charts look empty. | `export_gems.py` must enforce "Required Fields" (Category/Tags). |
| **Mobile Layout** | Charts overflow screen. | CSS `max-width: 100%` and `overflow-x: auto` on all Viz containers. |