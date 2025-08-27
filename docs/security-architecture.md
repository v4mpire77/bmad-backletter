# Security Architecture

## Summary

Principles and controls safeguarding data and execution.

## Threat Model

- Untrusted contract uploads.
- Accidental exposure of PII in logs or exports.
- Unauthorized access to analyses or reports.

## Controls

- Upload validation: MIME/type checks, 10 MB limit, checksum quarantine.
- Data handling: snippets redacted before any LLM call; no raw snippets logged.
- Transport: HTTPS everywhere; TLS termination at ingress.
- Secrets: environment variables with `git-secrets` scanning in CI.

## Access Management

- MVP: single-user local installs.
- Phase‑2: role-based access (Admin/Reviewer) with audit trails.

## Audit & Monitoring

- Log authentication events and settings changes.
- Periodic vulnerability scans of container images.
