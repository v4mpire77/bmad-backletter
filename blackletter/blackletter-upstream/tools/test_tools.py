#!/usr/bin/env python3
"""
Test script for Context Engineering tools.
This script verifies that all tools are working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from context_engineering_validator import ContextEngineeringValidator
        print("✅ ContextEngineeringValidator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ContextEngineeringValidator: {e}")
        return False
    
    try:
        from context_engineering_automation import ContextEngineeringAutomation
        print("✅ ContextEngineeringAutomation imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ContextEngineeringAutomation: {e}")
        return False
    
    return True

def test_validator():
    """Test the Context Engineering validator."""
    try:
        from context_engineering_validator import ContextEngineeringValidator
        
        validator = ContextEngineeringValidator()
        
        # Test with a sample response
        sample_response = """
        Context Assessment: I reviewed the Implementation Plan and Project Structure.
        Implementation Plan: I will create a new service following established patterns.
        Implementation: Here is my code implementation.
        Documentation: I updated the relevant documentation.
        Verification against checklist: All items completed.
        """
        
        results = validator.validate_response(sample_response)
        
        print(f"✅ Validator test completed")
        print(f"   Score: {results['overall_score']:.1f}%")
        print(f"   Passed: {results['passed']}")
        
        return results['passed']
        
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        return False

def test_automation():
    """Test the Context Engineering automation."""
    try:
        from context_engineering_automation import ContextEngineeringAutomation
        
        automation = ContextEngineeringAutomation()
        
        # Test context summary generation
        context_summary = automation.generate_context_summary("Test task implementation")
        
        print(f"✅ Automation test completed")
        print(f"   Task type: {context_summary['task_analysis']['type']}")
        print(f"   Complexity: {context_summary['task_analysis']['complexity']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        "context_engineering_validator.py",
        "context_engineering_automation.py",
        "context_engineering.ps1",
        "README.md"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("=" * 60)
    print("CONTEXT ENGINEERING TOOLS TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Validator Tool", test_validator),
        ("Automation Tool", test_automation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Context Engineering tools are ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
