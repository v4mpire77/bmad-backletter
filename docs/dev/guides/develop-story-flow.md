# Develop-Story Flow (BMAD Dev Agent)
Status: Approved

This guide operationalizes the BMAD develop-story process so Devs can implement stories precisely and verifiably.

## Preconditions
- Story status Approved with clear AC: `docs/stories/{id}*.md`
- Env set: web and/or api dependencies installed
- Demo flag as needed: `NEXT_PUBLIC_USE_MOCKS=1`

## Allowed Story File Updates Only
- Checkboxes under Tasks/Subtasks
- Dev Agent Record: Agent Model Used, Debug Log, Completion Notes, File List
- Change Log entries (dated), Status (when ready-for-review)

## Workflow
- Read story → confirm AC → list minimal files to touch
- Implement targeted changes per AC (avoid unrelated edits)
- Add tests first or alongside
- Validate locally (lint + tests) and document evidence in story Dev Agent Record
- Mark checkboxes, update File List and Change Log, set status when done

## Commands (Windows PowerShell)
- Web: `cd apps/web; npm install; npm run lint; npm run test; npm run dev`
- API: `cd apps/api; pip install -r requirements.txt; uvicorn blackletter_api.main:app --reload`
- API tests: `pytest apps/api/blackletter_api/tests -q`

## Web Testing
- Unit/integration (RTL + Jest): `apps/web/test/**/*.test.tsx`
- Coverage: `npm run coverage`
- Accessibility: test roles, labels, ESC behavior, focus

## API Testing
- Unit/integration via pytest under `apps/api/blackletter_api/tests/{unit,integration}`
- Use synthetic fixtures; no real documents

## Ready-for-Review Checklist
- All AC verified by tests or manual evidence
- Lint clean; coverage ≥80% on changed code
- Story Dev Agent Record updated (checkboxes, File List, Change Log, Debug Log)
- Demo instructions/screenshots if applicable
