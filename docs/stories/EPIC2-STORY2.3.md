# Story 2.3: Weak Language Lexicon Enhancement

**ID:** EPIC2-STORY2.3
**Priority:** HIGH

**As a compliance analyst, I want an enhanced weak language detection system so that I can accurately identify ambiguous clauses, assess their severity with confidence scores, and tune the analysis for different industries like legal and finance.**

## Features
- **Expanded Term Coverage:** Greatly increase the number of weak, ambiguous, and non-committal terms.
- **Industry-Specific Lexicons:** Introduce separate lexicons for Legal, Finance, and Healthcare domains.
- **Confidence Scoring:** Assign a confidence score (0-1) to each detected weak language term.
- **Configurable Sensitivity:** Allow users to set a sensitivity level (e.g., low, medium, high) to filter findings.

## Acceptance Criteria
- ✅ The system loads and manages multiple industry-specific lexicons (legal, finance, healthcare) from `rules/lexicons/`.
- ✅ Each weak language pattern in the lexicon YAML files includes a `confidence` score (e.g., `0.75`).
- ✅ The detection engine identifies weak language and stores the associated confidence score with each finding.
- ✅ A new API endpoint `POST /api/jobs/{job_id}/analyze` accepts a `sensitivity` parameter ('low', 'medium', 'high').
- ✅ Findings are filtered based on the sensitivity level (e.g., 'high' only shows findings with confidence > 0.8).
- ✅ Verdicts are downgraded from `Pass` to `Weak` only if detected terms meet the sensitivity threshold.
- ✅ The `GET /api/admin/lexicons` endpoint now lists all loaded lexicons, including industry-specific ones.
- ✅ Expanded lexicon for general use contains at least 50 new terms.

## Dev Notes

### Architecture Context
**Data Models:**
- The `Finding` model will be updated:
  - `weak_language_detected: bool` is replaced by `weak_language_finding: Optional[dict]`.
  - The `weak_language_finding` dict will contain `{ "term": "may", "confidence": 0.6, "lexicon": "legal_v1" }`.
- A new `lexicon_config` table in PostgreSQL will store metadata about loaded lexicons.

**Tech Stack:**
- Python 3.11: Use `regex` for pattern matching and Pydantic for data validation.
- FastAPI: Add new endpoints and update existing ones for sensitivity controls.

**File Locations:**
- Lexicon Engine: `apps/api/blackletter_api/services/lexicon_analyzer.py`
- Lexicon Data: `apps/api/blackletter_api/rules/lexicons/` (e.g., `general_v1.yaml`, `legal_v1.yaml`)
- Admin Endpoints: `apps/api/blackletter_api/routers/admin.py`
- Analysis Endpoint: `apps/api/blackletter_api/routers/jobs.py`

### Lexicon Structure Example
```yaml
version: "1.1.0"
language: "en"
name: "legal_weak_language"
patterns:
  - category: "conditional"
    term: "may"
    confidence: 0.6
  - category: "effort_based"
    term: "best efforts"
    confidence: 0.75
    notes: "Commonly litigated term."
counter_anchors:
  - patterns: ["must", "shall", "is required to"]
```

## Tasks / Subtasks

1.  **Lexicon Schema and Loader Enhancement**
    - Update the YAML schema to include `confidence` per pattern.
    - Modify the lexicon loader to handle industry-specific files from `rules/lexicons/`.
    - Create at least three lexicon files: `general_v1.yaml`, `legal_v1.yaml`, `finance_v1.yaml`.

2.  **Update Detection Engine with Confidence Scoring**
    - Modify the `lexicon_analyzer.py` to capture and store the confidence score.
    - Update the `Finding` data model to store the weak language details.

3.  **Implement Sensitivity Level Controls**
    - Add the `sensitivity` parameter to the analysis endpoint.
    - Implement filtering logic to include/exclude findings based on confidence and sensitivity.
    - Adjust the `Pass` -> `Weak` verdict logic to respect the sensitivity threshold.

4.  **Expand Lexicon Terminology**
    - Research and add at least 50 new general weak language terms.
    - Populate the industry-specific lexicons with at least 10 relevant terms each.

5.  **Update API and Admin Interface**
    - Enhance `GET /api/admin/lexicons` to show details for all loaded lexicons.
    - Add tests for the new sensitivity parameter in the analysis endpoint.

6.  **Testing**
    - Write unit tests for confidence score parsing and storage.
    - Write integration tests for the sensitivity level filtering.
    - Create test fixtures with various confidence levels to validate filtering.

## Artifacts
*   `apps/api/blackletter_api/rules/lexicons/general_v1.yaml`
*   `apps/api/blackletter_api/rules/lexicons/legal_v1.yaml`
*   `apps/api/blackletter_api/rules/lexicons/finance_v1.yaml`
*   `apps/api/blackletter_api/rules/lexicons/healthcare_v1.yaml`
*   `docs/artifacts/lexicon_schema_v2.yaml` - Updated schema definition.

## Change Log
- Status: **Revised**
- Updated: 2025-09-02
- Author: Jules
- Changes: Added confidence scoring, industry lexicons, and sensitivity controls.

## Dev Agent Record
- Status: **Complete**
- Next: Ready for implementation.
- Estimated effort: 5-7 days (high complexity due to architectural changes and content creation).
