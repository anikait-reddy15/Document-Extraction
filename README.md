# PDF to Structured JSON Extractor with Gemini

## Overview
This Streamlit app allows users to upload a PDF document and automatically extract structured key-value pairs and table data as JSON. It leverages PyMuPDF (`fitz`) to extract raw text from PDFs and Google's Gemini generative AI model to parse and format the extracted data into JSON.

---

## Features
- Upload PDF files via a simple web interface.
- Extract raw text from each page of the PDF.
- Generate a natural language prompt for Gemini API to parse key-value pairs and tables.
- Display the extracted JSON output in the app.
- Download the extracted data as a formatted JSON file.

---

## Technologies Used
- Python
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) for PDF text extraction
- [Google Generative AI API (Gemini)](https://developers.generativeai.google/) for text-to-JSON parsing
- Streamlit for building the interactive web UI
- dotenv for environment variable management

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-json-extractor.git
cd pdf-json-extractor

