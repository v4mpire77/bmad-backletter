#!/usr/bin/env python3
"""
Code Web Chat (CWC) Demo Script for Blackletter
This script demonstrates how CWC would integrate with your Blackletter project
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_JOB_ID = "test-job-123"

def test_contract_validation_endpoint() -> Dict[str, Any]:
    """
    Test the new validation status endpoint that we added for CWC demo
    """
    url = f"{API_BASE_URL}/api/contracts/validation-status/{TEST_JOB_ID}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def simulate_cwc_workflow():
    """
    Simulate how CWC would work with your Blackletter project
    """
    print("🔧 Code Web Chat (CWC) Demo for Blackletter")
    print("=" * 50)
    
    print("\n1. Testing the new validation endpoint...")
    result = test_contract_validation_endpoint()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("\n💡 To test this properly:")
        print("   1. Start your API: uvicorn blackletter_api.main:app --reload --app-dir apps/api")
        print("   2. Run this script again")
        return
    
    print("✅ API endpoint working!")
    print(f"📊 Validation Results: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 50)
    print("🎯 CWC Integration Demo")
    print("=" * 50)
    
    print("\n📝 How CWC would work with this project:")
    print("1. Chat with AI about adding new GDPR compliance checks")
    print("2. AI suggests code changes across multiple files:")
    print("   - apps/api/blackletter_api/routers/contracts.py")
    print("   - apps/api/blackletter_api/models/schemas.py")
    print("   - apps/api/blackletter_api/services/validation.py")
    
    print("\n3. Use CWC 'Apply Chat Response' to integrate changes")
    print("4. Use CWC 'Commit Changes' to generate commit message:")
    print("   feat(api): add enhanced GDPR compliance validation endpoint")
    
    print("\n🔧 CWC Commands you'd use:")
    print("- Code Web Chat: Apply Chat Response")
    print("- Code Web Chat: Code Completion")
    print("- Code Web Chat: Commit Changes")
    print("- Code Web Chat: Revert Last Changes")

if __name__ == "__main__":
    simulate_cwc_workflow()
