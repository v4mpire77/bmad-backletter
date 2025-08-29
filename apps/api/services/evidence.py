from typing import List, Tuple

def build_evidence_window(sentence_index: List[Tuple[int, int]], anchor_index: int, window_size: int) -> List[Tuple[int, int]]:
    """
    Builds an evidence window of +/- N sentences around a given anchor sentence.

    Args:
        sentence_index: A list of tuples, where each tuple is (start_offset, end_offset) for a sentence.
        anchor_index: The index of the anchor sentence in the sentence_index.
        window_size: The number of sentences to include before and after the anchor sentence.

    Returns:
        A new sentence index for the evidence window.
    """
    start = max(0, anchor_index - window_size)
    end = min(len(sentence_index), anchor_index + window_size + 1)
    return sentence_index[start:end]
