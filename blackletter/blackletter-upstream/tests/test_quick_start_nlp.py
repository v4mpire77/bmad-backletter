"""Tests for quick_start_nlp model loading."""

import os
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_load_model_returns_object_with_generate():
    """load_model should return an object that supports text generation."""

    mock_model = MagicMock()
    mock_model.generate = MagicMock()

    mock_engine = MagicMock()
    mock_engine.load_model.return_value = mock_model
    fake_module = SimpleNamespace(NLPEngine=MagicMock(return_value=mock_engine))

    with patch.dict(sys.modules, {"app.core.nlp_engine": fake_module}):
        from backend import quick_start_nlp

        model = quick_start_nlp.load_model("demo-model")

    assert hasattr(model, "generate")
    mock_engine.load_model.assert_called_once_with("demo-model", None)

