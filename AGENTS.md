# Repository Guidelines

## Project Structure & Modules
- API: `apps/api/blackletter_api/` — FastAPI app with `models/`, `routers/`, `services/`, `rules/` (e.g., `rules/art28_v1.yaml`, `rules/lexicons/`), and `tests/{unit,integration}/`.
- Docs: `docs/` — architecture, PRD, and MVP stories in `docs/stories/` (e.g., `1.1-upload-job-orchestration.md`, `2.2-detector-runner.md`).
- Agent Bundles: `web-bundles/agents/*.txt` and `web-bundles/expansion-packs/**` — role instructions and teams.
- Tooling: `requirements.txt` (Python deps), `package.json` (bundled `bmad-method`).

## Build, Run, and Test
- Setup (Windows PowerShell):
  - `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
  - `pip install -r requirements.txt`
- Run API (choose one):
  - `cd apps/api && uvicorn blackletter_api.main:app --reload`
  - Or from repo root: `uvicorn blackletter_api.main:app --reload --app-dir apps/api`
- Tests:
  - Place tests under `apps/api/blackletter_api/tests/{unit,integration}`.
  - If using pytest: `pytest apps/api/blackletter_api/tests -q`
  - If using unittest: `python -m unittest discover -s apps/api/blackletter_api/tests`

## Coding Style & Naming
- Python: PEP 8, 4‑space indent, type hints required for public functions.
- Names: `snake_case` for modules/functions, `PascalCase` for classes; tests `test_*.py` mirroring source paths.
- API routers: one module per domain under `routers/` (e.g., `uploads.py`, `jobs.py`), included in `main.py` with `prefix="/api"`.
- Rulepacks: versioned YAML in `rules/` (e.g., `art28_v1.yaml`), lexicons under `rules/lexicons/`.

## Testing Guidelines
- Aim for ≥80% coverage on changed code; include happy path, edge cases, and error handling.
- Use FastAPI `TestClient` (httpx) for API tests; fixture data must be synthetic (no real contracts).
- Name tests by behavior: `test_detector_runner_handles_empty_input()`.

## Commit & Pull Request Guidelines
- Commits: follow Conventional Commits, e.g., `feat(api): add rulepack loader` or `fix(rules): correct weak_language terms`.
- PRs: include description, linked story (`docs/stories/*.md`), test evidence (commands/output), and screenshots for any UI changes.
- Update docs if API routes, rulepacks, or story scope change.

## Security & Configuration
- Keep secrets in environment variables (e.g., `DATABASE_URL`, provider keys) via `.env` (do not commit).
- Validate and sanitize uploads; never store raw PII in logs.
- Pin rulepack versions explicitly in code/config to ensure determinism.

## Dev Agent Notes
- See `web-bundles/agents/dev.txt`. Implement stories strictly via the “develop-story” flow; update only the allowed Dev Agent Record sections in story files; present numbered options when offering choices.


## Automation Pack Baseline

- Tests & lint must pass before merge.
- No secrets/plaintext keys. Never commit .env or certs.
- PR title format: [Area] summary; labels area:* size:* risk:*
- Always mention @codex on PRs (workflow auto-injects).
- Merge: squash after green + CODEOWNER approval.
