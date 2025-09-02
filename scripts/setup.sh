#!/usr/bin/env bash
set -euo pipefail

# Blackletter Dev Setup (macOS/Linux)
# Mirrors setup.ps1 tasks: create virtualenv, install dependencies, install pre-commit hooks.

usage() {
  cat <<USAGE
Usage: $0 [--recreate-venv]

Creates local Python virtual environment, installs dependencies from requirements.txt,
and installs pre-commit hooks.

Options:
  --recreate-venv   Remove existing .venv before creating it
  -h, --help        Show this help message and exit
USAGE
}

if [[ "${1-}" == "-h" || "${1-}" == "--help" ]]; then
  usage
  exit 0
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PYTHON="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON" ]]; then
  echo "Python not found. Install Python 3.11+ and ensure it is on PATH." >&2
  exit 1
fi

if ! "$PYTHON" -m pip --version >/dev/null 2>&1; then
  echo "pip not found for $PYTHON. Install pip and retry." >&2
  exit 1
fi

VENV="$REPO_ROOT/.venv"
if [[ -d "$VENV" && "${1-}" == "--recreate-venv" ]]; then
  echo "[!] Recreating virtual environment..."
  rm -rf "$VENV"
fi

if [[ ! -d "$VENV" ]]; then
  echo "[>] Creating virtual environment at $VENV"
  "$PYTHON" -m venv "$VENV"
  echo "[✓] Virtual environment created"
else
  echo "[✓] .venv already exists"
fi

PIP="$VENV/bin/pip"
PY="$VENV/bin/python"

if [[ ! -x "$PIP" ]]; then
  echo "pip executable not found in .venv. Did venv creation fail?" >&2
  exit 1
fi

echo "[>] Upgrading pip"
"$PY" -m pip install --upgrade pip

echo "[>] Installing Python dependencies from requirements.txt"
"$PIP" install -r "$REPO_ROOT/requirements.txt"

echo "[>] Installing pre-commit"
"$PIP" install pre-commit

if [[ -f "$REPO_ROOT/.pre-commit-config.yaml" ]]; then
  echo "[>] Installing pre-commit hooks"
  "$VENV/bin/pre-commit" install
else
  echo "[!] No .pre-commit-config.yaml found, skipping hook installation"
fi

echo "[✓] Setup complete."
echo "Next steps:"
echo "  1) Activate venv: source .venv/bin/activate"
echo "  2) Run API: uvicorn blackletter_api.main:app --reload --app-dir apps/api"
echo "  3) (Optional) Run tests: python -m pytest apps/api/blackletter_api/tests -q"
