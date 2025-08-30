from __future__ import annotations

from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple, Literal
from dataclasses import dataclass
from enum import Enum

from .rulepack_loader import load_rulepack


class IndustryType(str, Enum):
    """Supported industry types for weak language analysis."""
    GENERAL = "general"
    LEGAL = "legal"
    TECHNICAL = "technical"
    BUSINESS = "business"


@dataclass
class WeakTerm:
    """Represents a weak language term with confidence and metadata."""
    term: str
    confidence: float
    category: str

    def __post_init__(self):
        if not isinstance(self.term, str):
            self.term = str(self.term)
        if not isinstance(self.confidence, (int, float)):
            self.confidence = float(self.confidence or 0.5)
        if not isinstance(self.category, str):
            self.category = str(self.category or "unknown")


@lru_cache(maxsize=1)
def get_weak_terms() -> List[str]:
    """Return normalized weak-language terms from the bundled lexicon.

    Loads rulepack and fetches the 'weak_language' lexicon terms. Returns
    lowercase, stripped terms suitable for exact term matching.
    """
    rp = load_rulepack()
    lx = rp.lexicons.get("weak_language") if rp and rp.lexicons else None
    if not lx or not lx.terms:
        return []

    terms = []
    for item in lx.terms:
        if isinstance(item, dict):
            term = item.get("term", "").strip().lower()
            if term:
                terms.append(term)
        elif isinstance(item, str):
            term = item.strip().lower()
            if term:
                terms.append(term)
    return terms


@lru_cache(maxsize=4)
def get_weak_terms_by_industry(industry: IndustryType = IndustryType.GENERAL) -> List[str]:
    """Return normalized weak-language terms for a specific industry.

    Loads rulepack and fetches the appropriate lexicon based on industry type.
    """
    rp = load_rulepack()
    if not rp or not rp.lexicons:
        return []

    # Map industry types to lexicon names
    lexicon_map = {
        IndustryType.GENERAL: "weak_language",
        IndustryType.LEGAL: "legal_weak_language",
        IndustryType.TECHNICAL: "technical_weak_language",
        IndustryType.BUSINESS: "business_weak_language"
    }

    lexicon_name = lexicon_map[industry]
    lx = rp.lexicons.get(lexicon_name)
    if not lx or not lx.terms:
        # Fallback to general lexicon if specific one not found
        if industry != IndustryType.GENERAL:
            return get_weak_terms_by_industry(IndustryType.GENERAL)
        return []

    terms = []
    for item in lx.terms:
        if isinstance(item, dict):
            term = item.get("term", "").strip().lower()
            if term:
                terms.append(term)
        elif isinstance(item, str):
            term = item.strip().lower()
            if term:
                terms.append(term)
    return terms


@lru_cache(maxsize=1)
def get_weak_terms_with_metadata() -> List[WeakTerm]:
    """Return weak language terms with confidence scores and categories."""
    rp = load_rulepack()
    lx = rp.lexicons.get("weak_language") if rp and rp.lexicons else None
    if not lx or not lx.terms:
        return []

    weak_terms = []
    for item in lx.terms:
        if isinstance(item, dict):
            term = item.get("term", "").strip()
            if term:
                weak_term = WeakTerm(
                    term=term.lower(),
                    confidence=item.get("confidence", 0.5),
                    category=item.get("category", "unknown")
                )
                weak_terms.append(weak_term)
        elif isinstance(item, str):
            term = item.strip()
            if term:
                weak_term = WeakTerm(
                    term=term.lower(),
                    confidence=0.8,  # Default confidence for legacy terms
                    category="legacy"
                )
                weak_terms.append(weak_term)
    return weak_terms


@lru_cache(maxsize=4)
def get_weak_terms_with_metadata_by_industry(industry: IndustryType = IndustryType.GENERAL) -> List[WeakTerm]:
    """Return weak language terms with confidence scores and categories for a specific industry."""
    rp = load_rulepack()
    if not rp or not rp.lexicons:
        return []

    # Map industry types to lexicon names
    lexicon_map = {
        IndustryType.GENERAL: "weak_language",
        IndustryType.LEGAL: "legal_weak_language",
        IndustryType.TECHNICAL: "technical_weak_language",
        IndustryType.BUSINESS: "business_weak_language"
    }

    lexicon_name = lexicon_map[industry]
    lx = rp.lexicons.get(lexicon_name)
    if not lx or not lx.terms:
        # Fallback to general lexicon if specific one not found
        if industry != IndustryType.GENERAL:
            return get_weak_terms_with_metadata_by_industry(IndustryType.GENERAL)
        return []

    weak_terms = []
    for item in lx.terms:
        if isinstance(item, dict):
            term = item.get("term", "").strip()
            if term:
                weak_term = WeakTerm(
                    term=term.lower(),
                    confidence=item.get("confidence", 0.5),
                    category=item.get("category", "unknown")
                )
                weak_terms.append(weak_term)
        elif isinstance(item, str):
            term = item.strip()
            if term:
                weak_term = WeakTerm(
                    term=term.lower(),
                    confidence=0.8,  # Default confidence for legacy terms
                    category="legacy"
                )
                weak_terms.append(weak_term)
    return weak_terms


@lru_cache(maxsize=1)
def get_counter_anchors() -> List[str]:
    """Return counter-anchor terms that prevent weak language downgrades from all lexicons."""
    rp = load_rulepack()
    if not rp or not rp.lexicons:
        return []

    counter_anchors = set()  # Use set to avoid duplicates

    # Load base weak language lexicon counter-anchors
    base_lx = rp.lexicons.get("weak_language")
    if base_lx and hasattr(base_lx, 'counter_anchors') and base_lx.counter_anchors:
        for anchor in base_lx.counter_anchors:
            anchor_str = str(anchor).strip().lower()
            if anchor_str:
                counter_anchors.add(anchor_str)

    # Load industry-specific lexicon counter-anchors
    industry_lexicons = [
        "weak_language_legal",
        "weak_language_technical",
        "weak_language_business"
    ]

    for lexicon_name in industry_lexicons:
        lx = rp.lexicons.get(lexicon_name)
        if lx and hasattr(lx, 'counter_anchors') and lx.counter_anchors:
            for anchor in lx.counter_anchors:
                anchor_str = str(anchor).strip().lower()
                if anchor_str:
                    counter_anchors.add(anchor_str)

    return list(counter_anchors)


@lru_cache(maxsize=4)
def get_counter_anchors_by_industry(industry: IndustryType = IndustryType.GENERAL) -> List[str]:
    """Return counter-anchor terms for a specific industry that prevent weak language downgrades."""
    rp = load_rulepack()
    if not rp or not rp.lexicons:
        return []

    # Map industry types to lexicon names
    lexicon_map = {
        IndustryType.GENERAL: "weak_language",
        IndustryType.LEGAL: "legal_weak_language",
        IndustryType.TECHNICAL: "technical_weak_language",
        IndustryType.BUSINESS: "business_weak_language"
    }

    lexicon_name = lexicon_map[industry]
    lx = rp.lexicons.get(lexicon_name)
    if not lx or not hasattr(lx, 'counter_anchors') or not lx.counter_anchors:
        # Fallback to general lexicon if specific one not found
        if industry != IndustryType.GENERAL:
            return get_counter_anchors_by_industry(IndustryType.GENERAL)
        return []

    return [str(anchor).strip().lower() for anchor in lx.counter_anchors if str(anchor).strip()]


def calculate_weak_confidence(text: str, weak_terms: List[WeakTerm]) -> Tuple[bool, float, Optional[str]]:
    """Calculate if text contains weak language and return confidence score and category.

    Enhanced logic considers:
    - Multiple weak terms with confidence aggregation
    - Proximity to counter-anchors
    - Term frequency and density
    - Context-based confidence adjustment

    Returns:
        (has_weak_language: bool, confidence_score: float, category: str)
    """
    text_lower = text.lower()
    found_terms = []

    # Find all weak terms present in the text
    for weak_term in weak_terms:
        if weak_term.term in text_lower:
            found_terms.append(weak_term)

    if not found_terms:
        return False, 0.0, None

    # Calculate base confidence from highest scoring term
    max_confidence = max(term.confidence for term in found_terms)
    best_category = next(term.category for term in found_terms
                        if term.confidence == max_confidence)

    # Apply confidence adjustments based on multiple factors
    adjusted_confidence = _adjust_confidence_for_context(text_lower, found_terms, max_confidence)

    # Apply density bonus for multiple weak terms
    if len(found_terms) > 1:
        density_bonus = min(0.1, len(found_terms) * 0.02)  # Max 10% bonus
        adjusted_confidence = min(1.0, adjusted_confidence + density_bonus)

    has_weak = adjusted_confidence > 0.0
    return has_weak, adjusted_confidence, best_category


def _adjust_confidence_for_context(text: str, found_terms: List[WeakTerm], base_confidence: float) -> float:
    """Adjust confidence based on contextual factors."""
    confidence = base_confidence

    # Check for proximity to counter-anchors (within same sentence)
    counter_anchors = get_counter_anchors()
    sentences = text.split('.')

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        if sentence_lower:
            has_weak_in_sentence = any(term.term in sentence_lower for term in found_terms)
            has_anchor_in_sentence = any(anchor in sentence_lower for anchor in counter_anchors)

            # If weak term and counter-anchor are in same sentence, reduce confidence
            if has_weak_in_sentence and has_anchor_in_sentence:
                # Reduce confidence by 20-40% depending on anchor proximity
                anchor_positions = [sentence_lower.find(anchor) for anchor in counter_anchors
                                  if anchor in sentence_lower]
                weak_positions = [sentence_lower.find(term.term) for term in found_terms
                                if term.term in sentence_lower]

                if anchor_positions and weak_positions:
                    min_distance = min(abs(wp - ap) for wp in weak_positions for ap in anchor_positions)
                    # Closer proximity = greater reduction
                    proximity_reduction = 0.2 if min_distance < 50 else 0.1
                    confidence *= (1 - proximity_reduction)

    # Check for industry-specific context adjustments
    if any(term.category and 'legal' in term.category for term in found_terms):
        # Legal terms might be less weak in legal contexts
        confidence *= 0.9

    if any(term.category and 'technical' in term.category for term in found_terms):
        # Technical terms might be acceptable in technical specs
        confidence *= 0.85

    return max(0.0, min(1.0, confidence))


def get_terms_by_confidence_threshold(min_confidence: float = 0.5) -> List[str]:
    """Get weak terms that meet or exceed the minimum confidence threshold."""
    weak_terms = get_weak_terms_with_metadata()
    return [wt.term for wt in weak_terms if wt.confidence >= min_confidence]



    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        if sentence_lower:
            has_weak_in_sentence = any(term.term in sentence_lower for term in found_terms)
            has_anchor_in_sentence = any(anchor in sentence_lower for anchor in counter_anchors)

            # If weak term and counter-anchor are in same sentence, reduce confidence
            if has_weak_in_sentence and has_anchor_in_sentence:
                # Reduce confidence by 20-40% depending on anchor proximity
                anchor_positions = [sentence_lower.find(anchor) for anchor in counter_anchors
                                  if anchor in sentence_lower]
                weak_positions = [sentence_lower.find(term.term) for term in found_terms
                                if term.term in sentence_lower]

                if anchor_positions and weak_positions:
                    min_distance = min(abs(wp - ap) for wp in weak_positions for ap in anchor_positions)
                    # Closer proximity = greater reduction
                    proximity_reduction = 0.2 if min_distance < 50 else 0.1
                    confidence *= (1 - proximity_reduction)

    # Check for industry-specific context adjustments
    if any(term.category and 'legal' in term.category for term in found_terms):
        # Legal terms might be less weak in legal contexts
        confidence *= 0.9

    if any(term.category and 'technical' in term.category for term in found_terms):
        # Technical terms might be acceptable in technical specs
        confidence *= 0.85

    return max(0.0, min(1.0, confidence))


def get_terms_by_confidence_threshold(min_confidence: float = 0.5) -> List[str]:
    """Get weak terms that meet or exceed the minimum confidence threshold."""
    weak_terms = get_weak_terms_with_metadata()
    return [wt.term for wt in weak_terms if wt.confidence >= min_confidence]

