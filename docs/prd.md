# Product Requirements Document: Pocket Lawyer & Firm-Aware

## 1. Goals and Background Context
**Goals:**

* To provide an accessible and affordable legal triage service for individuals and small businesses.
* To deliver a compliance-first, AI-powered tool that automates legal review and risk assessment for law firms.
* To establish the Blackletter engine as a trusted and auditable source of legal intelligence, reducing the risk of "hallucinations".
* To capture a significant share of the growing UK legal technology market, which has an estimated annual market opportunity of £22 billion in the UK alone.

**Background Context:**

The UK legal market is facing a dual problem: an access-to-justice gap for consumers and a need for greater efficiency and compliance for law firms. Our unified platform, powered by the Blackletter engine, directly addresses this dual problem by providing a single, seamless solution. This approach is backed by market research showing strong demand for AI-driven solutions and a clear gap in the market for a compliance-first tool.

**Change Log:**
| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2025-08-28 | 1.0 | Initial draft based on Market Opportunity Report. | John (PM) |

## 2. Requirements
### Functional
The functional requirements (FRs) detail the specific features and behaviors of the Blackletter legal suite.

* **FR1:** The system must allow users to upload or paste a legal document for analysis.
* **FR2:** The system must automatically identify the jurisdiction (e.g., UK) and category of the contract (e.g., supply agreement, NDA).
* **FR3:** The system must process the document in chunks to handle large files and overcome context window limitations.
* **FR4:** The system must break down the document into individual clauses and categorize them.
* **FR5:** The system must analyze each clause against a defined set of risks and legal principles from the Blackletter engine.
* **FR6:** The system must identify missing clauses that are typically found in a contract of that type.
* **FR7:** The system must, for every risk identified, provide a detailed finding that includes a snippet of the problematic text, its location in the document, and a rationale for why it is a risk.
* **FR8:** The system must generate a comprehensive, user-facing report in PDF or HTML format that summarizes the findings and includes an auditable trail of the analysis.
* **FR9:** The system must allow the user to select their role (e.g., buyer, seller, employee) to tailor the risk analysis accordingly.
* **FR10:** The system must provide a plain-English explanation for each legal finding to ensure accessibility for non-experts.
* **FR11:** The system must include a dedicated "GDPR Compliance Mode" that specifically analyzes the contract against a defined set of UK GDPR and Data Protection Act 2018 rules.
* **FR12:** The system must provide a verdict on a contract's GDPR compliance, specifically addressing the requirements of Article 28(3)(a-h) of the UK GDPR.
* **FR13:** The system must allow users to see a "diff" or a redline of a contract, showing proposed changes to mitigate identified risks.
* **FR14:** The system must offer a subscription-based model for access to its services.

### Non-Functional Requirements
The non-functional requirements (NFRs) describe the qualities of the system, which are crucial for user experience and trust.

* **NFR1: Security:** All data, including uploaded documents and client information, must be encrypted both in transit and at rest.
* **NFR2: Performance:** The system must respond to user actions and deliver a full report within a reasonable timeframe (e.g., under 60 seconds for a standard document).
* **NFR3: Consistency:** Running the same input through the system must produce the same output and findings each time.
* **NFR4: Explainability:** For every finding, the system must provide a clear and simple explanation of the legal principle applied.
* **NFR5: Scalability:** The system must be able to handle a growing number of users and documents without a significant degradation in performance.
* **NFR6: Compliance:** The system must adhere to all relevant UK legal and ethical standards, with a particular focus on GDPR.
* **NFR7: Usability:** The user interface must be intuitive, clean, and minimize cognitive load for both legal professionals and non-experts.
* **NFR8: Accessibility:** The user interface must be WCAG-compliant to ensure it is usable by individuals with disabilities.

## 3. User Interface Design Goals
### Overall UX Vision
The core UX vision is to transform the complex and often intimidating process of legal analysis into a clear, trustworthy, and efficient experience. The interface will be designed to handle the serious, high-stakes nature of legal work while providing a low cognitive load for the user. Our design will adhere to the principle of "Privacy by Design," ensuring that data protection is embedded into the product's core functionality from the very beginning.

### Key Interaction Paradigms
* **Progressive Disclosure:** We will use a progressive disclosure architecture to prevent users from being overwhelmed with information. The interface will show only the most relevant information first, such as a high-level risk assessment (e.g., Red, Amber, Green, or "RAG" status). Users can then "drill down" into specific details, such as the problematic clause, the legal principle behind the finding, and the recommended action.
* **Explainable AI:** The interface will be designed to make the AI's logic transparent. For every finding, the system will provide a clear explanation of the legal concept that was applied and provide an auditable link to the source. This directly addresses the fear of AI "hallucinations" and builds trust with a professional audience.
* **Human-in-the-Loop:** The interface will be designed to support human intervention and review. Users will be able to easily navigate, edit, and annotate the machine-generated results, and compare them against other documents. The UI will be simple and intuitive, so the user can focus on critical analysis rather than a complex interface.
* **Security and Trust:** The design will prioritize security and privacy from the outset. We will use features like clear dashboards, secure document handling functionalities, and transparent data processing notices to ensure that the user feels confident and safe.

### Core Screens and Views
Based on our discussions and a typical legal tech workflow, the most critical screens and views will include:

* **Document Upload/Intake:** A simple, clean interface for uploading a document, selecting the matter type, and initiating the analysis.
* **Matter Dashboard:** A dashboard that provides a quick overview of a document's status, key risks, and compliance verdicts.
* **Risk Analysis View:** An interactive view of the document with highlighted clauses, an explanations of the risks, and proposed redlines.
* **Report Generation View:** A simple interface for generating, customizing, and downloading the final report.

## 4. GDPR Compliance: Foundational Requirements
### 1. Data Processing Agreement (DPA) Analysis
The Blackletter engine's core functionality will be to analyze a contract to ensure it meets the strict requirements of a GDPR-compliant Data Processing Agreement (DPA). This is a legally binding contract that is mandatory when a data controller engages a processor to handle personal data. Our system must, at a minimum, verify that the contract addresses the following key points outlined in Article 28(3)(a-h) of the UK GDPR:

* **Documented Instructions (a):** The processor must only process personal data on the documented instructions of the controller.
* **Duty of Confidence (b):** Anyone authorized to process the data must be committed to confidentiality.
* **Security Measures (c):** The processor must implement appropriate technical and organizational security measures in line with Article 32 of the UK GDPR.
* **Sub-processors (d):** The processor must not engage another processor without the controller's prior written authorization.
* **Data Subjects' Rights (e):** The processor must assist the controller in responding to requests from data subjects exercising their rights.
* **Assistance with Compliance (f):** The processor must assist the controller in ensuring compliance with obligations such as data protection impact assessments (DPIAs) and data breach notifications.
* **End-of-Contract Provisions (g):** The contract must specify that upon termination, the processor will, at the controller's choice, either delete or return all personal data.
* **Audits and Inspections (h):** The processor must make available all necessary information to demonstrate compliance and allow for audits.

The DPO agent will verify that these clauses are present, clear, and compliant. If a clause is missing or problematic, the Blackletter engine will flag it and provide a detailed explanation of the required legal standard, transforming a potential vulnerability into a documented finding.

### 2. Privacy by Design & Default
The platform itself will be built on the principles of Privacy by Design and by Default, as required by the UK GDPR. This is a core, non-negotiable requirement of the project's architecture.

* **Proactive, Not Reactive:** The system will be designed to anticipate and prevent privacy issues before they occur, rather than reacting to them after the fact.
* **Privacy as the Default:** The strictest privacy settings will be applied automatically, ensuring that personal data is protected without any user intervention. This includes data minimization, where only the essential personal data is collected and processed for a specific purpose.
* **End-to-End Security:** Strong security measures, such as encryption and access controls, will be implemented from the beginning and maintained throughout the entire data lifecycle. All data will be processed securely and then destroyed securely when it is no longer needed.
* **Transparency:** The system will be transparent about its functions and data processing activities, ensuring that all actions are independently verifiable and that users can monitor the processing of their data.

## 5. Technical Assumptions
### Deterministic First
* All eight GDPR Art.28(3) detectors will be implemented via rulepacks (YAML/regex) with evidence windows (±2 sentences).
* LLMs are disabled by default; when enabled, only short snippets (≤220 tokens) are passed.
* Hard cap: ≤1,500 tokens per document; if exceeded → needs_review.

### Performance Targets
* End-to-end latency p95 ≤ 60 seconds for ≤10MB PDFs.
* Cost ≤ £0.10 per document at defaults.
* Accuracy thresholds: Precision ≥0.85, Recall ≥0.90, Explainability ≥95%.

### Storage & Infra
* MVP: SQLite for persistence + local filesystem for artefacts.
* Phase-2: Postgres (Supabase) + object storage.
* Queue: FastAPI BackgroundTasks in MVP; Celery+Redis later.
* Hosting: Windows-first local dev; optional Render/Supabase for demo.

### Security & Privacy
* No PII retention by default; ephemeral processing.
* Encryption at rest & in transit.
* Snippet-only LLM calls, with regex redaction of PII.
* .env secrets; Windows-safe config.

### API Contracts
* REST/JSON endpoints:
    * `POST /api/contracts` → upload & job.
    * `GET /api/jobs/{id}` → status.
    * `GET /api/analyses/{id}` → summary.
    * `GET /api/analyses/{id}/findings` → Finding[].
    * `POST /api/reports/{id}` → PDF/HTML export.
* Finding model: `{ detector_id, rule_id, verdict, snippet, page, start, end, rationale, reviewed }`.

### Frontend Assumptions
* Next.js 14, Tailwind, shadcn/ui, React Query.
* Evidence-first UX: Findings table with verdict chips + Evidence Drawer.
* WCAG AA accessibility; progressive disclosure for detail.
* Dark theme by default.

### Testing & Observability
* Gold set (10–20 DPAs) used for precision/recall evaluation.
* Metrics logged: latency, tokens/doc, %LLM invoked, explainability rate.
* Structured JSON logs; simple admin metrics wall.

## 6. Epic List
### Epic 1: Platform & Core Infrastructure
**Goal:** To build the foundational infrastructure, set up the development environment, and deliver a simple, user-facing document intake process. This epic will result in a fully deployable, albeit limited, version of the application that can receive a document and place it into a queue for processing. This proves the core architecture and user-facing intake process work before we build the complex back-end.

### Epic 2: Blackletter Core Analysis Engine
**Goal:** To implement the core of the Blackletter engine. This includes the deterministic processes for document segmentation, clause extraction, and rule-based risk detection against a basic, sample rulepack. The epic will not yet produce a user-facing report, but it will store the analysis findings, making them available for later display.

### Epic 3: Interactive Risk Dashboard & Reporting
**Goal:** To build the user-facing front end. This epic will create the Pocket Lawyer and Firm-Aware interfaces, including the risk dashboard with verdict chips, the evidence-first UX for findings, and the ability to generate a downloadable PDF/HTML report. This epic delivers the full user experience, making the analysis tangible and actionable.

### Epic 4: GDPR Compliance & Advanced Features
**Goal:** To implement the specialized, high-value compliance features. This includes the full GDPR Art.28(3) detectors, the redline negotiation functionality, and the integration of the "Legal Expert" personas. This epic will transform the platform from a general-purpose tool into a specialized, compliance-first legal suite.

### Epic 5: Production Readiness & Observability
**Goal:** To scale the application for production use. This epic will focus on non-functional requirements such as migrating the database to a production-grade service, implementing a robust background task queue, and setting up comprehensive logging and monitoring to track performance, cost, and system health.
