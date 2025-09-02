#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "[devcontainer setup] Setting up BMAD Backletter development environment..."

# Install pnpm globally first
echo "[devcontainer setup] Installing pnpm..."
npm install -g pnpm

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

# Install API requirements if they exist
if [ -f "apps/api/requirements.txt" ]; then
  echo "[devcontainer setup] Installing API requirements from apps/api/requirements.txt"
  pip install -r apps/api/requirements.txt || echo "[devcontainer setup] API pip install failed — continuing"
fi

# Install Node.js dependencies with pnpm (monorepo)
echo "[devcontainer setup] Installing Node.js dependencies with pnpm..."
pnpm install || echo "[devcontainer setup] pnpm install failed — continuing"

# Build shared packages
echo "[devcontainer setup] Building shared packages..."
pnpm --filter @bmad/shared build || echo "[devcontainer setup] shared package build failed — continuing"

# Install repo global CLIs that are safe to install
echo "[devcontainer setup] Installing recommended global CLIs if available: bmad-method"
if command -v npm >/dev/null 2>&1; then
  # Configure a user-local npm prefix to avoid permission errors when installing global packages
  NPM_PREFIX="${HOME}/.npm-global"
  mkdir -p "$NPM_PREFIX"
  npm config set prefix "$NPM_PREFIX" || true
  # Ensure PATH includes npm global bin for current session and future shells
  export PATH="$NPM_PREFIX/bin:$PATH"
  if ! grep -q "${NPM_PREFIX}/bin" "$HOME/.profile" 2>/dev/null; then
    printf "\n# Add npm user bin to PATH\nexport PATH=\"%s/bin:\$PATH\"\n" "$NPM_PREFIX" >> "$HOME/.profile"
  fi
  if ! grep -q "${NPM_PREFIX}/bin" "$HOME/.bashrc" 2>/dev/null; then
    printf "\n# Add npm user bin to PATH\nexport PATH=\"%s/bin:\$PATH\"\n" "$NPM_PREFIX" >> "$HOME/.bashrc"
  fi

  # Helper to retry npm global install
  retry_npm_install() {
    local pkg="$1"
    local tries=0
    local max=3
    until [ $tries -ge $max ]
    do
      tries=$((tries+1))
      echo "[devcontainer setup] npm attempt $tries to install $pkg"
      npm install -g "$pkg" && return 0 || sleep 1
    done
    return 1
  }

  echo "[devcontainer setup] Installing required CLI: bmad-method"
  if retry_npm_install bmad-method; then
    echo "[devcontainer setup] bmad-method installed via npm global"
  else
    echo "[devcontainer setup] npm global install bmad-method failed — attempting npx fallback"
    if command -v npx >/dev/null 2>&1; then
      npx --yes bmad-method install --yes && echo "[devcontainer setup] bmad-method installed via npx (install step executed)" || echo "[devcontainer setup] npx bmad-method fallback failed"
    else
      echo "[devcontainer setup] npx not available — cannot run fallback for bmad-method"
    fi
  fi
else
  echo "[devcontainer setup] npm not available — skipping global npm installs"
fi

# Optional: try to install gemini CLI if npm is present (best-effort)
if command -v npm >/dev/null 2>&1; then
  echo "[devcontainer setup] Installing optional CLI: @google/gemini-cli"
  if retry_npm_install @google/gemini-cli; then
    echo "[devcontainer setup] @google/gemini-cli installed"
  else
    echo "[devcontainer setup] @google/gemini-cli install failed — continuing"
  fi

  # Verify installed CLIs (print versions if available)
  if command -v bmad-method >/dev/null 2>&1; then
    echo "[devcontainer setup] bmad-method -> $(bmad-method --version 2>/dev/null || echo 'version unknown')"
  else
    echo "[devcontainer setup] bmad-method binary not found in PATH; you can run 'npx bmad-method' or reopen the terminal to pick up PATH changes"
  fi

  if command -v gemini >/dev/null 2>&1; then
    echo "[devcontainer setup] gemini -> $(gemini --version 2>/dev/null || echo 'version unknown')"
  else
    echo "[devcontainer setup] gemini binary not found in PATH"
  fi
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
