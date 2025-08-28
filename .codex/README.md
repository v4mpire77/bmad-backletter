Codex Rules for BMad-Method

Location
- `.codex/bmad-method/CODEX.md` — consolidated rules for all installed BMad agents (core + expansions).

How to use in Codex
- Open `CODEX.md` in your IDE and keep it available as reference context.
- In chat, activate agents using star-commands like `*dev`, `*qa`, `*bmad-orchestrator`.
- Follow each agent’s help to list tasks (always with `*` prefix) and proceed.

Keeping rules up to date
- Rebuild from Gemini bundle if agents change:
  - PowerShell: `pwsh -NoProfile -Command "& { $src='.gemini/bmad-method/GEMINI.md'; $dstDir='.codex/bmad-method'; New-Item -ItemType Directory -Force -Path $dstDir | Out-Null; $dst=Join-Path $dstDir 'CODEX.md'; $hdr=@'# Codex Agent Bundle (BMad-Method)

This file adapts the BMad-Method agent rules for use in Codex CLI.

---

'@; $c=Get-Content $src -Raw; $c=$c -replace '(?im)^#\s*Gemini\b','# Codex'; $c=$c -replace '(?i)\bGemini CLI\b','Codex CLI'; $c=$c -replace '(?i)\bGEMINI.md\b','CODEX.md'; Set-Content -Path $dst -Value ($hdr + $c) -Encoding UTF8 }"`
- Or run the Python helper at `tools/bmad/generate_codex_bundle.py` (requires local Python).

 npm scripts
- `npm run codex:bundle` — refresh `.codex/bmad-method/CODEX.md` from `.gemini/bmad-method/GEMINI.md`.
- `npm run codex:rules` — generate per-agent rules under `.codex/rules/bmad/` from Cursor `.mdc` rules.
- `npm run codex:all` — run both of the above.

Notes
- The rules mirror the Gemini bundle but are IDE-agnostic and suitable for Codex sessions.
