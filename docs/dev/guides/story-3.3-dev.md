# Story 3.3 — Dashboard History (Dev Guide)
Status: Approved

List analyses with verdict summaries and navigation.

## Summary
Expose `/api/analyses?limit=&query=&verdict=` and build a searchable dashboard list with chips and link to details. Falls back to mocks when `NEXT_PUBLIC_USE_MOCKS=1`.

## Allowed Repo Surface
- apps/api/blackletter_api/routers/analyses.py (list endpoint)
- apps/api/blackletter_api/models/schemas.py (AnalysisSummary/VerdictCounts)
- apps/web/src/app/dashboard/page.tsx
- apps/web/src/components/VerdictBadge.tsx
- apps/web/test/components (render/interaction tests)

## Implementation Steps
- API list returns `{ items: [ {id, filename, created_at, size, verdicts } ], next? }` with basic filtering by `query` and `verdict`.
- Web renders table with filename, created date, size, verdict badges, and “Open” link to `/analyses/{id}`; empty state CTA to `/new`.
- Keep UI accessible: table headers, focus styles, aria labels on chips.

## Tests
- API: list response includes expected fields; filters by query and verdict.
- Web: renders rows; filters/search update view; empty state displayed when no data.

## Commands
- API: `pytest apps/api/blackletter_api/tests -q`
- Web: `cd apps/web && npm run lint && npm run test && npm run dev`

