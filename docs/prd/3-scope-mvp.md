# 3) Scope (MVP)
**In‑Scope Functionalities**
1. **File Ingestion**: Upload PDF/DOCX ≤10MB. Async job model with progress.  
2. **Text Extraction & Indexing**: Extract text with **page map + sentence index**; OCR optional (off by default).  
3. **Rule‑Driven Detection**: Run rulepack **art28_v1** across indexed text; compute verdicts per detector.  
4. **Findings UI**: Table/cards with **R/A/G**-style coloring mapped to Pass/Weak/Missing (+ Needs review). Filters, search, and per‑finding detail panel (snippet, rule id, rationale).  
5. **Report Export**: PDF/HTML export with headings, findings, snippets, and metadata.  
6. **History**: Per‑org list of prior analyses with basic metadata (filename, date, verdict summary).  
7. **Settings**: Toggle LLM provider (default **none**), OCR on/off, retention policy, and token budget.

**Out of Scope (MVP)**
- Redline suggestions; vendor compare; cross‑document diffs.  
- Multi‑language contracts; deep PII discovery.  
- SSO & granular RBAC beyond Admin/Reviewer.

---
