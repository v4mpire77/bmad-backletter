# Blackletter — Tests & QA (shard)

This shard covers testing strategy, golden fixtures, and acceptance criteria for smoke and integration tests.

## Testing Strategy

### Backend Unit (Pytest)

- Focus: rule engine logic, sentence splitter, and PDF/DOCX extraction fallbacks.

### Backend Integration (Pytest)

- Focus: full pipeline from upload -> processing -> persistence.

### Frontend Component (Vitest + RTL)

- Focus: FindingsTable, VerdictBadge, EvidenceDrawer.

### E2E (Playwright)

- Single critical-path smoke test: upload document, poll job, view findings, open evidence, export report.

## Golden Fixtures

- Include 3–5 canonical DPA documents with expected JSON outputs for regression.

## CI Gates

- Run linters, unit tests, and integration smoke tests on every PR. Block merge if failing.
