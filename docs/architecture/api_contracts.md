# Blackletter - API Contracts

This document provides the authoritative API contract specifications for the Blackletter MVP, as approved by the Product Owner.

## 1. Endpoint Specifications

### POST /api/contracts
-   **Description**: Uploads a contract (PDF/DOCX ≤10MB), creates an `analysis` record, and enqueues an asynchronous analysis job.
-   **Request**: `multipart/form-data` with a `file` field.
-   **Response (201 Created)**:
    ```json
    {
      "job_id": "uuid",
      "analysis_id": "uuid",
      "status": "queued"
    }
    ```

### GET /api/jobs/{job_id}
-   **Description**: Returns the current status of a processing job.
-   **Response (200 OK)**:
    ```json
    {
      "job_id": "uuid",
      "status": "queued|running|done|error",
      "error": null | "error_details"
    }
    ```

### GET /api/analyses/{analysis_id}
-   **Description**: Returns a summary of findings for a completed analysis, including the verdict for each of the 8 detectors.
-   **Response (200 OK)**:
    ```json
    {
      "analysis_id": "uuid",
      "filename": "dpa.pdf",
      "created_at": "2025-08-26T19:12:00Z",
      "verdicts": [
        {"detector_id":"A28_3_a_instructions","verdict":"pass"},
        {"detector_id":"A28_3_b_confidentiality","verdict":"weak"},
        // ... 6 more detectors
      ]
    }
    ```

### GET /api/analyses/{analysis_id}/findings
-   **Description**: Returns the full array of detailed findings with evidence snippets for a completed analysis.
-   **Response (200 OK)**: `Finding[]` (See Finding Model below).

### POST /api/reports/{analysis_id}
-   **Description**: Triggers the generation of an exportable report (PDF/HTML).
-   **Response (201 Created)**:
    ```json
    {
      "url": "/api/reports/{generated_file_name}.pdf"
    }
    ```

### GET /api/reports
-   **Description**: Returns a list of generated report exports.
-   **Response (200 OK)**: `ReportExport[]`

## 2. Shared Schemas

### Finding Model
This is the authoritative shape for a single finding object.
```json
{
  "detector_id": "A28_3_c_security",
  "rule_id": "art28_v1.A28_3_c_security",
  "verdict": "pass|weak|missing|needs_review",
  "snippet": "...technical and organisational measures...",
  "page": 7,
  "start": 1423,
  "end": 1562,
  "rationale": "anchor present; no red-flag",
  "reviewed": false
}
```

### Error Model

All client-facing errors will use this standard shape.

```json
{
    "code": "error_code_string",
    "message": "User-friendly error message.",
    "hint": "Optional hint for resolution."
}
```