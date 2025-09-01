"""
Citations module for Blackletter Systems.

This module provides functionality for handling legal citations:
- Extract citations from text
- Format citations properly
- Validate citation references

Usage:
    from app.core.citations import extract_citations, format_citation
    
    # Extract citations from text
    citations = extract_citations("As stated in Smith v. Jones [2020] UKSC 1, paragraph 15...")
    
    # Format a citation
    formatted = format_citation(case_id="Smith v. Jones", year="2020", court="UKSC", number="1")
"""

import re
from typing import Dict, List, Optional, Tuple, Union, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Regular expressions for citation extraction
UK_CASE_PATTERN = r"([A-Za-z\s\-']+)\s+v\.?\s+([A-Za-z\s\-']+)\s+\[?(\d{4})\]?\s+([A-Z]+)\s+(\d+)"
UK_STATUTE_PATTERN = r"([A-Za-z\s]+)\s+Act\s+(\d{4}),?\s+(?:section|s\.?)\s+(\d+)"
EU_CASE_PATTERN = r"Case\s+(?:No\.\s+)?([CT]-\d+/\d+)\s+([A-Za-z\s\-']+)\s+v\.?\s+([A-Za-z\s\-']+)"
PARAGRAPH_PATTERN = r"(?:paragraph|para\.?|p\.?)\s+(\d+)"

class Citation:
    """Represents a legal citation"""
    def __init__(
        self,
        text: str,
        case_id: str,
        para: Optional[int] = None,
        year: Optional[str] = None,
        court: Optional[str] = None,
        number: Optional[str] = None,
        source_type: str = "case",
        source_id: Optional[str] = None
    ):
        self.text = text
        self.case_id = case_id
        self.para = para
        self.year = year
        self.court = court
        self.number = number
        self.source_type = source_type
        self.source_id = source_id

def extract_citations(text: str) -> List[Citation]:
    """
    Extract legal citations from text.
    
    Args:
        text: The text to extract citations from
        
    Returns:
        List[Citation]: List of extracted citations
    """
    citations = []
    
    # Extract UK case citations
    uk_case_matches = re.finditer(UK_CASE_PATTERN, text)
    for match in uk_case_matches:
        claimant, defendant, year, court, number = match.groups()
        case_id = f"{claimant.strip()} v {defendant.strip()}"
        
        # Look for paragraph references
        citation_text = match.group(0)
        para_match = re.search(PARAGRAPH_PATTERN, text[match.end():match.end() + 50])
        para = int(para_match.group(1)) if para_match else None
        
        if para:
            citation_text += f" {para_match.group(0)}"
        
        citations.append(Citation(
            text=citation_text,
            case_id=case_id,
            para=para,
            year=year,
            court=court,
            number=number,
            source_type="case"
        ))
    
    # Extract UK statute citations
    statute_matches = re.finditer(UK_STATUTE_PATTERN, text)
    for match in statute_matches:
        name, year, section = match.groups()
        case_id = f"{name.strip()} Act {year}"
        
        citations.append(Citation(
            text=match.group(0),
            case_id=case_id,
            para=int(section),
            year=year,
            source_type="statute"
        ))
    
    # Extract EU case citations
    eu_case_matches = re.finditer(EU_CASE_PATTERN, text)
    for match in eu_case_matches:
        case_number, claimant, defendant = match.groups()
        case_id = f"{claimant.strip()} v {defendant.strip()}"
        
        # Look for paragraph references
        citation_text = match.group(0)
        para_match = re.search(PARAGRAPH_PATTERN, text[match.end():match.end() + 50])
        para = int(para_match.group(1)) if para_match else None
        
        if para:
            citation_text += f" {para_match.group(0)}"
        
        citations.append(Citation(
            text=citation_text,
            case_id=case_id,
            para=para,
            number=case_number,
            source_type="eu_case"
        ))
    
    return citations

def format_citation(
    case_id: str,
    year: Optional[str] = None,
    court: Optional[str] = None,
    number: Optional[str] = None,
    para: Optional[int] = None,
    source_type: str = "case"
) -> str:
    """
    Format a legal citation.
    
    Args:
        case_id: The case identifier
        year: The year of the case
        court: The court abbreviation
        number: The case number
        para: The paragraph number
        source_type: The type of source (case, statute, eu_case)
        
    Returns:
        str: The formatted citation
    """
    if source_type == "case":
        citation = f"{case_id}"
        
        if year and court and number:
            citation += f" [{year}] {court} {number}"
        
        if para:
            citation += f", paragraph {para}"
    
    elif source_type == "statute":
        citation = f"{case_id}"
        
        if para:
            citation += f", section {para}"
    
    elif source_type == "eu_case":
        citation = f"Case {number} {case_id}"
        
        if para:
            citation += f", paragraph {para}"
    
    else:
        citation = case_id
    
    return citation

def validate_citations(
    citations: List[Dict[str, Any]],
    known_sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Validate citations against known sources.
    
    Args:
        citations: List of citation dictionaries
        known_sources: List of known source dictionaries
        
    Returns:
        List[Dict[str, Any]]: List of validated citations with additional metadata
    """
    validated_citations = []
    
    for citation in citations:
        # Convert dictionary to Citation object if needed
        if not isinstance(citation, Citation):
            citation = Citation(**citation)
        
        # Look for matching source
        matching_source = None
        for source in known_sources:
            if citation.case_id.lower() in source.get("title", "").lower():
                matching_source = source
                break
        
        # Create validated citation
        validated = {
            "text": citation.text,
            "case_id": citation.case_id,
            "para": citation.para,
            "year": citation.year,
            "court": citation.court,
            "number": citation.number,
            "source_type": citation.source_type,
            "valid": matching_source is not None
        }
        
        # Add source information if found
        if matching_source:
            validated["source_id"] = matching_source.get("id")
            validated["source_url"] = matching_source.get("url")
        
        validated_citations.append(validated)
    
    return validated_citations
