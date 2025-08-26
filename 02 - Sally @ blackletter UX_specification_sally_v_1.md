# Blackletter — UI/UX Specification (Sally v1)

**Project**: Blackletter — GDPR Processor‑Obligations Checker  
**Owner (UX Expert)**: Sally  
**Date**: 2025‑08‑26  
**Intended Readers**: PM, Architect, PO, SM, Dev, QA

> Purpose: Translate the PRD into a detailed, implementation‑ready UX spec (flows, IA, components, design tokens, accessibility, microcopy) and provide prompts for AI UI generators (e.g., v0 / Lovable). This document is self‑contained so Dev can scaffold UI immediately.

---

## I. Overall Vision & User Needs

### Personas
- **DPO / Data Protection Lead (Primary)**: Reviews vendor DPAs; needs fast, transparent checks with citations.  
- **In‑house Counsel**: Wants consistent triage before in‑depth review.  
- **External Solicitor**: Needs a shareable, client‑friendly report.  
- **SME Founder/Ops**: Quick sanity check during procurement.

### Primary Usability Goals
1) **Clarity** — Findings are understandable at a glance (R/A/G mapping).  
2) **Trustworthiness** — Every verdict shows a **why** (rule id + snippet + offsets).  
3) **Efficiency** — Upload → Findings → Export in under **3 minutes** for small docs.  
4) **Control** — Safe defaults (LLM off), explicit settings, predictable behavior.  
5) **Accessibility** — Keyboard‑first flows, clear focus states, WCAG AA contrast.

### Guiding Design Principles
- **Evidence‑first** (snippet over summary)  
- **Deterministic UX** (no hidden magic)  
- **Lean surface area** (few, focused screens)  
- **Progressive disclosure** (detail drawers, not modal pile‑ups)  
- **Respect for constraints** (token budget, document size, privacy)

---

## II. Information Architecture (IA) & User Flows

### Global Navigation (left sidebar on desktop; top nav on mobile)
- **Dashboard** (history list)  
- **New Analysis** (upload)  
- **Findings** (current analysis)  
- **Reports** (exports list)  
- **Metrics** (admin)  
- **Settings** (org, privacy, providers)

### Sitemap
```
/ (redirect → /dashboard)
/dashboard
/new
/analyses/:id (Findings)
/reports
/reports/:id
/admin/metrics (Admin only)
/settings
```

### Core User Journey — Upload → Findings → Export
1) **Upload** (drag‑and‑drop or file picker) → validate type/size → create job → route to **Job Status**.  
2) **Job Status** (inline panel): queued → extracting → detecting → reporting → **View Findings** CTA; errors shown with retry guidance.  
3) **Findings**: Table/cards of eight detectors with verdict colors; click a row to open **Evidence Drawer** with snippet & rule id.  
4) **Export**: PDF/HTML from the Findings screen; confirm dialog with options (logo, date format).  
5) **History/Dashboard**: New entry appears with summary chips and quick open.

### Critical Tasks
- Upload & track progress  
- Review findings and drill down  
- Filter/sort by verdict  
- Export report  
- Adjust org settings (LLM/OCR/retention)  
- View metrics & coverage

### Entry Points, Success Criteria, Edge Cases
- **Entry**: From Dashboard (New Analysis), drag‑drop anywhere on New page.  
- **Success**: Findings rendered with all eight detectors; export succeeds; history item created.  
- **Edge**: Oversize file; corrupted PDF; unsupported DOCX; OCR disabled but needed; token cap exceeded (show Needs review); server error; network loss mid‑upload; duplicate upload.

---

## III. Visual Design & Components

### Visual Style & Aesthetic
- **Professional, clean, modern.** Neutral greys, calm blues, limited accents. Minimal visuals; copy and structure carry trust.

### Brand & Design Tokens
- **Fonts**: UI — Inter (fallback: system UI); Mono — JetBrains Mono for code/offsets.  
- **Spacing scale**: 4/8/12/16/24/32 px.  
- **Radius**: 12–16 px (cards/buttons).  
- **Elevation**: soft shadows only (avoid heavy drop shadows).  
- **Color Tokens**:
  - `--bg`: #0B0D10 (shell dark) / #0F172A (slate‑900 alt)
  - `--surface`: #111827 (slate‑900)  
  - `--text-primary`: #E5E7EB  
  - `--text-secondary`: #9CA3AF  
  - **Verdicts**  
    - **Pass**: `--pass-600: #16A34A` (emerald‑600), `--pass-200: #A7F3D0`  
    - **Weak**: `--weak-600: #F59E0B` (amber‑600), `--weak-200: #FDE68A`  
    - **Missing**: `--missing-600: #DC2626` (red‑600), `--missing-200: #FCA5A5`  
    - **Needs review**: `--review-600: #0EA5E9` (sky‑600), `--review-200: #BAE6FD`
  - **Info/Warning/Error**: sky/amber/red Tailwind scales respectively.  
- **Contrast**: All text over colored badges meets WCAG AA (>= 4.5:1). Use `-700` foreground over `-200` backgrounds or white on `-600`.

### Component Library (shadcn/ui + Radix + lucide‑react)
- **Buttons** (primary, secondary, subtle, destructive)  
- **Input/FileDrop** (drag‑drop with progress)  
- **Table** (sticky header, resizable cols, row click)  
- **Badge** (verdict chips)  
- **Drawer/Sheet** (Evidence Drawer)  
- **Dialog** (export options, delete confirm)  
- **Alert/Toast** (errors, successes)  
- **Tabs** (Summary / Details / Raw)  
- **Tooltip** (rule id hover)  
- **Progress** (job status)  
- **Skeletons** (loading)  
- **Pagination** (history)

### Iconography (lucide)
- Upload, FileText, Scale, CheckCircle2, AlertTriangle, XCircle, HelpCircle, Search, Filter, Download, Settings, BarChart3, History, ClipboardList.

---

## IV. Specific UI Elements for Blackletter

### A) Document Upload Flow
- **Layout**: Full‑width card with drag‑drop zone; secondary file picker.  
- **States**: Empty → Drag‑hover → Uploading (progress%) → Queued → Extracting → Detecting → Reporting → Done.  
- **Feedback**: Inline stepper with icons; ETA if available; cancel/reset button.  
- **Errors**: Clear reason + action (e.g., “File too large (max 10MB). Try compressing or split PDF.”).  
- **Copy**: “Your file stays private. LLM is off by default.” (link to settings).

**Microcopy**
- Empty: “Drop a PDF or DOCX up to 10MB”  
- Uploading: “Uploading… 42%”  
- Detecting: “Running GDPR checks (A28(3)(a)–(h))…”

### B) Findings View
- **Header**: File name, upload date, checksum; Export button; badge group with counts (Pass/Weak/Missing/Needs review).  
- **Filters**: Verdict multi‑select; text search (within snippets).  
- **Table** (8 rows minimum): columns: Detector, Verdict (chip), Rationale (short), Actions.  
- **Row click → Evidence Drawer** (right sheet):
  - **Summary**: Detector title, verdict chip, rule id.  
  - **Snippet**: monospace block with highlighted **anchor phrases**; page + offsets; Copy and “Open raw text” tabs.  
  - **Why**: bullet list: anchors found, weak cues, red flags, algorithmic verdict mapping.  
  - **Actions**: Mark as “Reviewed” (client‑side note), Add comment.

**Verdict Colors & Semantics**  
- Pass = emerald; Weak = amber; Missing = red; Needs review = sky. Badges include accessible labels.

### C) Dashboard (History)
- **List**: cards or table rows with filename, date, size, verdict chips summary, open action.  
- **Empty state**: “No analyses yet. Drag a contract to start.” CTA → New Analysis.

### D) Reports
- **List**: recent exports with file name, type (PDF/HTML), size, date; Download action.  
- **Export Dialog**: options: include logo, include metadata, date format.

### E) Metrics (Admin)
- **Tiles**: p95 latency, tokens/doc, %LLM usage, explainability rate.  
- **Chart**: small sparkline per metric (last 30 runs).  
- **Coverage**: detector coverage bar (all eight must register).

### F) Settings
- **Sections**: General (branding logo), Privacy (retention), AI (provider toggle), OCR (off/on).  
- **Copy**: “LLM is **off by default**. When enabled, we only send **short snippets** to the provider.”

---

## V. Technical & Accessibility Considerations

### Targets
- **Web responsive** (desktop‑first, good on 1280–1440px; usable down to 360px).  
- **Breakpoints**: 360 / 768 / 1024 / 1280 / 1536 px.

### Accessibility (WCAG AA)
- All actionable elements keyboard navigable; visible focus rings.  
- Table has proper semantics (`role=table`, `th`, `scope`), ARIA labels on verdict chips (e.g., `aria-label="Verdict: Missing"`).  
- Color is **not** the only signal (add icons + text).  
- Evidence Drawer supports screen readers (region landmarks, headings).  
- Motion reduced when `prefers-reduced-motion` set.

### Performance Goals
- **First meaningful paint** < 2s on desktop baseline.  
- **Interactions** respond < 100ms.  
- Avoid heavy libraries; lazy‑load charts; stream job status updates.

### Micro‑interactions
- Subtle hover on rows; progress stepper animates between states; copy‑to‑clipboard toast; focus trap in dialogs.

---

## VI. Low‑Fidelity Wireframes (ASCII)

### New Analysis (Upload)
```
+------------------------------------------------------------+
|  New Analysis                                              |
|  [ Drop PDF/DOCX here ]  or  [ Choose file ]               |
|  (max 10MB • private • LLM off by default)                 |
|                                                            |
|  Status: [Queued] [Extracting] [Detecting] [Reporting]     |
|  Progress: [##########------] 42%                          |
|  Errors: —                                                 |
+------------------------------------------------------------+
```

### Findings
```
+------------------------------------------------------------+
|  Findings: acme_dpa.pdf         [Export]   Chips: P 5 | W 2 | M 1 | R 0 |
|  Filters: [Verdict: All v] [Search snippets…]                             |
|  ----------------------------------------------------------------------  |
|  Detector                     | Verdict  | Rationale        |  >         |
|  A28(3)(a) Instructions       | PASS     | anchor present…  |            |
|  A28(3)(b) Confidentiality    | WEAK     | hedge near…      |            |
|  A28(3)(c) Security           | MISSING  | no TOMs ref…     |            |
|  ...                                                                …     |
+------------------------------------------------------------+
 (Drawer →)  [A28(3)(c) Security]  [MISSING]
  Rule: art28_v1.A28_3_c_security
  Snippet (p.7 1423–1562):
  "… Processor implements [HIGHLIGHT: technical and organisational measures] …"
  Why: anchors found: 0; weak cues: 1; red flags: 1 → verdict: MISSING
  [Copy] [Mark reviewed] [Comment]
```

### Reports
```
+-------------------------------+
| Reports                       |
| acme_dpa_2025-08-26.pdf [DL] |
| beta_saas_2025-08-21.html[DL]|
+-------------------------------+
```

---

## VII. Copy & Content Design (key strings)
- **Upload empty**: “Drop a PDF or DOCX up to 10MB. Your file stays private.”  
- **Privacy note**: “LLM is off by default. When enabled, only short snippets are sent.”  
- **Needs review badge**: “Needs review (token cap or ambiguous phrasing)”  
- **Export dialog**: “Include logo”, “Include metadata”, “Date format”  
- **Error oversize**: “File too large (max 10MB). Try compressing or split into parts.”

---

## VIII. Acceptance Criteria (UI Stories → SM/Dev)

### Story 3.1 — Findings Table (UI)
- Show 8 detectors with verdict chips and rationale.  
- Filters: multi‑select verdict; text search (snippet index).  
- Row click opens Evidence Drawer; focus moves to drawer header; ESC closes.  
- Contrast AA; icons + text on chips.

### Story 3.2 — Report Export (UI)
- Export button → Dialog with options → Creates PDF/HTML → Toast on success.  
- Export matches table order and includes snippets + timestamps.  
- Download link available under Reports.

### Story 1.x — Upload UX
- Drag‑drop active state; progress bar; stepper status; cancel.  
- On error, explain cause + retry guidance.  
- On success, auto‑route to Findings.

---

## IX. AI UI Generation Prompts

### A) v0 Prompt (paste into Vercel v0)
```
Build a Next.js 14 + Tailwind app screen set for a legal compliance tool “Blackletter”.
Use shadcn/ui + Radix + lucide-react. Dark, professional style, Inter font.
Screens: Dashboard, New Analysis (upload), Findings (table + evidence drawer), Reports, Metrics, Settings.
Components: drag-drop uploader with progress stepper; data table with verdict badges (Pass=emerald, Weak=amber, Missing=red, Needs review=sky); right-side drawer with snippet (monospace) and rule id.
Accessibility: WCAG AA contrast; keyboard focus rings; ESC to close dialogs/drawers; icons + text (not color only).
```

### B) Lovable Prompt
```
Create a responsive web UI for “Blackletter — GDPR Processor Obligations Checker”.
Primary screens: Upload, Findings, Reports, Metrics, Settings. Use dark theme, clean typography (Inter), shadcn/ui components, lucide icons.
Findings page shows 8 detector rows with verdict chips; clicking a row opens a right drawer with snippet (monospace, highlighted anchors), rule id, offsets, and rationale.
Include export dialog and admin metrics tiles. Ensure keyboard navigation and ARIA labels on verdict chips.
```

---

## X. Handoff Checklist
- [ ] Tokens + theme variables defined (above).  
- [ ] Component inventory aligned with shadcn imports.  
- [ ] Wireframes approved by PM.  
- [ ] Stories 3.1, 3.2, and Upload UX accepted by PO.  
- [ ] Dev to scaffold pages/routes and components per IA.

