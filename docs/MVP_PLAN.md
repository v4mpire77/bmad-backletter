# MVP Plan for Blackletter

## Objective

Deliver a Minimum Viable Product (MVP) for the Blackletter contract analysis tool, focusing on the core functionality of uploading a contract, analyzing it for GDPR Article 28 compliance, and displaying the findings.

## Scope

The MVP will include the following core features:

1.  **Contract Upload & Job Orchestration (Story 1.1):** Users can upload PDF/DOCX contracts (≤10MB). The system will accept the file, create a job, and provide status updates (queued, running, done, error).
2.  **Text Extraction (Story 1.2):** Extract text, create a page map, and build a sentence index from uploaded PDF/DOCX files.
3.  **Evidence Window Builder (Story 1.3):** Build evidence windows around findings to provide context.
4.  **Rulepack Loader (Story 2.1):** Load and validate the GDPR Article 28 rulepack for the detection engine.
5.  **Detector Runner (Story 2.2):** Evaluate detectors over extracted text using the sentence index to produce findings with verdicts and snippets for GDPR Article 28 compliance analysis.
6.  **Findings Table (Story 3.1):** Display a table of findings for an analyzed contract, including Detector, Verdict, short rationale, and an evidence drawer.
7.  **Landing Page (Story 0.2):** A minimal landing page that introduces the product and provides a link to the new contract upload flow.

## Out of Scope

The following features are considered for future iterations and are not part of the initial MVP:

1.  **AI Risk Analysis Integration (Story 2.5):** Advanced multi-dimensional risk scoring.
2.  **Report Export (Story 3.2):** Exporting findings to PDF or HTML.
3.  **Dashboard History (Story 3.3):** A history of analyzed contracts.
4.  **Metrics Wall (Story 4.1):** A wall of metrics for monitoring system performance.
5.  **Coverage Meter (Story 4.2):** A meter to show the coverage of the rulepack.
6.  **Org Settings (Story 5.1):** Organization-level settings.
7.  **Minimal Auth Roles (Story 5.2):** Basic authentication and authorization.

## Implementation Order

1.  **Landing Page (Story 0.2):** This is a simple page that can be implemented quickly to provide a starting point for the application.
2.  **Contract Upload & Job Orchestration (Story 1.1):** This is the entry point for the core analysis functionality.
3.  **Text Extraction (Story 1.2):** This is a dependency for the detector runner.
4.  **Evidence Window Builder (Story 1.3):** This is a dependency for the detector runner.
5.  **Rulepack Loader (Story 2.1):** This is a dependency for the detector runner.
6.  **Detector Runner (Story 2.2):** This is the core analysis engine.
7.  **Findings Table (Story 3.1):** This is the primary way users will interact with the analysis results.

## Timeline

The implementation order above should allow for a focused and efficient development process. Each story should be completed and tested before moving on to the next. The goal is to have a working MVP within a short timeframe, prioritizing the core functionality and deferring advanced features for future releases.