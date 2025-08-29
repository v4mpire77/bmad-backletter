import pytest
from blackletter_api.services.evidence import build_window, EvidenceWindow

# Test data from the specification
TEXT = (
    "S1. Controllers give documented instructions. "
    "S2. Processor ensures confidentiality of authorised persons. "
    "S3. The parties shall implement technical and organisational measures (Art. 32). "
    "S4. Sub-processors require prior authorisation and flow-down equivalence. "
    "S5. Processor shall assist with data subject rights (Arts. 12–23). "
    "S6. Processor shall notify without undue delay of a personal data breach. "
)

# Build sentence boundaries by the 'S#. ' markers for the test
SENTS = []
pos = 0
for tok in ["S1. ", "S2. ", "S3. ", "S4. ", "S5. ", "S6. "]:
    start = TEXT.find(tok, pos)
    end = TEXT.find(". ", start) + 2 if TEXT.find(". ", start) != -1 else len(TEXT)
    # extend to next marker or end
    next_pos = TEXT.find("S", end)
    end = next_pos if next_pos != -1 else len(TEXT)
    SENTS.append((start, end))
    pos = end


class TestEvidenceWindowBuilderSpec:
    """Test suite for Story 1.3: Evidence Window Builder (spec compliant)."""
    
    def test_mid_doc_default_window(self):
        """span inside S3 → window should include S1..S5 (±2 around S3)"""
        s3 = SENTS[2]
        w = build_window(
            full_text=TEXT, 
            sentences=SENTS, 
            span_start=s3[0] + 10, 
            span_end=s3[0] + 20
        )
        assert w.start == SENTS[0][0]
        assert w.end == SENTS[4][1]
        assert "organisational measures" in w.text

    def test_boundary_head_clamped(self):
        """span inside S1 → clamp left boundary"""
        s1 = SENTS[0]
        w = build_window(
            full_text=TEXT, 
            sentences=SENTS, 
            span_start=s1[0] + 2, 
            span_end=s1[0] + 5
        )
        assert w.start == SENTS[0][0]
        assert w.end == SENTS[2][1]

    def test_boundary_tail_clamped(self):
        """span inside S6 → clamp right boundary"""
        s6 = SENTS[-1]
        w = build_window(
            full_text=TEXT, 
            sentences=SENTS, 
            span_start=s6[0] + 2, 
            span_end=s6[0] + 5
        )
        assert w.start == SENTS[3][0]
        assert w.end == SENTS[-1][1]

    def test_per_detector_override(self):
        """±3 around S4 → S1..S6"""
        s4 = SENTS[3]
        cfg = {"A28_3_c_security": 3}
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s4[0] + 1,
            span_end=s4[0] + 2,
            detector_id="A28_3_c_security",
            per_detector_windows=cfg,
        )
        # ±3 around S4 → S1..S6
        assert w.start == SENTS[0][0]
        assert w.end == SENTS[-1][1]

    def test_malformed_sentences_graceful(self):
        """Test graceful handling of malformed sentence data"""
        bad = [(None, None), SENTS[2], (None, None)]
        s3 = SENTS[2]
        w = build_window(
            full_text=TEXT, 
            sentences=bad, 
            span_start=s3[0] + 1, 
            span_end=s3[0] + 2
        )
        assert "organisational measures" in w.text

    def test_no_sentence_index_fallback(self):
        """No sentences → +/- 200 char clamp around span"""
        s2 = SENTS[1]
        w = build_window(
            full_text=TEXT, 
            sentences=None, 
            span_start=s2[0] + 3, 
            span_end=s2[0] + 10
        )
        assert w.text and w.start <= s2[0] and w.end >= s2[1]

    def test_evidence_window_class(self):
        """Test EvidenceWindow class functionality"""
        window = EvidenceWindow("test text", 10, 20)
        assert window.text == "test text"
        assert window.start == 10
        assert window.end == 20
        
        result_dict = window.dict()
        assert result_dict == {"text": "test text", "start": 10, "end": 20}

    def test_span_order_normalization(self):
        """Test that span_start > span_end gets normalized"""
        s3 = SENTS[2]
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s3[0] + 20,  # end first
            span_end=s3[0] + 10,    # start second
        )
        assert "organisational measures" in w.text

    def test_default_window_parameter(self):
        """Test custom default window size"""
        s3 = SENTS[2]
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s3[0] + 10,
            span_end=s3[0] + 20,
            default_window=1,  # ±1 instead of ±2
        )
        # Should include S2, S3, S4 (±1 around S3)
        assert w.start == SENTS[1][0]
        assert w.end == SENTS[3][1]

    def test_invalid_detector_config(self):
        """Test that invalid detector config falls back to default"""
        s3 = SENTS[2]
        cfg = {"A28_3_c_security": "invalid"}  # Invalid type
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s3[0] + 10,
            span_end=s3[0] + 20,
            detector_id="A28_3_c_security",
            per_detector_windows=cfg,
            default_window=1,
        )
        # Should use default_window=1, not the invalid config
        assert w.start == SENTS[1][0]
        assert w.end == SENTS[3][1]

    def test_default_window_zero(self):
        """default_window=0 should return only the containing sentence."""
        s4 = SENTS[3]
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s4[0] + 5,
            span_end=s4[0] + 10,
            default_window=0,
        )
        assert w.start == SENTS[3][0]
        assert w.end == SENTS[3][1]

    def test_empty_sentences_list_fallback(self):
        """Empty sentences list should fallback similarly to None index."""
        s2 = SENTS[1]
        w = build_window(
            full_text=TEXT,
            sentences=[],
            span_start=s2[0] + 1,
            span_end=s2[0] + 5,
        )
        assert w.text and w.start <= s2[0] and w.end >= s2[1]

    def test_between_sentences_chooses_nearest(self):
        """Span strictly between sentences ? choose nearest (ties prefer previous)."""
        # Construct a tiny text with a gap between sentences to force 'between' logic
        TEXT2 = "aaaaa     bbbbb"  # 5 'a', 5 spaces gap, 5 'b'
        SENTS2 = [(0, 5), (10, 15)]
        # Span at 7 is 2 chars from prev end (5) and 3 from next start (10) ? pick previous
        w = build_window(
            full_text=TEXT2,
            sentences=SENTS2,
            span_start=7,
            span_end=7,
            default_window=0,
        )
        assert w.start == 0
        assert w.end == 5
        assert w.text == "aaaaa"

    def test_span_strictly_before_first_selects_first(self):
        """Span before first sentence ? select first; default_window=0 isolates it."""
        s1 = SENTS[0]
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=s1[0] - 10,
            span_end=s1[0] - 10,
            default_window=0,
        )
        assert w.start == s1[0]
        assert w.end == s1[1]

    def test_span_strictly_after_last_selects_last(self):
        """Span after last sentence ? select last; default_window=0 isolates it."""
        sl = SENTS[-1]
        w = build_window(
            full_text=TEXT,
            sentences=SENTS,
            span_start=sl[1] + 10,
            span_end=sl[1] + 10,
            default_window=0,
        )
        assert w.start == sl[0]
        assert w.end == sl[1]



