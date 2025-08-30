# Repository Guidelines

## Project Structure & Module Organization
- API: `apps/api/blackletter_api/` – FastAPI app with `models/`, `routers/`, `services/`, and versioned `rules/` (e.g., `rules/art28_v1.yaml`, `rules/lexicons/`).
- Tests: `apps/api/blackletter_api/tests/{unit,integration}/` – synthetic fixtures; mirror source paths in `test_*.py`.
- Docs: `docs/` – architecture and stories in `docs/stories/` (e.g., `1.1-upload-job-orchestration.md`).
- Agents: `web-bundles/agents/*.txt`, `web-bundles/teams/*.txt`, and `web-bundles/expansion-packs/**`.
- Tooling: `requirements.txt` (Python), `package.json` (Node tools incl. `bmad-method`).

## Build, Test, and Development Commands
- Setup (Windows PowerShell):
  ```powershell
  python -m venv .venv; .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
- Run API:
  ```powershell
  cd apps/api; uvicorn blackletter_api.main:app --reload
  # or from repo root
  uvicorn blackletter_api.main:app --reload --app-dir apps/api
  ```
- Python tests:
  ```powershell
  pytest apps/api/blackletter_api/tests -q
  # or
  python -m unittest discover -s apps/api/blackletter_api/tests
  ```

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indent; type hints required for public functions.
- Names: `snake_case` modules/functions, `PascalCase` classes; tests `test_*.py` mirroring source.
- Routers: one domain per module in `routers/`; include in `main.py` with `prefix="/api"`.
- Rulepacks: YAML under `rules/`; lexicons under `rules/lexicons/`.

## Testing Guidelines
- Coverage: target ≥80% on changed code; include happy path, edge cases, and errors.
- API testing: FastAPI `TestClient` (httpx).
- Naming: behavior-focused, e.g., `test_detector_runner_handles_empty_input()`.

## Commit & Pull Request Guidelines
- Commits: Conventional Commits, e.g., `feat(api): add rulepack loader`, `fix(rules): correct weak_language terms`.
- PRs: description, link a story in `docs/stories/`, include test evidence (commands/output), and screenshots for any UI changes. Update docs if API/routes or rulepacks change.

## Security & Configuration
- Secrets via env vars (e.g., `DATABASE_URL`) in `.env` (do not commit).
- Validate and sanitize uploads; avoid logging raw PII.
- Pin rulepack versions for determinism.

## Full-Stack Development
- Node tooling (from repo root):
  ```powershell
  npm test            # runs Python test runner via Node
  npm run test:ui     # runs Vitest UI tests (if present)
  npm run lint        # ESLint for automation scripts
  npm run format      # Prettier formatting
  npm run codex:bundle # generate/update agent bundles
  npm run codex:rules  # generate/update rules from Cursor
  npm run codex:all    # run both generators
  ```
- Bundles & teams live under `web-bundles/agents/` and `web-bundles/teams/`; expansion packs under `web-bundles/expansion-packs/`.
