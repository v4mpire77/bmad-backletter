Title: Inline Diff Review in Findings Drawer
Goal: show red/green diff between problematic phrase and compliant suggested text with rule context.
Acceptance:
- Drawer shows side-by-side or inline diff with +/– gutters and strike/underline cues.
- Legend explains colours; AA contrast.
- Sticky rule chip (e.g., “Art 28(3)(a)”) and 1-line rationale.
- Buttons: Copy removed | Copy suggested | Copy with citation.
- Keyboard: j/k to move diffs, esc to close.
- API: findings payload includes original_text, suggested_text, rule_id per evidence.
Tests:
- Unit: renderer marks insertions/deletions correctly.
- Integration: GET /api/findings?job_id returns diff-ready fields.
- E2E: upload → open finding → diff visible, copy works.
