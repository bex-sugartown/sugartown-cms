# Product Requirements Document (PRD)
## Project 003: Sugartown Atomic Design System

| Metadata | Details |
| :--- | :--- |
| **Version** | **1.3 (The "Light Mode" Pivot)** |
| **Status** | 🟡 **In Progress** (Standardizing White-on-White Contrast) |
| **Owner** | Engineering & DX (Repo B: `2025-sugartown-pink`) |
| **Related Gems** | [Gem 21: The Pre-Design System](/gem/design-ops-the-pre-design-system-surviving-the-css-chaos) |

---

## 1. Executive Summary

**The Sugartown Design System** is the visual operating system for the site.
**Phase 1 Goal:** Formalize the existing "hacked" CSS into reusable Tokens and Components.
**Strategic Pivot (v1.2):** We are moving from a "Dark Mode Default" to a **"Light Mode Default"**. The system now assumes a white background, using the "Deep Void" color only for high-impact accents (Footers, Code Blocks, Terminal Modes).
**v1.3 Update:** We have successfully decoupled the "Pink Card" component from WordPress internals. We now use a custom "Clean HTML" pattern that ignores `wp-block-group` styles, preventing layout overlap and ensuring stability.

---

## 2. Current State: "The Alignment"

We are stabilizing the visual identity by removing the "Cascading Overwrites" that forced Dark Mode.

* **The Artifacts:** The Pink Card (now White-on-White), The Zebra Table, The Terminal Block.
* **The Pivot:** We no longer fight the browser's default white background. We embrace it.
* **The Fix:** We replaced `!important` wars with standard CSS specificity, relying on Borders and Shadows for contrast rather than background color.

---

## 3. Core Design Principles

1.  **Subtle Tech:** We use monospace fonts (`Menlo`, `Consolas`) for data, but distinct serifs (`Playfair Display`) for human narrative. It feels like a terminal that went to art school.
2.  **Duotone Reality:** Images are never raw. They are filtered to match the brand palette, using `multiply` blend modes to sit correctly on white backgrounds.
3.  **Data Density:** We prefer dense, information-rich layouts (Tables, Lists) over "marketing fluff."
4.  **Light Mode Default:** The system assumes a clean, high-contrast light canvas. Dark Mode is an opt-in context (e.g., Code Blocks), not the page default.

---

## 4. Atomic Tokens (The DNA)

These values must be formalized in `theme.json` to overwrite the default `Twenty Twenty-Five` palette.

### 4.1 Colors
| Token Name | Hex Value | Usage |
| :--- | :--- | :--- |
| `color.brand.primary` | `#FE1295` | **Sugartown Pink.** Borders, Links, Primary Buttons. |
| `color.brand.secondary` | `#00E5FF` | **Electric Cyan.** Accents, Toggles, Edge lighting. |
| `color.bg.page` | `#ffffff` | **Paper White.** The default page background (New in v1.2). |
| `color.bg.void` | `#0D1226` | **Deep Void.** Now used strictly for **Footers** and **Code Blocks**. |
| `color.text.body` | `#1e1e1e` | **Charcoal.** Standard body text on white pages. |
| `color.text.inverse` | `#F8F8F2` | **Ghost White.** Text on Void accents (Buttons, Code). |

### 4.2 Elevation (The "Lift")
*Crucial for White-on-White contrast.*
* `elevation.card.rest`: `0 4px 12px rgba(254, 18, 149, 0.05)` (Subtle Pink Glow)
* `elevation.card.hover`: `0 12px 30px rgba(254, 18, 149, 0.15)` (The Lift)

### 4.3 Filters (The Light Mode Duotone)
* `filter.duotone.base`: `grayscale(100%) contrast(1.1)`
* `filter.duotone.overlay`: `linear-gradient(135deg, #FE1295, #2BD4AA)`
* `filter.blend.mode`: **`multiply`** (Updated from `hard-light` to prevent washout on white).

---
## 5. Component Library (The Atoms)

### 5.1 The Pink Card (`.pink-card`) [v3.3 Stable]
The signature component for "Atoms & Ecosystems."

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

### 5.2 The Feature Image
* **Card Icons:** **Native SVGs.** No filters applied. Centered via `object-fit: contain` in a 48px strip.
* **Blog Headers:** **Duotone.** Applies `multiply` blend mode (Pink/Teal) over grayscale images.

### 5.3 The Tech Pill (`.skill-tag`)
* **Style:** Monospace font, `0.75rem` size.
* **Theme:** Light Grey background (`#f1f2f4`) with Deep Pink text (`#b91c68`).
* **Border:** 1px solid `#e1e3e6`.

---

## 6. Implementation Plan
| Phase | Task | Status |
| :--- | :--- | :--- |
| **1. Cleanse** | Remove WP-specific class dependencies. | ✅ Done |
| **2. Grid Fix** | Implement `auto-fill` and `box-sizing` fixes. | ✅ Done |
| **3. Automation** | Create `layout_engine.py` for HTML generation. | ✅ Done |
| **4. Integration** | Update `publish_gem.py` to utilize layout engine. | 🟡 Ready |
---

## 7. Risks & Dependencies
* **Duotone Legibility:** Light mode overlays can look "muddy." **Mitigation:** Use `multiply` blend mode and high-contrast base images.
* **Repo Separation:** Styles live in `2025-sugartown-pink`, but HTML structure lives in `sugartown-cms` (Python). Both must be synced for cards to render.