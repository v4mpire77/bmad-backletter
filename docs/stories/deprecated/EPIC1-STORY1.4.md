# Story 1.4: Environment & Dev Setup

**ID:** EPIC1-STORY1.4

**As a developer, I want a reproducible Windows-friendly setup so the whole team can run and test the system locally.**

## Tasks:
* Create a PowerShell setup script (`setup.ps1`).
* Create a `.env` file for all configuration variables.
* Update the `README.md` with clear setup instructions.

## Acceptance Criteria:
* A new developer can run `setup.ps1` and have a working local environment within 15 minutes.
* All secrets and API keys are stored in the `.env` file and not in the codebase.

## Test Fixtures:
* **Validation:** A fresh developer clone the repo and reports a successful setup.

## Artifacts:
* `setup.ps1`
* `README.md`

---

## Dev Agent Record

- Status: Ready for Review
- Agent Model Used: dev (James)

### Tasks / Subtasks Checkboxes
- [x] Create PowerShell setup script (`setup.ps1`) to automate venv creation, dependency install, `.env` creation, and data folder prep.
- [x] Provide `.env` defaults and placeholders via `.env.example`.
- [x] Update `README.md` with clear Windows quick-start and environment variable guidance.

### Debug Log References
- `.venv\\Scripts\\python.exe -m pip --version`
- `.venv\\Scripts\\python.exe -m pytest apps/api/blackletter_api/tests -q`
- `uvicorn blackletter_api.main:app --reload --app-dir apps/api`

### Completion Notes
- New developers can run `pwsh -NoProfile -File .\setup.ps1` to prepare the environment in minutes.
- All secrets and configuration are sourced from `.env` (not committed).
- Script prints next-step commands for running API and tests.

### File List
- Added: `setup.ps1`
- Modified: `.env.example`
- Modified: `README.md`

### Change Log
- chore(devx): add Windows setup script and environment guidance
- docs(readme): document setup flow and runtime toggles
