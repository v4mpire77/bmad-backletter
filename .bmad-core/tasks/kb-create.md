<!-- Powered by BMAD™ Core -->

# KB Create - Build BMAD knowledge bundles for web agents (Codex/web dev cycle)

## Purpose

Provide a deterministic, repeatable process for creating and maintaining a BMAD knowledge bundle (KB) optimized for web-deployable Codex-style agents used during the development cycle. The task defines inputs, outputs, validation steps, and maintenance guidance so developer agents can produce high-quality, self-contained KB artifacts.

## Scope

- Target audience: Dev and DevOps agents producing KB artifacts for Codex/web agents used in development, testing, and docs-driven workflows.
- Output: a single packaged KB (markdown bundle) that follows project conventions and is consumable by the web agent runtime.

## Inputs

- `source_root` (required): path to repository root or folder containing authoritative BMAD resources (default: repository root)
- `include_paths` (optional): list of globs to include (e.g., `.bmad-core/**`, `docs/**`, `deploy/**`). If omitted, include the default BMAD folders: `.bmad-core`, `bmad-core`, `docs`, `templates`.
- `exclude_paths` (optional): list of globs to explicitly exclude (e.g., `node_modules/**`, `.git/**`).
- `bundle_meta` (optional): YAML/JSON with metadata to embed (title, version, generated_by, date, important_notes).

## Outputs

- `kb_bundle.md` (or `kb_bundle_<timestamp>.md`): a single markdown file that concatenates selected resources with clear START/END tags for each original file, suitable for web-agent consumption.
- `kb_index.json` (optional): metadata index listing the files included, sections, and anchors.

## Success Criteria

- `kb_bundle.md` contains only the files and sections allowed by `include_paths` minus `exclude_paths`.
- All included files are bounded by START/END markers using the exact format:

  ====== START: <path> ======
  ...file contents...
  ====== END: <path> ======

- No secrets or credentials are included.
- Bundle metadata matches `bundle_meta` if provided.

## Process

1. Resolve inputs:
   - Read `source_root` and validate existence.
   - Normalize `include_paths` and `exclude_paths` to repository-relative globs.

2. Collect files (deterministic order):
   - Default include set: `.bmad-core/**`, `bmad-core/**`, `docs/**`, `.docs/**`, `templates/**`.
   - Walk the file tree and collect files that match include globs and do not match exclude globs.
   - Sort files lexicographically to ensure repeatable bundles.

3. Sanitize and filter content:
   - Remove lines that match common secret patterns (simple heuristic): `AWS_SECRET`, `SECRET_KEY`, `PASSWORD=`, `-----BEGIN PRIVATE KEY-----`.
   - If a possible secret is found, record a warning and skip the file; do not include it in the bundle.
   - Optionally run a configured secret-scanner (if available) and treat any findings as blocking.

4. Render bundle:
   - For each file, produce a section with exact START/END markers using the repository-relative path.
   - Preserve original file encoding and newlines.
   - Optionally trim very large binary or log files (size threshold configurable).

5. Generate index (optional):
   - Create `kb_index.json` summarizing included files with sizes, line counts, and top-level headings for markdown files.

6. Validate bundle:
   - Verify START/END pairs match.
   - Verify bundle filesize is within configured limits (configurable, default 2.5MB).
   - Confirm metadata included and consistent with `bundle_meta`.

7. Output and storage:
   - Write `kb_bundle_<YYYYMMDD_HHMMSS>.md` to `web-bundles/` (create folder if missing).
   - Write `kb_index.json` next to it when generated.
   - Optionally create a short checksum file `kb_bundle.sha256`.

## Usage examples

1. Minimal (pseudo-command):

   - source_root: repo root
   - include_paths: `.bmad-core/**, bmad-core/**`
   - exclude_paths: `.git/**, node_modules/**`

   Result: `web-bundles/kb_bundle_20250902_120501.md`

2. Developer agent flow (high-level):
   - Developer agent calls this task with `include_paths` tuned to the story domain.
   - Agent inspects the generated `kb_bundle.md` to answer queries or to pass to a Codex/web runtime.

## Validation rules and QA

- Block and HALT if `source_root` not found.
- Block and HALT if any included file contains a likely secret (report the file path and matched pattern).
- Emit warnings for files larger than 200KB; skip files > 2MB unless explicitly allowed.
- Ensure generated files are UTF-8 valid.

## Maintenance

- Rebuild the KB whenever major documentation changes occur (release, sprint boundary, or story branching).
- Keep `include_paths` minimal for each agent purpose (smaller bundles are faster and safer).

## Guidance for web/Codex agents

- Web agents should prefer KB bundles over direct repo access where network or sandboxing is constrained.
- Use `kb_index.json` for fast lookups when present.
- When the agent needs only a section, it should locate the START/END block by exact path and optionally by heading anchors inside the block.

## Example START/END block (exact format required in bundles)

====== START: .bmad-core/tasks/validate-next-story.md ======
# Validate Next Story Task
...content...
====== END: .bmad-core/tasks/validate-next-story.md ======

## Security and privacy

- Never include private keys, secrets, or credential files. If secrets are detected, the task should fail and list the offending paths.
- If sensitive information must be included for a controlled internal bundle, require explicit `allow_sensitive: true` in `bundle_meta` and log approvals.

## Implementation notes for developer agents

- Implementations may be a short script (Node, Python) that performs the steps above. Prefer small, dependency-free scripts for portability.
- Provide a flag `--dry-run` to emit a report of included/excluded files without writing the bundle.
- Provide `--max-bytes` to tune size limits.

## Files created

- `web-bundles/kb_bundle_<timestamp>.md` — bundle file for Codex/web agents
- `web-bundles/kb_index_<timestamp>.json` — optional index

## Troubleshooting

- If a needed file is missing from the bundle, verify `include_paths` globs and the `source_root` location.
- If the bundle is unexpectedly large, narrow `include_paths` or increase exclusion globs.

## Completion criteria

- The bundle file is written to `web-bundles/` and passes validation rules.
- No secret findings remained unresolved.

---

Version: 1.0
Generated: YYYY-MM-DD
