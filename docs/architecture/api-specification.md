# Blackletter Backend API Specification

This document provides a formal OpenAPI 3.0 specification for the Blackletter backend API, built on FastAPI. It serves as the single source of truth for all API endpoints, data models, and contracts, ensuring consistency between the frontend and backend development teams.

## 1. API Overview

  - **Title**: Blackletter GDPR Checker API
  - **Version**: 1.0
  - **Description**: A rules-first API for analyzing GDPR Art. 28(3) compliance in vendor contracts.
  - **Server URL**: `http://localhost:8000/api`

## 2. Core API Routes

The API is structured around the core user workflow: uploading a document, checking its status, retrieving findings, and exporting a report.

### 2.1 Document Upload

  - **Endpoint**: `POST /contracts`
  - **Description**: Initiates an analysis job for an uploaded contract.
  - **Request**: `multipart/form-data` with a `file` field (PDF/DOCX, ≤10MB).
  - **Response**: `200 OK` with a JSON object containing the `analysis_id`.
    ```json
    {
      "analysis_id": "string",
      "status": "queued"
    }
    ```
  - **Error Responses**: `400 Bad Request` for unsupported file types or sizes.

### 2.2 Analysis Status & Results

  - **Endpoint**: `GET /analyses/{analysis_id}`
  - **Description**: Retrieves a summary of a specific analysis, including its status and metrics.
  - **Response**: `200 OK` with an `Analysis` object.
  - **Endpoint**: `GET /analyses/{analysis_id}/findings`
  - **Description**: Retrieves a list of all findings for a given analysis.
  - **Response**: `200 OK` with an array of `Finding` objects.

### 2.3 Reports

  - **Endpoint**: `POST /reports/{analysis_id}`
  - **Description**: Generates an exportable report (HTML or PDF) for a completed analysis.
  - **Request**: JSON body with a `format` field.
    ```json
    {
      "format": "pdf"
    }
    ```
  - **Response**: `200 OK` with the URL path to the generated report file.

## 3. Data Models (Pydantic)

The following models define the structure of data exchanged via the API.

### 3.1 `Finding` Model

The `Finding` model represents a single compliance result from a detector.

```python
class Finding(BaseModel):
  detector_id: str
  rule_id: str
  verdict: Literal["pass", "weak", "missing", "needs_review"]
  snippet: str
  page: int | None
  start: int | None
  end: int | None
  rationale: str | None
```

  - **`detector_id`**: The ID of the specific GDPR detector (e.g., `A28_3_c_security`).
  - **`rule_id`**: The ID of the specific rule triggered within the rulepack.
  - **`verdict`**: The result of the detector, using our four-valued logic.
  - **`snippet`**: The relevant text from the contract document as evidence.
  - **`rationale`**: A short, human-readable explanation for the verdict.

### 3.2 `Analysis` Model

The `Analysis` model represents a single document analysis job and its metadata.

```python
class Analysis(BaseModel):
  id: str
  status: Literal["queued", "processing", "done", "error"]
  filename: str
  created_at: datetime
  metrics: dict  # {p95_ms: int, tokens: int, explainability: float}
```

  - **`status`**: The current state of the analysis job.
  - **`metrics`**: A dictionary containing key performance metrics for the analysis.
