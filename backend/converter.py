from pdf2docx import Converter
from pdfminer.high_level import extract_pages
from .config import UPLOAD_DIR, OUTPUT_DIR
from .ocr_engine import ocr_pdf_to_docx
import os

def detect_pdf_type(pdf_path):
    """
    Detect if the PDF is searchable (has text) or scanned (image-only).
    """
    try:
        pages = list(extract_pages(pdf_path, maxpages=2))
        for page in pages:
            # Check for LTTextContainer objects
            for element in page:
                if hasattr(element, 'get_text'):
                    return "searchable"
        return "scanned"
    except Exception as e:
        print(f"Error detecting PDF type: {e}")
        return "scanned"  # Fallback to scanned

def convert_searchable_to_docx(pdf_path, output_path, progress_callback=None):
    """
    Convert a searchable PDF using pdf2docx for layout preservation.
    """
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    if progress_callback:
        progress_callback(100)
    return True

def convert_pdf_to_word(pdf_path, output_path, progress_callback=None):
    """
    Unified entry point for both searchable and scanned PDF conversion.
    """
    pdf_type = detect_pdf_type(pdf_path)
    print(f"Detected PDF type: {pdf_type}")
    
    if pdf_type == "searchable":
        return convert_searchable_to_docx(pdf_path, output_path, progress_callback)
    else:
        return ocr_pdf_to_docx(pdf_path, output_path, progress_callback)
