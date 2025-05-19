import sys
import pathlib
import json
import fitz
import pdfplumber


def text_extraction(pdf_path):
    all_text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            all_text.append(text)
    return "\n".join(all_text)
    
text_extraction("Document Extaction 1.pdf")     