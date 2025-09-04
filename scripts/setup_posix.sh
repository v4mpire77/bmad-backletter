#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[x] Setup failed" >&2' ERR

# Usage:
#   ./scripts/setup_posix.sh [--recreate-venv] [--skip-install]

recreate_venv=false
skip_install=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --recreate-venv) recreate_venv=true ;;
    --skip-install) skip_install=true ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

write_step(){ echo "[>] $1"; }
write_ok(){ echo "[✓] $1"; }
write_warn(){ echo "[!] $1"; }

# Determine repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Detect python
write_step "Detecting Python..."
if command -v python3 >/dev/null 2>&1; then
  python=python3
elif command -v python >/dev/null 2>&1; then
  python=python
else
  echo "Python not found. Install Python 3.11+ and ensure it is on PATH." >&2
  exit 1
fi
write_ok "Using $($python --version)"

venv_path="$REPO_ROOT/.venv"
if [[ -d "$venv_path" && $recreate_venv == true ]]; then
  write_warn "Recreating virtual environment..."
  rm -rf "$venv_path"
fi

if [[ ! -d "$venv_path" ]]; then
  write_step "Creating virtual environment at .venv"
  "$python" -m venv "$venv_path"
  write_ok "Virtual environment created"
else
  write_ok ".venv already exists"
fi

pip="$venv_path/bin/pip"
py="$venv_path/bin/python"
if [[ ! -x "$pip" ]]; then
  echo "pip executable not found in .venv. Did venv creation fail?" >&2
  exit 1
fi

if [[ $skip_install != true ]]; then
  write_step "Upgrading pip"
  "$py" -m pip install --upgrade pip
  write_step "Installing Python dependencies from requirements.txt"
  "$pip" install -r "$REPO_ROOT/requirements.txt"
  write_ok "Dependencies installed"
else
  write_warn "Skipping dependency install by request"
fi

env_file="$REPO_ROOT/.env"
env_example="$REPO_ROOT/.env.example"
write_step "Ensuring .env exists"
if [[ ! -f "$env_file" ]]; then
  if [[ -f "$env_example" ]]; then
    cp "$env_example" "$env_file"
    write_ok "Created .env from .env.example"
  else
    cat > "$env_file" <<'ENVEOF'
CORS_ORIGINS=*
DATA_ROOT=.data
JOB_SYNC=0
ANALYSES_FS_ENABLED=0
# DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/blackletter
ENVEOF
    write_ok "Created .env with defaults"
  fi
else
  write_ok ".env already present"
fi

write_step "Ensuring data directories exist"
mkdir -p "$REPO_ROOT/.data/analyses"
write_ok "Data folders ready at .data/analyses"

echo
write_ok "Setup complete."
echo
cat <<'MSG'
Next steps:
  1) Activate venv: source .venv/bin/activate
  2) Run API: uvicorn blackletter_api.main:app --reload --app-dir apps/api
  3) (Optional) Run tests: .venv/bin/python -m pytest apps/api/blackletter_api/tests -q

Toggles:
  JOB_SYNC=1 (synchronous jobs)
  ANALYSES_FS_ENABLED=1 (list analyses from filesystem)
MSG
