# Integration Test Scenarios

High-level scenarios to exercise the system end to end.

1. **Document Upload and Query**
   - Upload a PDF via `/api/rag/upload`.
   - Query uploaded content using `/api/rag/query`.
   - Ensure citations reference correct document chunks.
2. **Authentication Enforcement**
   - Attempt to access protected endpoints without credentials.
   - Verify requests are rejected with `401` responses.
3. **Gemini Chat Endpoint**
   - Post a prompt to `/api/chat` with valid credentials.
   - Confirm a response is returned and logged.
4. **Health Check**
   - Call `/health` to verify service availability and headers.

These scenarios guide development of automated integration tests.
