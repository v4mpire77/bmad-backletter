# 8) Detailed Story Templates (for SM → Dev)
> Stories start as **status: draft**. PO will flip to **approved** before Dev.

## Story 1.1 — Upload & Job Orchestration
```
id: 1.1
epic: 1
title: Upload & Job Orchestration
status: draft
acceptance_criteria:
  - POST /contracts accepts PDF/DOCX ≤10MB; returns job_id
  - GET /jobs/{id} returns status: queued|running|done|error (+ error reason)
  - On done, analysis record exists with filename, size, created_at
  - Latency budget: enqueue < 500ms server time
notes:
  - Virus/size checks server‑side; signed upload URL optional
```  

## Story 1.2 — Text Extraction (PDF/DOCX)
```
id: 1.2
epic: 1
title: Text Extraction (PDF/DOCX)
status: draft
acceptance_criteria:
  - Extract text → page map (page→char range) + sentence index
  - Store extraction artefacts linked to analysis record
  - Malformed/corrupt docs handled with explicit error codes
  - OCR default off; config flag enables OCR path
```

## Story 1.3 — Evidence Window Builder
```
id: 1.3
epic: 1
title: Evidence Window Builder (±2 sentences)
status: draft
acceptance_criteria:
  - Given a char span, return ±2 sentences (configurable per detector)
  - Respect sentence boundaries; avoid cross‑page leakage
  - Unit tests with synthetic spans
```

## Story 2.1 — Rulepack Loader (art28_v1)
```
id: 2.1
epic: 2
title: Rulepack Loader (art28_v1)
status: draft
acceptance_criteria:
  - Load YAML; validate schema; list detectors and lexicons
  - On invalid YAML, surface clear errors
  - Config: rules path env var; hot‑reload disabled in prod
```

## Story 2.2 — Detector Runner
```
id: 2.2
epic: 2
title: Detector Runner (verdict + evidence)
status: draft
acceptance_criteria:
  - Evaluate anchors/weak/red‑flags within evidence window
  - Produce verdict per mapping; attach rule id + snippet + offsets
  - Unit tests: 3 positive + 3 hard negative per detector (a)–(c) to start
```

## Story 2.3 — Weak‑Language Lexicon v0
```
id: 2.3
epic: 2
title: Weak‑Language Lexicon v0
status: draft
acceptance_criteria:
  - Apply lexicon inside evidence window
  - Downgrade Pass→Weak unless counter‑anchor present
  - Configurable lexicon file
```

## Story 2.4 — Token Ledger & Caps
```
id: 2.4
epic: 2
title: Token Ledger & Caps
status: draft
acceptance_criteria:
  - Track tokens_per_doc; expose metric
  - Hard cap triggers needs_review; logged with reason
  - LLM provider off by default
```

## Story 3.1 — Findings Table
```
id: 3.1
epic: 3
title: Findings Table (evidence‑first)
status: draft
acceptance_criteria:
  - 8 detector rows with verdict color and short rationale
  - Detail drawer shows snippet + rule id + copy button
  - Filter by verdict; search within snippets
```

## Story 3.2 — Report Export
```
id: 3.2
epic: 3
title: Report Export (PDF/HTML)
status: draft
acceptance_criteria:
  - PDF/HTML export with headings, verdicts, snippets, timestamps
  - Include file metadata (name, checksum)
  - Asset is reproducible from stored artefacts
```

## Story 4.1 — Metrics Wall
```
id: 4.1
epic: 4
title: Metrics Wall (latency, tokens, %LLM, explainability)
status: draft
acceptance_criteria:
  - Capture and display p95 latency, tokens_per_doc, %docs_invoking_LLM
  - Explainability rate (findings with snippet+rule id)
  - Admin‑only page
```

## Story 4.2 — Coverage Meter
```
id: 4.2
epic: 4
title: Coverage Meter
status: draft
acceptance_criteria:
  - Visual shows detector coverage per doc
  - Warning if any detector returns unknown
```

## Story 5.1 — Org Settings
```
id: 5.1
epic: 5
title: Org Settings (LLM/OCR/Retention)
status: draft
acceptance_criteria:
  - Toggle LLM provider (none/default), OCR, retention policy
  - Persist securely; defaults conservative
  - Audit log for settings changes
```

## Story 5.2 — Minimal Auth & Roles
```
id: 5.2
epic: 5
title: Minimal Auth & Roles (Admin/Reviewer)
status: draft
acceptance_criteria:
  - Admin can manage settings; Reviewer can upload/export only
  - Sessions persisted; CSRF protected
```

---
