from pathlib import Path
from tempfile import TemporaryDirectory

from blackletter_api.services.token_ledger import TokenLedger


def test_add_and_get_usage() -> None:
    """TokenLedger should accumulate and return usage metrics."""
    with TemporaryDirectory() as tmp:
        ledger = TokenLedger(Path(tmp))
        ledger.add_tokens("a1", 100, 50)

        usage = ledger.get_usage("a1")
        assert usage.total_tokens == 150
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.estimated_cost > 0


def test_token_cap_exceeded(monkeypatch) -> None:
    """Adding tokens beyond the cap should return an error."""
    with TemporaryDirectory() as tmp:
        monkeypatch.setenv("TOKEN_CAP_PER_DOC", "10")
        ledger = TokenLedger(Path(tmp))

        exceeded, reason = ledger.add_tokens("a1", 8, 5)
        assert exceeded is True
        assert reason is not None and "Token cap exceeded" in reason


def test_reset_usage() -> None:
    """Resetting usage should remove cached and persisted data."""
    with TemporaryDirectory() as tmp:
        ledger = TokenLedger(Path(tmp))
        ledger.add_tokens("a1", 1, 1)
        usage_path = Path(tmp) / "a1" / "tokens.json"
        assert usage_path.exists()

        ledger.reset_usage("a1")
        assert not usage_path.exists()
        usage = ledger.get_usage("a1")
        assert usage.total_tokens == 0
