# Product Requirements Document (PRD)
## Sugartown Design System ("Sugartown Pink") v1.0

---

## 1. Overview

The **Sugartown Design System (SDS)**, internally referenced as **"Sugartown Pink,"** is the codified visual language of the Sugartown ecosystem. It is a **token-driven, platform-agnostic** design architecture that currently renders via a WordPress Block Theme (`2025-sugartown-pink`) but is structured to support a future migration to React/Next.js.

**Design Philosophy:** "Subtle Tech."
* **Aesthetic:** High-contrast, terminal-inspired, architectural.
* **Core Metaphor:** The "Digital Factory"—exposed pipes, raw data, and precision tooling.
* **Governance:** CSS Variables (`theme.json`) are the single source of truth for visual values.

---

## 2. Problem Statement

**The Friction:**
* **Inconsistent UI:** As we add new content types (Gems, Case Studies), manual styling leads to "drift" (e.g., 5 different shades of pink).
* **Hardcoded CSS:** The current `style.css` is becoming a monolith of `!important` overrides, making maintenance risky.
* **Portability Blockers:** Visual logic is trapped in WordPress PHP/HTML templates, making the future Headless React migration difficult.
* **Mobile Fragility:** Complex components (like the Mermaid Gantt chart) break on smaller screens without systemic handling.

---

## 3. Goals & Non-Goals

### 3.1 Goals

| Goal | Description |
| :--- | :--- |
| **Tokenization** | Extract all hardcoded hex codes and spacing units into semantic variables (e.g., `--color-primary-action` vs `#FF0055`). |
| **Component Portability** | Build UI units (Cards, Grids, Pills) that can be rendered in WP Blocks *or* React Components using the same tokens. |
| **"Terminal" Identity** | Enforce the specific "Dark Mode Code / Light Mode Text" aesthetic across all surfaces (Resume, Blog, Graph). |
| **Systemic Typography** | Establish a rigid type scale (Playfair Display for headers, Fira/Menlo for content) to prevent font bloat. |

### 3.2 Non-Goals

| Non-Goal | Description |
| :--- | :--- |
| **Figma Library** | We are "Code First." We will not maintain a pixel-perfect Figma mirror yet. The browser is the source of truth. |
| **User Theming** | We support System Light/Dark mode, but we do not offer user-selectable themes (e.g., "Blue Mode"). |

---

## 4. User Stories

| Story ID | Title | User Story | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **DS-001** | **Global Token Map** | As a developer, I need a single `theme.json` file for all colors/spacing. | CSS Variables generated for all primitives; 0 hardcoded hex values in `style.css`. | **P0** |
| **DS-002** | **The "Pink Card"** | As a user, I need a standard container for heterogeneous content. | Synced Pattern created; supports overrides; handles hover states & citations. | **P0** |
| **DS-003** | **Tech Typography** | As a reader, I want code to look like code and prose to look like prose. | `<code>` tags auto-style as "Pills"; `<pre>` blocks auto-style as "Terminals." | **P1** |
| **DS-004** | **Data Viz Styles** | As a reader, I want graphs to match the site aesthetic. | Mermaid.js config injected with Token values (Pink/Cyan/Dark). | **P1** |
| **DS-005** | **Dark Mode Switch** | As a user, I want the interface to respect my OS preference. | `@media (prefers-color-scheme: dark)` overrides defined for all components. | **P2** |

---

## 5. Technical Architecture

### 5.1 Token Taxonomy
We follow a 2-tier token system to ensure flexibility.

**Tier 1: Primitives (The Raw Values)**
* `color.pink.500` = `#FF0055`
* `color.cyan.400` = `#00E5FF`
* `font.mono` = `Menlo, Consolas, monospace`

**Tier 2: Semantics (The Usage)**
* `surface.primary` = `color.white` (Light) / `color.midnight` (Dark)
* `border.accent` = `color.pink.500`
* `text.code` = `color.pink.500`

### 5.2 Repository Structure
The Design System lives inside the **Theme Repo**, but distinct from the templates.

```text
2025-sugartown-pink/
├── theme.json            # THE DATABASE (Tokens)
├── style.css             # THE LOGIC (Global Classes)
├── assets/
│   ├── css/
│   │   ├── blocks/       # CSS per block (e.g., .wp-block-code.css)
│   │   └── components/   # CSS per component (e.g., .pink-card.css)
│   └── fonts/            # Local font files
└── patterns/             # Reusable HTML Layouts (Cards, Grids)
```

---

## 6. Component Library (Phase 1)

These are the "Lego Bricks" we have identified and partially built.

| Component | Status | Description | Technical Spec |
| :--- | :--- | :--- | :--- |
| **Pink Card** | 🟡 Beta | The universal container for content links. | Border: 1px Pink; Hover: Lift + Shadow; Footer: Citation. |
| **Terminal Block** | ✅ Done | Display container for code snippets. | Bg: `#1e1e1e`; Font: `Menlo`; Padding: `2.5rem`; Border-Left: Pink. |
| **Tech Pill** | ✅ Done | Inline code highlighter. | Bg: Light Grey; Text: Magenta; Border: 1px solid. |
| **Data Table** | ✅ Done | Structured data display. | Header: Pink; Rows: Zebra Stripe; Font: Condensed sans. |
| **Knowledge Graph** | 🟡 Beta | SVG Network Visualization. | Nodes: Gold/Cyan; Edges: White(10%); Physics: NetworkX. |

---

## 7. Success Criteria

| Area | Metric | Target |
| :--- | :--- | :--- |
| **Consistency** | Hardcoded Hex Values in CSS | **0** (All must use `var(--wp--...)`) |
| **Performance** | Lighthouse Accessibility Score | **100** (Contrast ratios on Pink/White) |
| **Maintainability** | Time to change "Pink" globally | < 5 minutes (One token update) |

---

## 8. Roadmap

* **Sprint 1:** Refactor `style.css` to remove `!important` hacks and implement Token Architecture.
* **Sprint 2:** Build "Pink Card" as a fully registered WordPress Pattern with Block Bindings.
* **Sprint 3:** Create `export_tokens.py` script to generate a JSON file for the future React app.