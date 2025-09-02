# Jules Optimization Plan

This document outlines my strategy for improving my operational efficiency and task performance within this repository. The plan is structured around three key areas: Speed, Accuracy, and Resourcefulness.

## 1. Speed

My goal is to complete tasks faster without sacrificing quality.

*   **1.1. Proactive File Reading:** Instead of reading files one by one and waiting, I will identify a set of important files upfront (`AGENTS.md`, `README.md`, `brief.md`, `package.json`, etc.) and read them sequentially to build context quickly.
*   **1.2. Focused Exploration:** I will use `grep` more strategically to find relevant code snippets and files, rather than manually browsing through directories. This will help me pinpoint the areas I need to change much faster.
*   **1.3. Assumption-based Planning:** For well-defined, small tasks, I will create a plan with initial assumptions and start working, verifying my assumptions as I go. This avoids over-analysis on simple changes.

## 2. Accuracy

My goal is to reduce errors and rework.

*   **2.1. Test-Driven Development (TDD) by Default:** For any code change, I will first look for existing tests. If there are none, I will write a failing test that captures the requirements *before* I write the implementation.
*   **2.2. Mandatory Self-Correction via Code Review:** Before submitting, I will use the `request_code_review()` tool as a mandatory step. This allows me to catch issues before they reach the user.
*   **2.3. Verification Checklists:** I will use internal checklists for common tasks to ensure all requirements are met. For a code change, this includes:
    *   [ ] Code compiles/builds successfully.
    *   [ ] All existing tests pass.
    *   [ ] New tests for the change are added and pass.
    *   [ ] The code adheres to the style guide (`AGENTS.md`).
    *   [ ] The change is verified functionally.
    *   [ ] Documentation is updated if necessary.

## 3. Resourcefulness

My goal is to make better use of the tools and information available to me.

*   **3.1. `AGENTS.md` as a Configuration File:** I will treat `AGENTS.md` as a live configuration file for my behavior in this repo, referring back to it for conventions like commit message formats.
*   **3.2. Learning from Failures:** When a command or test fails, I will analyze the error message to understand the root cause before trying a different approach. I will document my learnings to avoid repeating mistakes.
*   **3.3. Strategic Tool Usage:** I will consciously choose the best tool for the job. For example, using `grep` for targeted searches in large files or `ls -R` to quickly understand project structure.
