from pathlib import Path
import re


def transform_content(text: str) -> str:
    # Remove Cursor frontmatter if present at top
    text = re.sub(r"\A---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n", "", text)
    # Convert `@agent` to `*agent`
    text = re.sub(r"`@([a-z0-9-]+)`", r"`*\1`", text, flags=re.IGNORECASE)
    # Normalize mdc: links to normal markdown links
    text = text.replace("(mdc:", "(")
    return text


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    src_dir = repo_root / ".cursor" / "rules" / "bmad"
    out_dir = repo_root / ".codex" / "rules" / "bmad"
    if not src_dir.exists():
        raise SystemExit(f"Source not found: {src_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for mdc in sorted(src_dir.glob("*.mdc")):
        agent_id = mdc.stem
        out_path = out_dir / f"{agent_id}.md"
        txt = mdc.read_text(encoding="utf-8")
        out_path.write_text(transform_content(txt), encoding="utf-8")
        written += 1

    print(f"Wrote {written} per-agent Codex rule file(s) to {out_dir}")


if __name__ == "__main__":
    main()

