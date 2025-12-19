# Sugartown Release Notes

## v2025.12.19: st-card migration and design system alignment
**Date:** 2025-12-19  
**Status:** 🟢 Production Stable

### 🎨 Design System
* Migrated legacy `.pink-card` to canonical `.st-card` (light variant) with semantic header, content, and footer regions.
* Standardized radius rules across UI elements (cards, tags, code blocks, hero imagery).
* Updated gradient recipe using canonical Sugartown hex values (`#FE1295`, `#2AD4A973`).
* Refined card typography (title, subtitle, citation) for clarity and hierarchy.
* Unified tag/term base and hover styling across cards, posts, and tag clouds.
* Updated `st-callout` / note component to align with current design system rules.

### 🧩 Layout & Stability Fixes
* Fixed grid collapse caused by WordPress serializing HTML comments (`<!-- -->`) into paragraph nodes.
* Corrected center-bottom media alignment for cards.
* Resolved SVG sizing inconsistency affecting a single card instance.
* Prevented WordPress block styles from leaking into card internals.

---

## v2025.12.17: card layout and styling updates
**Date:** 2025-12-17  
**Status:** 🟢 Production Stable

### 🎨 Design System
* Updated card visual styling to improve hierarchy and spacing.
* Adjusted typography and color usage for consistency.

### 🧩 Layout & Stability Fixes
* Fixed grid alignment issues affecting multi-column layouts.
* Cleaned up legacy CSS causing layout inconsistencies.

---
