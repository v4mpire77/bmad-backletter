# Development Agent Workflow - Blackletter Systems

## Primary Directive

You are a development agent implementing the Blackletter Systems project. Follow established documentation and maintain consistency with the Context Engineering framework.

## Core Workflow Process

### Before Starting Any Task

1. **Consult Implementation Plan**
   - Read `/docs/Implementation.md` for current stage and available tasks
   - Check task dependencies and prerequisites
   - Verify scope understanding
   - Review timeline and resource requirements

2. **Check Project Structure**
   - Review `/docs/project_structure.md` for file organization
   - Understand module hierarchy and naming conventions
   - Verify correct file locations and structure

3. **Review UI/UX Requirements**
   - Consult `/docs/UI_UX_doc.md` before implementing any UI/UX elements
   - Follow design system specifications and responsive requirements
   - Ensure accessibility compliance

4. **Check Known Issues**
   - Review `/docs/Bug_tracking.md` for similar issues before starting
   - Understand current bug status and resolutions
   - Avoid repeating known problems

## Task Execution Protocol

### 1. Task Assessment

**Read subtask from `/docs/Implementation.md`**

**Assess subtask complexity:**
- **Simple subtask:** Implement directly following established patterns
- **Complex subtask:** Create a detailed todo list with sub-tasks

**Example Simple Task:**
```
- [ ] Add file upload validation to document upload component
```

**Example Complex Task:**
```
- [ ] Implement RAG system with document indexing
  - [ ] Create document processing pipeline
  - [ ] Implement vector embedding generation
  - [ ] Set up ChromaDB integration
  - [ ] Create semantic search functionality
  - [ ] Add context retrieval system
  - [ ] Implement response generation
```

### 2. Documentation Research

**Check `/docs/Implementation.md` for relevant documentation links in the subtask**

**Research requirements:**
- Read and understand official documentation
- Review best practices and implementation examples
- Check for any specific requirements or constraints
- Understand integration points with existing systems

**Example Research Process:**
```
Task: Implement FastAPI rate limiting
1. Check FastAPI documentation: https://fastapi.tiangolo.com/
2. Review rate limiting middleware examples
3. Understand integration with existing authentication
4. Check performance implications
```

### 3. UI/UX Implementation

**Consult `/docs/UI_UX_doc.md` before implementing any UI/UX elements**

**Follow design system:**
- Use established color palette and typography
- Follow component guidelines and patterns
- Ensure responsive design compliance
- Implement accessibility features

**Example UI Implementation:**
```typescript
// Follow established button patterns
<Button 
  variant="default" 
  size="default"
  className="bg-blue-600 hover:bg-blue-700"
>
  Analyze Document
</Button>

// Use proper spacing and layout
<div className="space-y-4 p-6">
  <Card className="p-6">
    <CardHeader>
      <CardTitle>Analysis Results</CardTitle>
    </CardHeader>
  </Card>
</div>
```

### 4. Project Structure Compliance

**Check `/docs/project_structure.md` before:**
- Running commands
- Creating files/folders
- Making structural changes
- Adding dependencies

**File Organization Rules:**
```
Frontend:
- Components: PascalCase (DocumentUpload.tsx)
- Utilities: camelCase (apiUtils.ts)
- Constants: UPPER_SNAKE_CASE (API_ENDPOINTS.ts)

Backend:
- Modules: snake_case (nlp_engine.py)
- Classes: PascalCase (ContractAnalyzer)
- Functions: snake_case (process_document)
```

### 5. Error Handling

**Check `/docs/Bug_tracking.md` for similar issues before fixing**

**Documentation requirements:**
- Document all errors and solutions in Bug_tracking.md
- Include error details, root cause, and resolution steps
- Update prevention strategies

**Example Error Documentation:**
```markdown
## Bug ID: BUG-007
**Date Reported:** 2024-01-16
**Priority:** P1
**Status:** Resolved

### Description
API endpoint returning 500 error during document processing

### Root Cause
Missing error handling in file validation function

### Resolution
Added try-catch blocks and proper error responses

### Files Modified
- backend/app/routers/contracts.py
- backend/app/utils/file_handlers.py
```

### 6. Task Completion

**Mark tasks complete only when:**
- All functionality implemented correctly
- Code follows project structure guidelines
- UI/UX matches specifications (if applicable)
- No errors or warnings remain
- All task list items completed (if applicable)
- Tests pass successfully
- Documentation updated

**Completion Checklist:**
```
□ Functionality implemented
□ Code follows naming conventions
□ UI/UX matches design system
□ Error handling implemented
□ Tests written and passing
□ Documentation updated
□ Code reviewed
□ No linting errors
```

## File Reference Priority

### 1. `/docs/Bug_tracking.md` - Check for known issues first
- Review existing bugs and resolutions
- Avoid repeating known problems
- Learn from previous solutions

### 2. `/docs/Implementation.md` - Main task reference
- Current implementation stage
- Available tasks and dependencies
- Timeline and resource requirements
- Technology stack and documentation links

### 3. `/docs/project_structure.md` - Structure guidance
- File organization and naming conventions
- Module hierarchy and dependencies
- Configuration file locations
- Build and deployment structure

### 4. `/docs/UI_UX_doc.md` - Design requirements
- Design system specifications
- Component guidelines and patterns
- Responsive design requirements
- Accessibility standards

## Critical Rules

### NEVER Rules
- **NEVER** skip documentation consultation
- **NEVER** mark tasks complete without proper testing
- **NEVER** ignore project structure guidelines
- **NEVER** implement UI without checking UI_UX_doc.md
- **NEVER** fix errors without checking Bug_tracking.md first
- **NEVER** create files in wrong locations
- **NEVER** use inconsistent naming conventions
- **NEVER** ignore accessibility requirements

### ALWAYS Rules
- **ALWAYS** document errors and solutions
- **ALWAYS** follow the established workflow process
- **ALWAYS** test thoroughly before completion
- **ALWAYS** update documentation when making changes
- **ALWAYS** use established design patterns
- **ALWAYS** follow coding standards and conventions
- **ALWAYS** consider performance implications
- **ALWAYS** implement proper error handling

## Development Environment Setup

### Required Tools
- **IDE:** VS Code with recommended extensions
- **Version Control:** Git with proper branching strategy
- **Testing:** pytest (backend), Jest (frontend)
- **Linting:** flake8 (Python), ESLint (TypeScript)
- **Documentation:** Markdown editor

### Environment Configuration
```bash
# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
npm run dev
```

## Code Quality Standards

### Backend (Python)
- **Style:** PEP 8 compliance
- **Type Hints:** Use type hints for all functions
- **Documentation:** Docstrings for all classes and functions
- **Testing:** Minimum 80% test coverage

```python
from typing import List, Optional
from pydantic import BaseModel

class DocumentAnalysis(BaseModel):
    """Model for document analysis results."""
    
    document_id: str
    analysis_type: str
    results: dict
    confidence: float
    
    def get_summary(self) -> str:
        """Return a summary of the analysis results."""
        return f"Analysis of {self.document_id}: {self.confidence}% confidence"
```

### Frontend (TypeScript/React)
- **Style:** ESLint and Prettier configuration
- **Types:** Proper TypeScript types for all components
- **Components:** Functional components with hooks
- **Testing:** Component and integration tests

```typescript
interface AnalysisResult {
  documentId: string;
  analysisType: string;
  results: Record<string, any>;
  confidence: number;
}

const AnalysisResults: React.FC<{ results: AnalysisResult[] }> = ({ results }) => {
  return (
    <div className="space-y-4">
      {results.map((result) => (
        <Card key={result.documentId}>
          <CardContent>
            <p>Confidence: {result.confidence}%</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
```

## Testing Requirements

### Backend Testing
```python
import pytest
from app.core.nlp_engine import NLPEngine

class TestNLPEngine:
    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality."""
        nlp = NLPEngine()
        result = nlp.analyze_sentiment("This is great!")
        assert result['label'] in ['positive', 'negative', 'neutral']
        assert 'score' in result
```

### Frontend Testing
```typescript
import { render, screen } from '@testing-library/react';
import { AnalysisResults } from './AnalysisResults';

describe('AnalysisResults', () => {
  it('renders analysis results correctly', () => {
    const mockResults = [
      { documentId: '1', analysisType: 'sentiment', results: {}, confidence: 85 }
    ];
    
    render(<AnalysisResults results={mockResults} />);
    expect(screen.getByText('Confidence: 85%')).toBeInTheDocument();
  });
});
```

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security scan completed

### Post-Deployment
- [ ] Health checks passing
- [ ] Performance monitoring active
- [ ] Error tracking configured
- [ ] Backup systems verified
- [ ] User acceptance testing completed

## Communication Protocol

### Daily Updates
- Update task status in Implementation.md
- Report any blockers or issues
- Document progress and decisions

### Issue Reporting
- Use Bug_tracking.md template
- Include all relevant information
- Assign appropriate priority
- Follow up on resolution

### Code Reviews
- Request reviews for all changes
- Address feedback promptly
- Document significant decisions
- Update documentation as needed

## Success Metrics

### Code Quality
- Test coverage > 80%
- No critical security vulnerabilities
- Performance benchmarks met
- Accessibility compliance achieved

### Development Efficiency
- Tasks completed on schedule
- Documentation always up to date
- Few bugs introduced
- Quick issue resolution

### User Experience
- UI/UX matches design specifications
- Responsive design working correctly
- Accessibility standards met
- Performance requirements satisfied

Remember: Build a cohesive, well-documented, and maintainable project. Every decision should support overall project goals and maintain consistency with established patterns. The Context Engineering framework ensures systematic, high-quality development that delivers value to users.
