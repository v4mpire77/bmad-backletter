# 6. Epic List
## Epic 1: Platform & Core Infrastructure
**Goal:** To build the foundational infrastructure, set up the development environment, and deliver a simple, user-facing document intake process. This epic will result in a fully deployable, albeit limited, version of the application that can receive a document and place it into a queue for processing. This proves the core architecture and user-facing intake process work before we build the complex back-end.

## Epic 2: Blackletter Core Analysis Engine
**Goal:** To implement the core of the Blackletter engine. This includes the deterministic processes for document segmentation, clause extraction, and rule-based risk detection against a basic, sample rulepack. The epic will not yet produce a user-facing report, but it will store the analysis findings, making them available for later display.

## Epic 3: Interactive Risk Dashboard & Reporting
**Goal:** To build the user-facing front end. This epic will create the Pocket Lawyer and Firm-Aware interfaces, including the risk dashboard with verdict chips, the evidence-first UX for findings, and the ability to generate a downloadable PDF/HTML report. This epic delivers the full user experience, making the analysis tangible and actionable.

## Epic 4: GDPR Compliance & Advanced Features
**Goal:** To implement the specialized, high-value compliance features. This includes the full GDPR Art.28(3) detectors, the redline negotiation functionality, and the integration of the "Legal Expert" personas. This epic will transform the platform from a general-purpose tool into a specialized, compliance-first legal suite.

## Epic 5: Production Readiness & Observability
**Goal:** To scale the application for production use. This epic will focus on non-functional requirements such as migrating the database to a production-grade service, implementing a robust background task queue, and setting up comprehensive logging and monitoring to track performance, cost, and system health.
