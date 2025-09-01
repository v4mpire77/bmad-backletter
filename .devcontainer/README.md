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

Gemini CLI / IDE companion

If you use the Gemini CLI, it may require an IDE companion extension inside Codespaces. After the devcontainer finishes you can install it by running:

```bash
gemini /ide install
```

If that command fails, open the VS Code Extensions view (Ctrl+Shift+X) and search for the Gemini or "IDE companion" extension and install it manually, then reload the window.
