import sys
import types

import pytest


@pytest.mark.usefixtures("fake_boto3_client")
def test_api_rules_summary_loads_from_s3(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "dummy")
    stub = types.ModuleType("apps.api.blackletter_api.models.rulepack_schema")
    stub.validate_rulepack = lambda *a, **k: None
    stub.RulepackValidationError = type("RulepackValidationError", (), {})
    stub.compare_versions = lambda *a, **k: 0
    sys.modules["apps.api.blackletter_api.models.rulepack_schema"] = stub

    from blackletter_api.services import rulepack_loader

    storage = rulepack_loader.S3CompatibleStorage(
        endpoint_url="https://s3.example.com",
        access_key="key",
        secret_key="secret",
        bucket="bucket",
    )
    result = storage.get_rulepack("dummy.yaml")
    assert result == {}
