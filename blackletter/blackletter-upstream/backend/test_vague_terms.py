#!/usr/bin/env python3
"""
Test script for the vague terms detection system.
Run this to see how the system detects and analyzes vague contractual language.
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.vague_detector import VagueTermsDetector
from app.services.rag_store import RAGStore
from app.services.gemini_judge import GeminiJudge

# Sample contract text with various vague terms
SAMPLE_CONTRACT = """
DATA PROCESSING AGREEMENT

1. SERVICES
The Processor shall use reasonable efforts to provide the Services in accordance with industry standard security practices.

2. DATA PROTECTION
The Processor shall implement appropriate measures to protect personal data and shall notify the Controller as soon as practicable after becoming aware of any data breach.

3. SUB-PROCESSORS
The Processor may, in its sole discretion, appoint sub-processors from time to time to assist in the provision of the Services.

4. TERMINATION
Either party may terminate this agreement on a case-by-case basis where practicable, provided that reasonable time is given for transition.

5. LIABILITY
The Processor's liability shall not be limited to the fees paid under this agreement and shall be determined on a case-by-case basis.
"""

async def test_vague_terms_detection():
    """Test the complete vague terms detection pipeline."""
    
    print("🔍 Testing Vague Terms Detection System")
    print("=" * 50)
    
    # Initialize services
    detector = VagueTermsDetector()
    rag_store = RAGStore()
    judge = GeminiJudge()
    
    # Store document in RAG store
    doc_id = "test_contract.pdf"
    rag_store.store_document(doc_id, SAMPLE_CONTRACT, {
        "filename": "test_contract.pdf",
        "test": True
    })
    
    print(f"📄 Document stored: {doc_id}")
    print(f"📝 Text length: {len(SAMPLE_CONTRACT)} characters")
    
    # Find vague terms
    vague_hits = detector.find_vague_spans(SAMPLE_CONTRACT)
    
    print(f"\n🎯 Found {len(vague_hits)} vague terms:")
    print("-" * 30)
    
    for i, hit in enumerate(vague_hits, 1):
        print(f"{i}. '{hit['text']}' ({hit['category']} - {hit['severity']})")
        print(f"   Position: {hit['start']}-{hit['end']}")
        print(f"   Description: {hit['description']}")
        print()
    
    # Process each vague term with LLM judgment
    print("🤖 LLM Analysis Results:")
    print("-" * 30)
    
    for i, hit in enumerate(vague_hits, 1):
        # Get context around the vague term
        context = rag_store.get_context_around_position(
            doc_id, hit["start"], window_size=800
        )
        
        # Create citations
        citations = [{
            "doc_id": doc_id,
            "page": context["page"],
            "start": hit["start"],
            "end": hit["end"]
        }]
        
        print(f"\n{i}. Analyzing: '{hit['text']}'")
        print(f"   Context: {context['context'][:100]}...")
        
        # Get LLM judgment
        judgment = await judge.judge_vague_term(hit, context["context"], citations)
        
        print(f"   Verdict: {judgment['verdict']}")
        print(f"   Risk: {judgment['risk']}")
        print(f"   Rationale: {judgment['rationale']}")
        
        if judgment['improvements']:
            print(f"   Suggested fix: {judgment['improvements'][0]}")
        
        if judgment.get('fallback'):
            print("   ⚠️  Using fallback judgment (Gemini not available)")
    
    print("\n✅ Test completed!")
    print("\nTo enable Gemini analysis, set the GEMINI_API_KEY environment variable:")
    print("export GEMINI_API_KEY='your-api-key-here'")

if __name__ == "__main__":
    asyncio.run(test_vague_terms_detection())
