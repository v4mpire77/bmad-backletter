#!/usr/bin/env python3
"""
RAG System Test Script

This script demonstrates the RAG system functionality with sample data.
"""

import asyncio
import json
from datetime import datetime

# Import RAG components
from app.services.rag_store import rag_store
from app.services.rag_analyzer import rag_analyzer
from app.core.llm_adapter import LLMAdapter

# Sample contract text for testing
SAMPLE_CONTRACT = """
EMPLOYMENT AGREEMENT

This Employment Agreement (the "Agreement") is entered into as of January 1, 2024, by and between:

ABC Corporation, a Delaware corporation (the "Company"), and John Doe (the "Employee").

1. POSITION AND DUTIES
The Employee shall serve as Senior Software Engineer and shall perform such duties as may be assigned by the Company from time to time. The Employee shall report directly to the Chief Technology Officer.

2. COMPENSATION
The Employee shall receive an annual base salary of $120,000, payable in accordance with the Company's normal payroll practices. The Employee shall also be eligible for an annual performance bonus of up to 20% of base salary, subject to the Company's discretion and performance criteria.

3. TERM AND TERMINATION
This Agreement shall commence on January 1, 2024, and shall continue until terminated by either party with 30 days written notice. The Company may terminate this Agreement immediately for cause, including but not limited to: (a) violation of Company policies; (b) poor performance; (c) misconduct; or (d) breach of this Agreement.

4. CONFIDENTIALITY
The Employee acknowledges that during employment, the Employee will have access to confidential information including trade secrets, customer lists, and proprietary technology. The Employee agrees to maintain the confidentiality of such information both during and after employment.

5. NON-COMPETE
For a period of 12 months following termination of employment, the Employee shall not engage in any business that competes with the Company within a 50-mile radius of the Company's principal place of business.

6. DATA PROTECTION
The Employee acknowledges and agrees to comply with all applicable data protection laws, including but not limited to the General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA). The Employee shall process personal data only as instructed by the Company and shall implement appropriate technical and organizational measures to ensure data security.

7. BENEFITS
The Employee shall be eligible to participate in the Company's health insurance, retirement, and other benefit plans in accordance with the terms of such plans.

8. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of California.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

ABC Corporation
By: _________________
Name: Jane Smith
Title: Chief Executive Officer

John Doe
Signature: _________________
Date: _________________
"""

async def test_rag_system():
    """Test the RAG system with sample data."""
    print("🚀 Testing RAG System for Blackletter Systems")
    print("=" * 50)
    
    # Initialize LLM adapter
    llm_adapter = LLMAdapter()
    
    # Test 1: Store document in RAG store
    print("\n1. 📄 Storing sample contract in RAG store...")
    doc_id = "test_contract_001"
    metadata = {
        "filename": "sample_employment_contract.pdf",
        "upload_time": datetime.utcnow().isoformat(),
        "contract_type": "employment",
        "parties": ["ABC Corporation", "John Doe"]
    }
    
    chunks = await rag_store.store_document(doc_id, SAMPLE_CONTRACT, metadata)
    print(f"✅ Created {len(chunks)} chunks from contract")
    
    # Test 2: Get RAG store statistics
    print("\n2. 📊 RAG Store Statistics:")
    stats = rag_store.get_stats()
    print(json.dumps(stats, indent=2))
    
    # Test 3: Test semantic search
    print("\n3. 🔍 Testing semantic search...")
    search_queries = [
        "What is the employee's salary?",
        "What are the termination conditions?",
        "What are the data protection obligations?",
        "What is the non-compete period?"
    ]
    
    for query in search_queries:
        print(f"\nQuery: {query}")
        try:
            results = await rag_store.semantic_search(query, top_k=3, doc_id=doc_id)
            if results:
                best_match = results[0]
                print(f"Best match (score: {best_match[1]:.3f}):")
                print(f"  Text: {best_match[0].text[:150]}...")
                print(f"  Page: {best_match[0].page}")
            else:
                print("No relevant results found")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 4: Test RAG query with context generation
    print("\n4. 🤖 Testing RAG query with context generation...")
    test_queries = [
        "What are the key terms of this employment agreement?",
        "What are the employee's obligations regarding confidentiality?",
        "What happens if the employee violates the non-compete clause?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = await rag_analyzer.query_contract(doc_id, query, include_context=True)
            if "error" not in result:
                print(f"Answer: {result['answer'][:200]}...")
                print(f"Chunks retrieved: {result['total_chunks_retrieved']}")
            else:
                print(f"Error: {result['error']}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 5: Test comprehensive analysis
    print("\n5. 📋 Testing comprehensive contract analysis...")
    try:
        analysis = await rag_analyzer.analyze_contract_with_rag(
            doc_id="test_contract_002",
            text=SAMPLE_CONTRACT,
            metadata={"filename": "test_contract.pdf"}
        )
        
        print("Analysis Results:")
        print(f"  - Vague terms found: {analysis.get('vague_terms_found', 0)}")
        print(f"  - Chunks created: {analysis.get('chunks_created', 0)}")
        
        if 'rag_insights' in analysis:
            insights = analysis['rag_insights']
            print(f"  - Key clauses identified: {len(insights.get('key_clauses', []))}")
            print(f"  - Important dates found: {len(insights.get('important_dates', []))}")
            print(f"  - Financial terms identified: {len(insights.get('financial_terms', []))}")
        
        if 'risk_assessment' in analysis:
            risk = analysis['risk_assessment']
            print(f"  - Overall risk level: {risk.get('overall_risk_level', 'Unknown')}")
            print(f"  - Total risk score: {risk.get('total_risk_score', 0)}")
            
    except Exception as e:
        print(f"Error in comprehensive analysis: {e}")
    
    # Test 6: Test document comparison
    print("\n6. ⚖️ Testing document comparison...")
    try:
        # Create a second sample contract for comparison
        sample_contract_2 = SAMPLE_CONTRACT.replace("$120,000", "$150,000").replace("John Doe", "Jane Smith")
        doc_id_2 = "test_contract_003"
        await rag_store.store_document(doc_id_2, sample_contract_2, metadata)
        
        comparison = await rag_analyzer.compare_contracts(
            doc_ids=[doc_id, doc_id_2],
            comparison_criteria=["compensation", "termination conditions", "confidentiality obligations"]
        )
        
        print("Comparison Results:")
        print(f"  - Documents compared: {len(comparison.get('documents_compared', []))}")
        print(f"  - Criteria compared: {len(comparison.get('comparison_criteria', []))}")
        
    except Exception as e:
        print(f"Error in document comparison: {e}")
    
    # Test 7: Test summary report generation
    print("\n7. 📝 Testing summary report generation...")
    try:
        report = await rag_analyzer.generate_summary_report(doc_id)
        if "error" not in report:
            print("Summary Report Generated:")
            print(f"  - Total chunks: {report.get('total_chunks', 0)}")
            print(f"  - Sections generated: {len(report.get('summary_sections', {}))}")
        else:
            print(f"Error generating report: {report['error']}")
    except Exception as e:
        print(f"Error generating summary report: {e}")
    
    # Test 8: Test embedding generation
    print("\n8. 🧠 Testing embedding generation...")
    try:
        test_texts = [
            "What is the employee's salary?",
            "What are the termination conditions?",
            "What are the data protection obligations?"
        ]
        
        embeddings = await llm_adapter.get_embeddings(test_texts)
        print(f"✅ Generated {len(embeddings)} embeddings")
        print(f"   Embedding dimension: {len(embeddings[0]) if embeddings else 0}")
        
    except Exception as e:
        print(f"Error generating embeddings: {e}")
    
    print("\n" + "=" * 50)
    print("✅ RAG System Test Completed!")
    print("\nKey Features Tested:")
    print("  ✓ Document storage and chunking")
    print("  ✓ Semantic search")
    print("  ✓ Context-aware querying")
    print("  ✓ Comprehensive analysis")
    print("  ✓ Document comparison")
    print("  ✓ Summary report generation")
    print("  ✓ Embedding generation")
    
    # Cleanup
    print("\n🧹 Cleaning up test data...")
    try:
        rag_store.clear_document(doc_id)
        rag_store.clear_document("test_contract_002")
        rag_store.clear_document("test_contract_003")
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"Warning: Could not clean up test data: {e}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_rag_system())
