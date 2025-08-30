# Repository Guidelines

## Project Structure & Module Organization
- API: `apps/api/blackletter_api/` — FastAPI app with `models/`, `routers/`, `services/`, `rules/` (e.g., `rules/art28_v1.yaml`, `rules/lexicons/`).
- Tests: `apps/api/blackletter_api/tests/{unit,integration}/` — keep fixtures synthetic; mirror source paths in `test_*.py`.
- Docs: `docs/` — architecture and stories in `docs/stories/` (e.g., `1.1-upload-job-orchestration.md`, `2.2-detector-runner.md`).
- Agents: `web-bundles/agents/*.txt` and `web-bundles/expansion-packs/**` — role instructions and teams.
- Tooling: `requirements.txt` (Python deps), `package.json` (bundled utilities like `bmad-method`).

## Build, Test, and Development Commands
- Setup (Windows PowerShell):
  ```powershell
  python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1
  pip install -r requirements.txt
  ```
- Run API:
  ```powershell
  cd apps/api; uvicorn blackletter_api.main:app --reload
  # or from repo root
  uvicorn blackletter_api.main:app --reload --app-dir apps/api
  ```
- Tests (choose one):
  ```powershell
  pytest apps/api/blackletter_api/tests -q
  # or
  python -m unittest discover -s apps/api/blackletter_api/tests
  ```

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent; type hints required for public functions.
- Names: `snake_case` for modules/functions, `PascalCase` for classes; tests `test_*.py` mirroring source.
- Routers: one module per domain in `routers/`; include in `main.py` with `prefix="/api"`.
- Rulepacks: versioned YAML under `rules/`; lexicons in `rules/lexicons/`.

## Testing Guidelines
- Coverage: target ≥80% on changed code; include happy path, edge cases, and error handling.
- Frameworks: FastAPI `TestClient` (httpx) for API-level tests.
- Naming: behavior-focused, e.g., `test_detector_runner_handles_empty_input()`.

## Commit & Pull Request Guidelines
- Commits: Conventional Commits, e.g., `feat(api): add rulepack loader`, `fix(rules): correct weak_language terms`.
- PRs: clear description, link relevant story in `docs/stories/`, attach test evidence (commands/output), and screenshots for any UI changes. Update docs when API routes, rulepacks, or story scope change.

## Security & Configuration
- Secrets via environment variables (e.g., `DATABASE_URL`) in `.env` (do not commit).
- Validate/sanitize uploads; avoid logging raw PII.
- Pin rulepack versions explicitly for determinism.

## Dev Agent Notes
- See `web-bundles/agents/dev.txt`. Implement stories via the “develop-story” flow only.
- Update only allowed Dev Agent Record sections in story files.
- When presenting choices, provide clear, numbered options.
