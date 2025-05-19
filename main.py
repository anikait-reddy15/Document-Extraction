import sys
import os
import pathlib
import json
import fitz
import pdfplumber

#Function for Text extraction
def text_extraction(pdf_path):  
    if not os.path.exists(pdf_path):
        return "File does not exit"

    all_text = []
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text()
                all_text.append(text)
        return "\n".join(all_text)
    except Exception as e:
        print(f"Error : {e}")
        
pdf_path = "PDF1.pdf"
text = text_extraction(pdf_path)
print(text)
