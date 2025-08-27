# Story 2.4 — Token Ledger & Caps (Dev Guide)
Status: Approved

Track tokens per analysis and enforce hard caps; expose metrics.

## Summary
Thread-safe per-analysis ledger accumulating token usage (when LLM enabled). If cap exceeded, set needs_review with reason. Provide admin metrics aggregate.

## Allowed Repo Surface
- apps/api/blackletter_api/services/token_ledger.py
- apps/api/blackletter_api/services/metrics.py
- apps/api/blackletter_api/routers/admin.py or routers/admin_metrics.py
- apps/api/blackletter_api/tests/integration/test_caps_metrics.py (exists, skipped)

## Implementation Steps
- Env: `TOKEN_CAP_PER_DOC` default 20000; `LLM_ENABLED=false` default.
- Accumulate counts via wrapper around provider calls; if exceeds cap, mark analysis state and annotate findings or job.
- Metrics: compute tokens_per_doc average and expose via admin endpoint.

## Tests (pytest)
- Unit: accumulation logic; cap breach sets needs_review; disabled LLM path is no-op.
- Integration: metrics endpoint returns fields; skipped test can be enabled.

