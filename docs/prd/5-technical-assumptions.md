# 5. Technical Assumptions
## Deterministic First
* All eight GDPR Art.28(3) detectors will be implemented via rulepacks (YAML/regex) with evidence windows (±2 sentences).
* LLMs are disabled by default; when enabled, only short snippets (≤220 tokens) are passed.
* Hard cap: ≤1,500 tokens per document; if exceeded → needs_review.

## Performance Targets
* End-to-end latency p95 ≤ 60 seconds for ≤10MB PDFs.
* Cost ≤ £0.10 per document at defaults.
* Accuracy thresholds: Precision ≥0.85, Recall ≥0.90, Explainability ≥95%.

## Storage & Infra
* MVP: SQLite for persistence + local filesystem for artefacts.
* Phase-2: Postgres (Supabase) + object storage.
* Queue: FastAPI BackgroundTasks in MVP; Celery+Redis later.
* Hosting: Windows-first local dev; optional Render/Supabase for demo.

## Security & Privacy
* No PII retention by default; ephemeral processing.
* Encryption at rest & in transit.
* Snippet-only LLM calls, with regex redaction of PII.
* .env secrets; Windows-safe config.

## API Contracts
* REST/JSON endpoints:
    * `POST /api/contracts` → upload & job.
    * `GET /api/jobs/{id}` → status.
    * `GET /api/analyses/{id}` → summary.
    * `GET /api/analyses/{id}/findings` → Finding[].
    * `POST /api/reports/{id}` → PDF/HTML export.
* Finding model: `{ detector_id, rule_id, verdict, snippet, page, start, end, rationale, reviewed }`.

## Frontend Assumptions
* Next.js 14, Tailwind, shadcn/ui, React Query.
* Evidence-first UX: Findings table with verdict chips + Evidence Drawer.
* WCAG AA accessibility; progressive disclosure for detail.
* Dark theme by default.

## Testing & Observability
* Gold set (10–20 DPAs) used for precision/recall evaluation.
* Metrics logged: latency, tokens/doc, %LLM invoked, explainability rate.
* Structured JSON logs; simple admin metrics wall.
