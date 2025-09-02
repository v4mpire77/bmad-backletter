# Testing Strategy

## Backend Unit (Pytest)

- Focus: rule engine logic, sentence splitter, and PDF/DOCX extraction fallbacks.

## Backend Integration (Pytest)

- Focus: full pipeline from upload -> processing -> persistence.

## Frontend Component (Vitest + RTL)

- Focus: FindingsTable, VerdictBadge, EvidenceDrawer.

## E2E (Playwright)

- Single critical-path smoke test: upload document, poll job, view findings, open evidence, export report.
