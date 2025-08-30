## Summary

Describe the change at a high level. Link the story/epic and include any screenshots (for UI) or logs (for API).

## Linked Stories / Docs

- PRD §7/§8
- Architecture Docs
- Story: <link to docs/stories/*.md>

## Changes

- [ ] API routes
- [ ] Services / pipeline
- [ ] Models / schemas
- [ ] Web UI
- [ ] Tests (unit/integration)
- [ ] Docs (deployment/usage)

## Acceptance Evidence

Commands run locally (Windows):

```
py -3.11 -m venv .venv; . .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JOB_SYNC = "1"
uvicorn blackletter_api.main:app --reload --app-dir apps/api

# In another shell
python -m pytest -q apps/api/blackletter_api/tests/integration
```

## Risk / Rollback

- Risk level: Low / Medium / High
- Rollback: Revert PR; no data migrations in this change

## Checklist

- [ ] Conventional Commits in history
- [ ] No secrets committed; envs documented
- [ ] Deterministic behavior (rulepack pinned where needed)
- [ ] Windows-first commands verified

