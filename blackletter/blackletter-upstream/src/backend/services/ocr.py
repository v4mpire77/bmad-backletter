import os
from typing import Optional

# Enable with: ENABLE_OCR=true
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"1", "true", "yes"}

def ocr_available() -> bool:
    """Return True if OCR functionality is enabled by flag."""
    return ENABLE_OCR

def extract_text_from_image(image_bytes: bytes, lang: Optional[str] = None) -> str:
    """
    Extract text using Tesseract OCR. Requires:
      - Python deps in src/backend/requirements-ocr.txt
      - System binary: tesseract-ocr
    """
    if not ENABLE_OCR:
        raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")

    # Lazy imports so startup never fails if OCR deps aren't present
    from PIL import Image  # type: ignore
    import io
    import pytesseract  # type: ignore

    img = Image.open(io.BytesIO(image_bytes))
    config = f"-l {lang}" if lang else ""
    return pytesseract.image_to_string(img, config=config).strip()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF using pdfplumber and OCR for images. Requires:
      - Python deps in src/backend/requirements-ocr.txt
      - System binary: tesseract-ocr
    """
    if not ENABLE_OCR:
        raise RuntimeError("OCR is disabled. Set ENABLE_OCR=true and install OCR deps.")

    # Lazy imports so startup never fails if OCR deps aren't present
    try:
        import pdfplumber  # type: ignore
        import pytesseract  # type: ignore
        from PIL import Image  # type: ignore
        import io
    except ImportError as e:
        raise RuntimeError(
            f"OCR dependencies not installed. Run: pip install -r src/backend/requirements-ocr.txt. Missing: {e}"
        )

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text_content = []

        for page in pdf.pages:
            # First try to extract text directly
            text = page.extract_text() or ""
            
            # If we get very little text, the page might be image-based
            if len(text.strip()) < 50:  # Arbitrary threshold
                try:
                    # Convert page to image and run OCR
                    img = page.to_image(resolution=150)
                    pil_image = img.original.convert('RGB')
                    ocr_text = pytesseract.image_to_string(pil_image) or ""
                    text = ocr_text
                except Exception:
                    # If OCR fails, keep the original text
                    pass

            text_content.append(text.strip())

        return "\n\n".join(text_content)