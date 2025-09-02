# Story 2.2: Obligation Detector Runner

**ID:** EPIC2-STORY2.2

**As a GDPR analyst, I want deterministic rule execution that produces verdicts and evidence snippets so that I can reliably assess contract compliance with auditable, repeatable results.**

## Tasks:
* Implement core detector engine that evaluates anchors, weak signals, and red flags
* Create verdict mapping logic (Pass/Weak/Missing/Needs Review) based on rule patterns
* Build evidence window integration to extract relevant text snippets
* Add rule execution logging with correlation IDs for auditability  
* Create detector orchestration service to run all detectors for a document
* Implement result aggregation and Finding record creation

## Acceptance Criteria:
* Detector evaluates anchors/weak/red-flags within evidence windows from Story 1.3
* Verdict produced per mapping rules with attached rule ID, snippet, and character offsets
* Each detector execution creates Finding record with proper metadata
* System handles graceful failure when individual detectors error
* Detector results include confidence scores and evidence quality metrics
* API endpoint `POST /api/analysis/{doc_id}/detect` triggers full detector run
* Results are deterministic - same input produces identical output every time

## Test Fixtures:
* **Positive cases:** 3 test documents with clear GDPR obligation language per detector (a)-(c)
* **Hard negatives:** 3 test documents that should NOT trigger each detector  
* **Edge cases:** Documents with ambiguous language requiring "Needs Review" verdict
* **Performance test:** Large document (50+ pages) completing analysis within SLA

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Extends Finding interface with verdict enum and confidence scoring
- Integration with existing Document and Job models for workflow continuity

**API Specifications:** [Source: shard-ready-arc/5-api-specification.md]  
- New analysis endpoint following existing /v1 API patterns
- Consistent error response format with structured error codes

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Detector engine: `apps/api/src/services/detector_engine.py`
- Verdict mapping: `apps/api/src/core/verdict_mapper.py`
- Orchestration: `apps/api/src/services/analysis_orchestrator.py`
- Analysis endpoints: `apps/api/src/routers/analysis.py`

### Technical Requirements
- Python: Use dataclasses for detector results and verdict structures
- Performance: Target <30 seconds for full 8-detector analysis on 50-page document
- Reliability: Implement circuit breaker pattern for individual detector failures
- Logging: Structured JSON logs with job_id and analysis_id correlation
- Determinism: All regex patterns and text processing must be reproducible

### Previous Story Dependencies
- **EPIC1-STORY1.3**: Evidence Window Builder - provides text snippet extraction
- **EPIC2-STORY2.1**: Rule Pack Loader - provides validated rule definitions and detector configurations

### Rule Execution Logic
1. Load rule pack for requested detector set
2. For each detector: extract evidence windows for potential matches
3. Apply anchor/weak/red-flag pattern matching within windows
4. Calculate verdict based on pattern combination rules
5. Generate Finding records with evidence and metadata
6. Aggregate results and update analysis status

## Tasks / Subtasks

1. **Core Detector Engine** (AC: 1, 7)
   - Implement pattern matching for anchors, weak signals, red flags
   - Create deterministic text processing pipeline  
   - Add confidence scoring algorithm based on pattern strength
   - Build error handling for malformed or incomplete rules

2. **Verdict Mapping System** (AC: 2, 7)
   - Implement Pass/Weak/Missing/Needs Review logic
   - Create verdict calculation based on anchor/weak/red-flag combinations
   - Add tie-breaking rules for ambiguous cases
   - Validate verdict consistency across rule variations

3. **Evidence Integration** (AC: 1, 3)
   - Integrate with Evidence Window Builder from Story 1.3
   - Extract character offset ranges for matched patterns
   - Ensure evidence snippets include sufficient context
   - Handle multi-page evidence windows correctly

4. **Analysis Orchestration** (AC: 4, 6)
   - Create service to run all 8 detectors in sequence
   - Implement graceful error handling for individual detector failures
   - Add progress tracking and status updates
   - Create POST /api/analysis/{doc_id}/detect endpoint

5. **Result Processing** (AC: 3, 5)
   - Generate Finding records from detector results
   - Add metadata: timestamps, rule versions, confidence scores
   - Implement result validation and consistency checks
   - Store findings with proper document relationships

6. **Unit Testing** (AC: All test fixtures)
   - Test positive cases: 3 per detector with expected Pass verdicts
   - Test hard negatives: 3 per detector with expected Missing verdicts
   - Test edge cases requiring human review
   - Performance test with large documents

## Testing
- Unit tests: Individual detector logic and verdict mapping
- Integration tests: Full analysis workflow with Evidence Window Builder
- Performance tests: Large document processing within SLA
- Regression tests: Ensure deterministic results across runs

## Artifacts
* `data/test-fixtures/gdpr-positive-samples/` - Test documents with clear obligations
* `data/test-fixtures/gdpr-negative-samples/` - Test documents without obligations  
* `docs/artifacts/detector_results_schema.json` - Detector output format specification
* `docs/artifacts/verdict_mapping_rules.md` - Documentation of verdict calculation logic

## Change Log
- Status: Draft
- Created: 2025-09-02  
- Epic: E2 (GDPR Rule Engine & Detection)
- Dependencies: EPIC1-STORY1.3 (Evidence Window Builder), EPIC2-STORY2.1 (Rule Pack Loader)

## Dev Agent Record
- Status: Draft
- Next: Ready for review and implementation planning
- Estimated effort: 5-8 days (complex logic with extensive testing requirements)
