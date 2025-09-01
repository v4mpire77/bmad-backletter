"""
Test module for OCR functionality with feature flag.
"""
import os
import sys
from unittest.mock import patch

# Add the src directory to the Python path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_ocr_disabled_by_default():
    """Test that OCR is disabled by default."""
    with patch.dict(os.environ, {}, clear=True):
        from backend.services.ocr import ocr_available
        assert not ocr_available(), "OCR should be disabled by default"


def test_ocr_enabled_with_flag():
    """Test that OCR can be enabled with environment flag."""
    with patch.dict(os.environ, {"ENABLE_OCR": "true"}):
        # Re-import to pick up new environment
        import importlib
        import backend.services.ocr
        importlib.reload(backend.services.ocr)
        assert backend.services.ocr.ocr_available(), "OCR should be enabled with ENABLE_OCR=true"


def test_ocr_flag_variations():
    """Test different ways to enable OCR flag."""
    test_cases = [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("YES", True),
        ("false", False),
        ("False", False),
        ("0", False),
        ("no", False),
        ("", False),
        ("invalid", False),
    ]
    
    for flag_value, expected in test_cases:
        with patch.dict(os.environ, {"ENABLE_OCR": flag_value}):
            import importlib
            import backend.services.ocr
            importlib.reload(backend.services.ocr)
            assert backend.services.ocr.ocr_available() == expected, f"Failed for flag '{flag_value}'"


def test_extract_text_from_image_disabled():
    """Test that image extraction fails when OCR is disabled."""
    with patch.dict(os.environ, {"ENABLE_OCR": "false"}):
        import importlib
        import backend.services.ocr
        importlib.reload(backend.services.ocr)
        
        try:
            backend.services.ocr.extract_text_from_image(b"fake_image_data")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "OCR is disabled" in str(e), f"Wrong error message: {e}"


if __name__ == "__main__":
    # Simple test runner for manual testing
    print("Running OCR tests...")
    
    try:
        test_ocr_disabled_by_default()
        print("✓ OCR disabled by default")
        
        test_ocr_enabled_with_flag()
        print("✓ OCR can be enabled")
        
        test_ocr_flag_variations()
        print("✓ OCR flag variations work")
        
        test_extract_text_from_image_disabled()
        print("✓ Image extraction properly disabled")
        
        print("All tests passed!")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()