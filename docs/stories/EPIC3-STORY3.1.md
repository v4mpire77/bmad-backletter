# Story 3.1: Findings Table

**ID:** EPIC3-STORY3.1

**As a GDPR compliance analyst, I want an evidence-first findings table that displays all 8 detector results with clear verdicts so that I can quickly assess contract compliance and investigate specific obligations.**

## Tasks:
* Build responsive findings table with 8 detector rows
* Implement verdict color coding (Pass/Weak/Missing/Needs Review)
* Create expandable detail drawer with evidence snippets
* Add filtering and search capabilities within findings
* Integrate with backend findings API from Epic 2
* Implement copy-to-clipboard functionality for evidence text

## Acceptance Criteria:
* Table displays 8 GDPR detector rows with verdict colors and short rationales
* Detail drawer opens on click showing full evidence snippet + rule ID + copy button
* Filter functionality allows filtering by verdict status (Pass/Weak/Missing/Needs Review)
* Search functionality works within evidence snippets and rule descriptions
* Table is responsive and works on mobile devices
* Loading states and error handling for API failures
* Evidence snippets highlight the specific text that triggered the verdict

## Test Fixtures:
* **Complete analysis:** Document with all 8 detectors showing varied verdicts
* **Mixed results:** Some Pass, some Weak, some Missing verdicts to test filtering
* **Large evidence:** Long evidence snippets to test drawer scrolling and copy functionality
* **Mobile view:** Responsive table behavior on different screen sizes

## Dev Notes

### Architecture Context
**Data Models:** [Source: shard-ready-arc/4-data-models.md]
- Uses Finding interface from Epic 2 with verdict, snippet, rule_id, location
- Integration with Document model for file metadata display

**Tech Stack:** [Source: shard-ready-arc/3-tech-stack.md]
- Next.js 14.2.x: Server-side rendering for findings page
- React 18.2.x: Interactive table and drawer components
- shadcn/ui: Table, drawer, and badge components
- Tailwind CSS 3.4.x: Responsive design and verdict color coding

**File Locations:** [Source: shard-ready-arc/6-project-structure.md]
- Main component: `apps/web/src/components/FindingsTable.tsx`
- Detail drawer: `apps/web/src/components/EvidenceDrawer.tsx`
- Verdict badges: `apps/web/src/components/VerdictBadge.tsx`
- Findings page: `apps/web/src/app/analysis/[id]/page.tsx`

### Technical Requirements
- Performance: Table should render <500ms for 8 findings
- Accessibility: Full keyboard navigation and screen reader support
- Responsive: Mobile-first design with collapsible columns
- UX: Smooth animations for drawer open/close
- Data: Real-time updates when analysis completes

### Previous Story Dependencies
- **EPIC2-STORY2.2**: Detector Runner - provides Finding records via API
- **EPIC1-STORY1.3**: Evidence Window Builder - provides formatted evidence snippets
- **Existing UI components**: VerdictBadge component already exists in codebase

### API Integration
- GET `/api/analysis/{doc_id}/findings` - Fetch all findings for document
- Findings data includes: verdict, rule_id, snippet, location, confidence_score
- Real-time updates via polling or WebSocket (optional enhancement)

## Tasks / Subtasks

1. **Core Table Component** (AC: 1, 6)
   - Create responsive FindingsTable component using shadcn/ui Table
   - Implement verdict color coding with proper contrast ratios
   - Add loading skeleton states for API calls
   - Create error boundary for graceful failure handling

2. **Evidence Detail Drawer** (AC: 2, 7)
   - Build EvidenceDrawer component with smooth slide animations
   - Display full evidence snippet with syntax highlighting
   - Add rule ID display with rule description lookup
   - Implement copy-to-clipboard with success feedback

3. **Filtering and Search** (AC: 3, 4)
   - Create verdict filter dropdown with multi-select capability
   - Implement client-side search within evidence snippets
   - Add search highlighting within evidence text
   - Create filter/search state management

4. **Responsive Design** (AC: 5)
   - Implement mobile-first responsive table layout
   - Add collapsible columns for smaller screens
   - Create touch-friendly drawer interactions
   - Test across device sizes and orientations

5. **API Integration** (AC: 6)
   - Integrate with findings API from Epic 2
   - Add proper error handling and retry logic
   - Implement loading states during API calls
   - Add data validation for finding records

6. **Testing and Accessibility** (AC: All)
   - Unit tests for component logic and interactions
   - Integration tests with mock API responses
   - Accessibility testing with screen readers
   - Visual regression testing for verdict colors

## Testing
- Unit tests: Component rendering, filtering, search functionality
- Integration tests: API integration and data flow
- E2E tests: Complete user workflow from upload to findings review
- Accessibility tests: Keyboard navigation and screen reader compatibility

## Artifacts
* `apps/web/src/components/FindingsTable.test.tsx` - Component unit tests
* `apps/web/src/types/findings.ts` - TypeScript interfaces for findings data
* `docs/artifacts/findings_ui_mockup.png` - UI design reference
* `docs/artifacts/mobile_findings_flow.mp4` - Mobile interaction demo

## Change Log
- Status: Draft
- Created: 2025-09-02
- Epic: E3 (Findings & Report UI)
- Dependencies: EPIC2-STORY2.2 (Detector Runner), EPIC1-STORY1.3 (Evidence Window Builder)

## Dev Agent Record
- Status: Draft
- Next: Ready for UI development and API integration
- Estimated effort: 4-6 days (complex UI with responsive design requirements)
