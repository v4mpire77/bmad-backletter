# v4mpire77/blackletter Integration Mapping Matrix

This document maps the components from `blackletter/blackletter-upstream/` (v4mpire77/blackletter source) to our target paths in the blackletter.systems monorepo.

## Backend Components

| Source Path (v4mpire77) | Target Path (blackletter.systems) | Status | Priority |
|--------------------------|-------------------------------------|---------|----------|
| `backend/app/core/config.py` | `apps/api/blackletter_api/core/config.py` | ⏳ Pending | High |
| `backend/app/routers/jobs.py` | `apps/api/blackletter_api/routers/jobs.py` | ⏳ Pending | High |
| `backend/app/services/gdpr_analyzer.py` | `apps/api/blackletter_api/services/gdpr_analyzer.py` | ⏳ Pending | High |
| `backend/workers/celery_app.py` | `apps/worker/celery_app.py` | ⏳ Pending | High |
| `backend/app/models/schemas.py` | `apps/api/blackletter_api/models/schemas.py` | ⏳ Pending | Medium |
| `backend/tests/` | `apps/api/blackletter_api/tests/` | ⏳ Pending | High |
| `backend/tests/fixtures/` | `apps/api/blackletter_api/tests/fixtures/` | ⏳ Pending | High |

## GDPR Rules and Detection

| Source Path (v4mpire77) | Target Path (blackletter.systems) | Status | Priority |
|--------------------------|-------------------------------------|---------|----------|
| `backend/rules/` | `apps/api/blackletter_api/rules/` | ⏳ Pending | High |
| `rules/art28v1.yaml` | `apps/api/blackletter_api/rules/art28v1.yaml` | ⏳ Pending | High |

## Frontend Components

| Source Path (v4mpire77) | Target Path (blackletter.systems) | Status | Priority |
|--------------------------|-------------------------------------|---------|----------|
| `frontend/lib/api.ts` | `apps/web/src/lib/api.ts` | ⏳ Pending | Medium |
| `frontend/components/` | `apps/web/src/components/` | ⏳ Pending | Medium |

## Infrastructure & Tools

| Source Path (v4mpire77) | Target Path (blackletter.systems) | Status | Priority |
|--------------------------|-------------------------------------|---------|----------|
| `docker-compose.yml` | Merge with existing `docker-compose.yml` | ⏳ Pending | Medium |
| `tools/context_engineering.ps1` | `tools/windows/context_engineering.ps1` | ⏳ Pending | Medium |
| `scripts/dev.ps1` | `scripts/dev.ps1` | ⏳ Pending | Low |

## Documentation

| Source Path (v4mpire77) | Target Path (blackletter.systems) | Status | Priority |
|--------------------------|-------------------------------------|---------|----------|
| `backend/README.md` | Merge content into `docs/` | ⏳ Pending | Low |
| `frontend/README.md` | Merge content into `docs/` | ⏳ Pending | Low |

## Epic Mapping

### Epic E1.1: Async Job Upgrade
- **Components**: `backend/app/routers/jobs.py`, `backend/workers/celery_app.py`
- **Target**: Replace current upload/job endpoints with 202-pattern
- **Validation**: PowerShell scripts can start worker

### Epic E2: GDPR Detector Swap-in
- **Components**: `backend/app/services/gdpr_analyzer.py`, rules YAML, golden fixtures
- **Target**: Merge with existing GDPR analysis
- **Validation**: Rule IDs align with existing art28v1.yaml

### Epic E11: Testing Harness
- **Components**: `backend/tests/fixtures`, Pytest suite
- **Target**: Copy and integrate test infrastructure  
- **Validation**: ≥85% precision, ≥90% recall scores

### Epic E0: Docker Compose Consolidation
- **Components**: `docker-compose.yml`
- **Target**: Merge with existing Docker setup
- **Validation**: Support FastAPI, Next.js, Celery, Redis, Supabase

## Implementation Priority

1. **High Priority** (Epic E1.1, E2, E11)
   - Async job pattern integration
   - GDPR analyzer and test fixtures
   - Core backend services

2. **Medium Priority** (Epic E0)
   - Docker compose consolidation
   - Context engineering validation
   - Frontend API integration

3. **Low Priority**
   - Documentation consolidation
   - PowerShell script improvements

## Notes

- Preserve existing file layout and naming conventions
- Maintain story IDs and existing verdicts (Pass | Weak | Missing | NeedsReview)
- Ensure Windows-friendly PowerShell scripts compatibility
- Target ≥85% precision, ≥90% recall for golden tests
- Framework compliance ≥80% required

---

**Created**: Current date  
**Status**: Planning Phase  
**Next Action**: Begin Epic E1.1 implementation