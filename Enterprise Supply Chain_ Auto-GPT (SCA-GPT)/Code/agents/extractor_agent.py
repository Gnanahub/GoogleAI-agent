import json
import pandas as pd
import traceback
import pdfplumber
import io

try:
    import google.generativeai as genai
    SDK_AVAILABLE = True
except:
    SDK_AVAILABLE = False


def _pdf_to_text(file_bytes):
    try:
        pages = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for p in pdf.pages:
                pages.append(p.extract_text() or "")
        return "\n".join(pages)
    except:
        return None


def _mock_extract(text):
    return {
        "tables": [
            {
                "name": "mock_table",
                "columns": ["material", "description", "ship_date", "qty"],
                "rows": [
                    ["A12", "Widget", "2024-11-10", 10],
                    ["", "Unknown", "20241105", "abc"],
                ]
            }
        ]
    }


def extract_data_from_document(file_bytes, file_type="pdf", use_api=True, model="gemini-1.5-pro"):
    text = _pdf_to_text(file_bytes) if file_type == "pdf" else None

    if not use_api or not SDK_AVAILABLE:
        return _mock_extract(text)

    try:
        resp = genai.generate_content(
            model=model,
            contents=[
                "Extract tables in JSON: {tables:[{name:'', columns:[], rows:[]}]}",
                text[:5000] if text else str(file_bytes)
            ],
            temperature=0,
            max_output_tokens=1000,
        )

        output = resp.text
        return json.loads(output)

    except:
        traceback.print_exc()
        return _mock_extract(text)


def json_to_dataframe(extracted_json):
    dfs = {}
    for t in extracted_json.get("tables", []):
        cols = t.get("columns", [])
        rows = t.get("rows", [])
        dfs[t.get("name", "table")] = pd.DataFrame(rows, columns=cols)
    return dfs
