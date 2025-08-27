# Blackletter - Coding Standards

This document outlines the coding standards, conventions, and best practices for the Blackletter project.

## 1. Python (Backend)

-   **Linting & Formatting**: Ruff and Black are strictly enforced. All code must be formatted with Black before merging.
-   **Type Hinting**: Use explicit types. Pydantic v2 models are required for all API request and response schemas.
-   **Asynchronous Code**: Use `async` endpoints for I/O-bound operations to maintain performance.
-   **Code Organization**: Business logic must reside in `services/` modules. API route handlers in `routers/` should be thin and only handle request/response orchestration.

## 2. TypeScript/React (Frontend)

-   **Linting & Formatting**: ESLint and Prettier are strictly enforced.
-   **Component Style**: Use functional components with hooks. Avoid class components.
-   **State Management**: Use React Query for all server state, caching, and data fetching logic. Custom hooks abstracting React Query calls should be placed in `web/lib/`.
-   **UI Logic**: The UI should remain evidence-first, avoiding heavy global state management where possible.

## 3. Testing Conventions

-   **Unit Tests**:
    -   Backend unit tests will be written using Pytest.
    -   Detector logic must be tested with a minimum of 3 positive and 3 hard negative examples to start.
    -   Frontend unit/integration tests will use Vitest.
-   **Integration Tests**:
    -   Focus on the end-to-end flow from upload to findings generation.
    -   Selected API responses should be snapshot tested to prevent regressions.
-   **End-to-End (E2E) Tests**:
    -   Playwright will be used to test critical user flows like document upload, reviewing the findings table, and exporting a report.