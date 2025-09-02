# Blackletter Systems

This repository contains the source code for the Blackletter Systems GDPR Vendor Contract Checker, a tool for automated legal document analysis.

This project is a monorepo containing:
- `apps/api`: The FastAPI backend.
- `apps/web`: The Next.js frontend.
- `apps/workers`: (Placeholder) Background job processors.
- `packages/shared`: (Placeholder) Shared code between applications.
- `tools/windows`: Development scripts for Windows environments.

## Quick Start (Windows)

### Prerequisites:
- Python 3.11+
- Node.js 20+ with pnpm (`npm install -g pnpm`)

### Backend Setup (API):

```powershell
# Create a virtual environment
py -3.11 -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install Python dependencies (create requirements.txt first)
# pip install -r apps/api/requirements.txt
```

### Frontend Setup (Web):

```bash
# Navigate to the web app directory
cd apps/web

# Install Node.js dependencies
pnpm install
```

### Run Development Servers:
From the repository root, run the main development script:

```powershell
.\tools\windows\dev.ps1
```

This will start the API on `http://localhost:8000` and the web app on `http://localhost:3000`.

## CI/CD

The continuous integration pipeline is defined in `.github/workflows/ci.yml`. It runs linting, testing, and build steps for both the frontend and backend on every pull request to `main`.
