# Story 2.1: Rule Pack Loader

**ID:** EPIC2-STORY2.1

**As a system administrator, I want to load YAML-based rule packs with versioning and validation so that the GDPR analysis engine can use standardized, auditable rules for contract evaluation.**

## Tasks:
* Implement YAML rule pack schema validation with proper error reporting
* Create rule pack loader service that reads from filesystem or S3-compatible storage  
* Add versioning support for rule packs (semantic versioning)
* Implement caching mechanism for loaded rule packs to avoid repeated parsing
* Create admin endpoint to list available rule packs and their versions

## Acceptance Criteria:
* Rule pack YAML files follow a strict schema with validation on load
* System can load multiple rule pack versions simultaneously
* Invalid rule packs are rejected with detailed error messages
* Rule pack metadata includes version, author, and creation date
* API endpoint `GET /api/admin/rulepacks` returns list of available rule packs
* Rule pack loading failures are logged with structured error details

## Test Fixtures:
* **Valid rule pack:** `art28_v1.yaml` with proper schema and 8 obligation rules
* **Invalid rule pack:** Malformed YAML that should trigger validation errors
* **Version test:** Multiple versions of same rule pack (v1.0, v1.1) loading correctly

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Rule pack structure will extend the existing data models with RulePack and Rule interfaces
- Integration with existing Finding model for rule_id references

**API Specifications:** [Source: shard-ready-arc/5-api-specification.md]  
- New admin endpoints to be added to existing /v1 API structure
- Follow existing error response patterns

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Rule pack loader: `apps/api/blackletter_api/services/rulepack_loader.py`
- Schema validation: `apps/api/blackletter_api/schemas/rulepack.py`
- Rule pack storage: `data/rulepacks/` directory
- Admin endpoints: `apps/api/blackletter_api/routers/admin.py`

### Technical Requirements
- Python: Use Pydantic for YAML schema validation
- Storage: Support both local filesystem and S3-compatible object storage
- Caching: Use Redis for rule pack caching with TTL
- Logging: Structured JSON logs for all rule pack operations
- Versioning: Semantic versioning (MAJOR.MINOR.PATCH) in rule pack metadata

### Previous Story Insights
From EPIC1-STORY1.2 completion notes: Job status tracking patterns established can be reused for rule pack loading status.

## Tasks / Subtasks

1. **Schema Definition** (AC: 1, 4)
   - Define Pydantic schemas for rule pack structure
   - Add validation rules for required fields and data types
   - Create error message templates for validation failures
   - [x] Implemented comprehensive Pydantic schema validation for rule packs
   - [x] Added detailed error reporting with field and value information
   - [x] Created custom RulepackValidationError for better error handling

2. **Rule Pack Loader Service** (AC: 2, 3, 6)
   - Implement file system rule pack discovery
   - Add YAML parsing with schema validation 
   - Create structured error logging for load failures
   - Add support for S3-compatible storage backends
   - [x] Enhanced RulepackLoader to support both filesystem and S3-compatible storage
   - [x] Added S3CompatibleStorage class for cloud storage integration
   - [x] Implemented fallback mechanism from S3 to filesystem
   - [x] Integrated schema validation with detailed error reporting

3. **Versioning System** (AC: 2, 4)
   - Implement semantic version parsing and comparison
   - Add rule pack metadata extraction
   - Create version conflict resolution logic
   - [x] Enhanced schema validation with semantic version support
   - [x] Added Version class for semantic version comparison
   - [x] Implemented version comparison utilities
   - [x] Added support for multiple rulepack versions in RulepackLoader
   - [x] Created functions to list and load specific versions

4. **Caching Layer** (AC: 2)
   - Implement Redis-based rule pack caching
   - Add cache invalidation on rule pack updates
   - Create cache warming for frequently used rule packs

5. **Admin API Endpoints** (AC: 5)
   - Create `GET /api/admin/rulepacks` endpoint
   - Add rule pack detail endpoint with metadata
   - Implement rule pack reload endpoint for development

6. **Unit Testing** (AC: All)
   - Test valid rule pack loading and caching
   - Test invalid rule pack rejection with proper errors
   - Test version handling and metadata extraction
   - Test API endpoints and error responses

## Testing
- Unit tests: Rule pack validation, loading, and caching logic
- Integration tests: API endpoints and error handling
- Load tests: Multiple concurrent rule pack loading operations
- Security tests: Path traversal and malformed YAML handling

## Artifacts
* `data/rulepacks/art28_v1.yaml` - Reference rule pack implementation
* `docs/artifacts/rulepack_schema.json` - JSON schema documentation  
* `docs/artifacts/admin_rulepacks_api.yaml` - OpenAPI spec for new endpoints

## Change Log
- Status: Draft
- Created: 2025-09-02
- Epic: E2 (GDPR Rule Engine & Detection)
- Dependencies: Requires completion of EPIC1 text extraction stories

## Dev Agent Record
- Status: In Progress
- Agent Model Used: dev (James)
- Next: Implementation planning and development
