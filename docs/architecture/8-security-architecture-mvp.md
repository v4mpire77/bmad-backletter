# 8) Security Architecture (MVP)

* **Uploads**: PDF/DOCX only; size limit 10MB; quarantine temp dir; checksum.
* **PII**: No snippets logged; redact before any LLM call.
* **Auth**: Minimal roles (Admin/Reviewer) in Phase 2; for MVP gate UI features behind local config.
* **Transport/At-Rest**: TLS; at-rest via platform storage/DB.
* **Secrets**: env vars; `git-secrets` in CI.
* **Audit**: settings changes, exports, role changes (Phase 2).
  Threats & controls are expanded in `docs/security_architecture.md`.
