# Sugartown Design System - AI Quick Reference Card

**For:** AI assistants (Claude, ChatGPT, Gemini, Copilot)  
**Purpose:** Fast lookup during active coding sessions

---

## ⚡ Critical Rules (Check EVERY Response)

1. ✅ Always use `st-*` namespace (never `ds-*`)
2. ✅ Use tokens (`--st-*`), never hardcode values
3. ✅ Check for existing components BEFORE creating new CSS
4. ✅ Semantic naming (`.st-metadata` not `.page-metadata`)
5. ✅ Page CSS must be <10 lines

---

## 🔍 Decision Tree (Use Every Time)

```
User asks for styling
    ↓
1. Search style.css for existing `.st-*` component
    ├─ Found? → Use it
    └─ Not found? → Continue
    ↓
2. Could 2+ pages use this?
    ├─ YES → Add to design system
    └─ NO → Question if needed
    ↓
3. Still think it's page-specific?
    └─ Must be <10 lines + use tokens only
```

---

## 🚫 Red Flags (Stop and Reconsider)

- Creating `.page-*` or `.app-*` classes
- Hardcoded `#hex` colors or `px` values
- Page CSS >10 lines
- Scoping element styles: `.st-wrapper a { }`
- Missing BEM structure
- Skipping component search

---

## 📐 Namespace Quick Reference

| Type | Format | Example |
|------|--------|---------|
| Component | `.st-*` | `.st-card` |
| Element | `.st-block__element` | `.st-card__header` |
| Modifier | `.st-block--modifier` | `.st-card--featured` |
| Token (primitive) | `--st-primitive-value` | `--st-color-pink-500` |
| Token (semantic) | `--st-purpose-*` | `--st-color-brand-primary` |
| Token (component) | `--st-component-property` | `--st-button-bg-primary` |
| Layout | `.st-layout-*` | `.st-layout-stack` |
| State | `.is-*` or `.has-*` | `.is-active` |

**Note:** State classes (`.is-*`, `.has-*`) do NOT use `st-` prefix

---

## 🎨 Common Patterns (Copy-Paste Ready)

### **Metadata Block**
```html
<dl class="st-metadata">
  <dt>Version</dt><dd>v2025.12.29</dd>
  <dt>Status</dt><dd>Active</dd>
</dl>
```

### **Content Page**
```html
<div class="st-content-constrained st-prose">
  <dl class="st-metadata">...</dl>
  <h1>Page Title</h1>
  <p>Content...</p>
  <footer class="st-content-footer">...</footer>
</div>
```

### **Card Grid**
```html
<div class="st-layout-grid">
  <article class="st-card">
    <div class="st-card__header">
      <h3 class="st-card__title">Title</h3>
    </div>
    <div class="st-card__body">Content</div>
  </article>
</div>
```

### **Vertical Stack**
```html
<div class="st-layout-stack" style="--st-spacing-stack: var(--st-spacing-4)">
  <p>Item 1</p>
  <p>Item 2</p>
  <p>Item 3</p>
</div>
```

---

## 🎯 Response Template

When user asks for styling:

```markdown
## 1. Existing Components
[List any `.st-*` classes that apply]

## 2. Approach
[Either: "Compose from design system" OR "Add new component"]

## 3. Implementation
[Show HTML using `.st-*` classes]

## 4. CSS (if adding to DS)
[Component CSS with `--st-*` tokens]
```

---

## ✅ Self-Check Before Submitting

Run this checklist mentally:

1. [ ] Did I search for existing `.st-*` components?
2. [ ] Did I use tokens (`--st-*`) not hardcoded values?
3. [ ] Is naming semantic (what it is, not where it's used)?
4. [ ] Is page CSS <10 lines (or zero)?
5. [ ] Did I avoid scoping elements to wrapper classes?
6. [ ] Did I use proper BEM structure?
7. [ ] Are base HTML elements styled globally?

**If ANY are NO → Revise response**

---

## 🚨 Common Mistakes to Avoid

### ❌ Wrong
```css
/* Generic namespace */
.ds-button { }

/* Hardcoded values */
padding: 24px;
color: #FF69B4;

/* Page-specific wrapper */
.page-ethics .st-button { }

/* Scoped element styles */
.st-content a { color: blue; }
```

### ✅ Correct
```css
/* Sugartown namespace */
.st-button { }

/* Token-based */
padding: var(--st-spacing-6);
color: var(--st-color-brand-primary);

/* Component is standalone */
.st-button { }

/* Global element styles */
a { color: var(--st-color-link); }
```

---

## 📚 Where to Find More

- **Full Ruleset:** `SUGARTOWN_DESIGN_SYSTEM_RULESET.md`
- **Implementation Guide:** `DS_RULESET_IMPLEMENTATION_GUIDE.md`
- **Namespace Guide:** `SUGARTOWN_NAMESPACE_GUIDE.md`

---

## 💬 Good Prompts from Users

✅ "Style this using Sugartown components"  
✅ "Does a `.st-*` component exist for X?"  
✅ "Review against design system ruleset"  
✅ "What Sugartown tokens should I use?"

❌ "Make it pretty" (too vague)  
❌ "Add custom CSS" (violates 10-line rule)  
❌ "Create new component" (without checking existing)

---

**Print this. Pin it. Reference it every session.** 📌

**Last Updated:** December 29, 2025  
**Version:** v2025.12.29  
**Status:** Canonical Quick Reference
