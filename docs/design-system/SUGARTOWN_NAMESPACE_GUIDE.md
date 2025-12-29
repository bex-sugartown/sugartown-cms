# Sugartown Design System Namespace Guide

## **Critical Rule: Always Use `st-` Prefix**

The Sugartown Pink design system uses the **`st-`** namespace for all classes and tokens.

### **Why Namespacing Matters:**

From the DS Ruleset (Section 1: Naming Conventions):
> **Namespacing Strategy:** Prefix all system classes to prevent collisions with application code.

- **Generic design systems** might use `.ds-*` 
- **Sugartown Pink** uses `.st-*`
- **Application-specific** would use `.app-*` or `.page-*`

---

## **Correct Sugartown Naming:**

### **CSS Classes:**
```css
✅ .st-card
✅ .st-button
✅ .st-metadata
✅ .st-content-constrained
✅ .st-github-content

❌ .ds-card        /* Generic, not Sugartown */
❌ .card           /* No namespace */
❌ .sugartown-card /* Too verbose */
```

### **CSS Custom Properties (Tokens):**
```css
✅ --st-color-brand-primary: #FF69B4;
✅ --st-spacing-4: 1rem;
✅ --st-font-heading-1: 1.875rem;

❌ --ds-color-brand-primary  /* Generic namespace */
❌ --color-pink              /* No namespace */
❌ --sugartown-color-pink    /* Too verbose */
```

---

## **Full Naming Convention:**

### **Components (BEM Structure):**
```css
/* Block */
.st-card { }

/* Element */
.st-card__header { }
.st-card__body { }
.st-card__footer { }

/* Modifier */
.st-card--featured { }
.st-card--compact { }
```

### **Tokens (Three-Tier System):**
```css
/* Tier 1: Primitives */
--st-color-pink-500: #FF69B4;
--st-spacing-4: 1rem;

/* Tier 2: Semantic */
--st-color-brand-primary: var(--st-color-pink-500);
--st-spacing-stack-md: var(--st-spacing-4);

/* Tier 3: Component */
--st-button-bg-primary: var(--st-color-brand-primary);
--st-button-padding-inline: var(--st-spacing-4);
```

### **Layout Primitives:**
```css
.st-layout-stack { }
.st-layout-cluster { }
.st-layout-grid { }
.st-layout-sidebar { }
```

### **Utility Classes:**
```css
.st-util-sr-only { }  /* Screen reader only */
.st-util-hidden { }   /* Visually hidden */
```

---

## **State Classes (Special Case):**

State classes use **`.is-*`** or **`.has-*`** prefixes without namespace:

```css
✅ .is-active
✅ .is-disabled
✅ .is-loading
✅ .has-error
✅ .has-icon

❌ .st-is-active  /* Don't namespace state classes */
```

**Why:** State classes are universal and apply across components.

---

## **For AI Assistants: Replacement Checklist**

When generating CSS or HTML for Sugartown:

1. **Find:** `\.ds-` → **Replace:** `.st-`
2. **Find:** `--ds-` → **Replace:** `--st-`
3. **Find:** `ds-` (in comments) → **Replace:** `st-` or `Sugartown`

**Exception:** Don't replace in documentation that discusses generic design system principles.

---

## **Example Conversions:**

### **Generic Design System → Sugartown:**

```css
/* ❌ Generic */
.ds-button {
  background: var(--ds-color-primary);
  padding: var(--ds-spacing-4);
}

/* ✅ Sugartown */
.st-button {
  background: var(--st-color-brand-primary);
  padding: var(--st-spacing-4);
}
```

### **HTML Classes:**

```html
<!-- ❌ Generic -->
<div class="ds-content-constrained ds-github-content">
  <dl class="ds-metadata">
    <dt>Version</dt><dd>v2025.12.29</dd>
  </dl>
</div>

<!-- ✅ Sugartown -->
<div class="st-content-constrained st-github-content">
  <dl class="st-metadata">
    <dt>Version</dt><dd>v2025.12.29</dd>
  </dl>
</div>
```

---

## **Python Script References:**

```python
# ✅ Correct
styled_html = f'''
<div class="st-content-constrained st-github-content">
  {html_content}
</div>
'''

# ❌ Wrong
styled_html = f'''
<div class="ds-content-constrained ds-github-content">
  {html_content}
</div>
'''
```

---

## **Project File Naming:**

```
✅ st-metadata-component.css
✅ required-sugartown-tokens.css
✅ st-card-variants.css

❌ ds-metadata-component.css
❌ required-design-tokens.css
❌ generic-card-variants.css
```

---

## **Documentation References:**

When writing docs, be specific:

```markdown
✅ "Add to the Sugartown design system..."
✅ "Use .st-metadata class..."
✅ "Set --st-color-brand-primary token..."

❌ "Add to the design system..."  (too vague)
❌ "Use .ds-metadata class..."    (wrong namespace)
```

---

## **Quick Reference Card:**

| Element | Namespace | Example |
|---------|-----------|---------|
| Component class | `.st-*` | `.st-card` |
| Element class | `.st-block__element` | `.st-card__header` |
| Modifier class | `.st-block--modifier` | `.st-card--featured` |
| Primitive token | `--st-primitive-*` | `--st-color-pink-500` |
| Semantic token | `--st-semantic-*` | `--st-color-brand-primary` |
| Component token | `--st-component-*` | `--st-button-bg-primary` |
| Layout primitive | `.st-layout-*` | `.st-layout-stack` |
| Utility class | `.st-util-*` | `.st-util-sr-only` |
| State class | `.is-*` or `.has-*` | `.is-active`, `.has-error` |

---

**Last Updated:** December 29, 2025  
**Status:** Canonical Reference  
**Applies To:** All Sugartown Pink design system code
