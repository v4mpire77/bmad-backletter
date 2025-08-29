import pytest
from blackletter_api.services.evidence import build_window, build_configurable_window


class TestEvidenceWindowBuilder:
    """Test suite for Story 1.3: Evidence Window Builder functionality."""
    
    def setup_method(self):
        """Setup common test data for evidence window tests."""
        # Sample sentences for a multi-page document
        self.sentences = [
            # Page 1 sentences
            {"page": 1, "start": 0, "end": 50, "text": "This is the first sentence of page one."},
            {"page": 1, "start": 51, "end": 95, "text": "This is the second sentence of page one."},
            {"page": 1, "start": 96, "end": 140, "text": "This is the third sentence of page one."},
            {"page": 1, "start": 141, "end": 185, "text": "This is the fourth sentence of page one."},
            {"page": 1, "start": 186, "end": 230, "text": "This is the fifth sentence of page one."},
            
            # Page 2 sentences  
            {"page": 2, "start": 250, "end": 295, "text": "This is the first sentence of page two."},
            {"page": 2, "start": 296, "end": 340, "text": "This is the second sentence of page two."},
            {"page": 2, "start": 341, "end": 385, "text": "This is the third sentence of page two."},
        ]
    
    def test_basic_window_middle_sentence(self):
        """Test building window around a middle sentence with default ±2 window."""
        # Target the third sentence of page 1 (index 2)
        target_span = (100, 120)  # Within third sentence
        
        result = build_window(self.sentences, target_page=1, target_span=target_span)
        
        assert result["page"] == 1
        assert result["text"] == "This is the first sentence of page one. This is the second sentence of page one. This is the third sentence of page one. This is the fourth sentence of page one. This is the fifth sentence of page one."
        assert result["sentence_indices"] == [0, 1, 2, 3, 4]  # All 5 sentences (2 before + target + 2 after)
        assert result["target_sentence_idx"] == 2
        assert result["window_size"] == {"before": 2, "after": 2}
    
    def test_window_at_document_start(self):
        """Test window at the beginning of document - should not go negative."""
        # Target the first sentence
        target_span = (10, 30)  # Within first sentence
        
        result = build_window(self.sentences, target_page=1, target_span=target_span)
        
        assert result["page"] == 1
        # Should include sentences 0, 1, 2 (can't go before 0)
        assert result["sentence_indices"] == [0, 1, 2]
        assert result["target_sentence_idx"] == 0
        assert "first sentence" in result["text"]
        assert "second sentence" in result["text"]
        assert "third sentence" in result["text"]
    
    def test_window_at_document_end(self):
        """Test window at the end of document - should not exceed available sentences."""
        # Target the last sentence of page 1
        target_span = (200, 220)  # Within fifth sentence
        
        result = build_window(self.sentences, target_page=1, target_span=target_span)
        
        assert result["page"] == 1
        # Should include sentences 2, 3, 4 (can't go beyond index 4)
        assert result["sentence_indices"] == [2, 3, 4]
        assert result["target_sentence_idx"] == 4
        assert "third sentence" in result["text"]
        assert "fourth sentence" in result["text"] 
        assert "fifth sentence" in result["text"]
    
    def test_window_respects_page_boundaries(self):
        """Test that window does not cross page boundaries."""
        # Target a sentence on page 2
        target_span = (300, 320)  # Within second sentence of page 2
        
        result = build_window(self.sentences, target_page=2, target_span=target_span)
        
        assert result["page"] == 2
        # Should only include page 2 sentences, not page 1
        assert all("page two" in sent_text for sent_text in result["text"].split(". "))
        assert "page one" not in result["text"]
        assert result["sentence_indices"] == [0, 1, 2]  # All 3 sentences of page 2
    
    def test_window_with_custom_size(self):
        """Test window with custom before/after sizes."""
        # Target middle sentence with larger window
        target_span = (100, 120)  # Third sentence
        
        result = build_window(self.sentences, target_page=1, target_span=target_span, before=1, after=1)
        
        assert result["page"] == 1
        assert result["sentence_indices"] == [1, 2, 3]  # 1 before + target + 1 after
        assert result["window_size"] == {"before": 1, "after": 1}
        assert "second sentence" in result["text"]
        assert "third sentence" in result["text"]
        assert "fourth sentence" in result["text"]
    
    def test_window_with_zero_size(self):
        """Test window with zero before/after - should return only target sentence."""
        target_span = (100, 120)  # Third sentence
        
        result = build_window(self.sentences, target_page=1, target_span=target_span, before=0, after=0)
        
        assert result["page"] == 1
        assert result["sentence_indices"] == [2]  # Only target sentence
        assert result["text"] == "This is the third sentence of page one."
        assert result["target_sentence_idx"] == 2
    
    def test_window_empty_page(self):
        """Test window for non-existent page."""
        target_span = (100, 120)
        
        result = build_window(self.sentences, target_page=99, target_span=target_span)
        
        assert result["page"] == 99
        assert result["text"] == ""
        assert result["sentence_indices"] == []
        assert result["start"] == 0
        assert result["end"] == 0
    
    def test_window_span_between_sentences(self):
        """Test window when target span falls between sentences."""
        # Target span between sentences
        target_span = (235, 245)  # Between 5th sentence of page 1 and 1st of page 2
        
        result = build_window(self.sentences, target_page=1, target_span=target_span)
        
        assert result["page"] == 1
        # Should find the last sentence as nearest
        assert result["target_sentence_idx"] == 4
        assert "fifth sentence" in result["text"]
    
    def test_window_overlapping_span(self):
        """Test window when target span overlaps multiple sentences."""
        # Span that crosses sentence boundaries  
        target_span = (180, 260)  # Overlaps 5th sentence of page 1 (starts at 186)
        
        result = build_window(self.sentences, target_page=1, target_span=target_span)
        
        assert result["page"] == 1
        # The span (180, 260) should find the 4th sentence (141-185) which contains 180
        assert result["target_sentence_idx"] == 3  # 4th sentence (0-indexed)
    
    def test_configurable_window_with_detector_config(self):
        """Test configurable window with detector-specific configuration."""
        detector_config = {
            "window": {
                "before": 3,
                "after": 1
            }
        }
        
        target_span = (100, 120)  # Third sentence
        
        result = build_configurable_window(
            self.sentences, 
            target_page=1, 
            target_span=target_span,
            detector_config=detector_config
        )
        
        assert result["window_size"] == {"before": 3, "after": 1}
        assert result["sentence_indices"] == [0, 1, 2, 3]  # 3 before + target + 1 after (capped by available)
    
    def test_configurable_window_with_bounds_capping(self):
        """Test that configurable window caps excessive window sizes."""
        detector_config = {
            "window": {
                "before": 50,  # Excessive
                "after": 50    # Excessive  
            }
        }
        
        target_span = (100, 120)
        
        result = build_configurable_window(
            self.sentences,
            target_page=1,
            target_span=target_span,
            detector_config=detector_config
        )
        
        # Should be capped at 10 sentences each
        assert result["window_size"]["before"] == 10
        assert result["window_size"]["after"] == 10
    
    def test_configurable_window_with_defaults(self):
        """Test configurable window falls back to defaults when no config provided."""
        result = build_configurable_window(
            self.sentences,
            target_page=1,
            target_span=(100, 120),
            detector_config=None,
            default_window_size=3
        )
        
        assert result["window_size"] == {"before": 3, "after": 3}
    
    def test_configurable_window_with_partial_config(self):
        """Test configurable window with partial detector configuration."""
        detector_config = {
            "window": {
                "before": 1
                # "after" missing - should use default
            }
        }
        
        result = build_configurable_window(
            self.sentences,
            target_page=1,
            target_span=(100, 120),
            detector_config=detector_config,
            default_window_size=2
        )
        
        assert result["window_size"]["before"] == 1
        assert result["window_size"]["after"] == 2  # Should use default
    
    def test_window_with_malformed_sentences(self):
        """Test window builder handles malformed sentence data gracefully."""
        malformed_sentences = [
            {"page": 1, "start": 0, "end": 50},  # Missing "text"
            {"page": 1, "text": "Complete sentence"},  # Missing start/end
            {"page": 1, "start": 100, "end": 150, "text": "Valid sentence"},
        ]
        
        # Should not crash, but may have unexpected behavior
        result = build_window(malformed_sentences, target_page=1, target_span=(120, 130))
        
        # Should return some result without crashing
        assert result["page"] == 1
        assert isinstance(result["text"], str)
        assert isinstance(result["sentence_indices"], list)

