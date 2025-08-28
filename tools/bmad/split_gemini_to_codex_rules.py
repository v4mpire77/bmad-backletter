import re
from pathlib import Path


INTRO = """<!-- Codex rule file generated from GEMINI.md. Do not edit by hand. -->\n"""


def extract_agent_id(section: str) -> str | None:
    # Prefer explicit star-command in prose
    m = re.search(r"`\*([a-z0-9-]+)`", section)
    if m:
        return m.group(1)
    # Fallback to YAML id: field inside code fences
    m = re.search(r"\bid:\s*([a-z0-9-]+)\b", section)
    if m:
        return m.group(1)
    return None


def split_sections(text: str) -> list[str]:
    # Sections are separated by lines containing only ---
    # Keep simple split to preserve content
    parts = re.split(r"^---\s*$", text, flags=re.MULTILINE)
    # Trim whitespace
    return [p.strip() for p in parts if p.strip()]


def adapt_for_codex(section: str) -> str:
    # Rename Gemini wording to Codex
    section = re.sub(r"(?im)^#\s*Gemini\b", "# Codex", section)
    section = re.sub(r"(?i)\bGemini CLI\b", "Codex CLI", section)
    section = re.sub(r"(?i)\bGEMINI.md\b", "CODEX.md", section)
    return section


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    src_path = repo_root / ".gemini" / "bmad-method" / "GEMINI.md"
    out_dir = repo_root / ".codex" / "rules" / "bmad"

    if not src_path.exists():
        raise SystemExit(f"Source not found: {src_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    raw = src_path.read_text(encoding="utf-8")

    sections = split_sections(raw)
    written = 0
    for sec in sections:
        # Identify agent sections by presence of 'Agent Rule' header
        if not re.search(r"^#\s+.+?Agent Rule\b", sec, flags=re.MULTILINE):
            # Skip non-agent chunks (if any)
            continue

        agent_id = extract_agent_id(sec)
        if not agent_id:
            # Could not find id; skip
            continue

        content = INTRO + adapt_for_codex(sec) + "\n"
        out_file = out_dir / f"{agent_id}.md"
        out_file.write_text(content, encoding="utf-8")
        written += 1

    print(f"Wrote {written} Codex rule file(s) to {out_dir}")


if __name__ == "__main__":
    main()

