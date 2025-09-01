# Gemini API Test Script

This directory contains a comprehensive test script for validating the Gemini API integration and contract analysis functionality.

## Files Created

### `llm_service.py`
A unified LLM service wrapper that provides a consistent interface for contract analysis across different LLM providers (Gemini, Ollama).

### `test_gemini.py`
The main test script that validates the Gemini API integration and contract analysis functionality.

### `tests/test_llm_service.py`
Unit tests for the LLMService wrapper class.

## Features

- **Multi-Provider Support**: Automatically detects and uses available LLM providers
- **Comprehensive Error Handling**: Provides detailed error messages and troubleshooting guidance
- **Fallback Mechanism**: Uses heuristic analysis when no LLM provider is available
- **Provider Information**: Shows detailed configuration and status information
- **Test Contract Analysis**: Uses a sample employment contract for testing

## Usage

### Basic Usage

```bash
cd backend
python test_gemini.py
```

### Testing with Gemini

```bash
cd backend
export GEMINI_API_KEY="your-gemini-api-key"
export LLM_PROVIDER="gemini"
python test_gemini.py
```

## Expected Output

### With Gemini API Key Configured

```
✅ LLM Service initialized with provider: gemini
📊 Provider Details:
   Model: gemini-2.0-flash
   Gemini configured: True
   Ollama available: False
🔄 Analyzing sample contract...
📋 Analysis Results:
Summary: Employment agreement for Software Developer role...
Risk Level: Medium
Risks: ['Short termination notice period', 'Limited confidentiality scope']
Dates: []
Next Steps: Not specified
✅ Gemini integration working!
```

### Without API Key

```
⚠️  Warning: GEMINI_API_KEY is missing.
✅ LLM Service initialized with provider: gemini
📊 Provider Details:
   Model: gemini-2.0-flash
   Gemini configured: False
   Ollama available: False
⚠️  Warning: GEMINI_API_KEY is missing.
🔄 Analyzing sample contract...
📋 Analysis Results:
Summary: EMPLOYMENT AGREEMENT...
Risk Level: Not specified
Risks: ['POSITION: Employee shall serve as Software Developer', 'TERMINATION: Either party may terminate with 30 days notice']
Dates: []
Next Steps: Not specified
❌ Analysis Error: GEMINI_API_KEY is missing.
```

## Environment Variables

- `GEMINI_API_KEY`: Your Gemini API key
- `LLM_PROVIDER`: Preferred provider (`gemini` or `ollama`)
- `GEMINI_MODEL`: Gemini model to use (default: `gemini-2.0-flash`)
- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://localhost:11434`)

## Troubleshooting

### Common Issues

1. **GEMINI_API_KEY is missing**
   - Set the environment variable: `export GEMINI_API_KEY="your-key"`
   - Verify the key is valid and has proper permissions

2. **Network connectivity errors**
   - Check internet connection
   - Verify firewall settings
   - Check API endpoint accessibility

3. **API quota exceeded**
   - Check your Google Cloud Console for quota usage
   - Verify billing account is active
   - Consider upgrading your plan

4. **No LLM backend configured**
   - Install and configure at least one LLM provider
   - Start Ollama server if using Ollama
   - Set appropriate API keys for cloud providers

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
python -m pytest tests/ -v

# Run specific tests
python -m pytest tests/test_llm_service.py -v
```

## Integration

The `LLMService` class can be easily integrated into other parts of the application:

```python
from llm_service import LLMService

# Initialize service
llm = LLMService()

# Check provider status
info = llm.get_provider_info()
print(f"Using provider: {info['provider']}")

# Analyze contract
result = await llm.analyze_contract("Contract text here...")
print(f"Analysis: {result}")
```

## API Response Format

The contract analysis returns a dictionary with the following structure:

```json
{
    "summary": "Brief summary of the contract (2-3 sentences)",
    "risks": ["List", "of", "identified", "risks"],
    "dates": ["List", "of", "important", "dates"],
    "risk_level": "Low/Medium/High (when available)",
    "next_steps": ["Recommended", "next", "steps"],
    "error": "Error message if any issues occurred"
}
```

## Architecture

The test script uses a layered architecture:

1. **LLMService**: High-level service interface
2. **LLMAdapter**: Low-level adapter handling multiple providers
3. **Provider Clients**: Individual provider implementations (Gemini, OpenAI, Ollama)

This design allows for easy testing, mocking, and provider switching while maintaining a consistent interface for contract analysis.