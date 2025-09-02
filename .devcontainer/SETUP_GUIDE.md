# 🚀 Complete Codespaces Setup Guide

This guide ensures your BMAD Backletter project sets up automatically in GitHub Codespaces.

## 📋 Current Status

✅ **Already Configured:**
- Dev container with Ubuntu base image
- Node.js and Python 3.11 features
- Python venv setup
- Basic VS Code settings
- pnpm monorepo structure
- Azure Static Web Apps deployment

❌ **Missing Setup:**
- pnpm installation in devcontainer
- Environment variables
- Database setup (if needed)
- VS Code extensions
- Git configuration

## 🔧 Required Files & Updates

### 1. **Update devcontainer.json**
Add missing features and extensions:

```json
{
  "name": "BMAD Backletter Dev Container",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "bash .devcontainer/setup-devcontainer.sh",
  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "${containerWorkspaceFolder}/.venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "typescript.preferences.includePackageJsonAutoImports": "auto",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        }
      },
      "extensions": [
        "ms-python.python",
        "ms-python.pylint",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next",
        "ms-azuretools.vscode-azurestaticwebapps",
        "github.copilot",
        "github.copilot-chat"
      ]
    }
  }
}
```

### 2. **Update setup-devcontainer.sh**
Add pnpm installation and proper monorepo setup:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "[devcontainer setup] Setting up BMAD Backletter development environment..."

# Install pnpm globally
echo "[devcontainer setup] Installing pnpm..."
npm install -g pnpm

# Python setup
echo "[devcontainer setup] Creating Python venv at .venv..."
if [ -d ".venv" ]; then
  echo "[devcontainer setup] .venv already exists — skipping venv creation"
else
  python3 -m venv .venv
  echo "[devcontainer setup] venv created"
fi

source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
if [ -f "requirements.txt" ]; then
  echo "[devcontainer setup] Installing Python requirements..."
  pip install -r requirements.txt
fi

if [ -f "apps/api/requirements.txt" ]; then
  echo "[devcontainer setup] Installing API requirements..."
  pip install -r apps/api/requirements.txt
fi

# Install Node.js dependencies with pnpm
echo "[devcontainer setup] Installing Node.js dependencies with pnpm..."
pnpm install

# Build shared packages
echo "[devcontainer setup] Building shared packages..."
pnpm --filter @bmad/shared build

echo "[devcontainer setup] ✅ Setup complete!"
echo ""
echo "🚀 Quick start commands:"
echo "  pnpm dev          # Start all development servers"
echo "  pnpm build        # Build all packages"
echo "  source .venv/bin/activate  # Activate Python environment"
```

### 3. **Environment Variables Setup**
Create `.devcontainer/.env.devcontainer`:

```bash
# Development environment variables
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:8000
PYTHON_ENV=development

# Optional: Add your API keys for full functionality
# GEMINI_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
```

### 4. **VS Code Workspace Settings**
Create/update `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "files.associations": {
    "*.yaml": "yaml",
    "*.yml": "yaml"
  },
  "tailwindCSS.includeLanguages": {
    "typescript": "typescript",
    "typescriptreact": "typescriptreact"
  }
}
```

### 5. **Task Configuration**
Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Development Servers",
      "type": "shell",
      "command": "pnpm dev",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "isBackground": true,
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "Build All",
      "type": "shell",
      "command": "pnpm build",
      "group": "build"
    },
    {
      "label": "Activate Python Environment",
      "type": "shell",
      "command": "source .venv/bin/activate",
      "group": "build"
    }
  ]
}
```

## 🔄 **What Happens on Codespace Creation:**

1. **Container starts** with Ubuntu + Node.js + Python
2. **pnpm gets installed** globally
3. **Python venv created** and dependencies installed
4. **All Node.js packages installed** via pnpm monorepo
5. **VS Code extensions installed** automatically
6. **Development servers ready** to start with `pnpm dev`

## ⚡ **Quick Start After Setup:**

```bash
# Start all development servers (web + api)
pnpm dev

# Or start individually:
cd apps/web && pnpm dev    # Frontend on :3000
cd apps/api && python -m uvicorn main:app --reload  # API on :8000
```

## 🚀 **Deployment Ready:**

- **Azure Static Web Apps:** Configured with GitHub Actions
- **Environment:** Production builds via `pnpm build`
- **Live URL:** `https://proud-cliff-03429dc03.azurestaticapps.net`

## 🔧 **Troubleshooting:**

- If pnpm fails: `npm install -g pnpm`
- If Python env fails: `python3 -m venv .venv && source .venv/bin/activate`
- If builds fail: `pnpm install && pnpm build`

Your Codespace will be fully ready to develop, build, and deploy your beautiful Blackletter app! 🎯
