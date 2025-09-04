# Gemini AI API Usage Examples

## Overview

The Blackletter API now includes Gemini AI integration for advanced contract analysis. This provides AI-powered insights, risk assessment, summarization, and interactive chat capabilities.

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your Gemini API key:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add it to your `.env` file:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Run the API:**
   ```bash
   python run_with_gemini.py
   ```

## API Endpoints

### 1. Service Status
Check if Gemini service is configured and available:

```bash
GET /api/gemini/status
```

**Response:**
```json
{
  "available": true,
  "model": "gemini-1.5-flash",
  "message": "Gemini service is available using model: gemini-1.5-flash"
}
```

### 2. Contract Analysis
Analyze contracts with different focus areas:

```bash
POST /api/gemini/analyze-contract
```

**Request Body:**
```json
{
  "contract_text": "This agreement is made between Company A and Company B...",
  "analysis_type": "general",
  "include_raw_response": false
}
```

**Analysis Types:**
- `general` - Overall contract analysis
- `risk` - Risk assessment and mitigation
- `compliance` - GDPR and legal compliance
- `financial` - Financial implications

**Response:**
```json
{
  "summary": "This is a standard service agreement with moderate risk factors...",
  "key_terms": ["termination", "liability", "payment terms"],
  "risk_factors": ["Unclear termination clauses", "High liability limits"],
  "recommendations": ["Clarify termination conditions", "Review liability caps"],
  "confidence_score": 0.87,
  "analysis_type": "general"
}
```

### 3. Contract Summarization
Generate concise summaries:

```bash
POST /api/gemini/summarize-contract
```

**Request Body:**
```json
{
  "contract_text": "Full contract text here...",
  "max_length": 300
}
```

**Response:**
```json
{
  "summary": "This agreement outlines the terms for software licensing between Vendor and Client...",
  "original_length": 2500,
  "summary_length": 45
}
```

### 4. Interactive Chat
Ask questions about contracts:

```bash
POST /api/gemini/chat
```

**Request Body:**
```json
{
  "message": "What are the key obligations in this contract?",
  "contract_context": "Optional: contract text for context"
}
```

**Response:**
```json
{
  "response": "Based on the contract text, the key obligations include...",
  "suggestions": ["Review payment terms", "Check termination conditions"],
  "follow_up_questions": ["Are there any penalty clauses?", "What's the governing law?"]
}
```

### 5. Health Check
Simple health check for the Gemini service:

```bash
GET /api/gemini/health
```

## Python Usage Examples

### Using with requests library:

```python
import requests

# Analyze contract
response = requests.post("http://localhost:8000/api/gemini/analyze-contract", json={
    "contract_text": "Your contract text here...",
    "analysis_type": "risk"
})

if response.status_code == 200:
    analysis = response.json()
    print(f"Risk Analysis: {analysis['summary']}")
    print(f"Key Risks: {analysis['risk_factors']}")
```

### Using with FastAPI TestClient:

```python
from fastapi.testclient import TestClient
from blackletter_api.main import app

client = TestClient(app)

# Test contract analysis
response = client.post("/api/gemini/analyze-contract", json={
    "contract_text": "Sample contract text...",
    "analysis_type": "compliance"
})

assert response.status_code == 200
result = response.json()
print(result)
```

## Integration with Existing Services

The Gemini service integrates seamlessly with existing Blackletter services:

### Combined Risk Analysis
You can use both the existing AI risk scorer and Gemini for comprehensive analysis:

```python
# First get traditional risk analysis
traditional_risks = ai_risk_scorer.analyze_contract_risk(contract_text, findings)

# Then get AI-powered insights
gemini_analysis = gemini_service.analyze_contract(contract_text, "risk")

# Combine results for comprehensive assessment
combined_analysis = {
    "traditional_risks": traditional_risks,
    "ai_insights": gemini_analysis,
    "confidence": gemini_analysis.confidence_score if gemini_analysis else 0
}
```

## Error Handling

The API includes comprehensive error handling:

- **503 Service Unavailable**: Gemini API key not configured
- **400 Bad Request**: Invalid analysis type or malformed request
- **500 Internal Server Error**: Gemini API errors or processing failures

## Configuration Options

Customize Gemini behavior via environment variables:

```bash
# Model selection
GEMINI_MODEL=gemini-1.5-flash  # or gemini-1.5-pro

# Response parameters
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
```

## Testing

Run the tests:

```bash
# Unit tests
python -m pytest apps/api/blackletter_api/tests/unit/test_gemini_service.py -v

# Integration tests
python -m pytest apps/api/blackletter_api/tests/integration/ -v
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

All Gemini endpoints are documented with examples and schemas.
