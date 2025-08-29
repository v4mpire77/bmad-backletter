# 2. Requirements
## Functional
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

## Non Functional
The non-functional requirements (NFRs) describe the qualities of the system, which are crucial for user experience and trust.

* **NFR1: Security:** All data, including uploaded documents and client information, must be encrypted both in transit and at rest.
* **NFR2: Performance:** The system must respond to user actions and deliver a full report within a reasonable timeframe (e.g., under 60 seconds for a standard document).
* **NFR3: Consistency:** Running the same input through the system must produce the same output and findings each time.
* **NFR4: Explainability:** For every finding, the system must provide a clear and simple explanation of the legal principle applied.
* **NFR5: Scalability:** The system must be able to handle a growing number of users and documents without a significant degradation in performance.
* **NFR6: Compliance:** The system must adhere to all relevant UK legal and ethical standards, with a particular focus on GDPR.
* **NFR7: Usability:** The user interface must be intuitive, clean, and minimize cognitive load for both legal professionals and non-experts.
* **NFR8: Accessibility:** The user interface must be WCAG-compliant to ensure it is usable by individuals with disabilities.
