# Story 0.2 — Landing Page Minimal (Dev Guide)
Status: Approved

Precise instructions to finish optional “How it works” links while preserving accessibility and performance.

## Scope
- Route: `/landing` (optional redirect from `/`)
- Files: `apps/web/src/app/landing/page.tsx`, `apps/web/src/content/landing.ts`

## Implementation
- Add “How it works” inline links:
  - If `process.env.NEXT_PUBLIC_USE_MOCKS === '1'`, render links to `/dashboard` and `/analyses/mock-1` near the How it works section.
  - Use `next/link`; include aria-labels; preserve tab order and visible focus.
- Ensure metadata in layout is correct (title/description/OG).

## Tests (RTL/Jest)
- Link presence only under demo flag; accessible names present; SSR safe.

## Commands
- `cd apps/web && npm run lint && npm run test && npm run dev`
