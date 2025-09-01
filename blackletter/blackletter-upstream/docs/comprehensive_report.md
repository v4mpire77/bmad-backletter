# Blackletter Systems — Comprehensive Report

## 1. Vision & Positioning

- **Tagline**: *Old rules. New game.*
- **Core Idea**: Blend traditional legal expertise with AI automation to shrink contract review from hours to minutes, focused on compliance-first transparency (GDPR, AML, SRA).
- **Market Position**: UK law firms & SMEs plagued by regulatory anxiety; unmet need for auditable, cost-efficient AI compliance automation.

## 2. Market & Strategy

- **Total Addressable Market**: Global legal-tech £26.7B (2024) → £46.8B (2030); UK market £1.4B → £2.43B.
- **Segment**: Contract Lifecycle Management (~£7B); even 1% = £70M ARR.
- **Competitive Gap**: No UK/EU compliance-automation specialist for mid-market firms (10–200 lawyers).
- **Go-To-Market Mode**: Stimulate (category creation). Must educate before selling.
- **Wedge Strategy**:
  - Phase 1: GDPR/AML compliance checker for contract review.
  - Phase 2: Employment + other compliance verticals.
  - Phase 3: Expand to EU & enterprise.
- **Target ICP**: Partners, legal ops, compliance managers (35–55 yrs, £100k–300k budgets).
- **Pricing**: £50–100/user/month; CAC £300–2,500; CLV £18k–36k.

## 3. Product — GDPR Processor Obligations Checker

### MVP Scope

- **Ingestion**: Upload PDF/DOCX ≤10MB → async job.
- **Extraction**: Text + page map + sentence index (OCR optional, off by default).
- **Detection**: 8 GDPR Art. 28(3) obligation checks (a–h).
- **Findings UI**: Evidence-first (snippet, rule id, rationale, verdict chip).
- **Report Export**: PDF/HTML with citations.
- **Metrics**: Latency, tokens, %LLM, explainability.
- **Settings**: LLM toggle (default none), OCR, retention.
- **Auth**: Minimal Admin/Reviewer roles.

### Verdicts

- **Pass** — anchor present, no red-flags.
- **Weak** — hedged or discretionary language.
- **Missing** — no anchor or contradicted.
- **Needs review** — ambiguous/over budget.

### Constraints

- **p95 latency** ≤60s; **≤£0.10/doc**; Precision ≥0.85; Recall ≥0.90; Explainability ≥95%.
- **Local-first, deterministic**; LLM snippet-only fallback; SQLite dev → Postgres later.
- **Windows-first dev environment**.

## 4. Architecture & Implementation

### Tech Stack

- **Frontend**: Next.js 14, React 18, TS 5.4, Tailwind, shadcn/ui, lucide.
- **Backend**: Python 3.11, FastAPI, Uvicorn, SQLAlchemy, PyMuPDF, docx2python, blingfire.
- **Storage**: SQLite (MVP) → Supabase/Postgres.
- **Infra**: Local dev; optional Supabase/Render/Vercel for cloud.
- **Testing**: pytest, Playwright, token ledger metrics.
- **CI/CD**: GitHub Actions (Windows-safe scripts in `/scripts/ps/`).

### Pipeline

1. Intake Router → validates upload, enqueues job.
2. Extractor → text + indexes.
3. Evidence Windower → ±2 sentences.
4. Detector Runner → YAML rulepack verdicts.
5. Reporter → Findings + export.
6. Metrics Writer → logs KPIs.

### Rule Engine

- YAML detectors (anchors, weak cues, red-flags).
- Weak-language lexicon v0 ("commercially reasonable", "may", etc.).
- Evidence window default ±2 sentences.
- Conservative defaults: unknown → Needs review.

### Source Tree (scaffold)

```
blackletter/
  apps/web/ (Next.js 14 frontend)
  apps/api/ (FastAPI backend)
    routers/ uploads, jobs, analyses, reports
    services/ tasks, extraction, evidence, detection, reporting, metrics
    rules/ art28_v1.yaml + lexicons
    models/ db, entities, schemas
  docs/ prd, architecture, stories
  scripts/ps/ dev.ps1, test.ps1, lint.ps1
```

## 5. UX Specification

- **Principles**: Evidence-first, deterministic, progressive disclosure, trust through transparency.
- **Flows**: Upload → Job Status → Findings → Export → History.
- **UI Elements**:
  - Drag-drop uploader + progress stepper.
  - Findings table (8 detectors, verdict chips, rationale).
  - Evidence Drawer (snippet, anchors, rationale).
  - Report Export dialog.
  - Metrics dashboard (p95 latency, tokens, coverage).
  - Settings (LLM, OCR, retention).
- **Design Tokens**: Inter font, JetBrains Mono, dark theme, WCAG AA compliant verdict colors (emerald, amber, red, sky).
- **Accessibility**: Keyboard-first, ARIA labels, icons + text (not color only).

## 6. Scrum Master Story Pack (SM v1)

- **Story 1.1** — Upload & Job Orchestration.
- **Story 1.2** — Text Extraction.
- **Story 2.1** — Rulepack Loader.
- **Story 2.2** — Detector Runner.
- **Story 3.1** — Findings Table UI.
- **Tests**: unit (3 pos + 3 neg per detector), integration, E2E (upload→findings→export).
- **Artifacts**: routers, services, models, components, fixtures.
- **Sprint Order**: 1.1 → 1.2 → 2.1 → 2.2 → 3.1 → (exports & metrics).

## 7. Risks & Mitigations

- **Clause variance** → broad anchors, weak lexicon, future classifiers.
- **False reassurance** → conservative defaults, never "green" without snippet.
- **LLM drift / cost blow-up** → token caps, provider=none by default, caching.
- **OCR fragility** → disabled by default; clear errors.
- **Trust/adoption** → explainability UI, human-in-loop workflows.
- **Market risk** → conservative buyers, entrenched vendors; mitigated with sharp compliance wedge + case studies.

## 8. Roadmap

### Short-term (0–3 mo)
- Complete MVP build (stories 1.1–3.1).
- Pilot with 10–20 UK property law SMEs.
- Publish 3–5 case studies with ROI.

### Mid-term (6–18 mo)
- Employment law detectors.
- Clio/MyCase integrations.
- Expand gold set, improve lexicon.
- Hire sales team; scale to 200+ customers.

### Long-term (18+ mo)
- Broaden to general contract review + case law research.
- EU expansion; enterprise tier.
- Adjacent innovations: multi-agent orchestration, playbook marketplace, regulatory forecasting, autonomous compliance counsel.

## 9. BMAD Method Alignment

- **Analyst (Mary)** → scope, acceptance wordings, lexicon.
- **PM (John)** → PRD & stories.
- **PO (Sarah)** → validation & approvals.
- **Architect (Winston)** → system design & tech stack.
- **UX (Sally)** → IA, wireframes, design tokens.
- **Scrum Master (Sam)** → dev-ready story packs.
- **Orchestrator (you)** → oversees integration across all roles.

## Summary

Blackletter Systems has a tight, compliance-first wedge: GDPR processor-obligations checker, rules-first, transparent, and cost-controlled. The market is ready but conservative; success hinges on delivering ROI case studies and trust signals. The build plan, UX spec, architecture, and SM story packs are aligned and green-lit for development. This foundation can scale into full legal-tech automation—compliance checklists, research assistants, negotiation agents—but the immediate focus is nailing GDPR Art. 28(3) detection with explainable evidence.

