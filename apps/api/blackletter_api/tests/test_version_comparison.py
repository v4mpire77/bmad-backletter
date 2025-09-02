"""Test for version comparison functionality."""
import pytest
from apps.api.blackletter_api.models.rulepack_schema import Version, compare_versions


def test_version_creation():
    """Test version creation and parsing."""
    v = Version("1.2.3")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert str(v) == "1.2.3"


def test_version_invalid_format():
    """Test that invalid version formats raise ValueError."""
    with pytest.raises(ValueError):
        Version("1.2")  # Missing patch
    
    with pytest.raises(ValueError):
        Version("1.2.3.4")  # Too many parts
    
    with pytest.raises(ValueError):
        Version("a.b.c")  # Non-numeric parts


def test_version_comparison():
    """Test version comparison operations."""
    v1 = Version("1.2.3")
    v2 = Version("1.2.4")
    v3 = Version("1.3.0")
    v4 = Version("2.0.0")
    v5 = Version("1.2.3")  # Same as v1
    
    # Test equality
    assert v1 == v5
    assert v1 == "1.2.3"
    assert not v1 == v2
    
    # Test less than
    assert v1 < v2
    assert v1 < v3
    assert v1 < v4
    assert v2 < v3
    assert v3 < v4
    
    # Test less than or equal
    assert v1 <= v5  # Equal
    assert v1 <= v2  # Less than
    
    # Test greater than
    assert v2 > v1
    assert v4 > v3
    assert v3 > v2
    assert v2 > v1
    
    # Test greater than or equal
    assert v5 >= v1  # Equal
    assert v2 >= v1  # Greater than


def test_compare_versions_function():
    """Test the compare_versions function."""
    # Test equal versions
    assert compare_versions("1.2.3", "1.2.3") == 0
    
    # Test version1 < version2
    assert compare_versions("1.2.3", "1.2.4") == -1
    assert compare_versions("1.2.3", "1.3.0") == -1
    assert compare_versions("1.2.3", "2.0.0") == -1
    
    # Test version1 > version2
    assert compare_versions("1.2.4", "1.2.3") == 1
    assert compare_versions("1.3.0", "1.2.3") == 1
    assert compare_versions("2.0.0", "1.2.3") == 1