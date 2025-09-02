"""Test for rulepack versioning functionality."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from apps.api.blackletter_api.services.rulepack_loader import RulepackLoader, S3CompatibleStorage


@patch('apps.api.blackletter_api.services.rulepack_loader.Path')
def test_list_available_versions_filesystem(mock_path):
    """Test listing available versions from filesystem."""
    # Mock the filesystem glob
    mock_rules_dir = MagicMock()
    mock_path.return_value = mock_rules_dir
    
    # Mock glob to return specific files
    mock_file1 = MagicMock()
    mock_file1.stem = "art28_v1.2.3"
    mock_file2 = MagicMock()
    mock_file2.stem = "art28_v1.0.0"
    mock_file3 = MagicMock()
    mock_file3.stem = "art28_v1.1.0"
    
    mock_rules_dir.glob.return_value = [mock_file1, mock_file2, mock_file3]
    mock_rules_dir.exists.return_value = True
    
    loader = RulepackLoader(rules_dir=mock_rules_dir)
    versions = loader.list_available_versions("art28")
    
    # Should be sorted in descending order
    assert versions == ["1.2.3", "1.1.0", "1.0.0"]


@patch('apps.api.blackletter_api.services.rulepack_loader.boto3')
def test_list_available_versions_s3(mock_boto3):
    """Test listing available versions from S3."""
    # Mock boto3 client
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.list_objects_v2.return_value = {
        'Contents': [
            {'Key': 'art28_v1.2.3.yaml'},
            {'Key': 'art28_v1.0.0.yaml'},
            {'Key': 'art28_v1.1.0.yaml'}
        ]
    }
    
    storage = S3CompatibleStorage(
        endpoint_url='https://s3.example.com',
        access_key='access_key',
        secret_key='secret_key',
        bucket='test-bucket'
    )
    
    loader = RulepackLoader(s3_storage=storage)
    with patch.object(loader, 'rules_dir') as mock_rules_dir:
        mock_rules_dir.exists.return_value = False  # No filesystem files
        versions = loader.list_available_versions("art28")
    
    # Should be sorted in descending order
    assert versions == ["1.2.3", "1.1.0", "1.0.0"]


def test_get_latest_version():
    """Test getting the latest version."""
    loader = RulepackLoader()
    
    # Mock list_available_versions
    with patch.object(loader, 'list_available_versions') as mock_list:
        mock_list.return_value = ["1.2.3", "1.1.0", "1.0.0"]
        latest = loader.get_latest_version("art28")
        assert latest == "1.2.3"
        
        # Test when no versions available
        mock_list.return_value = []
        latest = loader.get_latest_version("nonexistent")
        assert latest is None