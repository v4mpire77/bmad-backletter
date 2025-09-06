#!/usr/bin/env bash
# setup_codex_dev.sh — idempotent developer setup for the bmad-backletter repo
# Usage:
#   chmod +x scripts/setup_codex_dev.sh
#   ./scripts/setup_codex_dev.sh
# The script will:
# - create and activate a Python virtualenv at .venv
# - upgrade pip/tools and install Python requirements found in common locations
# - ensure pnpm is available and run `pnpm install` at workspace root and apps/web
# - copy .env.example -> .env if present (non-destructive)
# - print next steps and useful hints

set -euo pipefail
IFS=$'\n\t'

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "[setup] repo root: $REPO_ROOT"

# -- Optional system packages (commented out by default) --
# If you need system-level tools (lspci, build deps for cffi/libffi, or nvidia tools), uncomment and run with sudo.
# echo "Installing recommended system packages (requires sudo)..."
# sudo apt update
# sudo apt install -y build-essential libffi-dev libssl-dev python3-dev pciutils
# # If you want NVIDIA tools (nvidia-smi) on a machine with NVIDIA drivers, install the relevant package for your distro.
# # sudo apt install -y nvidia-utils-***

# -- Python virtualenv --
PYTHON_CMD="${PYTHON:-python3}"
VENV_DIR=".venv"

if [ ! -x "$PYTHON_CMD" ]; then
  echo "ERROR: $PYTHON_CMD not found on PATH. Install Python 3.10+ and retry." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "[setup] creating virtualenv at $VENV_DIR"
  $PYTHON_CMD -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "[setup] activated virtualenv: $(which python) (pyver: $(python -V 2>&1))"

pip install --upgrade pip setuptools wheel

# Install Python requirements from common locations if they exist
REQ_PATHS=( 
  "requirements.txt"
  "apps/api/requirements.txt"
  "blackletter/backend/requirements.txt"
  "blackletter/blackletter-upstream/requirements.txt"
)

for req in "${REQ_PATHS[@]}"; do
  if [ -f "$req" ]; then
    echo "[pip] installing from $req"
    pip install -r "$req"
  else
    echo "[pip] $req not found — skipping"
  fi
done

# -- Node dependency installation --
# Node module installer removed as part of cleanup

# Copy .env.example -> .env if .env doesn't exist
if [ -f .env ] ; then
  echo "[env] .env already exists — leaving it alone"
elif [ -f .env.example ]; then
  cp .env.example .env
  echo "[env] created .env from .env.example (please update secrets)"
else
  echo "[env] no .env or .env.example found — skip"
fi

# Create .data folders used by services if missing
mkdir -p .data/analyses

cat <<'EOF'

Setup completed. Next steps (recommended):

1) Activate the venv and run the dev servers:
   source .venv/bin/activate
   # Run backend API
   cd apps/api && uvicorn blackletter_api.main:app --reload --app-dir . &
   # Or run frontend
   cd apps/web && pnpm dev

2) Run tests (from repo root while venv is active):
   pytest -q apps/api/blackletter_api/tests

3) If Python packages that require system libs fail to build (e.g., cffi, numpy, torch), install the needed OS packages
   (e.g., build-essential, libffi-dev) and re-run this script's pip steps.

Notes:
- The script attempts to be idempotent and non-destructive. It will not auto-install kernel drivers or GPU drivers.
- If you need GPU tools (nvidia-smi) or PCI discovery (lspci), install pciutils and vendor packages with your package manager.

EOF

exit 0
