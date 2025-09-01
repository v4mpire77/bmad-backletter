# Quality Assurance Checklist

This checklist provides steps to validate the framework before release.

## Automated Verification
- [ ] Run unit tests: `pytest`
- [ ] Run integration tests: `pytest tests/integration`
- [ ] Run performance benchmarks: `python scripts/benchmark_rag.py`
- [ ] Lint code: `flake8` or `black --check .`
- [ ] Run security scan: `bandit -r backend`

## Manual Verification
- [ ] Validate major user flows in the UI
- [ ] Confirm API endpoints enforce authentication and authorization
- [ ] Review logs for sensitive information
- [ ] Verify error messages do not leak implementation details

Record outcomes for each item and escalate any failures according to project policy.
