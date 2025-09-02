import pytest

from blackletter_api.services.token_ledger import TokenLedger


def test_add_tokens_respects_cap(monkeypatch, tmp_path):
    """Tokens added beyond cap should set cap_exceeded and reason."""
    monkeypatch.setenv("TOKEN_CAP_PER_DOC", "100")
    ledger = TokenLedger(data_dir=tmp_path)
    analysis_id = "a1"

    exceeded, reason = ledger.add_tokens(analysis_id, 40, 0)
    assert not exceeded
    assert reason is None

    exceeded, reason = ledger.add_tokens(analysis_id, 50, 0)
    assert not exceeded
    assert reason is None

    exceeded, reason = ledger.add_tokens(analysis_id, 20, 0)
    assert exceeded
    assert "Token cap exceeded" in reason

    usage = ledger.get_usage(analysis_id)
    assert usage.cap_exceeded is True
    assert usage.cap_reason == reason
