============================================
SUGARTOWN 2.0 — JIRA EPIC + STORIES (MARKDOWN)
============================================

# EPIC: SUG-200 — Sugartown 2.0 Content Engine & Mini Design System

Deliver a Python-driven content engine, a WP rendering layer, and a portable mini design system.  
Python is the sole source of truth. WordPress is not a CMS.

---

# Story Breakdown (Markdown Tables)

## Table 1: Content Engine & Publishing Pipeline

| Story ID | Title | User Story | Acceptance Criteria | Dependencies | Status |
|----------|--------|------------|---------------------|--------------|--------|
| SUG-201 | Single Source of Truth | As the system owner, I need Python to be the only canonical source so the system remains reproducible. | All content originates in `sugartown-cms`; WP stores no unique content; rebuild works end-to-end. | None | To Do |
| SUG-202 | Gem CPT | As a frontend visitor, I need Gems structured as a CPT so I can browse them with metadata. | CPT registered; archive + single templates; shared taxonomy. | Theme repo | To Do |
| SUG-203 | Publishing Pipeline | As an operator, I need a Python→WP pipeline so content stays synced. | REST API POST/PUT works; new Gems created; existing updated. | CMS repo | To Do |
| SUG-204 | Idempotent Hashing | As the operator, I need hashing so unchanged posts are skipped. | MD5 implemented; logs show skip/update; API reduced by 90%. | SUG-203 | To Do |
| SUG-205 | Backup & Rollback | As the operator, I need backups so I can revert failures. | Timestamped backups; rollback restores content + logic. | SUG-203 | To Do |
| SUG-206 | Unified Taxonomy | As the maintainer, I need consistent taxonomy across CPTs. | Categories + tags shared by all CPTs; no drift. | SUG-202 | To Do |

---

## Table 2: Visualization Engine

| Story ID | Title | User Story | Acceptance Criteria | Dependencies | Status |
|----------|--------|------------|---------------------|--------------|--------|
| SUG-207 | CSV Export | As an analyst, I need content exported so I can visualize coverage. | CSV includes ID, title, category, status, project, tags. | CMS repo | To Do |
| SUG-208 | Knowledge Graph | As a visitor, I need a network graph to understand content relationships. | Graph PNG generated; stable filename; displayed in Gems. | SUG-207 | To Do |
| SUG-209 | Category Chart | As an analyst, I need category charts for content evaluation. | Bar chart rendered; stable filename; included in Gems. | SUG-207 | To Do |

---

## Table 3: Mini Design System

| Story ID | Title | User Story | Acceptance Criteria | Dependencies | Status |
|----------|--------|------------|---------------------|--------------|--------|
| SUG-210 | Define Tokens | As the design system owner, I need a canonical token set. | `sugartown.tokens.json` created; naming documented. | None | To Do |
| SUG-211 | Token Integration | As the developer, I need tokens mapped to WP so UI is consistent. | CSS variables; theme.json mapping; block styles aligned. | SUG-210 | To Do |
| SUG-212 | Component Styles | As a visitor, I need consistent UI components across Gems. | Styled tables, code blocks, badges, cards. | SUG-211 | To Do |
| SUG-213 | Figma Library | As a designer, I need Figma variables for parity with code. | Tokens imported; primitives created; published. | SUG-210 | To Do |
| SUG-214 | DS Documentation | As a maintainer, I need design system docs. | Token table; usage guidelines; theme mapping; React notes. | SUG-210, SUG-211, SUG-212 | To Do |

---

## Table 4: Architecture & Repo Structure

| Story ID | Title | User Story | Acceptance Criteria | Dependencies | Status |
|----------|--------|------------|---------------------|--------------|--------|
| SUG-215 | Two-Repo Architecture | As the developer, I need separated repos so the system scales. | `sugartown-cms` and `2025-sugartown-pink` created with README boundaries. | None | To Do |
| SUG-216 | System Documentation | As a maintainer, I need accurate documentation. | Architecture diagrams; pipeline overview; repo boundaries. | All prior | To Do |
| SUG-217 | Enforce WP Statelessness | As the owner, I need WP free of manual content. | No manual WP edits; policy documented; PRD updated. | SUG-201 | To Do |

---

## Table 5: Future Migration

| Story ID | Title | User Story | Acceptance Criteria | Dependencies | Status |
|----------|--------|------------|---------------------|--------------|--------|
| SUG-218 | React Token Package | As the developer, I need tokens structured for React. | JSON export ready for JS/TS modules. | SUG-210 | Backlog |
| SUG-219 | Headless Migration Brief | As the owner, I need a playbook for moving off WP. | Architecture diagram; data sourcing; token reuse plan. | SUG-214 | Backlog |
| SUG-220 | CMS Replacement Evaluation | As the product owner, I need to evaluate modern CMS options. | Comparison of Sanity / Contentful / Hygraph. | SUG-201 | Backlog |

