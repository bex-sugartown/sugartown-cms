
SUGARTOWN 2.0 — FULL PRD (MARKDOWN VERSION)


# Product Requirements Document (PRD)
## Sugartown 2.0 — Content Engine, Mini Design System, and WordPress Rendering Layer

---

## 1. Overview

Sugartown 2.0 is a hybrid headless publishing pipeline in which **Python is the single source of truth**.  
WordPress functions only as a **rendering layer** using a custom theme (`2025-sugartown-pink`) plus a minimal design system.

All content is authored and stored in `sugartown-cms`, including:
- Structured Gem objects
- Design tokens
- Visualization scripts
- Publishing pipeline logic

The front-end is fully reproducible, and the architecture supports migration to a future React/Next.js headless implementation.

---

## 2. Problem Statement

Traditional WP workflows create:
- Content drift
- Irreproducible state
- A second source of truth
- Barriers to automation and migration

Sugartown 2.0 solves this by enforcing:
- Python-only authorship  
- Stateless WordPress  
- Strict idempotent publishing  
- Token-driven UI consistency  

---

## 3. Goals & Non-Goals

### 3.1 Goals

| Goal | Description |
|------|-------------|
| Single Source of Truth | All content stored in Python, not WordPress. |
| Reproducibility | WP rebuildable from Python in one script run. |
| Structured Model | Gems defined with metadata, taxonomy, and relationships. |
| Idempotent Publishing | Hashing ensures efficient, safe updates. |
| Visualization Engine | Graph + category charts generated via Python. |
| Mini Design System | Portable tokens + components for WP and future React. |
| Repo Separation | `sugartown-cms` and `2025-sugartown-pink` independent. |

### 3.2 Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| WordPress editorial workflows | WP cannot store unique/manual content. |
| Protected Blocks | Conflicts with source-of-truth architecture. |
| Reverse-sync WP → Python | Non-reproducible and unnecessary. |
| Multi-author CMS | System is intentionally single-operator. |
| Full React front-end | A future-phase objective. |

---

## 4. User Stories

### 4.1 Frontend Visitor

- As a visitor, I need consistent Gem layouts so I can understand content structure.
- As a visitor, I need accurate taxonomy navigation.
- As a visitor, I need stable URLs for external linking.
- As a visitor, I need visualizations to understand content relationships.

### 4.2 Developer / PM (System Owner)

- As the system owner, I need Python to be the only canonical source so the system remains reproducible.
- As the operator, I need hashing and rollback to publish safely.
- As the maintainer, I need shared taxonomy across all CPTs.
- As the developer, I need separate theme and CMS repos.
- As the analyst, I need CSV exports and graph generation for insight.

---

## 5. Requirements

### 5.1 Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR0 | Canonical Content Rule | All content lives in `sugartown-cms`. WP stores no unique content. |
| FR1 | Gem CPT | Structured CPT with categories/tags + metadata fields. |
| FR2 | Publishing Pipeline | Python → WP API create/update logic. |
| FR3 | Idempotent Updates | MD5 hashing to skip unchanged posts. |
| FR4 | Backup + Rollback | Timestamped backups and restore script. |
| FR5 | Unified Taxonomy | Shared categories & tags across CPTs. |
| FR6 | Visualization Engine | PNG graph + bar chart generated from CSV. |
| FR7 | Two-Repo Architecture | Separate repos for content engine and theme. |
| FR8 | Design Tokens | Defined in JSON, exported to CSS + theme.json. |
| FR9 | Components | Token-driven styles for tables, code blocks, badges, cards. |

### 5.2 Removed Requirements

| Removed Requirement | Reason |
|---------------------|--------|
| WP Protected Blocks | Violates single source of truth. |

### 5.3 Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | Visualization scripts <5 sec; minimal API calls via hashing. |
| Reliability | Pipeline must avoid partial overwrites. |
| Observability | Logs for created/updated/skipped. |
| Portability | All design tokens portable to React. |
| Integrity | WP state reproducible from Python. |

---

## 6. Mini Design System

### 6.1 Token Architecture

Tokens stored in:
sugartown-cms/sugartown.tokens.json


| Category | Sample Tokens | Notes |
|----------|----------------|------|
| Colors | color.pink.500 | Sugartown brand palette |
| Typography | font.size.300 | theme.json mapping |
| Spacing | space.100 | layout consistency |
| Radius | radius.md | component rounding |
| Shadows | shadow.card | surface depth |
| Border | border.width.100 | tables, cards |

### 6.2 Token Distribution

- Figma Variables
- CSS Variables via :root
- WordPress theme.json
- Future React token module

### 6.3 Components

| Component | Implementation |
|----------|----------------|
| Headings | theme.json |
| Code Block | CSS override |
| Badge | CSS tokenized style |
| Table | Block style override |
| Card | Archive listing template |

### 6.4 Documentation

Located at:
sugartown-cms/docs/design-system/


---

## 7. Architecture & System Flow

### 7.1 Content Flow

1. `content_store.py` defines content.  
2. `publish_gem.py` transforms & pushes via API.  
3. WP receives structured posts.  
4. WP theme renders using tokens + templates.  

### 7.2 Visualization Flow

1. CSV export from Python  
2. networkx + matplotlib create graph + charts  
3. PNGs published to WP  
4. Gems display visuals automatically  

### 7.3 Repo Structure

| Repo | Purpose |
|------|---------|
| `sugartown-cms` | Content, tokens, scripts, visualizations |
| `2025-sugartown-pink` | Theme (templates, styles, block configs) |

---

## 8. Dependencies & Risks

### 8.1 Dependencies

- WordPress REST API
- Theme CPT registration
- Python environment (requests, networkx, pandas, matplotlib)

### 8.2 Risks

| Risk | Mitigation |
|------|------------|
| WP content drift | Enforce no manual editing |
| Theme breakage | Repo separation & version control |
| API failure | Rollback and backups |
| Migration blockers | Avoid WP-only content patterns |

---

## 9. Success Criteria

| Area | Metric |
|-------|--------|
| Reproducibility | Full WP rebuild from Python works |
| Performance | Hashing → >90% fewer updates |
| Stability | No manual WP content; rollback works |
| Consistency | Gems render uniformly with tokens |
| Future-proofing | Tokens map cleanly to React |

---

## 10. Backlog & Future Considerations

| Feature | Status | Notes |
|---------|--------|-------|
| WP Protected Blocks | Deferred | Conflicts with Python source-of-truth |
| React/Next.js Front End | Future | Tokens designed to support migration |
| CMS Replacement Evaluation | Future | Possible move to Sanity or Contentful |

