import pytesseract
from PIL import Image, ImageEnhance
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import THAI_FONT_NAME, THAI_FONT_PATH
import os

# Default Windows Tesseract Path
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def preprocess_image(img):
    """Enhance image for better OCR accuracy."""
    img = img.convert('L')  # Grayscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return img

def ocr_pdf_to_docx(pdf_path, output_path, progress_callback=None):
    """
    Convert a scanned PDF to Word using Tesseract OCR (Thai+English).
    """
    doc = Document()
    
    # Configure default style for Thai font
    style = doc.styles['Normal']
    font = style.font
    font.name = THAI_FONT_NAME
    font.size = Pt(16)
    
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        
        # High resolution for OCR (300 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        img = preprocess_image(img)
        
        # OCR with Thai and English support
        text = pytesseract.image_to_string(img, lang='tha+eng', config='--oem 3 --psm 6')
        
        # Add page text to doc
        doc.add_paragraph(text)
        
        if progress_callback:
            progress_callback(int(((page_num + 1) / total_pages) * 100))
            
    doc.save(output_path)
    pdf_document.close()
    return True
