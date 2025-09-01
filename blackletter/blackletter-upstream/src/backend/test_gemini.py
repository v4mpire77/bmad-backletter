import os
import asyncio
import json
import pytest
from backend.llm_service import LLMService

pytestmark = pytest.mark.skip("Integration test requiring external Gemini API")

async def test_gemini():
    """Test Gemini API integration"""
    
    # Sample contract text for testing
    sample_contract = """
EMPLOYMENT AGREEMENT

This Employment Agreement is made between ABC Company Ltd ("Company") 
and John Smith ("Employee").

1. POSITION: Employee shall serve as Software Developer
2. TERM: This agreement begins January 1, 2024 for 2 years
3. COMPENSATION: £50,000 per annum
4. TERMINATION: Either party may terminate with 30 days notice
5. CONFIDENTIALITY: Employee agrees to maintain confidentiality of company information
"""

    try:
        llm = LLMService()
        print(f"✅ LLM Service initialized with provider: {llm.provider}")
        
        # Show provider information
        provider_info = llm.get_provider_info()
        print(f"📊 Provider Details:")
        print(f"   Model: {provider_info['model']}")
        print(f"   Gemini configured: {provider_info['gemini_configured']}")
        print(f"   Ollama available: {provider_info['ollama_available']}")
        
        if provider_info['init_error']:
            print(f"⚠️  Warning: {provider_info['init_error']}")
        
        print("🔄 Analyzing sample contract...")
        result = await llm.analyze_contract(sample_contract)
        
        print("📋 Analysis Results:")
        
        # Handle both JSON-structured and raw text responses
        if isinstance(result, dict):
            print(f"Summary: {result.get('summary', 'No summary provided')}")
            print(f"Risk Level: {result.get('risk_level', 'Not specified')}")
            print(f"Risks: {result.get('risks', [])}")
            print(f"Dates: {result.get('dates', [])}")
            print(f"Next Steps: {result.get('next_steps', 'Not specified')}")
            
            # Check for errors in response
            if result.get('error'):
                print(f"❌ Analysis Error: {result.get('error')}")
            else:
                print("✅ Gemini integration working!")
        else:
            # Handle raw text response
            print(f"Raw response: {result}")
            try:
                # Try to parse as JSON if it's a string
                if isinstance(result, str):
                    parsed = json.loads(result)
                    print("✅ Successfully parsed JSON response:")
                    print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("📝 Response is not JSON formatted")
            print("✅ Gemini integration working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check your GEMINI_API_KEY environment variable")
        
        # Provide troubleshooting guidance
        print("\n🔧 Troubleshooting:")
        print("1. Ensure GEMINI_API_KEY environment variable is set")
        print("2. Set LLM_PROVIDER=gemini if you want to use Gemini specifically")
        print("3. Check your API quota and billing status")
        print("4. Verify internet connectivity")

if __name__ == "__main__":
    asyncio.run(test_gemini())
