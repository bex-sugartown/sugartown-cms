# CSS File Organization Rules

## Core Principle

CSS file organization is not housekeeping—it's **cascade contract definition**.

**Rule: Lower in file = Higher specificity weight**

Files should read **abstract → concrete** to prevent unintended cascade conflicts and maintain predictable override behavior.

---

## Standard Load Order

### 1. Design Tokens & CSS Variables

**Position:** Top of file  
**Purpose:** Global design system primitives

```css
:root {
  /* Color system */
  --color-brand-primary: #value;
  --color-text-primary: #value;
  
  /* Typography scale */
  --font-family-base: system-ui, sans-serif;
  --font-size-base: 1rem;
  
  /* Spacing, layout, motion */
  --spacing-unit: 8px;
  --border-radius: 4px;
}
```

**Rules:**
- Define once at top of file
- Never redefine tokens lower in cascade
- Treat as immutable constants

---

### 2. Semantic HTML Defaults (Canonicals)

**Position:** After tokens  
**Purpose:** Base styling for raw HTML elements

```css
body { }
h1, h2, h3, h4, h5, h6 { }
p, ul, ol { }
table, th, td { }
button, input, select { }
```

**Rules:**
- Use element selectors only
- Establish baseline appearance
- All components build on these foundations

---

### 3. Platform Integration Layer

**Position:** After canonicals  
**Purpose:** CMS/framework-specific adapter styles

```css
/* WordPress */
.wp-block-table table { }
.wp-element-button { }

/* Other frameworks */
.cms-specific-class { }
```

**Rules:**
- Keep platform coupling explicit and isolated
- Inherit from canonicals where possible
- Easy to remove during platform migration

---

### 4. Components

**Position:** After platform layer  
**Purpose:** Reusable, scoped UI patterns

```css
.component-name { }
.component-name__element { }
.component-name--modifier { }
```

**Rules:**
- Use class selectors only (no element selectors)
- Follow consistent naming methodology (BEM, SMACSS, etc.)
- Assume canonicals are already defined

---

### 5. Variants & State Classes

**Position:** After base components  
**Purpose:** Intentional component overrides

```css
.component--dark { }
.component--compact { }

.is-active { }
.is-disabled { }
.has-error { }
```

**Rules:**
- Must cascade after base components
- State classes use present-tense verbs (`is-`, `has-`)
- Variants use descriptive modifiers

---

### 6. Utilities & Overrides

**Position:** Bottom of file  
**Purpose:** Single-purpose, high-specificity helpers

```css
.u-sr-only { }
.u-text-center { }
.u-margin-0 { margin: 0 !important; }
```

**Rules:**
- May use `!important` when necessary
- Single responsibility per class
- Prefix with `u-` or similar namespace
- Use sparingly—overuse indicates design system gaps

---

## Critical Constraints

### Never Do This:
```css
/* ❌ BAD: Token redefinition later in file */
.component { }

:root {
  --new-token: value; /* CASCADE CONFLICT */
}
```

### Always Do This:
```css
/* ✅ GOOD: All tokens at top */
:root {
  --token-one: value;
  --token-two: value;
}

.component { }
```

---

## Multi-File Architecture

When splitting into multiple files, maintain import order:

```css
@import 'tokens.css';
@import 'canonicals.css';
@import 'platform-bridges.css';
@import 'components/*.css';
@import 'variants.css';
@import 'utilities.css';
```

---

## Mental Model

Think of CSS organization as **gravitational weight:**

1. **Tokens** = Laws of physics (universal constants)
2. **Canonicals** = Building codes (structural requirements)
3. **Components** = Architectural blueprints (designed systems)
4. **Variants** = Interior design (intentional customization)
5. **Utilities** = Emergency tools (break glass when needed)

The system works because **each layer trusts the layer above it** and **overrides the layer below it**.

---

# Addendum: Sugartown CMS Implementation

## Project-Specific Conventions

**Namespace:** `st-` prefix for all custom classes

**Brand Tokens:**
```css
:root {
  --st-color-brand-primary: #FF69B4; /* Sugartown Pink */
  --st-color-accent: #2BD4AA;        /* Seafoam */
}
```

**Component Naming:**
- BEM methodology required
- Examples: `.st-card`, `.st-card__header`, `.st-table--review`

**Platform Bridge:**
- WordPress Block Editor integration layer
- Aliases WordPress classes to canonical HTML behavior

**File Location:**
- Single consolidated file: `gem-archive-styles_v4_NEW_LAYOUT.css`
- Maintained in sugartown-pink theme repository

**Documentation Reference:**
- Design system classification: PROJ-003
- Follow calendar-based versioning (vYYYY.MM.DD)
- See `SUGARTOWN_DESIGN_SYSTEM_RULESET.md` for full specs
