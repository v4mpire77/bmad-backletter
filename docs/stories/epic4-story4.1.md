# <!-- Powered by BMAD™ Core -->
template:
  id: story-template-v2
  name: Story Document
  version: 2.0
  output:
    format: markdown
    filename: docs/stories/4.1.metrics-wall.md
    title: "Story 4.1: Metrics Wall"

workflow:
  mode: interactive
  elicitation: advanced-elicitation

agent_config:
  editable_sections:
    - Status
    - Story
    - Acceptance Criteria
    - Tasks / Subtasks
    - Dev Notes
    - Testing
    - Change Log

sections:
  - id: status
    title: Status
    type: choice
    choices: [Draft, Approved, InProgress, Review, Done]
    instruction: Select the current status of the story
    owner: scrum-master
    editors: [scrum-master, dev-agent]
    value: Draft

  - id: story
    title: Story
    type: template-text
    template: |
      **As a** System Administrator,
      **I want** a real-time metrics display system with performance monitoring and alerting capabilities,
      **so that** I can have a comprehensive overview of the system's health, performance, and costs.
    instruction: Define the user story using the standard format with role, action, and benefit
    elicit: true
    owner: scrum-master
    editors: [scrum-master]

  - id: acceptance-criteria
    title: Acceptance Criteria
    type: numbered-list
    instruction: Copy the acceptance criteria numbered list from the epic file
    elicit: true
    owner: scrum-master
    editors: [scrum-master]
    value: |
      1. A dedicated, real-time metrics dashboard page is available.
      2. The dashboard displays key performance indicators (KPIs) with visual charts and graphs.
      3. Performance monitoring for API endpoints is implemented, tracking metrics like p95 latency.
      4. The system includes an alerting mechanism for critical system health events (e.g., high error rates, latency spikes).
      5. Metrics for the document processing pipeline are tracked, including `tokens_per_doc` and the percentage of documents invoking LLMs.
      6. An "explainability rate" is displayed, showing the percentage of findings with associated evidence snippets and rule IDs.
      7. Access to the metrics dashboard is restricted to users with an 'Admin' role.

  - id: tasks-subtasks
    title: Tasks / Subtasks
    type: bullet-list
    instruction: |
      Break down the story into specific tasks and subtasks needed for implementation.
      Reference applicable acceptance criteria numbers where relevant.
    template: |
      - [ ] Task 1 (AC: # if applicable)
        - [ ] Subtask1.1...
      - [ ] Task 2 (AC: # if applicable)
        - [ ] Subtask 2.1...
      - [ ] Task 3 (AC: # if applicable)
        - [ ] Subtask 3.1...
    elicit: true
    owner: scrum-master
    editors: [scrum-master, dev-agent]
    value: |
      - [ ] **Backend:** Instrument API endpoints to capture performance metrics (p95 latency). (AC: 3)
      - [ ] **Backend:** Implement a service to collect and aggregate metrics for the document processing pipeline (`tokens_per_doc`, `%docs_invoking_LLM`, explainability rate). (AC: 5, 6)
      - [ ] **Backend:** Create a new API endpoint to expose the collected metrics data. (AC: 1)
      - [ ] **Backend:** Implement an alerting system to notify administrators of system health issues. (AC: 4)
      - [ ] **Frontend:** Create a new admin-only dashboard page for displaying metrics. (AC: 1, 7)
      - [ ] **Frontend:** Develop visual charts and graphs to display the key KPIs on the dashboard. (AC: 2)
      - [ ] **Frontend:** Integrate the dashboard with the backend metrics endpoint to display real-time data. (AC: 1)

  - id: dev-notes
    title: Dev Notes
    instruction: |
      Populate relevant information, only what was pulled from actual artifacts from docs folder, relevant to this story:
      - Do not invent information
      - If known add Relevant Source Tree info that relates to this story
      - If there were important notes from previous story that are relevant to this one, include them here
      - Put enough information in this section so that the dev agent should NEVER need to read the architecture documents, these notes along with the tasks and subtasks must give the Dev Agent the complete context it needs to comprehend with the least amount of overhead the information to complete the story, meeting all AC and completing all tasks+subtasks
    elicit: true
    owner: scrum-master
    editors: [scrum-master]
    value: |
      - **Tech Stack:** The frontend is a Next.js application. The backend is a Python FastAPI application.
      - **Authentication:** The application uses role-based access control. Ensure the new dashboard page is only accessible by users with the 'Admin' role.
      - **Data Visualization:** Use a library like Recharts or Chart.js for creating the charts and graphs on the frontend.
      - **Metrics Collection:** Consider using a library like Prometheus for collecting and storing metrics on the backend.
      - **Alerting:** The alerting system could be integrated with a service like PagerDuty or send notifications via email or Slack.
      - **Token Metrics:** Integration with the token ledger (Story 2.4) will be necessary for accurate token metrics.

  - id: testing-standards
    title: Testing
    instruction: |
      List Relevant Testing Standards from Architecture the Developer needs to conform to:
      - Test file location
      - Test standards
      - Testing frameworks and patterns to use
      - Any specific testing requirements for this story
    elicit: true
    owner: scrum-master
    editors: [scrum-master]
    value: |
      - **Unit Tests:** Write unit tests for the new backend services and API endpoints.
      - **Integration Tests:** Create integration tests to verify the end-to-end flow of metrics collection and display.
      - **Frontend Tests:** Write component tests for the new dashboard page and its components.
      - **E2E Tests:** Add end-to-end tests to simulate an admin user viewing the metrics dashboard.
      - **Security Tests:** Ensure that the new endpoint and dashboard page are properly secured and only accessible by admin users.

  - id: change-log
    title: Change Log
    type: table
    columns: [Date, Version, Description, Author]
    instruction: Track changes made to this story document
    owner: scrum-master
    editors: [scrum-master, dev-agent, qa-agent]
    value: |
      | Date       | Version | Description              | Author |
      |------------|---------|--------------------------|--------|
      | 2025-09-02 | 1.0     | Initial draft of the story | Jules  |

  - id: dev-agent-record
    title: Dev Agent Record
    instruction: This section is populated by the development agent during implementation
    owner: dev-agent
    editors: [dev-agent]
    sections:
      - id: agent-model
        title: Agent Model Used
        template: "{{agent_model_name_version}}"
        instruction: Record the specific AI agent model and version used for development
        owner: dev-agent
        editors: [dev-agent]

      - id: debug-log-references
        title: Debug Log References
        instruction: Reference any debug logs or traces generated during development
        owner: dev-agent
        editors: [dev-agent]

      - id: completion-notes
        title: Completion Notes List
        instruction: Notes about the completion of tasks and any issues encountered
        owner: dev-agent
        editors: [dev-agent]

      - id: file-list
        title: File List
        instruction: List all files created, modified, or affected during story implementation
        owner: dev-agent
        editors: [dev-agent]

  - id: qa-results
    title: QA Results
    instruction: Results from QA Agent QA review of the completed story implementation
    owner: qa-agent
    editors: [qa-agent]
