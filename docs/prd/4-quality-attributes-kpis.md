# 4) Quality Attributes & KPIs
- **Latency**: p95 ≤ 60s end‑to‑end for ≤10MB PDF.  
- **Cost**: ≤ £0.10/document at defaults; token ledger visible per doc.  
- **Accuracy**: Precision ≥ 0.85; Recall ≥ 0.90 on Gold Set v1.  
- **Explainability**: ≥ 95% of findings include snippet + rule id.  
- **Coverage**: No undetected topic among the eight detectors for a compliant DPA.

**Security & Privacy**
- LLM **snippet‑only** gate; provider disabled by default.  
- No PII stored unless retention is explicitly enabled.  
- Signed URLs, server‑side scanning, minimal metadata.

**Accessibility**
- Keyboard navigable; adequate contrast; export readable by screen readers.

---
