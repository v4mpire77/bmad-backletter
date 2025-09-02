# Story 3.1 — Findings Table (UI) (Dev Guide)
Status: Approved

Accessible findings UI with verdict filters, search, and evidence drawer.

## Summary
Render 8 detector rows with verdict colors, short rationale, and accessible interactions. Uses API when mocks disabled.

## Allowed Repo Surface
- apps/web/src/components/{FindingsTable,EvidenceDrawer,VerdictBadge}.tsx
- apps/web/src/app/analyses/[id]/page.tsx
- apps/web/src/lib/{mocks,anchors}.ts
- apps/web/test/components/*.test.tsx

## Implementation Steps
- Table semantics with role/table headers; filter by verdict, search across snippet/rationale/detector.
- Drawer with snippet highlight, copy, and Reviewed badge (client state) plus ESC close and aria bindings.
- Chips with ARIA labels for counts.

## Tests (RTL/Jest)
- Filter/search behavior; empty state; drawer ESC; chip ARIA labels present.

