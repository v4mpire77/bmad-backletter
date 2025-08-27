# Story 2.1 — Rulepack Loader (Dev Guide)
Status: Approved

Load and validate `rules/art28_v1.yaml` and lexicons under `rules/lexicons/`.

## Summary
Provide a deterministic loader with schema validation and error reporting. Expose detectors and shared lexicon.

## Allowed Repo Surface
- apps/api/blackletter_api/services/rulepack_loader.py
- apps/api/blackletter_api/rules/** (data)
- apps/api/blackletter_api/tests/unit/test_rulepack_loader.py (exists)
- Optional API: apps/api/blackletter_api/routers/rules.py (already present)

## Implementation Steps
- Schema: detectors[{ id, anchors_any?, anchors_all?, redflags_any? }], shared_lexicon: { name: [terms...] }.
- Validate YAML; on error, raise with precise path; disallow unknown top-level keys in strict mode.
- Provide `load_rulepack(path) -> Rulepack` and cache in memory; disable hot-reload in prod.

## Tests (pytest)
- Happy load; invalid YAML; missing required fields; unknown lexicon referenced.

