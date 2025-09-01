"""
OCR router for PDF text extraction.
Only available when ENABLE_OCR=true and OCR dependencies are installed.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.ocr import ocr_available, extract_text_from_pdf

router = APIRouter()

class OCRDisabledError(Exception):
    """Raised when OCR is disabled or dependencies are missing."""
    pass

@router.post("/extract")
async def extract_text_from_pdf_endpoint(file: UploadFile = File(...)):
    """
    Extract text from a PDF file using OCR.
    
    Returns:
        - ok: boolean indicating success
        - chars: character count of extracted text
        - text: extracted text (potentially truncated for demo)
    """
    if not ocr_available():
        raise HTTPException(
            status_code=400, 
            detail="OCR is disabled. Set ENABLE_OCR=true and install OCR dependencies."
        )
    
    if not file.content_type or not file.content_type.startswith('application/pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported for OCR extraction."
        )
    
    try:
        # Read the PDF file
        pdf_data = await file.read()
        
        # Extract text from PDF using pdfplumber + OCR
        extracted_text = extract_text_from_pdf(pdf_data)
        
        # Truncate for demo (as mentioned in problem statement)
        truncated_text = extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
        
        return {
            "ok": True,
            "chars": len(extracted_text),
            "text": truncated_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")