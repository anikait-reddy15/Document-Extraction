import fitz  # PyMuPDF
import google.generativeai as genai
import json
import re
import streamlit as st
from dotenv import load_dotenv
import os
from io import BytesIO

# Load environment variables
load_dotenv()

# Extract raw text from PDF
def extract_raw_text_from_file(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n\n"
    return full_text

# Prepare Gemini prompt
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

# Call Gemini API
def call_gemini_api(prompt, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
    response = model.generate_content(prompt)

    response_text = response.text.strip()
    response_text = re.sub(r"^```json|```$", "", response_text).strip()
    return response_text

# Streamlit UI
def main():
    st.set_page_config(page_title="PDF to JSON Extractor with Gemini", layout="centered")
    st.title("PDF to Structured JSON Extractor")
    st.write("Upload a PDF document, and Gemini will extract structured key-value pairs and table data.")

    api_key = os.getenv("GEMINI_API_KEY")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and st.button("Extract Data"):
        with st.spinner("Extracting text and calling Gemini..."):
            raw_text = extract_raw_text_from_file(uploaded_file)
            prompt = prepare_prompt(raw_text)
            json_text = call_gemini_api(prompt, api_key)

        st.subheader("Extracted JSON:")
        st.code(json_text, language='json')

        # Attempt to parse and allow download
        try:
            parsed_json = json.loads(json_text)
            json_bytes = json.dumps(parsed_json, indent=4, ensure_ascii=False).encode("utf-8")
            st.download_button(
                label="Download JSON",
                data=json_bytes,
                file_name="extracted_output.json",
                mime="application/json"
            )
        except json.JSONDecodeError:
            st.warning("The output is not valid JSON.")

if __name__ == "__main__":
    main()
