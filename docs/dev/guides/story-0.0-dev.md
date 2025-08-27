# Story 0.0 — Demo Mock Contract Flow (Dev Guide)
Status: Approved

Authoritative spec for the mock‑only demo flow. No backend.

## Scope
- Routes: `/dashboard`, `/analyses/mock-1`, `/reports`
- Components: FindingsTable, EvidenceDrawer, VerdictChips, ExportDialog, DemoBanner
- Mocks: `src/lib/mocks.ts`, `src/lib/anchors.ts`, `src/lib/mockStore.ts`
- Env gate: `NEXT_PUBLIC_USE_MOCKS=1`

## Implementation
- Dashboard lists seeded ACME_DPA_MOCK.pdf (id `mock-1`), chips visible, link to findings
- Findings shows 8 detectors a–h, rationale, filter/search, drawer with highlights, copy, mark reviewed (local)
- ExportDialog logs options and navigates to `/reports` (mock store)
- Reports lists latest export from mock store

## A11y
- ESC closes dialog/drawer; `aria-modal` + `aria-labelledby`
- ARIA labels on verdict chips and table filters

## Tests (RTL/Jest)
- Dialog ESC + focus, Drawer ESC + highlight marks, Table filter/empty‑state, Chip ARIA labels

## Commands
- `cd apps/web && npm run lint && npm run test && npm run dev`
