import pytest
from apps.api.services.evidence import build_evidence_window

@pytest.fixture
def sentence_index():
    """Provides a sample sentence index for testing."""
    return [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50)]

def test_build_evidence_window_middle(sentence_index):
    """Tests building an evidence window from the middle of the document."""
    window = build_evidence_window(sentence_index, 2, 1)
    assert window == [(11, 20), (21, 30), (31, 40)]

def test_build_evidence_window_start(sentence_index):
    """Tests building an evidence window from the beginning of the document."""
    window = build_evidence_window(sentence_index, 0, 2)
    assert window == [(0, 10), (11, 20), (21, 30)]

def test_build_evidence_window_end(sentence_index):
    """Tests building an evidence window from the end of the document."""
    window = build_evidence_window(sentence_index, 4, 2)
    assert window == [(21, 30), (31, 40), (41, 50)]

def test_build_evidence_window_zero_size(sentence_index):
    """Tests building an evidence window with a window size of 0."""
    window = build_evidence_window(sentence_index, 2, 0)
    assert window == [(21, 30)]

def test_build_evidence_window_large_size(sentence_index):
    """Tests building an evidence window with a large window size."""
    window = build_evidence_window(sentence_index, 2, 10)
    assert window == [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50)]
