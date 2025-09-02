# Story 2.3: Weak-Language Lexicon v0

**ID:** EPIC2-STORY2.3

**As a GDPR compliance analyst, I want weak language detection within evidence windows so that I can identify contract clauses that use ambiguous or non-committal language that may undermine legal obligations.**

## Tasks:
* Implement configurable lexicon loader for weak language patterns
* Create weak language detector that scans evidence windows for qualifying terms
* Build verdict downgrading logic: Pass→Weak when weak language detected
* Add counter-anchor detection to prevent false downgrades
* Create lexicon configuration system supporting multiple languages
* Implement lexicon versioning and hot-reloading for development

## Acceptance Criteria:
* Lexicon applies pattern matching inside evidence windows from previous stories
* Verdict downgraded from Pass→Weak when weak language patterns detected
* Counter-anchors prevent downgrade when strong language also present
* Configurable lexicon file supports YAML format with versioning
* System handles multiple lexicon files (e.g., English, German, French)
* API endpoint `GET /api/admin/lexicons` lists available lexicon configurations
* Lexicon changes are logged with before/after verdict comparisons

## Test Fixtures:
* **Weak language samples:** Contract clauses with "may", "should", "endeavor to", "reasonable efforts"
* **Counter-anchor samples:** Strong language that overrides weak patterns ("must", "shall", "required")
* **Mixed language:** Evidence windows containing both weak and strong language patterns
* **Multi-language:** Test lexicon with German/French weak language patterns

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Extends Finding model with weak_language_detected boolean flag
- Add lexicon_version field to track which lexicon rules were applied

**Tech Stack:** [Source: shard-ready-arc/3-tech-stack.md]
- Python 3.11: Use regex and dataclasses for pattern matching
- PostgreSQL 15: Store lexicon metadata and application history
- Redis 7.x: Cache compiled lexicon patterns for performance

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Lexicon engine: `apps/api/src/services/lexicon_analyzer.py`
- Pattern matching: `apps/api/src/core/weak_language_detector.py`
- Lexicon data: `data/lexicons/weak_language_v0.yaml`
- Admin endpoints: `apps/api/src/routers/admin.py` (extend existing)

### Technical Requirements
- Pattern matching: Support regex patterns, case-insensitive matching
- Performance: Lexicon scanning must add <2 seconds to analysis time
- Configuration: YAML-based lexicon files with pattern categories
- Versioning: Semantic versioning for lexicon updates
- Internationalization: Support for multiple language lexicons

### Previous Story Dependencies
- **EPIC2-STORY2.1**: Rule Pack Loader - established configuration loading patterns
- **EPIC2-STORY2.2**: Detector Runner - provides verdict calculation pipeline to extend

### Lexicon Structure Example
```yaml
version: "1.0.0"
language: "en"
weak_patterns:
  - category: "conditional"
    patterns: ["may", "might", "could potentially"]
  - category: "effort_based" 
    patterns: ["reasonable efforts", "endeavor to", "attempt to"]
counter_anchors:
  - patterns: ["must", "shall", "required", "mandatory"]
```

## Tasks / Subtasks

1. **Lexicon Configuration System** (AC: 4, 5)
   - Design YAML schema for lexicon definitions
   - Implement lexicon loader with validation
   - Add support for multiple language files
   - Create lexicon versioning and metadata tracking

2. **Weak Language Detection Engine** (AC: 1, 2)
   - Build pattern matching engine using compiled regex
   - Implement case-insensitive and word-boundary matching
   - Create evidence window scanning with position tracking
   - Add performance optimization for large documents

3. **Verdict Downgrading Logic** (AC: 2, 3)
   - Integrate with existing verdict calculation from Story 2.2
   - Implement Pass→Weak downgrade logic
   - Add counter-anchor detection to prevent false downgrades
   - Create conflict resolution for mixed language patterns

4. **Integration with Detector Runner** (AC: 1, 7)
   - Extend EPIC2-STORY2.2 detector pipeline
   - Add lexicon analysis as post-processing step
   - Update Finding records with weak language metadata
   - Implement before/after verdict logging

5. **Admin Interface** (AC: 6)
   - Create GET /api/admin/lexicons endpoint
   - Add lexicon reload endpoint for development
   - Implement lexicon validation API
   - Create lexicon statistics and usage metrics

6. **Unit Testing** (AC: All test fixtures)
   - Test weak language pattern detection
   - Test counter-anchor prevention logic
   - Test multi-language lexicon support
   - Performance testing with large evidence windows

## Testing
- Unit tests: Pattern matching accuracy and performance
- Integration tests: End-to-end verdict downgrading
- Regression tests: Ensure existing detector functionality unchanged
- Performance tests: Lexicon processing within SLA requirements

## Artifacts
* `data/lexicons/weak_language_v0.yaml` - Initial English weak language lexicon
* `data/test-fixtures/weak-language-samples/` - Test contracts with weak language
* `docs/artifacts/lexicon_schema.yaml` - YAML schema for lexicon files
* `docs/artifacts/weak_language_detection_flow.md` - Process documentation

## Change Log
- Status: Draft
- Created: 2025-09-02
- Epic: E2 (GDPR Rule Engine & Detection)
- Dependencies: EPIC2-STORY2.1 (Rule Pack Loader), EPIC2-STORY2.2 (Detector Runner)

## Dev Agent Record
- Status: Draft
- Next: Ready for review and lexicon content creation
- Estimated effort: 3-4 days (moderate complexity, requires linguistic analysis)
