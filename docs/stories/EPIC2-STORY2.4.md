# Story 2.4: Token Ledger & Caps

**ID:** EPIC2-STORY2.4

**As a system administrator, I want to track token usage and enforce hard caps so that I can control costs and ensure the system operates within budget constraints while maintaining audit trails for compliance.**

## Tasks:
* Implement token tracking ledger for all text processing operations
* Create configurable hard cap system that triggers "needs_review" verdicts
* Add token usage metrics and reporting dashboard
* Build cost estimation and budget monitoring
* Implement LLM provider toggle (default: disabled) 
* Create token usage alerts and notifications

## Acceptance Criteria:
* System tracks tokens_per_doc for all processing operations
* Hard cap triggers automatic "needs_review" verdict with detailed logging
* LLM provider functionality is disabled by default in configuration
* Token usage metrics exposed via admin API endpoint
* Cost estimation provides real-time budget tracking
* Alert system notifies administrators when approaching token limits
* All token usage logged with correlation IDs for audit trails

## Test Fixtures:
* **Normal usage:** Documents processing within token limits
* **Hard cap trigger:** Large document that exceeds configured token limits
* **Cost tracking:** Multiple documents with cumulative token usage reporting
* **LLM toggle:** Verify system works with LLM disabled (default state)

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Add TokenUsage model with doc_id, operation_type, token_count, timestamp
- Extend Document model with total_tokens_used field
- Add budget tracking fields to organization settings

**Tech Stack:** [Source: shard-ready-arc/3-tech-stack.md]
- PostgreSQL 15: Store token usage ledger and budget tracking
- Redis 7.x: Cache token usage counters for real-time monitoring
- FastAPI: Expose token metrics via admin endpoints

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Token ledger: `apps/api/blackletter_api/services/token_ledger.py`
- Budget monitoring: `apps/api/blackletter_api/core/budget_monitor.py`
- Metrics endpoints: `apps/api/blackletter_api/routers/admin.py` (extend existing)
- Configuration: `apps/api/blackletter_api/config/token_settings.py`

### Technical Requirements
- Performance: Token tracking must add <100ms to processing time
- Accuracy: All token counts must be precisely recorded and auditable
- Reliability: Hard caps must be enforced consistently across all operations
- Configuration: Token limits configurable via environment variables
- Monitoring: Real-time token usage visibility for administrators

### Previous Story Dependencies
- **EPIC2-STORY2.1**: Rule Pack Loader - provides rule processing context
- **EPIC2-STORY2.2**: Detector Runner - main token consumption source
- **EPIC2-STORY2.3**: Lexicon - additional processing that uses tokens

### Token Usage Sources
1. Text extraction and preprocessing
2. Evidence window generation
3. Rule pattern matching operations
4. Lexicon analysis processing
5. Future LLM calls (when enabled)

## Tasks / Subtasks

1. **Token Ledger System** (AC: 1, 7)
   - Design TokenUsage data model with proper indexing
   - Implement token counting for all text processing operations
   - Create ledger service with atomic transaction support
   - Add correlation ID tracking for audit compliance

2. **Hard Cap Enforcement** (AC: 2, 7)
   - Implement configurable token limits per document/organization
   - Create automatic verdict override to "needs_review"
   - Add detailed logging when caps are triggered
   - Implement graceful degradation when limits exceeded

3. **LLM Provider Management** (AC: 3)
   - Create LLM provider toggle in configuration system
   - Ensure system defaults to LLM disabled
   - Add runtime checks to prevent accidental LLM usage
   - Create admin interface for LLM provider control

4. **Metrics and Reporting** (AC: 4, 5)
   - Create GET /api/admin/token-usage endpoint
   - Implement real-time cost estimation algorithms
   - Add budget tracking and remaining quota calculations
   - Create usage analytics with time-series data

5. **Alert System** (AC: 6)
   - Implement configurable alert thresholds (75%, 90%, 95%)
   - Create notification system for administrators
   - Add webhook support for external monitoring systems
   - Implement rate limiting to prevent alert spam

6. **Unit Testing** (AC: All test fixtures)
   - Test token counting accuracy across all operations
   - Test hard cap enforcement and verdict overrides
   - Test LLM provider toggle functionality
   - Performance testing for ledger overhead

## Testing
- Unit tests: Token counting accuracy and ledger operations
- Integration tests: End-to-end cap enforcement in analysis pipeline
- Performance tests: Ledger overhead within acceptable limits
- Security tests: Prevent token limit bypass attempts

## Artifacts
* `apps/api/blackletter_api/config/token_limits.yaml` - Default token limit configurations
* `data/test-fixtures/large-documents/` - Documents for testing hard caps
* `docs/artifacts/token_usage_schema.json` - Token ledger data model
* `docs/artifacts/budget_monitoring_api.yaml` - Admin API specifications

## Change Log
- Status: Draft
- Created: 2025-09-02
- Epic: E2 (GDPR Rule Engine & Detection)
- Dependencies: EPIC2-STORY2.1, EPIC2-STORY2.2, EPIC2-STORY2.3

## Dev Agent Record
- Status: Approved
- Next: Ready for implementation by @dev
- Estimated effort: 4-5 days (moderate complexity, requires financial controls)

## Scrum Master Validation

| Category                             | Status | Issues |
| ------------------------------------ | ------ | ------ |
| 1. Goal & Context Clarity            | PASS   |        |
| 2. Technical Implementation Guidance | PASS   |        |
| 3. Reference Effectiveness           | PASS   |        |
| 4. Self-Containment Assessment       | PASS   |        |
| 5. Testing Guidance                  | PASS   |        |

**Final Assessment:** READY

The story provides sufficient context for implementation.
