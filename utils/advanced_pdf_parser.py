import fitz  # PyMuPDF

def parse_pdf_report_advanced(file):
    """
    Reads and cleans text from a PDF report using PyMuPDF.
    Works better than pdfplumber for analyst reports.
    """
    try:
        # Open the PDF
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                page_text = page.get_text("text")
                text += page_text + "\n"

            # Optional cleanup: remove extra spaces, fix line breaks
            clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

            return clean_text
    except Exception as e:
        return f"❌ Error parsing PDF: {str(e)}"
