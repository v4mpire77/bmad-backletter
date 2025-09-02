import pytest
from blackletter_api.services.evidence import build_window, build_window_legacy, handle_boundary_cases

# A constant list of sentences to be used across tests.
# Spans multiple pages to test for cross-page leakage.
SAMPLE_SENTENCES = [
    {"page": 1, "start": 0, "end": 25, "text": "This is the first sentence."},
    {"page": 1, "start": 26, "end": 55, "text": "This is the second sentence."},
    {"page": 1, "start": 56, "end": 83, "text": "This is the third sentence."},
    {"page": 1, "start": 84, "end": 113, "text": "This is the fourth sentence."},
    {"page": 1, "start": 114, "end": 142, "text": "This is the fifth sentence."},
    {"page": 1, "start": 143, "end": 171, "text": "This is the sixth sentence."},
    {"page": 1, "start": 172, "end": 201, "text": "This is the seventh sentence."},
    {"page": 2, "start": 0, "end": 20, "text": "A sentence on page 2."},
]


# Story 1.3 Tests - New build_window function with updated signature
def test_story_1_3_build_window():
    """Test Story 1.3 build_window function with new signature."""
    analysis_id = "test_analysis_123"
    start = 100
    end = 200
    n_sentences = 2
    
    result = build_window(analysis_id, start, end, n_sentences)
    
    # Verify the response structure matches acceptance criteria
    assert "snippet" in result
    assert "page" in result
    assert "start" in result
    assert "end" in result
    assert result["analysis_id"] == analysis_id
    assert result["sentence_window"] == n_sentences


def test_story_1_3_build_window_default_sentences():
    """Test that build_window uses default of 2 sentences."""
    analysis_id = "test_analysis_456"
    start = 50
    end = 100
    
    result = build_window(analysis_id, start, end)
    
    assert result["sentence_window"] == 2


def test_story_1_3_build_window_custom_sentences():
    """Test build_window with custom sentence count."""
    analysis_id = "test_analysis_789"
    start = 50
    end = 100
    n_sentences = 5
    
    result = build_window(analysis_id, start, end, n_sentences)
    
    assert result["sentence_window"] == n_sentences


def test_handle_boundary_cases_start_of_document():
    """Test boundary handling at start of document."""
    text = "This is a test document with multiple sentences. " * 10
    start = 5
    end = 15
    
    result = handle_boundary_cases(text, start, end, 2)
    
    assert result["start"] == 0  # Should start at beginning
    assert result["boundary_adjusted"] is True
    assert "snippet" in result


def test_handle_boundary_cases_end_of_document():
    """Test boundary handling at end of document."""
    text = "Short text."
    start = 8
    end = 10
    
    result = handle_boundary_cases(text, start, end, 2)
    
    assert result["end"] == len(text)  # Should end at document end
    assert result["boundary_adjusted"] is True


def test_handle_boundary_cases_non_ascii():
    """Test handling of non-ASCII characters."""
    text = "This has émojis 🎉 and unicode ñ characters."
    start = 10
    end = 20
    
    result = handle_boundary_cases(text, start, end, 2)
    
    # Should handle non-ASCII without errors
    assert "snippet" in result
    assert len(result["snippet"]) > 0


# Legacy tests - using build_window_legacy for backward compatibility
def test_build_window_standard_case():
    """Tests a standard window with default before=2, after=2 values."""
    target_span = (90, 94)  # A finding in the middle of sentence 4
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=1, target_span=target_span)

    # Expects sentence 4, plus 2 before (2, 3) and 2 after (5, 6)
    assert result["text"] == "This is the second sentence. This is the third sentence. This is the fourth sentence. This is the fifth sentence. This is the sixth sentence."
    assert result["sentence_indices"] == [1, 2, 3, 4, 5]
    assert result["page"] == 1


def test_build_window_start_edge_case():
    """Tests a window for a finding at the very beginning of the page."""
    target_span = (5, 10)  # A finding in sentence 1
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=1, target_span=target_span)

    # Expects sentence 1, plus 2 after (2, 3), with no sentences before
    assert result["text"] == "This is the first sentence. This is the second sentence. This is the third sentence."
    assert result["sentence_indices"] == [0, 1, 2]
    assert result["page"] == 1


def test_build_window_end_edge_case():
    """Tests a window for a finding at the very end of the page."""
    target_span = (180, 185)  # A finding in sentence 7
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=1, target_span=target_span)

    # Expects sentence 7, plus 2 before (5, 6), with no sentences after
    assert result["text"] == "This is the fifth sentence. This is the sixth sentence. This is the seventh sentence."
    assert result["sentence_indices"] == [4, 5, 6]
    assert result["page"] == 1


def test_build_window_custom_size():
    """Tests a window with a custom before=1, after=1 size."""
    target_span = (90, 94)  # A finding in sentence 4
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=1, target_span=target_span, before=1, after=1)

    # Expects sentence 4, plus 1 before (3) and 1 after (5)
    assert result["text"] == "This is the third sentence. This is the fourth sentence. This is the fifth sentence."
    assert result["sentence_indices"] == [2, 3, 4]
    assert result["page"] == 1


def test_build_window_span_between_sentences():
    """Tests a span that falls between two sentences, which should anchor to the next one."""
    target_span = (83, 84)  # A span between sentences 3 and 4
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=1, target_span=target_span)

    # The logic finds the sentence containing the start_char (sentence 3, index 2).
    # The window is built around index 2, resulting in indices [0, 1, 2, 3, 4].
    assert result["text"] == "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence. This is the fifth sentence."
    assert result["sentence_indices"] == [0, 1, 2, 3, 4]


def test_build_window_no_page_leakage():
    """Ensures the window builder only considers sentences from the target page."""
    target_span = (5, 10)  # A finding on page 2
    result = build_window_legacy(SAMPLE_SENTENCES, target_page=2, target_span=target_span)

    # Expects only the single sentence from page 2
    assert result["text"] == "A sentence on page 2."
    assert result["sentence_indices"] == [0] # Index is relative to the page's sentences
    assert result["page"] == 2
