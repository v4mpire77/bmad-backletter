# API Specification

The backend will expose a RESTful API. The initial endpoints for Sprint 1 are defined below in OpenAPI 3.0 format.

```yaml
openapi: 3.0.0
info:
  title: Blackletter API
  version: v1.0
servers:
  - url: /v1
    description: Version 1 API
paths:
  /docs/upload:
    post:
      summary: Upload a contract for analysis
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        '202':
          description: Accepted for processing
          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id:
                    type: string
  /jobs/{job_id}:
    get:
      summary: Get the status of a processing job
      parameters:
        - name: job_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Job status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'
  /docs/{doc_id}/findings:
    get:
      summary: Get the analysis findings for a document
      parameters:
        - name: doc_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: List of findings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Finding'
  /exports/{doc_id}.html:
    get:
      summary: Export the findings as an HTML report
      parameters:
        - name: doc_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: HTML report
          content:
            text/html:
              schema:
                type: string
components:
  schemas:
    Job:
      type: object
      properties:
        id: { type: string }
        doc_id: { type: string }
        status: { type: string, enum: [queued, running, done, error] }
        error_message: { type: string }
    Finding:
      type: object
      properties:
        id: { type: string }
        rule_id: { type: string }
        verdict: { type: string, enum: [pass, weak, missing, needs_review] }
        snippet: { type: string }
        location:
          type: object
          properties:
            page: { type: integer }
            start_char: { type: integer }
            end_char: { type: integer }
```
