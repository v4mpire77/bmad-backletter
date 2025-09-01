# Agent Context Engineering Workflow

This document defines the mandatory workflow that all agents must follow when working with the Blackletter Systems codebase. Following this workflow ensures consistency, quality, and maintainability across the project.

## 1. Workflow Sequence

Every agent MUST follow this exact sequence when handling any task:

### 1.1. Business Context Assessment (ALWAYS FIRST)

1. **Analyze Business Requirements** (`docs/Business_Requirements.md`)
   - Understand the business value proposition and stakeholder needs
   - Identify key performance indicators and success metrics
   - Determine business priority and impact of the task

2. **Review Implementation Plan** (`docs/Implementation.md`)
   - Understand the feature being implemented in the broader context
   - Identify which implementation stage the task belongs to
   - Note any dependencies or prerequisites
   - Align technical implementation with business objectives

3. **Assess Business Value** (`docs/Business_Value_Assessment.md`)
   - Evaluate user impact and experience improvements
   - Identify potential revenue or cost implications
   - Determine strategic alignment with business goals

### 1.2. Technical Context Assessment (AFTER Business Context Assessment)

1. **Examine Project Structure** (`docs/project_structure.md`)
   - Locate where new code should be placed
   - Understand how components should interact
   - Follow established naming conventions

2. **Check UI/UX Guidelines** (`docs/UI_UX_doc.md`)
   - For frontend tasks, ensure compliance with design system
   - Verify component usage patterns
   - Confirm accessibility requirements

3. **Review Bug Tracking** (`docs/Bug_tracking.md`)
   - Check for known issues related to the current task
   - Avoid reintroducing fixed bugs
   - Follow established resolution workflows

### 1.3. Risk and Compatibility Analysis (BEFORE Implementation)

1. **Identify Technical Risks**
   - Assess potential impact on existing functionality
   - Identify integration complexity
   - Determine rollback requirements

2. **Define Compatibility Requirements**
   - Ensure existing APIs remain unchanged
   - Maintain backward compatibility for database schema changes
   - Follow existing UI patterns

### 1.4. Code Implementation (AFTER Context Assessment)

1. **Follow Established Patterns**
   - Examine similar existing code before writing new code
   - Maintain consistent coding style and patterns
   - Use existing utilities and helpers

2. **Adhere to Architecture**
   - Keep adapters vendor-agnostic (everything behind `core/*`)
   - Use dependency injection for providers
   - Follow the modular design pattern

3. **Implement with Quality**
   - Write small, composable functions
   - Include type hints and docstrings
   - Avoid "magic" or unexplained code

4. **Ensure Testability**
   - Write unit tests for pure logic
   - Make components easy to test
   - Consider edge cases

5. **Maintain Business Focus (BMAD-Enhanced)**
   - Ensure implementation aligns with business objectives
   - Consider user experience impact
   - Maintain system performance standards
   - Document business value delivered by each component
   - Validate that implementation meets success criteria defined in business context assessment

6. **Apply Advanced Elicitation Techniques (BMAD-Enhanced)**
   - After drafting significant sections of code or documentation, offer advanced elicitation options
   - Present 9 carefully selected elicitation methods plus "Proceed" option
   - Allow stakeholders to select methods for deeper exploration of ideas
   - Execute selected methods and provide actionable insights
   - Continue offering elicitation options until stakeholder selects "Proceed"
   - Methods include: Expand/Contract for Audience, Critique and Refine, Identify Potential Risks, Assess Alignment with Goals, Tree of Thoughts, ReWOO, Meta-Prompting, Agile Team Perspective, Stakeholder Roundtable, Innovation Tournament, Escape Room Challenge, Red Team vs Blue Team, Hindsight Reflection

7. **Business Value Documentation (BMAD-Enhanced)**
   - For each implemented feature, document how it delivers business value
   - Link implementation to specific business requirements and success metrics
   - Capture any insights about business impact during implementation
   - Record any deviations from business requirements and rationale

### 1.5. Documentation (CONCURRENT with Implementation)

1. **Update Documentation**
   - Add/update docstrings for all functions, classes, and modules
   - Document any non-obvious design decisions
   - Update relevant documentation files
   - Document business logic and decision rationale

2. **Maintain Changelog**
   - Document significant changes
   - Note any breaking changes or deprecations
   - Record bug fixes
   - Document business impact of changes

3. **Knowledge Transfer (BMAD-Enhanced)**
   - Document lessons learned during implementation
   - Capture architectural decisions and rationale
   - Update team knowledge base
   - Record implementation challenges and solutions
   - Document technical debt and future improvement opportunities
   - Capture business context and value delivery insights
   - Maintain implementation narrative with clear problem-solving progression
   - Record insights gained through advanced elicitation techniques

## 2. Critical Rules

### 2.1. NEVER Rules

- **NEVER** ignore the Context Engineering workflow
- **NEVER** hardcode API keys or secrets
- **NEVER** write to local disk for artifacts (use S3/MinIO)
- **NEVER** embed PDFs without chunking (target 1-2k tokens)
- **NEVER** implement features without consulting documentation first
- **NEVER** leave code in a broken state
- **NEVER** commit code that doesn't follow established patterns
- **NEVER** proceed without understanding business context
- **NEVER** ignore risk assessment requirements
- **NEVER** skip advanced elicitation when working on significant features

### 2.2. ALWAYS Rules

- **ALWAYS** follow the workflow sequence (Business Context → Technical Context → Risk Analysis → Implementation → Documentation)
- **ALWAYS** keep adapters vendor-agnostic
- **ALWAYS** write tests for core functionality
- **ALWAYS** include proper error handling
- **ALWAYS** use existing components and utilities
- **ALWAYS** follow naming conventions
- **ALWAYS** document your code
- **ALWAYS** consider security implications
- **ALWAYS** analyze business context and stakeholder needs
- **ALWAYS** assess risks and document mitigation strategies
- **ALWAYS** include business logic documentation
- **ALWAYS** validate implementation against business success criteria
- **ALWAYS** document business value delivered by implementations
- **ALWAYS** apply advanced elicitation techniques for deeper exploration of ideas
- **ALWAYS** document insights gained through advanced elicitation

## 3. File Reference Priority

When working on a task, ALWAYS consult files in this exact order:

1. `docs/Business_Requirements.md` - Business context and stakeholder needs
2. `docs/Business_Value_Assessment.md` - Business impact evaluation criteria
3. `docs/Implementation.md` - Overall project plan
4. `docs/project_structure.md` - Where code should go
5. `docs/UI_UX_doc.md` - Design guidelines (for frontend)
6. `docs/Bug_tracking.md` - Known issues
7. `docs/ARCHITECTURE.md` - System architecture
8. `docs/Risk_Management_Framework.md` - Risk assessment and mitigation strategies
9. Similar existing code files - For patterns and examples

## 4. Quality Standards

### 4.1. Code Quality

- Follow language-specific best practices
- Maintain consistent formatting
- Use meaningful variable and function names
- Keep functions small and focused
- Use comments for complex logic
- Implement proper error handling
- Include business logic documentation
- Apply advanced elicitation techniques to validate design decisions

### 4.2. Testing Requirements

- Write unit tests for pure functions
- Include integration tests for key workflows
- Test edge cases and error conditions
- Maintain 80%+ test coverage for core modules
- Include business scenario testing
- Use advanced elicitation to identify additional test scenarios

### 4.3. Documentation Quality

- Clear and concise docstrings with business context
- Updated README files with user impact information
- Accurate architectural documentation with decision rationale
- Proper changelog entries with business impact assessment
- Document insights from advanced elicitation sessions

## 5. Context Engineering Checklist

Before considering any task complete, verify:

- [ ] Business context and stakeholder needs were analyzed
- [ ] Business value and impact were assessed
- [ ] All relevant documentation was reviewed
- [ ] Code follows established project patterns
- [ ] Tests are implemented and passing
- [ ] Documentation is updated
- [ ] Code meets quality standards
- [ ] Risks were identified and mitigation strategies documented
- [ ] No NEVER rules were violated
- [ ] All ALWAYS rules were followed
- [ ] Implementation validates against business success criteria
- [ ] Business value delivered by implementation is documented
- [ ] Advanced elicitation techniques were applied where appropriate
- [ ] Insights from advanced elicitation were incorporated

## 6. Implementation Example

### Good Implementation (Following Context Engineering with BMAD)

```python
# First analyzed business requirements to understand stakeholder needs
# Reviewed docs/Business_Value_Assessment.md to evaluate user impact
# Then reviewed docs/Implementation.md to understand the feature
# Checked docs/project_structure.md to determine placement
# Examined existing code in app/core/ for patterns

"""
OCR module for Blackletter Systems.

This module provides functionality for extracting text from PDF documents using:
- pdfplumber for direct text extraction
- pytesseract for OCR when needed

Business Value:
- Enables automated contract analysis for GDPR compliance
- Reduces manual review time by 80%
- Improves accuracy of obligation detection

Success Metrics:
- Process 100+ contracts per hour
- 95%+ accuracy in obligation detection
- Reduce manual review time from 8 hours to 1.6 hours per contract
"""

import os
from typing import Dict, List, Optional
import logging

import pdfplumber
from PIL import Image
import pytesseract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF document.

    Args:
        file_path: Path to the PDF file

    Returns:
        str: Extracted text content

    Business Impact:
        Critical component for contract analysis pipeline
        Directly affects accuracy of GDPR obligation detection
        Enables compliance automation reducing manual effort
    """
    # Implementation following established patterns
    # ...
```

### Bad Implementation (Ignoring Context Engineering with BMAD)

``python
# Jumped straight to coding without reviewing documentation
# Ignored existing patterns and project structure
# No business context analysis

def get_pdf_text(pdf):
    # No docstring
    # Hardcoded paths
    # No error handling
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # ...
```

## 7. Conclusion

The Context Engineering workflow is not optional. It is a mandatory process that ensures the Blackletter Systems codebase remains consistent, maintainable, and high-quality. All agents MUST follow this workflow without exception.

By adhering to this workflow, you will:
- Produce higher quality code
- Maintain consistency across the codebase
- Reduce bugs and technical debt
- Make the codebase more maintainable
- Ensure documentation stays up-to-date
- Deliver better business value
- Improve risk management
- Enhance knowledge transfer
