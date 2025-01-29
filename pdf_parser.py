import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_content):
    """Extract text from PDF content."""
    pdf_file = BytesIO(pdf_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def truncate_text(text, max_chars=50000):
    """Truncate text to a maximum number of characters."""
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

def parse_pdf(pdf_file_path: str) -> str:
    """
    Read a PDF file and return its text content.
    
    Args:
        pdf_file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted and truncated text from the PDF
    """
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
    
    # Extract and truncate text from PDF
    text_content = extract_text_from_pdf(pdf_content)
    return truncate_text(text_content) 