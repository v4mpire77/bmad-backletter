# Story 1.4 — Display Analysis Findings UI (Dev Notes)

## Scope
Implement frontend logic for the Findings UI on the analysis detail page, including:
- Integration with analysis and findings API endpoints
- Displaying verdict chips with counts
- Handling asynchronous states with skeleton loaders
- Integrating the evidence drawer component

## Checklist
- Analyze API endpoints and determine data requirements
- Set up React Query hooks for data fetching (analysis and findings)
- Build UI components: `SkeletonLoader`, `VerdictChip`, `FindingsTable`, and `EvidenceDrawer`
- Integrate evidence drawer and verdict chips into the `FindingsTable`
- Implement verdict summary and filtering interactions
- Add unit tests for `FindingsTable` and `EvidenceDrawer`

## API Endpoints
- `GET /api/analyses/{id}`: Fetches job metadata and status
- `GET /api/analyses/{id}/findings`: Fetches an array of findings with verdicts in lowercase

## Frontend Changes
- Convert `apps/web/src/app/analyses/[jobId]/page.tsx` to a client component
- Add `useAnalysis` and `useFindings` hooks using React Query
- Create a `SkeletonLoader` component for shimmer loading states
- Implement a `VerdictChip` component to display verdict status
- Build a `FindingsTable` that shows verdict chips, the evidence drawer, and summary counts

## Acceptance Criteria (from PRD)
- The table lists obligations with verdicts: Pass, Weak, Missing, Needs Review
- Each finding displays a snippet and rule ID
- Table supports filtering by verdict
- Evidence drawer opens upon row click

## Implementation Notes
- API hooks: Use `NEXT_PUBLIC_API_URL` if set; otherwise, default to relative `/api/...` paths
- Show `SkeletonLoader` during data fetching
- Map lowercase API verdict values to user-friendly display labels on verdict chips
- `FindingsTable` includes counts, summary chips, and filter controls

## Validation
- Confirm data loads correctly and asynchronous states (error/skeleton/loading) are handled gracefully
- Ensure UI matches the specified behavior: chip displays, verdict summary, and evidence drawer interactions
- Test that filtering and evidence drawer operate according to requirements
- If any validation fails, attempt minimal corrections and revalidate before continuing

## Next Steps
- Replace the filter select dropdown with clickable verdict chips for improved UX
- Add a `VerdictSummary` component above the table for chip-based counts and filters
- Link the analyses list (`/analyses`) to detail pages
- Connect the `ExportDialog` to `POST /api/reports/{analysis_id}`

## Definition of Done
- Visiting `/analyses/{id}` fetches the analysis and findings from the API
- Verdict summary chips and the findings table are displayed
- Evidence drawer opens, showing a snippet, rule ID, and rationale
- Unit tests cover `FindingsTable` and `EvidenceDrawer` interactions

