# Story 2.2 — Detector Runner (Dev Guide)
Status: Approved

Produce detector verdicts and evidence by evaluating anchors/flags within evidence windows.

## Summary
Integrate extraction + windows + rulepack to emit findings and summary counts. Persist `findings.json` and support API reads.

## Allowed Repo Surface
- apps/api/blackletter_api/services/detector_runner.py
- apps/api/blackletter_api/services/{extraction,evidence}.py
- apps/api/blackletter_api/services/rulepack_loader.py
- apps/api/blackletter_api/routers/analyses.py (endpoints list/detail/findings — already present)
- apps/api/blackletter_api/tests/unit/test_detector_mapping.py (exists)

## Implementation Steps
- For each detector: check anchors_any/all present within window; if redflags_any present, downgrade.
- Verdict mapping: pass | weak | missing | needs_review (reserve needs_review for external caps/ambiguous cases).
- Build Finding: detector_id, rule_id, verdict, snippet, page, start, end, rationale; accumulate VerdictCounts.
- Persist `.data/analyses/{id}/findings.json` and `analysis.json` verdict summary.

## Tests (pytest)
- 3 positive + 3 hard negatives for detectors a–c minimum; rationale messages; offsets/snippets plausible.

