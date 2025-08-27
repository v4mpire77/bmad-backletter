# Story 0.1 — Job Status Mock (Dev Guide)
Status: Approved

Client‑only upload simulation with a stepper and keyboard controls.

## Scope
- Route: `/new`
- Components: DropZone/Picker, Stepper, controls (Resume/Cancel/Start over)
- State machine: queued → extracting → detecting → reporting → done (~0.9s each in demo)

## Implementation
- ESC cancels simulation; visible focus rings; aria labels on stepper items
- On Done, CTA to `/analyses/mock-1` using `next/link`

## Tests (RTL/Jest)
- Advance on timer; Cancel resets running; Start over resets to initial
- a11y: role/labels for progress UI and keyboard handling

## Commands
- `cd apps/web && npm run lint && npm run test && npm run dev`
