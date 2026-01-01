# Sugartown Release Notes

## v2026.01.01: Design System Alignment & Accessibility Audit

**Date:** 2026-01-01  
**Status:** 🟢 Production Stable  
**Scope:** Design System, Accessibility, Documentation

### 🎨 Design System

* Canonicalized `st-chip` as single interactive primitive across archive filters, hero navigation, and metadata tags
* Removed competing chip variant classes
* Normalized metadata card border colors and grid spacing
* Prevented global link underline styles from affecting chip components

### ⚙️ CMS / Architecture

* Fixed anchor links on AI Ethics page (publish_ethics_page.py)
* Removed duplicate H1 headings via CSS hide for WordPress auto-generated titles
* Enhanced metadata detection logic for semantic HTML structure

### 🧩 Layout & Stability Fixes

* Refactored CSS architecture: moved element styles from scoped wrappers to global base rules
* Fixed responsive table rendering to prevent column squish and overflow
* Tightened metadata grid spacing for visual consistency

### 📚 Documentation & Governance

* Completed accessibility audit with 16 documented issues and priority levels
* Created `CSS_FILE_ORGANIZATION_RULES.md` as platform-agnostic reference
* Standardized namespace across all CSS and documentation (ds- → st-)

---

## v2025.12.29: AI Governance + Design System Foundations
**Date:** 2025-12-29  
**Status:** 🟢 Production Stable  
**Scope:** Design System, Governance, Documentation

### 🎨 Design System
* Moved base HTML element styles to global scope
* Introduced semantic content utilities and layout components
* Standardized class and token namespaces to st-*
* Defined three-tier design token system with brand colors, spacing, and typography

### ⚙️ CMS / Architecture
* Updated AI Ethics page rendering and metadata structure
* Improved publisher metadata capture and semantic output

### 📘 Governance & Documentation
* Published AI Ethics & Operations policy
* Published design system ruleset and implementation guides
* Published AI prompt templates, deployment checklist, and reference documentation

---

## v2025.12.27: Taxonomy v4 + Interactive Filter System
**Date:** 2025-12-27
**Status:** 🟢 Production Stable
**Scope:** Archive, Taxonomy, Publisher, Design System

### 🎨 Design System
* Refactored archive filters to use st-chip interactive primitives
* Implemented floating multi-column dropdowns for Topic filtering
* Normalized mobile filter behavior (full-width overlay, single column)
* Created st-label primitive for consistent metadata typography
* Deprecated kg-filter-bar__label and uppercase filter labels
* Implemented st-chip-row utility for uniform chip layouts
* Converted Hero "Start Here" links to st-chip components
* Aligned filter bar and hero elements with 800px content container
* CSS Grid refactoring for st-card header: baseline-aligned eyebrow and badge positioning
* Archive footer layout: two-column design (action left, date right) in archive context
* Mobile footer: vertical stack with right-aligned date

### ⚙️ CMS / Architecture
* Taxonomy v4 migration complete: WordPress categories now single source of truth, eliminated gem_category meta field duplication
* Content store: converted 24/24 gems from plural categories to singular category format
* Publisher v4.1: dynamic category ID lookup replaces hardcoded mappings, auto-creates missing categories
* Archive query hygiene: unified WP_Query for rendering and counting, fixed pagination accuracy
* Removed gem_category from functions.php registration and archive template queries
* Deleted archive-gem-filter.js (server-side filtering only via WP_Query)

### 🧩 Layout & Stability Fixes
* Archive result counter: "Showing X-Y of Z gems" now reflects actual filtered results
* Removed duplicate gem count display from JavaScript filter
* Category subtitles now clickable for filtering by category
* Character encoding fixes throughout (em-dashes, bullets, checkmarks, emojis)

---

## v2025.12.24: Knowledge Graph Landing Page + Template Integration
**Date:** 2025-12-24  
**Status:** 🟢 Production Stable  
**Scope:** Knowledge Graph, Templates, Content Model

### ⚙️ CMS / Architecture
* Migrated Knowledge Graph from generic CPT archive (`/gem/`) to intentional section landing (`/knowledge-graph/`) with narrative context
* Extracted "The Scope Creep Origin Story" from hardcoded archive content into first-class Gem with proper meta fields (`gem_status`, `gem_action_item`, `gem_related_project`)
* Established content model rule: narrative content lives as Gems; archive templates render structure, not story
* Confirmed routing strategy: `/knowledge-graph/` shows landing + grid; `/knowledge-graph/?tag=X` shows filtered cards only

### 🧩 Layout & Stability Fixes
* Fixed WordPress Block Theme template integration: Site Editor template parts (Pink Header/Pink Footer) now properly render in PHP templates via `do_blocks()`
* Updated `header.php` and `footer.php` to render block template parts instead of hardcoded markup
* Resolved visual disconnect: gem archives now share header navigation, footer layout, and typography with rest of site
* Fixed landing content incorrectly rendering on filtered archive views (tag/project searches)
* Removed Gutenberg block comment artifacts from archive content

### 🎨 Design System
* Knowledge graph background SVG extended to 120% width with 40px card gaps for visibility in margins
* Increased background opacity to 65% for better visual presence
* Category subtitles in card headers now clickable for category filtering

---


## v2025.12.23: Taxonomy v4 — Archive Stability + Single Category Migration
**Date:** 2025-12-23  
**Status:** 🟢 Production Stable  
**Scope:** Archive, Taxonomy, Publisher, Content Model

### ⚙️ CMS / Architecture
* Completed Taxonomy v4 migration: eliminated duplicate category storage (gem_category meta), WordPress categories now single source of truth
* Publisher v4.1: dynamic category handling with runtime ID lookup, environment-agnostic deployment (no hardcoded IDs)
* Removed gem_category from functions.php registration and archive template queries
* Content store: migrated all 24 gems from plural `categories` to singular `category` format
* Archive query hygiene: unified WP_Query for rendering and counting, accurate pagination and result counts
* Removed client-side filtering JavaScript (archive-gem-filter.js), server-side only via WP_Query

### 🎨 Design System
* Archive card footer: two-column layout (action stacked left, date right-aligned) with proper baseline alignment
* Category subtitles now clickable—clicking filters archive by that category
* Fixed character encoding throughout (em-dashes, bullets, checkmarks, emojis)
* Dark card variant: automatic `.st-card--dark` class applied when gem has tags matching dark_trigger_slugs (system, meta, architecture, dx)

### 🧩 Layout & Stability Fixes
* Fixed archive result counter accuracy: "Showing X-Y of Z gems" now reflects actual displayed cards
* Proper pagination display: only shown when max_num_pages > 1
* Removed duplicate counter displays on filtered archives
* Mobile footer layout: stacks vertically but maintains date right-alignment for visual balance

---

## v2025.12.21: Canonical st-card adoption for Gem archive search
**Date:** 2025-12-21  
**Status:** 🟢 Production Stable  
**Scope:** Design System, Archive, Components

### 🎨 Design System
* Replaced archive-specific gem cards with canonical `st-card` component
* Standardized card anatomy, spacing, and hover behavior across archive views
* Unified tag, badge, and metadata presentation with system tokens
* New st-card--dark variant: Tag-driven behavior (system tag ⇒ dark card). Intent: signals system / infrastructure gems, not dark mode

### ⚙️ CMS / Architecture
* No content model or CMS logic changes
* Rendering aligned with existing design system primitives

### 🧩 Layout & Stability Fixes
* Standardized archive grid using shared `st-grid` / wrapper pattern
* Removed legacy grid overrides and conflicting layout rules
* Eliminated background and z-index collisions in archive cards

---

## v2025.12.19: st-card migration and design system alignment
**Date:** 2025-12-19  
**Status:** 🟢 Production Stable  
**Scope:** Design System, Components, Layout

### 🎨 Design System
* Migrated legacy `.pink-card` to canonical `.st-card` (light variant) with semantic header, content, and footer regions
* Standardized radius rules across UI elements (cards, tags, code blocks, hero imagery)
* Updated gradient recipe using canonical Sugartown hex values (`#FE1295`, `#2AD4A973`)
* Refined card typography (title, subtitle, citation) for clarity and hierarchy
* Unified tag/term base and hover styling across cards, posts, and tag clouds
* Updated `st-callout` / note component to align with current design system rules

### 🧩 Layout & Stability Fixes
* Fixed grid collapse caused by WordPress serializing HTML comments (`<!-- -->`) into paragraph nodes
* Corrected center-bottom media alignment for cards
* Resolved SVG sizing inconsistency affecting a single card instance
* Prevented WordPress block styles from leaking into card internals

---

## v2025.12.17: card layout and styling updates
**Date:** 2025-12-17  
**Status:** 🟢 Production Stable  
**Scope:** Design System, Layout

### 🎨 Design System
* Updated card visual styling to improve hierarchy and spacing
* Adjusted typography and color usage for consistency

### 🧩 Layout & Stability Fixes
* Fixed grid alignment issues affecting multi-column layouts
* Cleaned up legacy CSS causing layout inconsistencies

---