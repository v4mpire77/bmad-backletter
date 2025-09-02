# Story 3.2: Report Export

**ID:** EPIC3-STORY3.2

**As a compliance officer, I want to export analysis findings as PDF and HTML reports so that I can share results with stakeholders, archive compliance records, and integrate with existing documentation workflows.**

## Tasks:
* Implement PDF report generation with professional formatting
* Create HTML export with embedded CSS for standalone viewing
* Include document metadata (filename, checksum, analysis timestamp)
* Add verdict summaries with evidence snippets and rule references
* Implement report template system for consistent branding
* Create batch export functionality for multiple documents

## Acceptance Criteria:
* PDF/HTML export reproduces findings with clear headings, verdict colors, and evidence snippets
* Reports include complete file metadata (name, size, checksum, upload timestamp)
* Generated reports are reproducible from stored analysis artifacts
* Export includes rule ID references and confidence scores for audit trails
* Reports contain executive summary with verdict distribution
* Export functionality accessible via both UI button and API endpoint
* Generated files follow consistent naming convention with timestamps

## Test Fixtures:
* **Complete report:** Document with all verdict types for comprehensive export testing
* **Large document:** Multi-page contract to test pagination and layout
* **Minimal findings:** Document with few findings to test layout edge cases
* **Batch export:** Multiple documents exported as single ZIP archive

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Uses Finding, Document, and Analysis models for complete report data
- Includes file metadata with SHA256 checksum for integrity verification

**Tech Stack:** [Source: shard-ready-arc/3-tech-stack.md]
- FastAPI: Backend PDF/HTML generation endpoints
- Python libraries: WeasyPrint for PDF, Jinja2 for HTML templating
- Next.js: Frontend export trigger and download handling
- S3-compatible storage: Report archival and retrieval

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Report generator: `apps/api/src/services/report_generator.py`
- Templates: `apps/api/src/templates/report_template.html`
- Export endpoints: `apps/api/src/routers/reports.py`
- Frontend trigger: `apps/web/src/components/ExportButton.tsx`

### Technical Requirements
- Performance: PDF generation <10 seconds for 50-page analysis
- Quality: Professional formatting suitable for executive presentation
- Compliance: Include all required metadata for audit requirements
- Storage: Generated reports stored with 90-day retention policy
- Security: Report access controlled by user permissions

### Previous Story Dependencies
- **EPIC3-STORY3.1**: Findings Table - provides UI patterns for verdict display
- **EPIC2-STORY2.2**: Detector Runner - provides Finding records for export
- **EPIC2-STORY2.4**: Token Ledger - provides cost/usage data for reports

### Report Structure
1. **Executive Summary**: Verdict distribution, compliance score
2. **Document Metadata**: File info, analysis timestamp, checksum
3. **Detailed Findings**: Each detector with verdict, evidence, rule ID
4. **Technical Details**: Token usage, processing time, rule versions
5. **Appendices**: Full evidence snippets, methodology notes

## Tasks / Subtasks

1. **Report Template System** (AC: 3, 5)
   - Design professional HTML template with CSS styling
   - Create reusable components for verdicts, evidence, metadata
   - Implement responsive layout for different content lengths
   - Add branding elements and consistent typography

2. **PDF Generation Engine** (AC: 1, 3)
   - Integrate WeasyPrint for HTML-to-PDF conversion
   - Configure page breaks and pagination handling
   - Add headers/footers with page numbers and timestamps
   - Implement high-quality rendering for charts and badges

3. **HTML Export System** (AC: 1, 6)
   - Create standalone HTML with embedded CSS and assets
   - Ensure offline viewing capability without external dependencies
   - Add print-friendly CSS media queries
   - Implement collapsible sections for large reports

4. **Metadata Integration** (AC: 2, 4)
   - Include complete document metadata in report header
   - Add SHA256 checksum verification information
   - Display analysis parameters and rule pack versions
   - Include confidence scores and processing timestamps

5. **Export API and UI** (AC: 6, 7)
   - Create POST /api/reports/export endpoint
   - Add export progress tracking for large reports
   - Implement frontend export button with download handling
   - Create batch export functionality for multiple documents

6. **Testing and Validation** (AC: All)
   - Test report generation with various document types
   - Validate PDF quality and professional appearance
   - Test HTML standalone functionality
   - Performance testing with large analysis datasets

## Testing
- Unit tests: Template rendering and data transformation logic
- Integration tests: End-to-end export workflow from findings to PDF
- Performance tests: Large document export within SLA requirements
- Visual tests: PDF layout and formatting consistency

## Artifacts
* `apps/api/src/templates/report_template.html` - Main report template
* `apps/api/src/static/report_styles.css` - Report styling and branding
* `data/test-fixtures/export-samples/` - Sample generated reports
* `docs/artifacts/report_format_spec.md` - Report structure documentation

## Change Log
- Status: Draft
- Created: 2025-09-02
- Epic: E3 (Findings & Report UI)
- Dependencies: EPIC3-STORY3.1 (Findings Table), EPIC2-STORY2.2 (Detector Runner)

## Dev Agent Record
- Status: Draft
- Next: Ready for template design and PDF generation implementation
- Estimated effort: 5-7 days (complex formatting and PDF generation requirements)
