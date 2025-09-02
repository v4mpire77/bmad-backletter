#!/usr/bin/env bash
set -e

# Blackletter Dev Setup (macOS/Linux)
# Usage: ./scripts/setup.sh [--recreate-venv] [--skip-install]
# - Creates a local Python virtual environment in .venv
# - Installs Python dependencies from requirements.txt
# - Copies .env.example -> .env if missing
# - Creates local data folders under .data/analyses
# - Prints handy dev commands

RECREATE_VENV=false
SKIP_INSTALL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recreate-venv)
      RECREATE_VENV=true
      ;;
    --skip-install)
      SKIP_INSTALL=true
      ;;
  esac
  shift
done

write_step() { echo -e "[>] $1"; }
write_ok()   { echo -e "[\u2713] $1"; }
write_warn() { echo -e "[!] $1"; }

write_step "Detecting Python..."
PYTHON=$(command -v python3 || command -v python || true)
if [[ -z "$PYTHON" ]]; then
  echo "Python not found. Install Python 3.11+ and ensure it is on PATH."
  exit 1
fi
write_ok "Using $($PYTHON --version)"

VENV_DIR=".venv"
if [[ -d "$VENV_DIR" && "$RECREATE_VENV" == true ]]; then
  write_warn "Recreating virtual environment..."
  rm -rf "$VENV_DIR"
fi

if [[ ! -d "$VENV_DIR" ]]; then
  write_step "Creating virtual environment at $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
  write_ok "Virtual environment created"
else
  write_ok "$VENV_DIR already exists"
fi

PIP="$VENV_DIR/bin/pip"
PY="$VENV_DIR/bin/python"
if [[ ! -x "$PIP" ]]; then
  echo "pip executable not found in $VENV_DIR. Did venv creation fail?"
  exit 1
fi

if [[ "$SKIP_INSTALL" == false ]]; then
  write_step "Upgrading pip"
  "$PY" -m pip install --upgrade pip
  write_step "Installing Python dependencies from requirements.txt"
  "$PIP" install -r requirements.txt
  write_ok "Dependencies installed"
else
  write_warn "Skipping dependency install by request"
fi

write_step "Ensuring .env exists"
if [[ ! -f .env ]]; then
  if [[ -f .env.example ]]; then
    cp .env.example .env
    write_ok "Created .env from .env.example"
  else
    cat <<'ENV' > .env
CORS_ORIGINS=*
DATA_ROOT=.data
JOB_SYNC=0
ANALYSES_FS_ENABLED=0
# DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/blackletter
ENV
    write_ok "Created .env with defaults"
  fi
else
  write_ok ".env already present"
fi

write_step "Ensuring data directories exist"
mkdir -p .data/analyses
write_ok "Data folders ready at .data/analyses"

echo
echo "Next steps:"
echo "  1) Activate venv: source .venv/bin/activate"
echo "  2) Run API: uvicorn blackletter_api.main:app --reload --app-dir apps/api"
echo "  3) (Optional) Run tests: .venv/bin/python -m pytest apps/api/blackletter_api/tests -q"
echo
echo "Toggles:"
echo "  JOB_SYNC=1 (synchronous jobs)"
echo "  ANALYSES_FS_ENABLED=1 (list analyses from filesystem)"
