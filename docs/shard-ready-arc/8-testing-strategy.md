# Testing Strategy

## Backend Unit Tests (Pytest)

Focus on the business logic within the services, particularly the rule engine's verdict logic and the text extraction/sentence splitting functions.

## Backend Integration Tests (Pytest)

Test the API endpoints' interaction with the database and the full processing pipeline from file upload to finding persistence.

## Frontend Component Tests (Vitest/RTL)

Test individual React components in isolation to verify rendering and user interactions.

## E2E Smoke Test (Playwright)

A single, critical-path test that simulates the entire user journey: uploading a document, polling for completion, viewing the findings, opening the evidence drawer, and exporting the report.
