import json
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

sys.path.append(str(Path(__file__).resolve().parents[5] / "blackletter" / "blackletter-upstream" / "backend"))
from app.services.gemini_judge import GeminiJudge, JudgmentResult


@pytest.mark.asyncio
async def test_judge_rule_compliance_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    judge = GeminiJudge()
    rule = {
        "id": "R01",
        "name": "Lawful basis",
        "description": "desc",
        "severity": "high",
        "required": True,
    }

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_data = json.dumps(
        {
            "verdict": "compliant",
            "risk": "low",
            "rationale": "ok",
            "improvements": [],
            "quotes": [],
            "confidence": 0.9,
        }
    )
    mock_response = Mock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": mock_data}]}}]
    }
    mock_response.raise_for_status.return_value = None
    mock_client.post.return_value = mock_response

    with patch("app.services.gemini_judge.httpx.AsyncClient", return_value=mock_client):
        result = await judge.judge_rule_compliance(rule, "snippet", "context", [])

    assert isinstance(result, JudgmentResult)
    assert result.verdict == "compliant"
    assert result.risk == "low"


@pytest.mark.asyncio
async def test_judge_rule_compliance_failure(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    judge = GeminiJudge()
    rule = {
        "id": "R01",
        "name": "Lawful basis",
        "description": "desc",
        "severity": "high",
        "required": True,
    }

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.side_effect = httpx.TimeoutException("boom")

    with patch("app.services.gemini_judge.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(RuntimeError):
            await judge.judge_rule_compliance(rule, "snippet", "context", [])

    assert mock_client.post.call_count == 3
