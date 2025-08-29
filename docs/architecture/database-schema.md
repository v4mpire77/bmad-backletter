# Blackletter Database Schema Document

This document defines the database schema for the Blackletter application. The primary goal is to provide a single source of truth for the data layer, ensuring consistency between the backend services and the storage solution.

## 1. Database Strategy

The project will initially use **SQLite** for a lightweight, file-based local development environment. In Phase 2, the application will migrate to a production-grade **PostgreSQL** database, such as **Supabase**, to support scalability and multi-tenancy. All schema definitions in this document are designed to be compatible with both database systems.

## 2. Core Tables

The following tables represent the core data entities of the Blackletter application, corresponding to the Pydantic models defined in our API specification:

### 2.1 `analyses` Table

This table stores the metadata for each document analysis job.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY` | Unique identifier for the analysis. |
| `filename` | `TEXT` | `NOT NULL` | The original name of the uploaded file. |
| `size_bytes` | `INTEGER` | `NOT NULL` | The size of the file in bytes. |
| `mime` | `TEXT` | `NOT NULL` | The MIME type of the uploaded file. |
| `status` | `TEXT` | `NOT NULL` | The current status of the analysis job (`queued`, `processing`, `done`, `error`). |
| `created_at` | `TIMESTAMP` | `NOT NULL` | The timestamp when the analysis job was created. |
| `updated_at` | `TIMESTAMP` | `NULL` | The timestamp of the last update to the analysis job. |
| `metrics` | `JSONB` | `NULL` | Stores key performance metrics for the analysis job. |
| `org_id` | `UUID` | `NULL` | Identifier for the organization, for future multi-tenancy. |

### 2.2 `findings` Table

This table stores the results from the rule-based detection engine for each document. It is related to the `analyses` table by a foreign key.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Unique identifier for the finding. |
| `analysis_id` | `UUID` | `NOT NULL` `REFERENCES analyses(id)` | Foreign key linking to the analysis job. |
| `detector_id` | `TEXT` | `NOT NULL` | The ID of the specific GDPR detector (e.g., `A28_3_c_security`). |
| `rule_id` | `TEXT` | `NOT NULL` | The specific rule triggered within the rulepack. |
| `verdict` | `TEXT` | `NOT NULL` | The verdict for the finding (`pass`, `weak`, `missing`, `needs_review`). |
| `snippet` | `TEXT` | `NOT NULL` | The relevant text snippet as evidence. |
| `page` | `INTEGER` | `NULL` | The page number where the finding was located. |
| `start_offset` | `INTEGER` | `NULL` | The character start offset of the snippet. |
| `end_offset` | `INTEGER` | `NULL` | The character end offset of the snippet. |
| `rationale` | `TEXT` | `NULL` | A short, human-readable rationale for the verdict. |
| `reviewed` | `BOOLEAN` | `NOT NULL` `DEFAULT FALSE` | A flag to track if the finding has been reviewed by a user. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | The timestamp when the finding was created. |

### 2.3 `storage_artifacts` Table

This table tracks the location and metadata of files created during the analysis process.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Unique identifier for the artifact. |
| `analysis_id` | `UUID` | `NOT NULL` `REFERENCES analyses(id)` | Foreign key linking to the analysis job. |
| `artifact_type` | `TEXT` | `NOT NULL` | The type of artifact (`text`, `report_pdf`, `report_html`, `page_map`, etc.). |
| `filepath` | `TEXT` | `NOT NULL` | The relative path to the artifact file on disk. |
| `checksum` | `TEXT` | `NULL` | The checksum of the file to ensure integrity. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | The timestamp when the artifact was created. |
