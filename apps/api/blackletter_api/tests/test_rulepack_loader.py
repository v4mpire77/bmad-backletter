"""Tests for rulepack loader service and S3-compatible storage."""
import os
import pytest
from unittest.mock import patch, MagicMock
from apps.api.blackletter_api.services.rulepack_loader import (
    RulepackLoader,
    S3CompatibleStorage,
)


def test_rulepack_loader_instantiation() -> None:
    """Basic smoke test that the loader can be constructed."""
    loader = RulepackLoader()
    assert loader is not None


@patch('apps.api.blackletter_api.services.rulepack_loader.S3CompatibleStorage')
def test_rulepack_loader_s3_fallback(mock_s3_storage) -> None:
    """When S3 returns None, loader should fall back to filesystem without crashing."""
    mock_s3 = MagicMock()
    mock_s3.enabled = True
    mock_s3.get_rulepack.return_value = None
    mock_s3_storage.return_value = mock_s3

    loader = RulepackLoader()
    assert loader.s3_storage.enabled is True


def test_s3_compatible_storage_init_env() -> None:
    """Environment variables should configure the storage and enable it."""
    with patch.dict(os.environ, {
        'S3_ENDPOINT_URL': 'https://s3.example.com',
        'S3_ACCESS_KEY': 'access_key',
        'S3_SECRET_KEY': 'secret_key',
        'S3_BUCKET': 'test-bucket',
    }, clear=True):
        storage = S3CompatibleStorage()
        assert storage.endpoint_url == 'https://s3.example.com'
        assert storage.access_key == 'access_key'
        assert storage.secret_key == 'secret_key'
        assert storage.bucket == 'test-bucket'
        assert storage.enabled is True


def test_s3_compatible_storage_disabled_when_missing() -> None:
    with patch.dict(os.environ, {}, clear=True):
        storage = S3CompatibleStorage()
        assert storage.enabled is False


@patch('apps.api.blackletter_api.services.rulepack_loader.boto3')
def test_s3_compatible_storage_get_rulepack_success(mock_boto3) -> None:
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.get_object.return_value = {
        'Body': MagicMock(read=MagicMock(return_value=b'name: test\nversion: 1.0.0'))
    }

    storage = S3CompatibleStorage(
        endpoint_url='https://s3.example.com',
        access_key='access_key',
        secret_key='secret_key',
        bucket='test-bucket',
    )

    result = storage.get_rulepack('test_rulepack.yaml')
    assert isinstance(result, dict)
    assert result.get('name') == 'test'


@patch('apps.api.blackletter_api.services.rulepack_loader.boto3')
def test_s3_compatible_storage_get_rulepack_error(mock_boto3) -> None:
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.get_object.side_effect = Exception('S3 Error')

    storage = S3CompatibleStorage(
        endpoint_url='https://s3.example.com',
        access_key='access_key',
        secret_key='secret_key',
        bucket='test-bucket',
    )

    result = storage.get_rulepack('test_rulepack.yaml')
    assert result is None

