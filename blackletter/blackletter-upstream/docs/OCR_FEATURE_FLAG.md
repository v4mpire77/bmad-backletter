# OCR Feature Flag Implementation

This document describes the implementation of the OCR feature flag that allows the Blackletter API to boot successfully without heavy OCR dependencies while providing a clean way to enable OCR functionality when needed.

## Overview

The OCR functionality is now gated behind an `ENABLE_OCR` environment variable with lazy imports to ensure the API always boots successfully, even if OCR dependencies are not installed.

## Files Changed

### 1. `src/backend/requirements.txt`
Updated to remove OCR dependencies:
- Removed: `Pillow`, `pdfplumber`, `pytesseract`, `openai>=1.0.0`
- Updated: `requests` version to `2.32.3`
- Kept all core API dependencies for FastAPI, Uvicorn, etc.

### 2. `src/backend/requirements-ocr.txt`
Separate requirements file containing only OCR dependencies:
- `Pillow==10.4.0`
- `pdfplumber==0.11.4`
- `pytesseract==0.3.10`

### 3. `src/backend/services/ocr.py`
Updated OCR service with feature flag:
- Uses `ENABLE_OCR` environment variable (accepts: "1", "true", "yes")
- Lazy imports OCR dependencies inside functions
- Clear error messages when OCR is disabled or dependencies missing
- Added language parameter support for Tesseract

### 4. `src/backend/routers/ocr_example.py` (Optional)
Example router showing how to use OCR safely:
- Checks OCR availability before processing
- Returns HTTP 501 when OCR is disabled
- Proper error handling for OCR failures

## Usage

### Default (No OCR)
```bash
# Install core dependencies only
pip install -r src/backend/requirements.txt

# Start server - boots successfully without OCR deps
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --app-dir src
```

### With OCR Enabled
```bash
# Install both core and OCR dependencies
pip install -r src/backend/requirements.txt -r src/backend/requirements-ocr.txt

# Set environment variable and start server
ENABLE_OCR=true uvicorn backend.main:app --host 0.0.0.0 --port 8000 --app-dir src
```

### Docker with OCR
```dockerfile
FROM python:3.11-slim

# Install system binary for Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install all dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r src/backend/requirements.txt -r src/backend/requirements-ocr.txt

# Enable OCR
ENV ENABLE_OCR=true

CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000","--app-dir","src"]
```

## API Usage

### Check OCR Availability
```python
from backend.services.ocr import ocr_available

if ocr_available():
    # OCR is enabled and available
    pass
else:
    # OCR is disabled
    pass
```

### Extract Text from Image
```python
from backend.services.ocr import extract_text_from_image

try:
    text = extract_text_from_image(image_bytes, lang="eng")
    print("Extracted text:", text)
except RuntimeError as e:
    print("OCR error:", e)
```

### Router Implementation
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.ocr import ocr_available, extract_text_from_image

@router.post("/upload-image-ocr")
async def upload_image_ocr(file: UploadFile = File(...)):
    if not ocr_available():
        raise HTTPException(
            status_code=501, 
            detail="OCR is disabled on this deployment."
        )
    
    data = await file.read()
    try:
        text = extract_text_from_image(data)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Testing

### Boot Test (Default)
```bash
# Should boot successfully without OCR dependencies
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --app-dir src
curl http://localhost:8000/health  # Should return 200 OK
```

### OCR Disabled Test
```bash
# Should return 501 when OCR endpoints are called
curl -F "file=@image.png" http://localhost:8000/api/upload-image-ocr
# Response: {"detail":"OCR is disabled on this deployment."}
```

### OCR Enabled Test
```bash
# Install OCR dependencies first
pip install -r src/backend/requirements-ocr.txt

# Start with OCR enabled
ENABLE_OCR=true uvicorn backend.main:app --host 0.0.0.0 --port 8000 --app-dir src

# Should process images (requires tesseract-ocr system binary)
curl -F "file=@image.png" http://localhost:8000/api/upload-image-ocr
```

## Environment Variables

- `ENABLE_OCR`: Controls OCR functionality
  - Accepts: `"1"`, `"true"`, `"yes"` (case-insensitive) to enable
  - Any other value (including empty/unset) disables OCR
  - Default: `"false"` (disabled)

## Deployment

### Render (Default - No OCR)
Keep existing build commands as they are:
```bash
# Build
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi; \
$PY -m pip install --upgrade pip setuptools wheel && \
$PY -m pip install -r src/backend/requirements.txt && \
cd frontend && npm ci && NEXT_PUBLIC_API_URL=/ npm run build && npm run export && cd ..

# Start
uvicorn backend.main:app --host 0.0.0.0 --port $PORT --app-dir src
```

### Docker with OCR
Use the Docker example above to enable OCR in containerized deployments.

## Benefits

1. **Faster Builds**: Render builds no longer fail due to heavy OCR dependencies
2. **Reliable Startup**: API always boots successfully, even without OCR deps
3. **Clean Architecture**: Clear separation between core API and OCR functionality  
4. **Easy Migration**: Existing code can gradually adopt the feature flag pattern
5. **Flexible Deployment**: Choose OCR support per deployment environment