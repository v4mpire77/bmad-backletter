"""
OCR module for Blackletter Systems.

This module provides functionality for extracting text from PDF documents using:
- pdfplumber for direct text extraction
- pytesseract for OCR when needed

Usage:
    from app.core.ocr import extract_text, extract_text_with_locations
    
    # Extract plain text from a PDF
    text = extract_text("path/to/document.pdf")
    
    # Extract text with page and position information
    text_with_locations = extract_text_with_locations("path/to/document.pdf")
"""

import os
import io
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from dataclasses import dataclass

import pdfplumber
from pypdf import PdfReader
import pytesseract
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TextSpan:
    """Text span with location information"""
    text: str
    page_num: int
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x0, y0, x1, y1)
    confidence: Optional[float] = None

def _is_scanned_page(page: Any) -> bool:
    """
    Check if a page is likely scanned (has few or no text elements).
    
    Args:
        page: A pdfplumber page object
        
    Returns:
        bool: True if the page is likely scanned, False otherwise
    """
    # Extract text from the page
    text = page.extract_text()
    
    # If there's very little text, it's likely a scanned page
    if not text or len(text.strip()) < 50:
        return True
    
    return False

def _process_with_tesseract(image: Image.Image, dpi: int = 300) -> Tuple[str, float]:
    """
    Process an image with Tesseract OCR.
    
    Args:
        image: PIL Image object
        dpi: DPI for image processing (higher can improve accuracy)
        
    Returns:
        Tuple[str, float]: Extracted text and confidence score
    """
    # Convert to higher DPI if needed
    if hasattr(image, 'info') and image.info.get('dpi', (72, 72))[0] < dpi:
        scale_factor = dpi / image.info.get('dpi', (72, 72))[0]
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        image = image.resize(new_size, Image.LANCZOS)
    
    # Use Tesseract to extract text with confidence data
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Combine text and calculate average confidence
    text_parts = []
    confidence_values = []
    
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            text_parts.append(data['text'][i])
            confidence_values.append(float(data['conf'][i]))
    
    text = ' '.join(text_parts)
    avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0
    
    return text, avg_confidence

def extract_text(file_path_or_bytes: Union[str, bytes, io.BytesIO]) -> str:
    """
    Extract text from a PDF document using pdfplumber and pytesseract as needed.
    
    Args:
        file_path_or_bytes: Path to PDF file or PDF bytes
        
    Returns:
        str: Extracted text content
    """
    text_parts = []
    
    try:
        # Open the PDF file
        with pdfplumber.open(file_path_or_bytes) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                logger.info(f"Processing page {page_num} of {len(pdf.pages)}")
                
                # Try direct text extraction first
                page_text = page.extract_text()
                
                # If little or no text is extracted, it might be a scanned page
                if _is_scanned_page(page):
                    logger.info(f"Page {page_num} appears to be scanned, using OCR")
                    # Convert page to image and use OCR
                    img = page.to_image(resolution=300)
                    ocr_text, confidence = _process_with_tesseract(img.original)
                    logger.info(f"OCR confidence: {confidence:.2f}")
                    text_parts.append(ocr_text)
                else:
                    text_parts.append(page_text)
    
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        # Fallback to pypdf for basic extraction
        try:
            logger.info("Falling back to pypdf for text extraction")
            reader = PdfReader(file_path_or_bytes)
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
        except Exception as fallback_error:
            logger.error(f"Fallback extraction failed: {str(fallback_error)}")
            raise
    
    return "\n\n".join(text_parts)

def extract_text_with_locations(
    file_path_or_bytes: Union[str, bytes, io.BytesIO]
) -> List[TextSpan]:
    """
    Extract text from a PDF document with location information.
    
    Args:
        file_path_or_bytes: Path to PDF file or PDF bytes
        
    Returns:
        List[TextSpan]: List of text spans with location information
    """
    spans = []
    
    try:
        # Open the PDF file
        with pdfplumber.open(file_path_or_bytes) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                logger.info(f"Processing page {page_num} of {len(pdf.pages)}")
                
                # Check if it's a scanned page
                if _is_scanned_page(page):
                    logger.info(f"Page {page_num} appears to be scanned, using OCR")
                    # Convert page to image and use OCR
                    img = page.to_image(resolution=300)
                    ocr_text, confidence = _process_with_tesseract(img.original)
                    
                    # Create a span for the whole page since we don't have precise coordinates
                    spans.append(TextSpan(
                        text=ocr_text,
                        page_num=page_num,
                        bbox=(0, 0, page.width, page.height),
                        confidence=confidence
                    ))
                else:
                    # Extract text with character information
                    words = page.extract_words()
                    
                    # Group words into paragraphs based on y-position
                    if words:
                        y_threshold = 3  # Threshold for considering words on the same line
                        current_y = words[0]['top']
                        current_line = []
                        
                        for word in words:
                            # If the word is on a new line
                            if abs(word['top'] - current_y) > y_threshold:
                                # Save the current line
                                if current_line:
                                    line_text = ' '.join(w['text'] for w in current_line)
                                    x0 = min(w['x0'] for w in current_line)
                                    y0 = min(w['top'] for w in current_line)
                                    x1 = max(w['x1'] for w in current_line)
                                    y1 = max(w['bottom'] for w in current_line)
                                    
                                    spans.append(TextSpan(
                                        text=line_text,
                                        page_num=page_num,
                                        bbox=(x0, y0, x1, y1)
                                    ))
                                
                                # Start a new line
                                current_y = word['top']
                                current_line = [word]
                            else:
                                # Add to current line
                                current_line.append(word)
                        
                        # Don't forget the last line
                        if current_line:
                            line_text = ' '.join(w['text'] for w in current_line)
                            x0 = min(w['x0'] for w in current_line)
                            y0 = min(w['top'] for w in current_line)
                            x1 = max(w['x1'] for w in current_line)
                            y1 = max(w['bottom'] for w in current_line)
                            
                            spans.append(TextSpan(
                                text=line_text,
                                page_num=page_num,
                                bbox=(x0, y0, x1, y1)
                            ))
    
    except Exception as e:
        logger.error(f"Error extracting text with locations: {str(e)}")
        # Fallback to basic extraction without locations
        try:
            logger.info("Falling back to basic text extraction")
            reader = PdfReader(file_path_or_bytes)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                if text:
                    spans.append(TextSpan(
                        text=text,
                        page_num=page_num
                    ))
        except Exception as fallback_error:
            logger.error(f"Fallback extraction failed: {str(fallback_error)}")
            raise
    
    return spans

def detect_clauses(
    text_spans: List[TextSpan], 
    clause_patterns: Dict[str, List[str]]
) -> Dict[str, List[TextSpan]]:
    """
    Detect legal clauses in the document based on patterns.
    
    Args:
        text_spans: List of text spans from the document
        clause_patterns: Dictionary of clause types and their regex patterns
        
    Returns:
        Dict[str, List[TextSpan]]: Dictionary of clause types and their spans
    """
    import re
    
    results = {clause_type: [] for clause_type in clause_patterns}
    
    for span in text_spans:
        for clause_type, patterns in clause_patterns.items():
            for pattern in patterns:
                if re.search(pattern, span.text, re.IGNORECASE):
                    results[clause_type].append(span)
                    break  # Found a match for this clause type
    
    return results