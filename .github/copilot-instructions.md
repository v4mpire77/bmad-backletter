# Blackletter Contract Analysis Platform
Blackletter is a contract analysis platform built with Python FastAPI backend and Next.js frontend using the BMAD methodology for automated GDPR compliance checking.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Build Process
- Bootstrap the repository:
  - `./scripts/setup.sh` (Unix/Linux) - takes **40 seconds**. NEVER CANCEL. Set timeout to 60+ minutes.
  - OR `pwsh -NoProfile -File setup.ps1` (Windows)
  - Creates Python virtual environment in `.venv`
  - Installs Python dependencies from `requirements.txt` 
  - Creates `.env` file if missing
- Frontend dependencies:
  - Install pnpm: `curl -fsSL https://get.pnpm.io/install.sh | sh -` 
  - `export PATH="$HOME/.local/share/pnpm:$PATH"`
  - `pnpm install` - takes **35 seconds**. NEVER CANCEL. Set timeout to 60+ minutes.
- Build applications:
  - `pnpm build` - takes **25 seconds**. NEVER CANCEL. Set timeout to 45+ minutes.
  - Frontend builds Next.js app with static export

### Running the Applications
- **CRITICAL**: Always activate Python environment first: `source .venv/bin/activate`
- Backend API (currently has Pydantic v2 compatibility issues):
  - `uvicorn blackletter_api.main:app --reload --app-dir apps/api`
  - Should run on http://localhost:8000
  - **WARNING**: Backend currently fails to start due to Pydantic v2 validator syntax issues
- Frontend development:
  - `pnpm dev` - starts Next.js dev server on http://localhost:3000
  - Includes mock data mode via `NEXT_PUBLIC_USE_MOCKS=1`

### Testing and Validation
- **ALWAYS** run these validation steps after changes:
- Frontend tests: `pnpm test` - takes **6 seconds**. NEVER CANCEL. Set timeout to 30+ minutes.
- Frontend type checking: `cd apps/web && pnpm typecheck` - takes **4 seconds**. NEVER CANCEL. Set timeout to 30+ minutes.
- Backend tests (when working): `python -m pytest apps/api/blackletter_api/tests -v`
- **MANUAL VALIDATION REQUIREMENT**: After changes, test the upload flow:
  1. Navigate to http://localhost:3000/new
  2. Test file upload interface
  3. Check contract analysis functionality
  4. Verify report generation at /reports

## Common Issues and Fixes

### Backend Issues
- **Pydantic v2 Compatibility**: The backend currently has validation syntax errors
  - Files affected: `apps/api/blackletter_api/models/rulepack_schema.py`
  - Error: `@validator` decorators need updating to Pydantic v2 syntax
  - Fix required before API can start
- **Import Path Issues**: Fixed relative imports in `services/rulepack_loader.py`
- **Configuration**: Requires `SECRET_KEY` in `.env` file

### Frontend Issues  
- **Build Artifacts**: `apps/web/out/` should be in `.gitignore` (already fixed)
- **Static Export**: Uses Next.js static export, middleware disabled
- **Mock Mode**: Set `NEXT_PUBLIC_USE_MOCKS=1` for demo without backend

## Validation Scenarios
After making changes, ALWAYS test these complete user scenarios:

### Frontend Scenario (Currently Working)
1. Start frontend: `pnpm dev`
2. Navigate to http://localhost:3000
3. Test navigation: Home -> New Upload -> Reports
4. Verify mock data displays correctly
5. Test responsive design on different viewport sizes

### Full Stack Scenario (Currently Blocked)
1. Fix backend Pydantic issues first
2. Start backend: `source .venv/bin/activate && uvicorn blackletter_api.main:app --reload --app-dir apps/api`
3. Start frontend: `pnpm dev` 
4. Test complete flow: Upload -> Analysis -> Results -> Export

## Project Structure

### Backend (`apps/api/blackletter_api/`)
- **FastAPI application** with modular structure
- `main.py` - Application entry point
- `models/` - Pydantic data models (needs v2 fixes)
- `routers/` - API endpoints (rules, analyses, findings, analysis)
- `services/` - Business logic (rulepack loader, analysis engine)
- `rules/` - YAML rulepacks (e.g., `art28_v1.yaml`)
- `tests/` - Unit and integration tests

### Frontend (`apps/web/`)
- **Next.js 14** application with TypeScript
- `src/app/` - App router pages (upload, analyses, reports)
- `src/components/` - React components (upload, tables, dialogs)
- Static export configuration for deployment

### Configuration
- **Python dependencies**: `requirements.txt` (includes all API requirements)
- **Node.js workspace**: `pnpm-workspace.yaml` with `package.json`
- **Environment**: `.env` file (requires `SECRET_KEY` for backend)

## Build Timing and Commands

### Measured Command Timings
All times measured with full environment setup:

| Command | Time | Timeout | Notes |
|---------|------|---------|--------|
| `./scripts/setup.sh` | 40s | 60+ min | NEVER CANCEL - Python environment setup |
| `pnpm install` | 35s | 60+ min | NEVER CANCEL - Downloads all dependencies |
| `pnpm build` | 25s | 45+ min | NEVER CANCEL - Builds Next.js static export |
| `pnpm test` | 6s | 30+ min | Frontend tests with Vitest |
| `pnpm typecheck` | 4s | 30+ min | TypeScript validation |

### Critical Timeout Settings
- **NEVER CANCEL** long-running commands - they are normal
- **Setup commands**: Always use 60+ minute timeouts
- **Build commands**: Always use 45+ minute timeouts  
- **Test commands**: Always use 30+ minute timeouts

## Development Workflow

### Making Changes
1. **ALWAYS** run bootstrap first: `./scripts/setup.sh`
2. Test current state: `pnpm test && pnpm typecheck`
3. Make minimal, surgical changes
4. **NEVER** delete working code unless absolutely necessary
5. Run validation after each change
6. Test complete user scenarios before completing

### Repository Management
- Follow conventional commits: `feat(api):`, `fix(frontend):`, etc.
- Update documentation when changing API routes or rulepacks
- Keep secrets in environment variables, never commit to git
- Pin dependency versions for deterministic builds

## Current Status Summary
- ✅ **Frontend**: Fully functional, builds and tests pass
- ✅ **Python Environment**: Setup working, dependencies installed  
- ✅ **Build Process**: All frontend build and test commands validated
- ⚠️ **Backend API**: Blocked by Pydantic v2 compatibility issues
- ⚠️ **Full Stack Testing**: Requires backend fixes first

**Next Priority**: Fix backend Pydantic v2 compatibility to enable full testing scenarios.