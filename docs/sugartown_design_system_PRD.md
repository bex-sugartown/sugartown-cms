# Product Requirements Document (PRD)
## Project 003: Sugartown Atomic Design System

| Metadata | Details |
| :--- | :--- |
| **Version** | **1.4 (The Canonical Card Release)** |
| **Status** | 🟢 **Active / Stable** |
| **Owner** | Engineering & DX (Repo B: `2025-sugartown-pink`) |
| **Related Gems** | [Gem 21: The Pre-Design System](/gem/design-ops-the-pre-design-system-surviving-the-css-chaos) |

Note: PRD versions are semantic and track document evolution.
Production releases follow calendar-based versioning (vYYYY.MM.DD).

---

## 1. Executive Summary

**The Sugartown Design System** is the visual operating system for the site.
**Phase 1 Goal:** Formalize the existing "hacked" CSS into reusable Tokens and Components.
**Strategic Pivot (v1.2):** We are moving from a "Dark Mode Default" to a **"Light Mode Default"**. The system now assumes a white background, using the "Deep Void" color only for high-impact accents (Footers, Code Blocks, Terminal Modes).
**v1.3 Update:** We have successfully decoupled the "Pink Card" component from WordPress internals. We now use a custom "Clean HTML" pattern that ignores `wp-block-group` styles, preventing layout overlap and ensuring stability.
**v1.4 Update:** The legacy Pink Card has been formally deprecated and replaced by the canonical `st-card` component. This release also aligns the design system with a locked, calendar-based release process and a changelog-driven governance model.

---

## 2. Current State: "The Alignment"

We are stabilizing the visual identity by removing the "Cascading Overwrites" that forced Dark Mode.

* **The Artifacts:** The Pink Card (now White-on-White), The Zebra Table, The Terminal Block.
* **The Pivot:** We no longer fight the browser's default white background. We embrace it.
* **The Fix:** We replaced `!important` wars with standard CSS specificity, relying on Borders and Shadows for contrast rather than background color.

---

## 3. Core Design Principles

1.  **Subtle Tech:** We use monospace fonts (`Menlo`, `Consolas`) for data, but distinct serifs (`Playfair Display`) for human narrative. It feels like a terminal that went to art school.
2.  **Duotone Reality:** Images are never raw. They are filtered to match the brand palette, using `hard-light` blend modes to sit correctly on white backgrounds.
3.  **Data Density:** We prefer dense, information-rich layouts (Tables, Lists) over "marketing fluff."
4.  **Light Mode Default:** The system assumes a clean, high-contrast light canvas. Dark Mode is an opt-in context (e.g., Code Blocks), not the page default.

---

## 4. Design Tokens (Canonical)

Design tokens are the single source of truth for visual consistency across Sugartown.
They must be referenced—not redefined—by components.

### 4.1 Colors (Corrected)

Replace the previous secondary brand color entry with the following:

| Token                   | Value     | Usage Description                                      |
|------------------------|-----------|--------------------------------------------------------|
| 'color.brand.primary'    | '#FE1295'   | **Sugartown Pink** (primary accent, links, emphasis)       |
| 'color.brand.secondary'  | '#2AD4A9'   | **Teal** accent (used in gradients and overlays)            |
| `color.bg.page` | `#ffffff` | **Paper White.** The default page background (New in v1.2). |
| `color.bg.void` | `#0D1226` | **Deep Void.** Now used strictly for **Footers** and **Code Blocks**. |
| `color.text.body` | `#1e1e1e` | **Charcoal.** Standard body text on white pages. |
| `color.text.inverse` | `#F8F8F2` | **Ghost White.** Text on Void accents (Buttons, Code). |

**Note:**  
Opacity is applied contextually (e.g. ~45% in gradients and duotone overlays).  
Do not encode opacity directly into token values.

---

### 4.2 Radius Rules (Locked)

Border radius values are standardized and must not be overridden ad-hoc.

| Context                 | Radius Value |
|-------------------------|--------------|
| Code, buttons, tags     | 4px (0.25rem)|
| .wp-block-code          | 8px          |
| Cards                   | 12px (0.75rem)|
| Hero / feature images   | 35px         |


Any deviation requires a documented exception in the PRD.


### 4.3 Elevation (The "Lift")
*Crucial for White-on-White contrast.*
* `elevation.card.rest`: `0 4px 12px rgba(254, 18, 149, 0.05)` (Subtle Pink Glow)
* `elevation.card.hover`: `0 12px 30px rgba(254, 18, 149, 0.15)` (The Lift)

### 4.4 Filters (The Light Mode Duotone)
* `filter.duotone.base`: `grayscale(100%) contrast(1.1)`
* `filter.duotone.overlay`: `linear-gradient(135deg, #FE1295, #2BD4AA)`
* `filter.blend.mode`: **`hard-light`** 

### 4.5 Typography Usage

Typography establishes hierarchy and semantic clarity.

- **Card Titles**
  - Font: Playfair Display
  - Weight: 700
  - Color: `#FE1295`
  - Decoration: underline with controlled thickness and offset

- **Card Subtitles**
  - Font: Fira Sans
  - Weight: 400
  - Color: neutral gray
  - Spacing intentionally reduced for compact hierarchy

- **Citations / Metadata**
  - Font: monospace
  - Color: muted gray
  - Links are non-underlined by default

Typography decisions must reinforce structure, not decoration.


---
## 5. Component Library 

### 5.1 Canonical Primitive: System Card (`.st-card`)

The `st-card` is the canonical **layout-stable card primitive** for Sugartown.

It does not replace existing components immediately.
It defines the **structural contract** that future components must follow.

**Design goals:**
- Semantic HTML
- Predictable layout behavior
- CMS-agnostic rendering
- Safe for AI-assisted generation and mutation

#### Required Structure

```html
<div class="st-card [variant]">
  <div class="st-card__bg"></div>

  <div class="st-card__inner">
    <header class="st-card__header">
      <p class="st-card__eyebrow"></p>
      <h2 class="st-card__title"></h2>
      <h3 class="st-card__subtitle"></h3>
    </header>

    <div class="st-card__content">
      <p></p>
    </div>

    <footer class="st-card__footer">
      <div class="st-card__citation"></div>
      <div class="st-card__tags"></div>
    </footer>
  </div>

  <div class="st-card__media"></div>
</div>
```

#### Behavioral Guarantees

- Header is pinned to the top
- Footer is pinned to the bottom
- Content flexes naturally between
- Media aligns center-bottom
- Layout does not depend on WordPress block classes
- No reliance on `!important` for stability

#### Variants

- `st-card` (default, light)
- `st-card--illustrative` (background imagery enabled)

Future variants (e.g. dark) must **extend this structure without mutation**.

### 5.2 Supported Component: Pink Card (`.pink-card`) [Stable]
The pink-card remains a supported, production-stable component.
It is visually opinionated and optimized for editorial density.
Internally, it is being gradually aligned to the st-card structural model where possible, without breaking existing layouts.

* **Structure:** Decoupled from WP. Must use the `.st-grid-wrapper` parent.
    * **Wrapper:** `<div class="st-grid-wrapper">` (Grid Context)
    * **Container:** `<div class="pink-card">` (Visual Boundary)
    * **Content:** `.pink-card__content` (Text/Tags) + `.pink-card__media` (Icon Strip)
* **Grid Logic:** Uses `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))` to prevent collapsing.
* **Box Model:** Enforces `box-sizing: border-box !important` to prevent padding from causing overlap.
* **Visual Layers:**
    1.  **Texture:** `.pink-card__bg` (z-0, opacity 0.15, grayscale).
    2.  **Canvas:** White background (z-1).
    3.  **Content:** Text and Media (z-2).

### 5.3 Supporting Components

#### 5.3.1 Callouts / Notes (`st-callout`, `st-note`)

Callout components must align with global design system rules:

- Use canonical radius tokens
- Respect color and typography tokens
- Avoid layout dependencies on CMS-specific wrappers

Callouts are supporting components and must not introduce new visual primitives.

#### 5.3.2 The Feature Image
* **Card Icons:** **Native SVGs.** No filters applied. Centered via `object-fit: contain` in a 48px strip.
* **Blog Headers:** **Duotone.** Applies `hard-light` blend mode (Pink/Teal) over grayscale images.

#### 5.3.3 The Tech Pill (`.skill-tag`)
* **Style:** Monospace font, `0.75rem` size.
* **Theme:** Light Grey background (`#f1f2f4`) with Deep Pink text (`#b91c68`).
* **Border:** 1px solid `#e1e3e6`.


### 5.4 WordPress Adaptation Layer (Non-Negotiable)

Sugartown components must render correctly inside WordPress block contexts.

Known behaviors accounted for:

- WordPress serializes `<!-- -->` comments into `<p>` elements
- Inline media may be wrapped in unexpected `<p>` or `<br>` tags
- Global block styles may leak into nested markup

Mitigations:
- Component layouts must not rely on block wrapper classes
- Media containers must defensively normalize child elements
- Grid systems must tolerate injected nodes without collapsing

These constraints are considered **part of the system**, not edge cases.

---

## 6. Implementation Plan
This plan reflects the current hybrid Python + CMS architecture already in production.

| Phase | Task | Status |
| :--- | :--- | :--- |
| **1. Cleanse** | Remove WP-specific class dependencies. | ✅ Done |
| **2. Grid Fix** | Implement `auto-fill` and `box-sizing` fixes. | ✅ Done |
| **3. Automation** | Create `layout_engine.py` for HTML generation. | ✅ Done |
| **4. Integration** | Update `publish_gem.py` to utilize layout engine. | 🟡 Ready |
---

## 7. Risks & Dependencies
* **Repo Separation:** Styles live in `2025-sugartown-pink`, but HTML structure lives in `sugartown-cms` (Python). Both must be synced for cards to render.

---
## Appendix A: Canonical Design Tokens & Style Rules

## Appendix B: Canonical Component Contracts

## Appendix C: Release Lint Rules (Enforced)

A release must not ship if:

- Canonical components are modified without PRD updates
- Component structure deviates from documented contracts
- Changelog entries do not follow calendar-based versioning
- Documentation reflects intent rather than shipped reality

This design system documents **what exists**, not what is planned.
