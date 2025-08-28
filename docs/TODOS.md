# Project TODOs

This document tracks pending tasks and future work items.

## Epic 1 Follow-ups

-   **Story 1.5 Polish**: Add `log_format_spec.json` and a tiny log viewer (optional).
-   **PR Preparation**: The PR for Epic 1 has been prepared and is ready for review and merging.

## Epic 2 - Detector Runner (Story 2.2)

-   **Implement Lexicon Detector Logic**: Enhance `run_detectors` in `services/detector_runner.py` to use the actual lexicon from `extraction.json` and a rulepack to generate findings.
-   **Implement Regex Detector Logic**: Add support for regex-based detectors in `run_detectors`.
-   **Update Unit Tests**: Modify `test_detector_runner.py` to test the actual lexicon and regex detector logic.
-   **Update Integration Tests**: Ensure integration tests verify the correct findings are generated and persisted.

## General Project Tasks

-   **Error Code Standardization**: Review and standardize all API error codes across the application (though initial work for Story 1.1 is complete, a broader review might be beneficial).
-   **POSIX Setup**: Create a setup script for POSIX-compliant systems (e.g., Linux, macOS).