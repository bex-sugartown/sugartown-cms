# Sugartown Release Notes

## v2025.12.21: Canonical st-card adoption for Gem archive search
**Date:** 2025-12-21  
**Status:** 🟢 Production Stable

### 🎨 Design System
* Replaced archive-specific gem cards with canonical `st-card` component
* Standardized card anatomy, spacing, and hover behavior across archive views
* Unified tag, badge, and metadata presentation with system tokens

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
