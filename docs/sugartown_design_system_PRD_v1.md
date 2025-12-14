# Product Requirements Document (PRD)
## Project 003: Sugartown Atomic Design System

| Metadata | Details |
| :--- | :--- |
| **Version** | 1.2 (Semantic Convergence Update) |
| **Status** | 🟡 In Progress |
| **Owner** | Engineering & DX |
| **Related Gems** | Gem: The Pre-Design System · Gem: Resume Factory · Gem: Knowledge Graph |

---

## 1. Executive Summary

The **Sugartown Atomic Design System** is a governed, semantic UI system designed to support a composable, content-as-code portfolio.

It is not a visual kit.  
It is an **agreement** between humans, AI agents, and code about how structure, meaning, and presentation relate.

This update formalizes:
- Semantic component naming
- Centralized styling in `style.css`
- Shared layout primitives (Cards, Grids, Callouts)
- Variants instead of forks (Light, Dark, KG)

---

## 2. Current State: The Pre-Design System

Sugartown currently operates with:
- Strong visual identity
- Multiple valid but divergent implementations
- CSS that “works” but does not scale

### 2.1 The Multi-Agent Drift Problem

Multiple AI agents (and humans) have independently implemented similar UI components:
- Pink Cards
- Gem Archive Cards
- Filter Notices
- Editorial Callouts

These implementations are visually aligned but **semantically disconnected**.

**Risk:**  
Visual consistency without semantic consistency creates CSS debt and blocks safe theming.

**Opportunity:**  
Introduce a semantic component layer that reconciles existing implementations without breaking markup.

---

## 3. Core Design Principles

1. **Subtle Tech**  
   Editorial typography for narrative, monospace for data.

2. **Duotone Reality**  
   Images are always filtered to match the system palette.

3. **Data Density**  
   Information-rich layouts over marketing abstraction.

4. **Light Mode First**  
   The system assumes a light canvas as the baseline.  
   Dark Mode and Knowledge Graph views are variants, not defaults.

5. **Semantic First**  
   Components must have durable semantic identities, not just visual styles.

6. **Variants, Not Forks**  
   Light Mode, Dark Mode, and Knowledge Graph are variants of the same components.

---

## 4. Atomic Tokens (The DNA)

### 4.1 Color Tokens

| Token | Value | Usage |
|-----|------|------|
| color.brand.primary | #FE1295 | Sugartown Pink |
| color.brand.secondary | #00E5FF | Electric Cyan |
| color.bg.surface | #FFFFFF | Primary surface (Light Mode) |
| color.bg.void | #0D1226 | Dark / KG surfaces |
| color.text.body | #1e1e1e | Body text on light |
| color.text.inverse | #F8F8F2 | Text on dark |

### 4.2 Elevation Tokens

- elevation.card.rest: 0 4px 12px rgba(254,18,149,0.05)
- elevation.card.hover: 0 12px 30px rgba(254,18,149,0.15)

### 4.3 Layout Tokens

| Token | Value | Usage |
|-----|------|------|
| layout.card.radius | 8px | All cards |
| layout.card.padding.sm | 20px | Dense views |
| layout.card.padding.lg | 32px | Editorial views |
| layout.grid.min | 340px | Card grids |
| layout.grid.gap | 30px | Grid spacing |

---

## 5. Component Library

### 5.1 Card System (`.st-card`)

The **Card System** is the foundational organism across the site.

**Base Class:** `.st-card`  
**Elements:**
- `.st-card__header`
- `.st-card__body`
- `.st-card__meta`
- `.st-card__footer`

**Variants:**
- `.st-card--light` (default)
- `.st-card--dark`
- `.st-card--kg-dark`

**Behavioral Guarantees:**
- Flex column layout
- Sticky footer behavior
- Grid alignment regardless of content length

**Legacy Compatibility:**
- `.pink-card` and `.gem-card` remain valid aliases
- No breaking template changes permitted during convergence

---

### 5.2 Callout System (`.st-callout`)

Used for:
- Filter notices
- Editorial asides
- System annotations

**Base Class:** `.st-callout`  
**Variants:**
- `.st-callout--info`
- `.st-callout--soft`
- `.st-callout--dark`
- `.st-callout--kg-dark`

Legacy classes (e.g. `.filter-active-notice`) map to this system.

---

### 5.3 Tag / Pill System (`.st-tag`)

Used for:
- Skills
- Tags
- Metadata

**Rules:**
- Single semantic pill component
- Variants via modifiers only
- No page-specific tag styling

---

## 6. Implementation Plan

| Phase | Task | Deliverable | Status |
|----|----|----|----|
| 1 | Identify duplicate components | Component Drift Map | 🟡 |
| 2 | Introduce `.st-*` semantic layer | Centralized style.css | 🟡 |
| 3 | Migrate archive styles | Single stylesheet | 🟡 |
| 4 | Define Dark/KG variants | Token + Variant spec | 🔴 |
| 5 | Template cleanup | Non-breaking PRs | 🔴 |

---

## 7. Risks & Mitigations

**AI Drift Risk:**  
Future AI output may reintroduce divergent components.

**Mitigation:**  
Enforce `.st-*` vocabulary in prompts, reviews, and documentation.

---

## 8. Success Criteria

- One card system
- One callout system
- One grid system
- Zero visual regressions
- Dark Mode implemented via modifiers only
