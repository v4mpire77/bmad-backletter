# ADR 0002: Verdict Policy

## Status
Accepted

## Context
Findings must be deterministic and evidence-backed. A "pass" without a supporting anchor risks false confidence.

## Decision
- Every finding must contain at least one anchor span.
- Default to deterministic detection; LLM reasoning augments but never overrides evidence.

## Consequences
- Simplifies auditability and compliance.
- Requires rulepacks to define clear anchors.
