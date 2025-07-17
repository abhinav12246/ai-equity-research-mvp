import pdfplumber

def parse_pdf_report_advanced(file):
    """
    Reads and cleans text from a PDF report using PyMuPDF.
    Works better than pdfplumber for analyst reports.
    """
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"❌ Error parsing PDF: {str(e)}"
