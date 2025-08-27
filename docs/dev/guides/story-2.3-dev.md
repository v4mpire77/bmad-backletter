# Story 2.3 — Weak Language Lexicon (Dev Guide)
Status: Approved

Apply weak-language post-processing to downgrade Pass→Weak unless counter-anchors present.

## Summary
Load lexicon terms and scan evidence windows; if weak term appears without a nearby counter-anchor, downgrade verdict to Weak.

## Allowed Repo Surface
- apps/api/blackletter_api/services/weak_lexicon.py
- apps/api/blackletter_api/rules/lexicons/** (data)
- apps/api/blackletter_api/services/detector_runner.py (hook-in)
- apps/api/blackletter_api/tests/unit/test_detector_mapping.py (extend cases)

## Implementation Steps
- Configurable toggle; normalize text (lowercase), exact term matching initial; optional stemming later.
- Counter-anchors: detector config may list terms that prevent downgrade.

## Tests (pytest)
- Terms trigger downgrade; counter-anchors prevent it; toggle-off path preserves original verdict.

