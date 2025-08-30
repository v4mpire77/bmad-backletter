# Gemini AI Integration Setup

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Database Configuration
DATABASE_URL=sqlite:///./blackletter.db

# CORS Configuration
CORS_ORIGINS=*

# Gemini AI Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.7

# Logging Configuration
LOG_LEVEL=INFO

# Security Configuration
SECRET_KEY=your-secret-key-change-this-in-production
```

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key and paste it in your `.env` file as `GEMINI_API_KEY`

## Available Gemini Models

- `gemini-1.5-flash`: Fast and efficient for most tasks
- `gemini-1.5-pro`: More powerful for complex analysis
- `gemini-pro`: Previous generation model

## Installation

Install the required dependencies:

```bash
pip install google-generativeai pydantic-settings
```

## API Endpoints

Once integrated, the Gemini service will provide:

- `/api/gemini/analyze-contract`: Analyze contract text using Gemini AI
- `/api/gemini/risk-assessment`: Advanced risk assessment with AI insights
- `/api/gemini/summarize`: Generate contract summaries
- `/api/gemini/chat`: Interactive AI chat for contract questions
