# Product Requirements Document (PRD)
## Project 003: Sugartown Atomic Design System

| Metadata | Details |
| :--- | :--- |
| **Version** | 1.1 (The "Pre-Design" Update) |
| **Status** | 🟡 **In Progress** (Migrating from CSS to Tokens) |
| **Owner** | Engineering & DX |
| **Related Gems** | [Gem 21: The Pre-Design System](/gem/design-ops-the-pre-design-system-surviving-the-css-chaos) |

---

## 1. Executive Summary

**The Sugartown Design System** is the visual operating system for the site. It is not just a UI kit; it is a strict governance model for how "Sugartown Pink" (`#FE1295`) and "Electric Cyan" (`#00E5FF`) interact with the "Deep Void" (`#0D1226`) background.

**Phase 1 Goal:** Formalize the existing "hacked" CSS (Pink Cards, Code Blocks, Duotone Images) into reusable Tokens and Components to eliminate `!important` wars in the stylesheet.

---

## 2. Current State: "The Pre-Design System"

We are currently in a transitional phase where the visual identity exists but is brittle.

* **The Artifacts:** We have strong distinct components (The Pink Card, The Zebra Table, The Terminal Block).
* **The Debt:** Styles are applied via a monolithic `style.css` that fights against the WordPress `theme.json`.
* **The Friction:** "Cascading Overwrites" are common. We frequently use `!important` to force Dark Mode styles over the default theme.

---

## 3. Core Design Principles 

1.  **Subtle Tech:** We use monospace fonts (`Menlo`, `Consolas`) for data, but distinct serifs (`Playfair Display`) for human narrative. It should feel like a terminal that went to art school.
2.  **Duotone Reality:** Images are never raw. They are always filtered to match the brand palette (Grayscale + Hard Light Gradient).
3.  **Data Density:** We prefer dense, information-rich layouts (Tables, Lists) over "marketing fluff."
4.  **Dark Mode First:** The system assumes a dark canvas. Light mode is the variant, not the default.

---

## 4. Atomic Tokens (The DNA)

These values must be extracted from `style.css` and formalized in `theme.json` or a `tokens.js` file.

### 4.1 Colors
| Token Name | Hex Value | Usage |
| :--- | :--- | :--- |
| `color.brand.primary` | `#FE1295` | **Sugartown Pink.** Borders, Links, Primary Buttons. |
| `color.brand.secondary` | `#00E5FF` | **Electric Cyan.** Accents, Toggles, Edge lighting. |
| `color.bg.void` | `#0D1226` | **Deep Void.** Main background for "Dark Mode" feel. |
| `color.text.body` | `#1e1e1e` | **Charcoal.** Body text on white cards. |
| `color.text.inverse` | `#F8F8F2` | **Ghost White.** Text on Void backgrounds. |

### 4.2 Elevation (Shadows)
* `elevation.card.rest`: `0 4px 12px rgba(254, 18, 149, 0.05)` (Subtle Pink Glow)
* `elevation.card.hover`: `0 12px 30px rgba(254, 18, 149, 0.15)` (The Lift)

### 4.3 Filters (The "Duotone" Effect)
* `filter.duotone.base`: `grayscale(100%) contrast(1.1)`
* `filter.duotone.overlay`: `linear-gradient(135deg, #FE1295, #2BD4AA)`
* `filter.blend.mode`: `hard-light`

---

## 5. Component Library (The Atoms)

### 5.1 The Pink Card (`.pink-card`)
The signature component for "Atoms & Ecosystems."
* **Structure:** Flex Column.
* **Behavior:** "Sticky Footer" logic (`margin-top: auto`) forces metadata to the bottom.
* **Variants:**
    * **Standard:** White background, Pink Border.
    * **Interactive:** Hover state triggers `translateY(-4px)`.

### 5.2 The Feature Image (`.wp-block-post-featured-image`)
Context-aware image presentation.
* **Archive View:** `aspect-ratio: 1/1` (Circle), `border-radius: 50%`.
* **Single Post:** `aspect-ratio: 21/9` (Cinematic Banner), `border-radius: 16px`.
* **Global:** Always applies `filter.duotone` overlay.

### 5.3 The Tech Pill (`.skill-tag`)
Used for displaying skills, tags, and versions.
* **Style:** Monospace font, `0.75rem` size.
* **Theme:** Light Grey background (`#f1f2f4`) with Deep Pink text (`#b91c68`).
* **Border:** 1px solid `#e1e3e6`.

---

## 6. Implementation Plan

| Phase | Task | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **1. Audit** | Inventory all hard-coded HEX values in `style.css`. | `token_map.csv` | 🟡 In Progress |
| **2. Tokenize** | Move HEX values to CSS Variables (`--color-brand-primary`). | Updated `style.css` | 🔴 To Do |
| **3. Blockify** | Convert `.pink-card` HTML into a native WordPress Block Pattern. | `patterns/pink-card.php` | 🔴 To Do |
| **4. Strict Mode** | Remove `!important` tags and rely on specific CSS selectors. | Clean Stylesheet | 🔴 To Do |

---

## 7. Risks & Dependencies
* **WordPress Overwrites:** Theme updates (`Twenty Twenty-Five`) may reset `theme.json`. **Mitigation:** Use a Child Theme.
* **Dark Mode Flash:** CSS loading delay causes a white flash before the "Void" background loads. **Mitigation:** Inline critical CSS.