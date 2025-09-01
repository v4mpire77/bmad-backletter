# Devcontainer setup for Codespaces

This devcontainer config prepares the workspace for Codespaces and VS Code Remote - Containers.

What it does:

- Uses base Ubuntu devcontainer image with Node and Python features.
- Creates a Python 3.11 virtual environment at `.venv` and installs `requirements.txt` if present.
- Runs `npm install` inside `web/` if a `package.json` exists there.
- Attempts to install the `bmad-method` CLI globally (used by this repo).
- Writes basic VS Code workspace settings to use the `.venv` interpreter.

How Codespaces uses it:

- `postCreateCommand` runs `.devcontainer/setup-devcontainer.sh` after container creation.
- `postStartCommand` prints a small readiness message.

If something fails during best-effort installs (like optional global CLIs), the script continues so the container is still usable.

To re-run locally:

```bash
bash .devcontainer/setup-devcontainer.sh
```

If you want additional tools installed on Codespaces, edit `devcontainer.json` and add them under `features` or update the setup script.
