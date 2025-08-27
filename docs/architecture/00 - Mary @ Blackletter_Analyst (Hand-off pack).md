# Blackletter — Analyst (Mary) Hand‑Off Pack (v1)

**Project**: Blackletter (GDPR Vendor Contract Checker)

**Owner (Analyst)**: Mary  
**Audience**: PM, Architect, PO, SM  
**Purpose**: Single, self‑contained analyst deliverable that captures scope, decisions, acceptance wordings, rulepack skeleton, weak‑language lexicon, gold‑set plan, risks, KPIs, and next steps. Ready for PM/Architect to proceed.

---

## 0) Executive Summary
Blackletter reduces vendor‑contract review time by surfacing **explainable GDPR Art. 28(3) findings** (R/A/G) with **pinpoint citations** and a **deterministic, rules‑first** approach. LLMs are optional and gated to **snippet‑only** analysis. MVP targets **p95 ≤ 60s**, **≤ £0.10/doc**, and **P≥0.85 / R≥0.90** on a labeled gold set.

**Guiding Principles**
- Determinism first; LLMs only for ambiguous edges and only over **short snippets**.  
- Three‑valued logic: **pass / weak / missing** (+ **needs_review** as conservative default).  
- Verifiability: every finding shows **why** (rule id + snippet + location).  
- Local‑first & cost‑aware: token ledger, hard caps, caching; OCR opt‑in.

---

## 1) Users & Constraints
**Primary users**: UK SME founders/ops, in‑house counsel, external solicitors/DPOs.  
**Promise**: 10 GDPR‑critical topics checked with grounded evidence; fast, cheap, transparent.  
**Constraints**: Windows‑friendly dev; low/no PII retention by default; free/cheap infra; explainability ≥95%.

---

## 2) Method Pillars → Design Hooks
- **Determinism →** rulepacks (YAML/regex), header‑aware chunking, fixed evidence windows.  
- **Three‑valued logic →** verdict mapping table; conservative defaults.  
- **Verifiability →** clause path + page/char offsets; exportable report.  
- **Token discipline →** snippet‑only LLM, token‑ledger, caps, local cache.  
- **Local‑first →** provider=none by default; env toggle to enable LLM.

---

## 3) Decision Log (locked for MVP)
- **LLM default**: `provider=none`; **gate_policy**: `snippet_only`  
- **Snippet window**: ±2 sentences; **snippet_max_tokens** ≈ 220  
- **Budget**: hard cap tokens per doc; on exceed → `needs_review`  
- **Caching**: local SQLite cache by `(prompt_id, snippet_hash)`  
- **OCR**: off by default (opt‑in)

---

## 4) KPI & Quality Gates (MVP)
- **Latency**: p95 ≤ 60s (PDF ≤ 10 MB).  
- **Cost**: ≤ £0.10 per doc at default settings.  
- **Accuracy**: Precision ≥ 0.85, Recall ≥ 0.90 on gold set.  
- **Explainability**: ≥ 95% of findings include rule id + snippet.  
- **Coverage**: no undetected topic among the 8 detectors.

---

## 5) Detector Catalog (GDPR Art. 28(3) (a)–(h))
Eight detectors with acceptance wordings, weak language cues, red‑flags, evidence windows, and test examples.

> **Verdicts**: **Pass** (must‑include satisfied, no red‑flag), **Weak** (must‑include present but hedged), **Missing** (must‑include absent or contradicted), **Needs_review** (ambiguous/noisy).  
> **Evidence Window**: default ±2 sentences around anchor; configurable per detector.

### 5.1 A28(3)(a) — Controller Instructions Only
**Must‑include (any)**:  
- "only on documented instructions (of the Controller)"  
- "process personal data **only** on (the Controller’s) **documented/written** instructions"  
- variants: "documented written instructions", "unless required by law" (allowed carve‑out if notice given)

**Weak language (risk)**:  
- "commercially reasonable", "where practicable", "endeavour", "may" when tied to instruction compliance  

**Red‑flags**:  
- provider discretion to process without controller instructions  
- "subject solely to provider policies" overriding controller directions

**Tests (examples)**:  
- **Positive**: "Processor shall process personal data **only on documented instructions** of the Controller"  
- **Positive**: "…**only** on the Controller’s **written instructions**, unless required by Union or Member State law"  
- **Positive**: Heading "**Controller Instructions**" + sentence with "only on documented instructions"  
- **Hard negative**: "Processor **may** process personal data as necessary to operate its services" (no controller instruction)  
- **Hard negative**: "Processor follows **industry practices** and **policies**" (no controller instruction anchor)  
- **Hard negative**: "Processor will **endeavour** to follow Controller guidance" (hedged, no must‑include)

### 5.2 A28(3)(b) — Confidentiality of Authorised Persons
**Must‑include (all)**:  
- reference to "**persons authorised** to process personal data"  
- those persons are under "**confidentiality**" obligations (contractual or statutory)

**Weak language**: "industry standard", "reasonable efforts" to ensure confidentiality  
**Red‑flags**: confidentiality "where feasible" only; broad exceptions for "business purposes"

**Tests**: 3 positive + 3 hard negative in the same style as §5.1.

### 5.3 A28(3)(c) — Security Measures (Art. 32)
**Must‑include (anchor)**:  
- "appropriate **technical and organisational measures**" (TOMs) to ensure security per **Article 32**, or equivalent formulation  
- optional annex/link to TOMs

**Weak**: "commercially reasonable security" w/o TOM specifics  
**Red‑flags**: security "subject to change without notice"; no TOM commitment

**Tests**: 3 positive + 3 hard negative.

### 5.4 A28(3)(d) — Sub‑processors & Flow‑down
**Must‑include**:  
- **prior authorisation/notice** of sub‑processors (general or specific)  
- **flow‑down** obligations equivalent to processor terms (Art. 28(4))

**Weak**: "materially similar" obligations without equivalence; notice only after onboarding  
**Red‑flags**: unrestricted appointment; opt‑out only via termination with no alternative

**Tests**: 3 positive + 3 hard negative.

### 5.5 A28(3)(e) — Assist with Data Subject Rights (Arts. 12–23)
**Must‑include**:  
- "Processor shall **assist the Controller** in fulfilling obligations under Articles **12–23**" (or name rights)  
- response timing/information support

**Weak**: "reasonable efforts" only  
**Red‑flags**: assistance only if paid consulting or at processor’s sole discretion

**Tests**: 3 positive + 3 hard negative.

### 5.6 A28(3)(f) — Breach Notification without Undue Delay
**Must‑include**:  
- "**notify the Controller without undue delay**" upon personal data breach  
- (optional) content scope (nature, contact point, likely consequences, measures)

**Weak**: "notify within a reasonable time"; vague "as soon as practicable"  
**Red‑flags**: notify only if breach meets provider’s internal threshold; no timing promise

**Tests**: 3 positive + 3 hard negative.

### 5.7 A28(3)(g) — Return/Deletion at End of Services
**Must‑include**:  
- at end of provision, **delete or return** personal data (Controller choice)  
- deletion of **copies** unless law requires retention (with notice)

**Weak**: "periodically delete" without controller choice  
**Red‑flags**: retain for provider analytics by default; deletion only upon request with no default

**Tests**: 3 positive + 3 hard negative.

### 5.8 A28(3)(h) — Information & Audits
**Must‑include**:  
- "**make available all information** necessary to demonstrate compliance"  
- "**allow for and contribute to audits**, including inspections, conducted by the Controller or an auditor mandated by the Controller"

**Weak**: audits "subject to provider policies" without equivalence; only third‑party reports allowed  
**Red‑flags**: audits disallowed; only annual SOC2 allowed regardless of scope

**Tests**: 3 positive + 3 hard negative.

> **Note**: Each detector will carry *heading variants* (e.g., "Instructions", "Controller Directions"), *verb families* (shall/must), and *negation traps* (unless/except) in its pattern set.

---

## 6) Weak‑Language Lexicon v0 (seed)
Categorised cues that **soften** obligations. Used to downgrade to **Weak** unless accompanied by clear must‑include anchors.

- **Hedges**: commercially reasonable; reasonable efforts; industry standard; where practicable/feasible; as appropriate; to the extent possible; periodically  
- **Discretion**: may; at our discretion; subject to provider policies; if we deem necessary  
- **Ambiguity**: materially similar; substantially equivalent; generally consistent  
- **Timing vagueness**: as soon as practicable; within a reasonable time; from time to time

*(Weights can be added later; initial rule: one or more hedges near an anchor → downgrade to **Weak** unless a counter‑anchor is present.)*

---

## 7) Rulepack Skeleton (YAML)

```yaml
# rules/processor_obligations.yaml
meta:
  pack_id: art28_v1
  evidence_window_sentences: 2
  verdicts: [pass, weak, missing, needs_review]
  tokenizer: sentence

shared_lexicon:
  hedges: ["commercially reasonable", "reasonable efforts", "industry standard", "where practicable", "where feasible", "endeavour", "as appropriate", "periodically", "to the extent possible"]
  discretion: ["may", "at our discretion", "subject to provider policies", "if we deem necessary"]

# Detector (a)
detectors:
  - id: A28_3_a_instructions
    anchors_any:
      - "only on documented instructions"
      - "only on written instructions"
      - "process .* only on .* instructions"
    allow_carveouts:
      - "unless required by (Union|Member State) law"
    weak_nearby: { any: "@hedges" }
    redflags_any:
      - "subject to provider policies"
      - "at (our|its) discretion .* process personal data"

  - id: A28_3_b_confidentiality
    anchors_all:
      - "persons authorised"
      - "confidentiality"
    weak_nearby: { any: "@hedges" }
    redflags_any: ["where feasible", "business purposes"]

  - id: A28_3_c_security
    anchors_any:
      - "technical and organisational measures"
      - "Article 32"
    weak_nearby: { any: ["commercially reasonable security", "industry standard"] }
    redflags_any: ["subject to change without notice"]

  # …repeat for (d)–(h)
```

**Config extract (core‑config.yaml)**
```yaml
llm:
  provider: none
  gate_policy: snippet_only
  snippet_max_tokens: 220
budget:
  hard_cap_tokens_per_doc: 1500
  on_exceed: needs_review
cache:
  kind: sqlite
  key: [prompt_id, snippet_hash]
ocr:
  enabled: false
```

---

## 8) Gold Set & Measurement Plan
**Goal**: 10–20 contracts (public/synthetic). Label each detector with verdict + **snippet offsets** (page, char start/end) and rationale.

**Label Schema (JSON line)**
```json
{
  "doc_id": "acme_dpa_001",
  "detector": "A28_3_a_instructions",
  "verdict": "pass|weak|missing",
  "span": {"page": 7, "start": 1423, "end": 1562},
  "rationale": "only on documented instructions present"
}
```

**Scoring**
- Compute Precision/Recall per detector and macro‑averages.  
- Track p95 latency, tokens_per_doc, %docs_invoking_LLM, explainability rate.  
- Dashboard: “time‑to‑first‑insight” < 3 minutes target.

**Test Sets**
- **Positives**: 3+ per detector with clear anchors.  
- **Hard negatives**: 3+ per detector with look‑alike phrasing that fails must‑include.  
- **Ambiguous**: edge phrasing to calibrate `needs_review`.

---

## 9) Risks → Design Responses
- **Clause variance/oblique phrasing** → heading‑aware extraction; lexicon; later add tiny local classifier for ambiguous triage.  
- **Hallucination/over‑claim** → verify‑only prompts; never green without anchor + snippet.  
- **Token blow‑ups** → snippet‑only gates; hard caps; caching; OCR opt‑in.  
- **False reassurance** → conservative defaults; surface rule id + why.

---

## 10) Seven‑Day Slice (Analyst view)
- **Day 1–2**: repo skeleton; extractor draft; rulepack stubs (a)–(c); token ledger; cache; env toggles.  
- **Day 3**: gold set v1 + scorer; wire metrics (p95, tokens_per_doc, %LLM).  
- **Day 4–5**: detectors (d)–(h); weak‑language v0; report export; coverage meter.  
- **Day 6**: smoke eval; tighten rules; UX polish (evidence‑first table + filters).  
- **Day 7**: pilot; freeze KPIs; author “How we test”.

---

## 11) Open Decisions (now resolved)
1) Evidence window = **±2 sentences** (configurable).  
2) Verdict mapping policy locked (see §5 header note).  
3) Metrics wall = Latency p95, cost, tokens_per_doc, %LLM, explainability, coverage.

---

## 12) Hand‑Off Notes
**For PM**  
- Use Detector Catalog (§5) to author **Epics/Stories** per detector.  
- Include acceptance criteria tying UI findings to rule ids + snippet locations.  
- Non‑functional: enforce KPIs (§4) and cost/latency budgets.

**For Architect**  
- Lock stack (e.g., FastAPI + Postgres/Supabase; Next.js 14; Redis optional).  
- Provide **dev_load_always_files**: tech_stack.md, coding_standards.md, source_tree.md.  
- Expose config toggles from §7 (env‑driven).  
- Plan **job queue** for extraction & checks; export service.

**For PO**  
- Run master checklist for cohesion (PRD⇄Architecture⇄Detectors).  
- Approve the first story batch (2–3) for SM/Dev.

---

## 13) Appendices

### A) Acceptance‑Wording Table (compact view)
| Detector | Must‑Include (anchors) | Weak Cues | Red‑Flags |
|---|---|---|---|
| (a) Instructions | only on documented/written instructions; lawful carve‑out notice | commercially reasonable; where practicable; endeavour | provider discretion; subject to provider policies |
| (b) Confidentiality | authorised persons; confidentiality obligation | industry standard; reasonable efforts | where feasible only; business purposes exception |
| (c) Security | technical and organisational measures; Article 32 | commercially reasonable security; industry standard | subject to change without notice |
| (d) Sub‑processors | prior authorisation/notice; flow‑down equivalence | materially similar; post‑hoc notice | unrestricted appointment; terminate‑only |
| (e) DSAR Assist | assist controller under Arts. 12–23 | reasonable efforts | assistance at sole discretion; paid consulting only |
| (f) Breach Notice | notify without undue delay | as soon as practicable; within a reasonable time | internal threshold required; no timing promise |
| (g) Return/Delete | delete or return at end; delete copies | periodically delete | retain by default for analytics |
| (h) Audits/Info | make available info; allow & contribute to audits | subject to provider policies; only attestations | audits disallowed; SOC2 only regardless of scope |

### B) Story Seed Template (for SM)
```
id: 1.1
epic: Ingestion & Extraction
title: Basic upload, text extraction, and evidence windowing
status: draft
acceptance_criteria:
  - User uploads PDF/DOCX ≤10MB; server extracts text + page map
  - Evidence windows produced (±2 sentences) for matched anchors
  - Metrics logged: latency, tokens_per_doc (0 if no LLM)
subtasks:
  - API: POST /contracts (upload → job id); GET /jobs/{id}
  - Extractor: PDF→text, heading map, sentence index
  - Evidence: window builder (±2 sentences)
  - Tests: 3 pos/3 neg snippets fixture; latency budget test
```

### C) Change Log (init)
- v1: Initial analyst hand‑off pack.

