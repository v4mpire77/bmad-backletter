from typing import Optional
import pdfplumber
import pytesseract
from PIL import Image
import io

class OCRProcessor:
    def __init__(self):
        # Configure pytesseract path for Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    async def extract_text(self, file_content: bytes) -> str:
        """Extract text from a PDF file using pdfplumber and pytesseract for images."""
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                text_content = []
                
                for page in pdf.pages:
                    # Extract text content
                    text = page.extract_text() or ""
                    
                    # If page has little or no text, try OCR on the page image
                    if len(text.strip()) < 50:  # Arbitrary threshold
                        img = page.to_image()
                        # Convert to PIL Image
                        pil_image = Image.frombytes(
                            mode='RGB',
                            size=(img.width, img.height),
                            data=img.original.tobytes()
                        )
                        # Perform OCR
                        text = pytesseract.image_to_string(pil_image) or ""
                    
                    text_content.append(text.strip())
                
                return "\n\n".join(text_content)
                
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
