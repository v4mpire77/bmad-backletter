# Always‑On Dev Guide (BMAD Blackletter)

Use this as your quick‑start and navigation map. It outlines agent flows, the Scrum Master + Dev cycle, core commands, and where to find the spec “shards” across the repo.

## Quick Commands

- Web dev: `cd apps/web && pnpm install && pnpm dev` (open http://localhost:3000)
- Web lint/tests: `pnpm lint` • `pnpm test` • `pnpm coverage`
- Demo mode: copy `apps/web/.env.example` to `.env.local` and keep `NEXT_PUBLIC_USE_MOCKS=1`
- API dev: `cd apps/api && uvicorn blackletter_api.main:app --reload`
- API tests: `pytest apps/api/blackletter_api/tests -q`

## Agent Flows (1–5)

- 1 — Orchestrator: entrypoint to BMAD roles and workflows
  - Agent: `web-bundles/teams/team-ide-minimal.txt` (bmad-orchestrator section)
  - What: choose role, list commands, guide workflow

- 2 — Product Owner (PO): backlog, stories, AC
  - Agent: `web-bundles/agents/po.txt`
  - Templates/specs: `docs/prd/8-detailed-story-templates-for-sm-dev.md`
  - Key commands: create‑story, validate‑story‑draft

- 3 — Scrum Master (SM): prepare executable story
  - Agent: `web-bundles/agents/sm.txt`
  - Tasks/checklists: `.bmad-core/tasks/*` surfaced inside the agent file
  - Key commands: draft (create‑next‑story), story‑checklist

- 4 — Developer (Dev): implement story via develop‑story flow
  - Agent: `web-bundles/agents/dev.txt`
  - Key commands: develop‑story, run‑tests, review‑qa, explain
  - Only update allowed sections in `docs/stories/*.md` (Dev Agent Record, file list, change log, checkboxes)

- 5 — QA: validate, gate, and feed fixes
  - Agent: `web-bundles/agents/qa.txt`
  - QA gates/assessments (when present): `docs/project/qa/**`

## Scrum Master + Dev Cycle (6–7)

- 6 — SM Cycle
  - Refine story from PRD/architecture; ensure AC are testable
  - Run story checklist; link impacted docs
  - Handoff: set story Status to Approved for Dev when ready

- 7 — Dev Cycle
  - Pick story → open `docs/stories/{id}*.md`
  - Implement against AC; keep changes minimal and focused
  - Add/execute tests; update Dev Agent Record: file list, change log, checkboxes
  - Demo and ready‑for‑review when lint/tests pass and docs updated

## Spec Shards Map (where to look)

- Stories: `docs/stories/*.md` (ID‑prefixed, e.g., `0.0`, `1.1`, `2.2`)
- PRD: `docs/prd/*.md` (vision, scope, story templates, DoR/DoD)
- Architecture: `docs/architecture/*.md` + diagrams (`*.mmd`)
- API (FastAPI):
  - App: `apps/api/blackletter_api/`
  - Routers: `apps/api/blackletter_api/routers/*.py`
  - Models: `apps/api/blackletter_api/models/*.py`
  - Services: `apps/api/blackletter_api/services/*.py`
  - Rules & lexicons: `apps/api/blackletter_api/rules/**` (e.g., `art28_v1.yaml`, `lexicons/`)
  - Tests: `apps/api/blackletter_api/tests/{unit,integration}`
- Web (Next.js):
  - Routes: `apps/web/src/app/**/page.tsx`
  - Components: `apps/web/src/components/*.tsx`
  - Mocks/anchors: `apps/web/src/lib/{mocks,anchors}.ts`
  - Demo env: `apps/web/.env.example`
- BMAD Agents/Teams: `web-bundles/agents/*.txt`, `web-bundles/teams/*.txt`

## Develop‑Story Cheatsheet (Dev agent)

- Pick story → open `docs/stories/{id}*.md`
- Implement minimal changes scoped to AC
- Add tests (≥80% coverage on changed code)
- Validate: `npm run lint` • `npm run test` (web), `pytest` (api)
- Update story Dev Agent Record sections only (checkboxes, file list, change log, notes)
- Stop when “ready for review” criteria met

## Useful Paths

- Landing content: `apps/web/src/content/landing.ts`
- Landing page: `apps/web/src/app/landing/page.tsx`
- Demo flow: `apps/web/src/app/dashboard/page.tsx`, `apps/web/src/app/analyses/[id]/page.tsx`, `apps/web/src/app/reports/page.tsx`
- Demo a11y tests: `apps/web/test/components/*.test.tsx`

## Environment & Security

- Env vars via `.env` files; never commit real secrets
- Demo flag: `NEXT_PUBLIC_USE_MOCKS=1` for deterministic UI
- Validate/sanitize uploads (API); avoid PII in logs

## SM/Dev Prompt Library

Use these copy‑paste prompts to drive the BMAD workflow without touching code until Dev mode. They are Windows‑friendly and reference PowerShell helpers when present (see `scripts\ps*.ps1`).

### SM Planning Prompt (once per story)

```
Scrum Master mode. Story 1.1 Upload & Job Orchestration. Produce STORY_PACKET.md + TEST_PLAN.md.
HARD CAPS:

Do not change any code files.

Output only docs and stub paths.

Reference Windows scripts (scripts\ps*.ps1).

Repo allowlist for this story:

apps/api/blackletter_api/routers/uploads.py
apps/api/blackletter_api/services/tasks.py
apps/api/blackletter_api/models/entities.py
apps/web/src/app/new/page.tsx
tests/unit/api/test_uploads.py
tests/integration/test_upload_flow.py

Return: REPO_MAP (short), STORY_PACKET.md, TEST_PLAN.md.
```

Expected outputs (docs only):
- `docs/dev/templates/STORY_PACKET.md` (use as template)
- `docs/dev/templates/TEST_PLAN.md` (use as template)
- `docs/dev/templates/REPO_MAP.md` (fill with allowlisted file paths)

### Dev Patch Prompt (run repeatedly, one file at a time)

```
Dev mode. Implement only one file for Story 1.1:
Target file: apps/api/blackletter_api/routers/uploads.py
HARD CAPS:

Max 1 file touched.

Max 120 changed lines.

Use FastAPI router; validate PDF/DOCX ≤10MB; return { job_id, analysis_id, status:'queued' }.

No business logic in router; call services/tasks.enqueue('analyze', {analysis_id}).

Leave TODO markers where future stories fill in details.
After patch, print a short TEST PLAN snippet and stop.
```

Tip: For each subsequent file, re‑issue the Dev Patch Prompt with the new `Target file:` while keeping the same constraints and Story ID.

## Deep Dives

- Dev Guides Index: `docs/dev/guides/index.md` (per‑story developer specs)
- Develop‑Story Flow: `docs/dev/guides/develop-story-flow.md`
