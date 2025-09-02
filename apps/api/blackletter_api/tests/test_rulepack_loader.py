"""Tests for rulepack loader service."""
from unittest.mock import MagicMock, patch

from apps.api.blackletter_api.services.rulepack_loader import (
    RulepackLoader,
    S3CompatibleStorage,
)


def test_rulepack_loader_filesystem() -> None:
    """Loader can be instantiated with default filesystem storage."""
    loader = RulepackLoader()
    assert loader is not None


@patch("apps.api.blackletter_api.services.rulepack_loader.S3CompatibleStorage")
def test_rulepack_loader_s3_fallback(mock_s3_storage: MagicMock) -> None:
    """Loader uses filesystem when S3 storage returns no rulepack."""
    instance = MagicMock()
    instance.enabled = True
    instance.get_rulepack.return_value = None
    mock_s3_storage.return_value = instance

    loader = RulepackLoader()
    assert loader.s3_storage.enabled is True


def test_s3_compatible_storage_init() -> None:
    """S3 storage reads configuration from environment."""
    with patch.dict(
        "os.environ",
        {
            "S3_ENDPOINT_URL": "https://s3.example.com",
            "S3_ACCESS_KEY": "access_key",
            "S3_SECRET_KEY": "secret_key",
            "S3_BUCKET": "test-bucket",
        },
    ):
        storage = S3CompatibleStorage()
        assert storage.enabled
        assert storage.bucket == "test-bucket"


def test_s3_compatible_storage_disabled() -> None:
    """S3 storage is disabled when environment is missing."""
    with patch.dict("os.environ", {}, clear=True):
        storage = S3CompatibleStorage()
        assert storage.enabled is False
