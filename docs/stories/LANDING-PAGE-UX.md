# Story: Enhance Landing Page UX and Functionality

- **Epic:** `LANDING-PAGE-UX`
- **Story ID:** `UX-1`
- **Jira:** `BL-78`
- **Dependencies:** `0.2-landing-page-minimal`

## Description

As a user, I want a more intuitive and feature-rich landing page that seamlessly integrates the contract analysis workflow, offers a comfortable viewing experience with a dark theme, and provides a clear and engaging user journey.

## Acceptance Criteria

### AC1: Contract Analysis Workflow Integration
- A prominent and intuitive file upload area is present, supporting drag-and-drop.
- Upon file upload, a new analysis job is initiated, and the user is redirected to a job status page.
- A section "Recent Analyses" is displayed, listing the last 5 contract analyses with their status (e.g., "Completed," "In Progress") and a link to the alysis.
- The "Start Analysis" button from the minimal landing page is replaced with this more advanced upload component.

### AC2: Dark Theme Optimization
- A theme switcher (e.g., a toggle button with a moon/sun icon) is available in the header.
- The entire landing page, including text, buttons, and background, correctly adapts to the selected theme (light/dark).
- The selected theme is persisted across sessions (e.g., using `localStorage`).
- All UI components are legible and aesthetically pleasing in both themes.

### AC3: User Journey Enhancement
- A clear and concise headline and sub-headline explain the value proposition of Blackletter.
- A "How it Works" section with 3-4 simple steps (e.g., Upload, Analyze, Review) visually guides the user.
- A "Features" section highlights key capabilities of the application (e.g., AI-powered analysis, comprehensive rule sets, detailed reporting).
- The navigation header is clean and provides links to key sections (e.g., Dashboard, Settings, Help).

## Technical Implementation Notes

- **File Upload:**
  - Use a library like `react-dropzone` or a custom hook for the drag-and-drop functionality.
  - On file drop, call the `/api/jobs` endpoint (or equivalent) to create a new analysis job.
  - Use `next/router` to redirect the user to the job status page (`/status/[jobId]`).
- **Dark Theme:**
  - Implement theme switching using `next-themes` library with `ThemeProvider`.
  - Use CSS variables for colors to allow for easy theme switching. Tailwind CSS's dark mode variant (`dark:`) is recommended.
- **UI Components:**
  - Use a component library like `shadcn/ui` to build the UI elements (buttons, cards, etc.) for a consistent look and feel.
  - The "Recent Analyses" section will require fetching data from a new API endpoint (e.g., `/api/analyses/recent`). This can be mocked for this story if the API is not ready.
- **State Management:**
  - Use `React Query` or `SWR` for fetching and managing server state (e.g., recent analyses).

## Testing Requirements

- **Unit Tests:**
  - Test the file upload component: verify that it accepts files and calls the upload function.
  - Test the theme switcher: verify that it toggles the theme and updates the UI.
  - Test any new UI components in isolation.
- **Integration Tests:**
  - Test the end-to-end file upload flow: upload a file and verify redirection to the status page.
  - Test that the "Recent Analyses" section correctly displays data from the (mocked) API.
- **Manual QA:**
  - Verify the entire landing page in both light and dark modes on major browsers (Chrome, Firefox, Safari).
  - Test the drag-and-drop functionality with various file types.
  - Ensure the layout is responsive and looks good on different screen sizes.
