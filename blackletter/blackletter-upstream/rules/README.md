# Compliance Rules

This directory houses regulatory and compliance rule definitions used by
Blackletter Systems. Rules are grouped by category so related regulations stay
organized and easy to manage.

## Organization

- Top-level YAML files (for example `gdpr.yaml`, `uk_ics.yaml`) contain broad
  guidance for specific regimes.
- `compliance/` holds JSON rule sets such as `aml_kyc.json` and `gdpr.json`.
- `property/` contains property-specific clauses and references.

When adding a new rule, place it in the directory that matches the regulation or
create a new subdirectory if needed. Include a descriptive filename and update
this list accordingly.

## Existing Rule Categories

- GDPR
- UK ICS
- AML/KYC
- Property compliance

