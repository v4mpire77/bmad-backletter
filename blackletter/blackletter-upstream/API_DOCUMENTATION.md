# Blackletter Systems - API Documentation

## Overview

The Blackletter Systems API provides endpoints for document upload, processing, and analysis. The API is built with FastAPI and follows RESTful principles.

## Base URL

```
Development: http://localhost:8000
Production: https://api.blacklettersystems.com
```

## Authentication

Currently, the API operates without authentication for development. Production will implement JWT-based authentication.

## Endpoints

### 1. Health Check

**GET** `/health`

Check API health and status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### 2. Document Upload & Review

**POST** `/api/review`

Upload a document for analysis and review.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file

**Parameters:**
- `file` (required): PDF document to analyze
- `analysis_type` (optional): Type of analysis ("contract", "compliance", "risk")

**Response:**
```json
{
  "job_id": "job_12345",
  "status": "processing",
  "message": "Document uploaded successfully",
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

**Error Responses:**
```json
{
  "error": "File too large",
  "message": "Maximum file size is 10MB",
  "status_code": 400
}
```

### 3. Job Status

**GET** `/api/job/{job_id}`

Get the status of a processing job.

**Response:**
```json
{
  "job_id": "job_12345",
  "status": "completed",
  "progress": 100,
  "result": {
    "document_id": "doc_67890",
    "analysis_url": "/api/analysis/doc_67890"
  }
}
```

### 4. Analysis Results

**GET** `/api/analysis/{document_id}`

Retrieve the analysis results for a processed document.

**Response:**
```json
{
  "document_id": "doc_67890",
  "filename": "contract.pdf",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:32:00Z",
  "analysis": {
    "summary": "This is a commercial lease agreement...",
    "risk_score": 7.5,
    "risk_level": "medium",
    "key_findings": [
      {
        "type": "termination_clause",
        "severity": "high",
        "description": "Unusual termination terms detected",
        "location": "Section 12, Page 3"
      }
    ],
    "compliance_issues": [
      {
        "regulation": "GDPR",
        "issue": "Data processing clause missing",
        "recommendation": "Add explicit data processing terms"
      }
    ],
    "recommendations": [
      "Review termination clause for fairness",
      "Add data protection provisions",
      "Clarify liability limitations"
    ]
  },
  "metadata": {
    "parties": ["Landlord Ltd", "Tenant Corp"],
    "effective_date": "2024-01-01",
    "expiry_date": "2029-01-01",
    "document_type": "commercial_lease"
  }
}
```

### 5. Document List

**GET** `/api/documents`

List all processed documents (paginated).

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)
- `status` (optional): Filter by status ("completed", "processing", "failed")

**Response:**
```json
{
  "documents": [
    {
      "document_id": "doc_67890",
      "filename": "contract.pdf",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "status": "completed",
      "risk_score": 7.5
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### 6. Export Report

**GET** `/api/export/{document_id}`

Export analysis results in various formats.

**Query Parameters:**
- `format` (required): Export format ("pdf", "docx", "json")

**Response:**
- File download with appropriate Content-Type

### 7. Batch Processing

**POST** `/api/batch`

Upload multiple documents for batch processing.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Multiple PDF files

**Response:**
```json
{
  "batch_id": "batch_12345",
  "total_files": 5,
  "accepted_files": 4,
  "rejected_files": 1,
  "jobs": [
    {
      "filename": "contract1.pdf",
      "job_id": "job_12346",
      "status": "queued"
    }
  ]
}
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid input or file format
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File exceeds size limit
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Rate Limiting

- **Upload endpoints:** 10 requests per minute
- **Analysis endpoints:** 60 requests per minute
- **Status endpoints:** 120 requests per minute

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642234567
```

## File Requirements

### Supported Formats
- **Primary:** PDF (recommended)
- **Future:** DOCX, TXT

### File Size Limits
- **Maximum:** 10MB per file
- **Recommended:** Under 5MB for optimal performance

### Content Requirements
- Text-based documents (not scanned images)
- Clear, readable text
- Standard legal document formatting

## WebSocket Endpoints

### Real-time Status Updates

**WebSocket:** `/ws/job/{job_id}`

Receive real-time updates on job processing:

```json
{
  "type": "progress",
  "job_id": "job_12345",
  "progress": 75,
  "stage": "analysis",
  "message": "Analyzing document structure..."
}
```

## SDK Examples

### Python Client

```python
import requests

# Upload document
with open('contract.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/review',
        files={'file': f}
    )
    job_id = response.json()['job_id']

# Check status
status = requests.get(f'http://localhost:8000/api/job/{job_id}')
print(status.json())

# Get results
results = requests.get(f'http://localhost:8000/api/analysis/{document_id}')
print(results.json())
```

### JavaScript Client

```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/review', {
  method: 'POST',
  body: formData
});

const { job_id } = await response.json();

// Check status
const status = await fetch(`/api/job/${job_id}`);
const statusData = await status.json();
```

## Testing

Use the provided test file `scripts/test_upload.http` with VS Code REST Client extension:

```http
POST http://localhost:8000/api/review
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

< ./test.pdf
------WebKitFormBoundary--
```

## Versioning

API versioning is handled through URL paths:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, etc.

## Deprecation Policy

- Deprecated endpoints will be marked with `X-Deprecated` header
- 6-month notice before removal
- Migration guides provided for breaking changes
