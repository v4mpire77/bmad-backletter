id: 2.5
epic: 2
title: AI Risk Analysis Integration
status: draft
story: |
  As a contract reviewer, I want to leverage AI-powered risk analysis to get a more nuanced understanding of contract risks beyond simple rule-based detection, so that I can identify and mitigate potential issues more effectively.
acceptance_criteria:
  - "AC1: Successful LLM Integration: The system can successfully send a contract snippet to the configured LLM and receive a structured response."
  - "AC2: Risk and Confidence Score: The AI analysis returns a risk level (Low, Medium, High) and a confidence score for each identified risk."
  - "AC3: Pipeline Integration: The AI analysis step can be enabled or disabled for a job. When enabled, it runs after the rule-based detectors."
  - "AC4: Merged Findings: AI-identified risks are included in the final analysis report, clearly marked as originating from the AI model."
  - "AC5: Token Limiter: The system prevents an LLM call if the estimated token count exceeds a configurable threshold."
  - "AC6: Secure API Key Management: API keys are not hardcoded and are loaded from a secure configuration source."
notes:
  - "The system should be designed to be provider-agnostic to avoid vendor lock-in."
  - "The scoring logic should be tunable."
  - "Results from the AI analysis should be merged with the findings from the rule-based system."
  - "Implement token counting and cost estimation before making an API call."
dev_agent_record:
  proposed_tasks:
    - "backend: Integrate with a major LLM provider (e.g., OpenAI, Anthropic)."
    - "backend: Develop a confidence scoring mechanism."
    - "backend: Integrate the AI analysis as an optional step in the detection pipeline."
    - "backend: Implement token counting and cost estimation with configurable limits."
    - "backend: Implement secure API key management."
  dependencies:
    - "story: 2.2-detector-runner"
    - "story: 2.4-token-ledger-caps"
  open_decisions:
    - "Which specific LLM provider to use for the initial implementation."
    - "The exact structure of the structured response from the LLM."

### dev_spec
- "LLM Integration: A new service, `services/ai_risk_analyzer.py`, will handle communication with the LLM."
- "Configuration: LLM provider and API keys will be managed in `config.py` and loaded from environment variables."
- "Pipeline: The `DetectorRunner` in `services/detector_runner.py` will be modified to conditionally call the `AIRiskAnalyzer` service."
- "Data Model: The `Finding` model in `models/analysis.py` will be updated to include an optional `source` field (e.g., 'rule-based', 'ai-analyzed')."
- "Cost Management: The `AIRiskAnalyzer` will use the `TokenLedger` service from story 2.4 before making API calls."

### qa_tests
- "Unit Test: `test_ai_risk_analyzer.py` to mock LLM calls and verify request/response handling."
- "Unit Test: Test the token limiting logic within the `AIRiskAnalyzer`."
- "Integration Test: Test the `DetectorRunner` pipeline with the AI analysis step enabled and disabled."
- "Integration Test: Verify that AI findings are correctly merged and stored in the database."
- "Manual QA: Review the quality of AI risk assessment on a sample set of 10-15 contracts."
