# Integration Architecture

## Summary

Explains how Blackletter interacts with external systems and services.

## External Services

- **LLM providers** – optional detectors; access abstracted behind `llm_gate`.
- **Object storage** – store generated PDFs for download links.
- **Email/Notification services** – future hook for report delivery.

## Patterns

- Prefer synchronous REST calls for Phase‑1 integrations.
- Use webhooks or message queues for future asynchronous flows.

## Data Exchange

- All data serialized as JSON or multipart form data.
- Strict schema validation on ingress and egress.

## Resilience

- Timeouts and retries for external calls.
- Circuit breakers around non-critical integrations.
