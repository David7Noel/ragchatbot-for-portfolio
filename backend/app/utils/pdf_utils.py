from PyPDF2 import PdfReader
from typing import List

def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Reads PDF from file path and returns list of non-empty lines.
    """
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            lines = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    for ln in txt.splitlines():
                        ln = ln.strip()
                        if ln:
                            lines.append(ln)
        if not lines:
            raise ValueError("PDF enthält keinen extrahierbaren Text")
        return lines
    except Exception as e:
        raise ValueError(f"Fehler beim Lesen der PDF: {e}")
