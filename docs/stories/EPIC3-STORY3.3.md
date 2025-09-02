# Story 3.3: Dashboard History

**ID:** EPIC3-STORY3.3

**As a user, I want to view a history of my past analyses on the dashboard so that I can track my work, identify trends, and access previous results without re-running an analysis.**

## Tasks:
* Implement a dashboard view to display a list of historical analyses.
* Show key information for each analysis, such as filename, date, and a summary of findings.
* Allow users to click on a historical analysis to view its detailed report.
* Implement filtering and searching capabilities to help users find specific past analyses.
* Provide visualizations of historical data, such as trends in compliance over time.
* Establish a data retention policy and a mechanism for archiving or purging old analyses.

## Acceptance Criteria:
* The dashboard displays a list of the user's past analyses, sorted by date in descending order.
* Each item in the list shows the document filename, analysis timestamp, and a summary of verdicts (e.g., compliant, non-compliant counts).
* Clicking on an analysis in the list navigates the user to the detailed findings view for that analysis.
* Users can filter the history list by verdict type (e.g., show only analyses with non-compliant findings).
* A search bar allows users to find analyses by filename.
* The dashboard includes a chart showing the trend of compliance verdicts over the last 30 days.
* A clear data retention policy is defined and communicated to the user (e.g., "Analysis history is kept for 90 days").
* The system automatically archives or deletes analyses older than the retention period.

## Test Fixtures:
* **Populated History:** A user account with a significant number of past analyses (e.g., >50) to test pagination and performance.
* **Empty History:** A new user account with no analysis history to test the empty state.
* **Mixed Verdicts:** A set of analyses with a variety of verdict distributions to test filtering and summary accuracy.
* **Long Filenames:** Analyses with long filenames to test UI layout and truncation.

## Dev Notes

### Architecture Context
**Data Models:**
- Leverages the existing `Analysis` and `Finding` models.
- May require adding a `last_accessed` timestamp to the `Analysis` model for tracking user activity.

**Tech Stack:**
- **Frontend:** Next.js for the dashboard UI, a charting library (e.g., Recharts or Chart.js) for visualizations.
- **Backend:** FastAPI to provide API endpoints for fetching historical data.
- **Database:** PostgreSQL to store analysis metadata and findings.

**File Locations:**
- **Dashboard Component:** `apps/web/src/components/DashboardHistory.tsx`
- **API Endpoints:** `apps/api/blackletter_api/routers/dashboard.py`
- **Service Layer:** `apps/api/blackletter_api/services/dashboard_service.py`

### Technical Requirements
- **Performance:** The dashboard history should load within 2 seconds for a user with up to 1,000 analyses.
- **Scalability:** The backend should be able to handle a large volume of historical data and user activity.
- **Data Integrity:** Historical data must be accurate and consistent with the original analysis results.
- **Security:** Users should only be able to see their own analysis history.

### Dependencies
- **EPIC1-STORY1.4:** Display Analysis Findings UI - The history view will link to the detailed findings page.
- **EPIC3-STORY3.2:** Report Export - Users may want to export reports from the history view.

## Tasks / Subtasks

1.  **Backend API Development** (AC: 1, 2, 5)
    *   Create a new endpoint `GET /api/dashboard/history` that returns a paginated list of a user's past analyses.
    *   The endpoint should support filtering by verdict and searching by filename.
    *   Create an endpoint `GET /api/dashboard/trends` that returns data for the compliance trend chart.

2.  **Frontend Dashboard UI** (AC: 1, 2, 3, 4)
    *   Develop a new React component `DashboardHistory` to display the list of past analyses.
    *   Implement client-side controls for filtering and searching.
    *   Ensure the UI is responsive and works well on different screen sizes.

3.  **Data Visualization** (AC: 6)
    *   Integrate a charting library into the frontend.
    *   Develop a component to render the compliance trend chart based on data from the backend.

4.  **Data Retention and Archiving** (AC: 7, 8)
    *   Implement a scheduled job (e.g., using Celery or a similar task queue) to enforce the data retention policy.
    *   Define the archiving strategy (e.g., move to cold storage or delete).

5.  **Testing and Validation** (AC: All)
    *   Write unit tests for the new API endpoints and backend services.
    -   Write component tests for the `DashboardHistory` UI.
    *   Perform end-to-end testing to ensure the entire feature works as expected.

## Testing
- **Unit Tests:** Verify the logic of the backend services and API endpoints.
- **Integration Tests:** Test the interaction between the frontend and backend.
- **E2E Tests:** Simulate user flows, such as filtering the history and clicking on an analysis.
- **Performance Tests:** Ensure the dashboard loads quickly, even with a large amount of historical data.

## Artifacts
*   `docs/api/dashboard.md` - API documentation for the new dashboard endpoints.
*   `docs/schemas/Dashboard.ts` - TypeScript definitions for the data structures used in the dashboard.

## Change Log
- **Status:** Draft
- **Created:** 2025-09-02
- **Epic:** E3 (Findings & Report UI)
- **Dependencies:** EPIC1-STORY1.4, EPIC3-STORY3.2

## Dev Agent Record
- **Status:** Draft
- **Next:** Ready for implementation.
- **Estimated effort:** 8-10 days
