#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "[devcontainer setup] Creating Python venv at .venv using python3..."
if [ -d ".venv" ]; then
  echo "[devcontainer setup] .venv already exists — skipping venv creation"
else
  python3 -m venv .venv
  echo "[devcontainer setup] venv created"
fi

# Activate for installs
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

if [ -f "requirements.txt" ]; then
  echo "[devcontainer setup] Installing Python requirements from requirements.txt"
  pip install -r requirements.txt || echo "[devcontainer setup] pip install failed — continuing"
else
  echo "[devcontainer setup] No requirements.txt found — skipping Python deps"
fi

# Node workspace installs (web app)
if [ -f "web/package.json" ]; then
  echo "[devcontainer setup] Installing Node deps in ./web"
  if command -v npm >/dev/null 2>&1; then
    (cd web && npm install) || echo "[devcontainer setup] npm install failed in web/ — continuing"
  else
    echo "[devcontainer setup] npm not found — skipping web npm install"
  fi
fi

# Install repo global CLIs that are safe to install
echo "[devcontainer setup] Installing recommended global CLIs if available: bmad-method"
if command -v npm >/dev/null 2>&1; then
  npm install -g bmad-method || echo "[devcontainer setup] npm global install bmad-method failed — continuing"
else
  echo "[devcontainer setup] npm not available — skipping global npm installs"
fi

# Optional: try to install gemini CLI if npm is present (best-effort)
if command -v npm >/dev/null 2>&1; then
  echo "[devcontainer setup] Attempting best-effort install of @google/gemini-cli (optional)"
  npm install -g @google/gemini-cli || echo "[devcontainer setup] gemini CLI install failed — it's optional"
fi

# Create a .vscode devcontainer recommended workspace settings if missing
mkdir -p .vscode
cat > .vscode/settings.json <<'JSON'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
JSON

# Ensure the venv is owned by the current user (avoid root-owned files inside container)
if [ "$(id -u)" -ne 0 ]; then
  echo "[devcontainer setup] Fixing permissions for .venv"
  chown -R "$(id -u):$(id -g)" .venv || true
fi

echo "[devcontainer setup] Done. Activate the venv with: source .venv/bin/activate"
