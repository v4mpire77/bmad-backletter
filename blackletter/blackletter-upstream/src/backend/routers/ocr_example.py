# backend/routers/ocr_example.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.ocr import ocr_available, extract_text_from_image

router = APIRouter()

@router.post("/upload-image-ocr")
async def upload_image_ocr(file: UploadFile = File(...)):
    if not ocr_available():
        raise HTTPException(status_code=501, detail="OCR is disabled on this deployment.")
    data = await file.read()
    try:
        text = extract_text_from_image(data)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))