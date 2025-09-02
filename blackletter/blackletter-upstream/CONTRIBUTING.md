# Contributing to Blackletter Systems

Thank you for your interest in contributing to Blackletter Systems! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment for our community include:

- Using welcoming and inclusive language
- Being respectful of differing opinions and viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery, and sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- Docker (optional, for containerized development)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/blackletter-systems.git
   cd blackletter-systems
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-org/blackletter-systems.git
   ```

## Development Setup

### Backend Development

1. **Create Virtual Environment:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Set Environment Variables:**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/blackletter"
   export REDIS_URL="redis://localhost:6379"
   export LLM_PROVIDER="openai"
   export OPENAI_API_KEY="your-api-key"
   ```

4. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start Development Server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Development

1. **Install Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set Environment Variables:**
   ```bash
   export NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```

3. **Start Development Server:**
   ```bash
   npm run dev
   ```

### Services Setup

#### Using Docker Compose

```bash
# Start required services
docker-compose up -d postgres redis

# Or start all services for full development
docker-compose up -d
```

#### Manual Setup

**PostgreSQL:**
```bash
# Install PostgreSQL
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Create database
createdb blackletter
```

**Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

## Coding Standards

### Python (Backend)

#### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting

#### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

#### Type Hints

- Use type hints for all function parameters and return values
- Use mypy for static type checking

Example:
```python
from typing import List, Optional, Dict, Any

def process_document(
    file_path: str,
    options: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Process a document and return analysis results."""
    pass
```

#### Documentation

- Use Google-style docstrings
- Include type information in docstrings
- Document all public functions and classes

Example:
```python
def analyze_contract(text: str) -> Dict[str, Any]:
    """Analyze contract text for legal risks and compliance issues.
    
    Args:
        text: The contract text to analyze.
        
    Returns:
        Dictionary containing analysis results with keys:
        - risk_score: Overall risk score (0-10)
        - issues: List of identified issues
        - recommendations: List of recommendations
        
    Raises:
        ValueError: If text is empty or invalid.
    """
    pass
```

### TypeScript/JavaScript (Frontend)

#### Code Style

- Use ESLint and Prettier
- Follow Airbnb JavaScript Style Guide
- Use TypeScript for all new code

#### Component Structure

```typescript
import React from 'react';
import { ComponentProps } from './types';

interface Props {
  title: string;
  onAction: () => void;
}

export const Component: React.FC<Props> = ({ title, onAction }) => {
  return (
    <div>
      <h1>{title}</h1>
      <button onClick={onAction}>Action</button>
    </div>
  );
};
```

#### File Naming

- Use kebab-case for file names
- Use PascalCase for component names
- Use camelCase for functions and variables

## Testing

### Backend Testing

#### Unit Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ocr.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_ocr.py::test_extract_text
```

#### Test Structure

```python
# tests/test_ocr.py
import pytest
from app.core.ocr import extract_text

class TestOCR:
    def test_extract_text_success(self):
        """Test successful text extraction."""
        result = extract_text("test.pdf")
        assert result is not None
        assert len(result) > 0
    
    def test_extract_text_invalid_file(self):
        """Test handling of invalid file."""
        with pytest.raises(ValueError):
            extract_text("nonexistent.pdf")
```

#### Integration Tests

```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_document():
    """Test document upload endpoint."""
    with open("tests/fixtures/test.pdf", "rb") as f:
        response = client.post(
            "/api/review",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    assert "job_id" in response.json()
```

### Frontend Testing

#### Unit Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- --testNamePattern="UploadComponent"
```

#### Test Structure

```typescript
// __tests__/components/UploadComponent.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { UploadComponent } from '../UploadComponent';

describe('UploadComponent', () => {
  it('should render upload button', () => {
    render(<UploadComponent onUpload={jest.fn()} />);
    expect(screen.getByText('Upload Document')).toBeInTheDocument();
  });

  it('should handle file upload', () => {
    const mockOnUpload = jest.fn();
    render(<UploadComponent onUpload={mockOnUpload} />);
    
    const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/upload/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    expect(mockOnUpload).toHaveBeenCalledWith(file);
  });
});
```

#### E2E Tests

```bash
# Run E2E tests
npm run test:e2e
```

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the coding standards
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Changes

Use conventional commit messages:

```bash
git commit -m "feat: add document upload functionality"
git commit -m "fix: resolve OCR text extraction issue"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for contract analysis"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 4. Push Changes

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to GitHub and create a new pull request
2. Fill out the pull request template
3. Request reviews from maintainers
4. Address any feedback and make necessary changes

### 6. Pull Request Template

```markdown
## Description

Brief description of the changes made.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or breaking changes documented)

## Screenshots (if applicable)

Add screenshots for UI changes.
```

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

1. **Environment:**
   - Operating system and version
   - Python/Node.js version
   - Browser version (if applicable)

2. **Steps to Reproduce:**
   - Clear, step-by-step instructions
   - Sample data or files if needed

3. **Expected vs Actual Behavior:**
   - What you expected to happen
   - What actually happened

4. **Additional Information:**
   - Error messages or logs
   - Screenshots if applicable

### Feature Requests

When requesting features, please include:

1. **Problem Statement:**
   - What problem does this feature solve?

2. **Proposed Solution:**
   - How should this feature work?

3. **Use Cases:**
   - Who would benefit from this feature?

4. **Alternatives Considered:**
   - What other approaches were considered?

## Documentation

### Code Documentation

- Document all public APIs
- Include examples in docstrings
- Keep README files updated
- Update architecture documentation for significant changes

### User Documentation

- Write clear, concise user guides
- Include screenshots for UI features
- Provide troubleshooting guides
- Keep documentation in sync with code changes

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH**
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Steps

1. **Prepare Release:**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Update Version:**
   - Update version in `pyproject.toml` (backend)
   - Update version in `package.json` (frontend)
   - Update CHANGELOG.md

3. **Create Release Branch:**
   ```bash
   git checkout -b release/v1.2.0
   git commit -m "chore: prepare release v1.2.0"
   git push origin release/v1.2.0
   ```

4. **Create Pull Request:**
   - Create PR from release branch to main
   - Get approval from maintainers
   - Merge after approval

5. **Tag Release:**
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

6. **Deploy:**
   - Deploy to staging for testing
   - Deploy to production after validation

### Changelog

Keep a CHANGELOG.md file with:

- All notable changes for each version
- Breaking changes clearly marked
- Migration guides for breaking changes
- Links to relevant issues and PRs

## Getting Help

- **Discussions:** Use GitHub Discussions for questions and ideas
- **Issues:** Use GitHub Issues for bugs and feature requests
- **Documentation:** Check the docs folder for detailed guides
- **Code Review:** Request reviews from maintainers

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Release notes
- Project documentation
- Community acknowledgments

Thank you for contributing to Blackletter Systems!
