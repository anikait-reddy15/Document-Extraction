import fitz  # PyMuPDF
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv()
import os

load_dotenv()

def extract_raw_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n\n"
    return full_text

def prepare_prompt(raw_text):
    prompt = f"""
Extract the key-value pairs and table information from the following document text.

Return a JSON object with keys for metadata fields and a 'List Items' array for table rows.

Document text:
\"\"\" 
{raw_text}
\"\"\"

Output example:
{{
    "PO Number": "11748477",
    "List Items": [
        {{
            "Sr. No.": "1",
            "Description": "NVIDIA"
        }},
        {{
            "Sr. No.": "2",
            "Description": "LINUX"
        }}
    ]
}}
"""
    return prompt

def call_gemini_api(prompt, api_key):
    genai.configure(api_key=api_key)

    # Use Gemini Pro with the GENERATIVE TEXT model
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

    response = model.generate_content(prompt)

    # Clean Markdown formatting if present
    response_text = response.text.strip()
    response_text = re.sub(r"^```json|```$", "", response_text).strip()

    return response_text

def main():
    PDF_PATH = "PDF1.pdf"
    API_KEY =   os.getenv("GEMINI_API_KEY")

    raw_text = extract_raw_text(PDF_PATH)
    prompt = prepare_prompt(raw_text)
    json_text = call_gemini_api(prompt, API_KEY)

    print("Extracted JSON:\n")
    print(json_text)

    # Save JSON output if valid
    try:
        parsed = json.loads(json_text)
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)
        print("\nData saved to output.json")
    except json.JSONDecodeError:
        print("\nWarning: The output is not valid JSON.")

if __name__ == "__main__":
    main()
