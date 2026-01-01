# Product Requirements Document (PRD)
## Sugartown Resume Factory v2.0 — Headless Career Data Engine

---

## 1. Overview

The **Resume Factory v2.0** is a headless publishing pipeline that transforms career history from a static document into a structured, queryable dataset. It moves beyond "Static Versions" to **"Dynamic Composition,"** decoupling **Content** (a "Golden Record" in CSV/JSON) from **Presentation** (PDF, Markdown).

**Architectural Philosophy:**
* **Single Source of Truth:** All data originates in `master_resume_data.json` (derived from CSV).
* **Dynamic Composition:** The engine assembles resumes based on a hierarchical logic (Anchor > Domain > Flavor), not just flat filtering.
* **Stateless Output:** Generated resumes are artifacts (builds), not source files.

---

## 2. Problem Statement

**The Friction:**
* **"The Specialist Trap":** Leading with hard skills (e.g., "Headless CMS") risks pigeonholing the candidate as an Implementation Specialist rather than a Product Leader.
* **Resume Drift:** Maintaining 5 different Google Docs for "Product," "Technical," and "Strategy" roles leads to out-of-sync dates and titles.
* **AI Hallucination:** Using LLMs to "rewrite" bullets often invents metrics or skills that don't exist.
* **Manual Toil:** Tweaking margins and spacing in Word/GDocs is a low-value use of time.

---

## 3. Goals & Non-Goals

### 3.1 Goals

| Goal | Description |
| :--- | :--- |
| **Hierarchical Precision** | Ensure every generated resume anchors Seniority (Primary) before detailing Skills (Secondary). |
| **Personalization at Scale** | Generate role-specific variants (e.g., "The AI Role" vs. "The Strategy Role") instantly from a single data source. |
| **Zero Hallucinations** | Eliminate generative text in the *assembly* phase. Content is selected, not invented. |
| **Headless Publishing** | Push the "Live Resume" to WordPress via API without logging into the CMS. |

### 3.2 Non-Goals (Out of Scope)

| Non-Goal | Description |
| :--- | :--- |
| **AI Text Generation** | We do not use AI to write bullet points in this phase. AI is for extraction/analysis only. |
| **Visual Design Tooling** | We are not building a drag-and-drop editor. Styling is handled via CSS/Markdown templates. |

---

## 4. User Stories

| Story ID | Title | User Story | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **RES-001** | **Ingest Golden Record** | As the Candidate, I want to manage my history in a CSV so I can easily edit bullets in bulk. | `ingest_resume.py` parses CSV into `master_resume_data.json` with nested "Slots" and "Variants." | **P0** |
| **RES-002** | **Generate Variant** | As the Candidate, I want to build a "Technical" resume so I can apply to Engineering roles. | `build_resume.py` filters bullets by `variant_id` and outputs a clean Markdown file. | **P0** |
| **RES-003** | **Dynamic Identity** | As the Candidate, I want my "Role Title" to anchor my seniority level, regardless of the specific skill set. | Header data changes dynamically (e.g., "Principal PM" -> "Technical Lead") but maintains level hierarchy. | **P1** |
| **RES-004** | **Auto-Publish** | As the Candidate, I want my web resume to update automatically so recruiters see the latest info. | `publish_resume.py` pushes HTML payload to WordPress Page ID 207 via REST API. | **P1** |

---

## 5. Technical Architecture

### 5.1 The Data Flow
1.  **Source:** `data/source/resume_data.csv` (Manual Entry / Google Sheets).
2.  **ETL Layer:** `ingest_resume.py` transforms CSV rows into a hierarchical JSON object (`master_resume_data.json`).
3.  **Logic Layer:** `build_resume.py` applies "Strict Match" logic.
4.  **Presentation Layer:** Markdown -> VS Code PDF Export / WordPress REST API.

### 5.2 Repository Structure (`sugartown-cms`)

```text
data/
├── source/
│   └── resume_data.csv       # The Human Input
└── json/
    └── master_resume_data.json # The Machine Input (Golden Record)

scripts/
├── ingest_resume.py          # CSV -> JSON Converter
├── build_resume.py           # JSON -> Markdown/PDF Generator
└── publish_resume.py         # Markdown -> WordPress API Pusher

output/
└── resumes/
    ├── CMS-DS-PDM-01.md      # Generated Variant A
    └── CMS-AI-PDM-01.md      # Generated Variant B
```

### 5.3 Composition Logic: The Hierarchy of Needs
To prevent "Level Drift" (appearing too junior), the builder script must assemble content in this strict priority order:

| Tier | Component | Function | Purpose | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **1. Primary** | **The Anchor** | **Target Role** | Defines Scope & Seniority (Salary Band). | *"Principal Product Manager"* |
| **2. Secondary** | **The Domain** | **Hard Skills** | Defines Context. | *"Headless CMS & Design Systems"* |
| **3. Tertiary** | **The Flavor** | **The Hook** | Satisfies Recruiter Persona. | *"AI", "SEO", "Change Mgmt"* |

*Implementation Note:* The script must inject the **Primary** title into the H1/Header, ensuring the **Secondary** and **Tertiary** keywords appear in the Summary and Skills table, but never override the Role Title.

---

## 6. Dependencies & Risks

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **CSV Formatting Errors** | Script crashes or data is lost. | Strict column validation in `ingest_resume.py` with error logging. |
| **API Auth Failure** | Web resume fails to update. | Use `config.py` for secure App Passwords; add connection retry logic. |
| **Over-Filtering** | Resume generated with zero bullets. | Implement "Master Fallback" logic to ensure core bullets always appear. |

---

## 7. Success Criteria

| Area | Metric | Target |
| :--- | :--- | :--- |
| **Efficiency** | Time to generate a new resume version | < 5 seconds (vs 30 mins manual) |
| **Accuracy** | Data parity between CSV and PDF | 100% (Bit-perfect) |
| **Availability** | Web Resume Uptime | 99.9% (Decoupled from build process) |

---

## 8. Future Roadmap

* **Phase 3 (The Agent):** Integrate a local LLM to analyze a Job Description URL and automatically suggest the best `variant_id` config to run.
* **Phase 4 (The Interface):** Build a simple React front-end to toggle variants and preview the PDF in real-time.

---

**Document Version:** 2.0.0  
**Last Updated:** December 2025  
**Author:** Bex, with architectural input from Gemini3  
**Next Review:** Upon completion of v2 MVP