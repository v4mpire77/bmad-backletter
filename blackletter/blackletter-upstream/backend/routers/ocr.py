from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from backend.app.core.ocr import OCRProcessor, ocr_available
from ..app.core.auth import verify_supabase_jwt

router = APIRouter()

@router.post("/process-pdf")
async def process_pdf_for_ocr(file: UploadFile = File(...), user=Depends(verify_supabase_jwt)):
    if not ocr_available():
        raise HTTPException(status_code=501, detail="OCR functionality is not enabled or dependencies are missing.")
    
    ocr_processor = OCRProcessor()
    try:
        file_content = await file.read()
        extracted_text = await ocr_processor.extract_text(file_content)
        return {"filename": file.filename, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")
