import re
from pathlib import Path


HEADER = """# Codex Agent Bundle (BMad-Method)

This file adapts the BMad-Method agent rules for use in Codex CLI.

Usage
- In Codex, you can open this file (`.codex/bmad-method/CODEX.md`) to reference agent commands and personas.
- Activate an agent by typing a star-command like `*dev`, `*qa`, or `*bmad-orchestrator` in the chat.
- All commands listed in each agent section require the `*` prefix.

Notes
- Content below is derived from `.gemini/bmad-method/GEMINI.md` and is functionally identical for Codex.
- Where the original text mentions “Gemini”, interpret as “Codex”.

---
"""


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    gemini_path = repo_root / ".gemini" / "bmad-method" / "GEMINI.md"
    codex_dir = repo_root / ".codex" / "bmad-method"
    codex_path = codex_dir / "CODEX.md"
    print(f"Repo root: {repo_root}")
    print(f"Source:    {gemini_path}")
    print(f"Target:    {codex_path}")

    if not gemini_path.exists():
        raise SystemExit(f"Missing source file: {gemini_path}")

    codex_dir.mkdir(parents=True, exist_ok=True)

    src = gemini_path.read_text(encoding="utf-8")

    # Light-touch adaptation: replace leading title occurrences and obvious mentions
    # without altering agent content semantics.
    adapted = src
    adapted = re.sub(r"(?i)^#\s*Gemini\b", "# Codex", adapted)
    adapted = re.sub(r"(?i)\bGemini CLI\b", "Codex CLI", adapted)
    adapted = re.sub(r"(?i)\bGEMINI.md\b", "CODEX.md", adapted)

    codex_path.write_text(HEADER + adapted, encoding="utf-8")
    print(f"Wrote {codex_path}")


if __name__ == "__main__":
    main()
