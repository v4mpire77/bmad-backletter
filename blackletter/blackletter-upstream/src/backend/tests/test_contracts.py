import asyncio
import types
import sys
from pathlib import Path
from io import BytesIO


from fastapi import UploadFile
from backend.routers import contracts


def test_review_contract_handles_page_without_text(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    class DummyPage:
        def extract_text(self):
            return None

    class DummyPdf:
        pages = [DummyPage()]

    def fake_pdf_reader(_):
        return DummyPdf()

    monkeypatch.setattr(contracts, "PdfReader", fake_pdf_reader)

    class DummyResponse:
        choices = [types.SimpleNamespace(message=types.SimpleNamespace(content="Summary\n\n- Risk 1"))]

    class DummyCompletions:
        @staticmethod
        def create(*args, **kwargs):
            return DummyResponse()

    class DummyChat:
        completions = DummyCompletions()

    from unittest.mock import MagicMock

    # Create a mock response that matches the actual OpenAI response structure
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Summary\n\n- Risk 1"
                }
            }
        ]
    }

    mock_create = MagicMock(return_value=mock_response)
    mock_completions = MagicMock()
    mock_completions.create = mock_create
    mock_chat = MagicMock()
    mock_chat.completions = mock_completions
    dummy_openai = types.SimpleNamespace(chat=mock_chat)
    monkeypatch.setattr(contracts, "openai", dummy_openai)

    upload = UploadFile(filename="test.pdf", file=BytesIO(b"%PDF"), headers={"content-type": "application/pdf"})
    result = asyncio.run(contracts.review_contract(upload))
    assert result.summary == "Summary"
    assert result.risks == ["Risk 1"]
