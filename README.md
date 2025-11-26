# GoogleAI-agent
This Capstone Project is part of the 5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025) and is open to all participants. The project lets you apply what you’ve learned during the course by building AI agents.


# Supply Chain LLM ETL Pipeline  
Automated pipeline that extracts tables from PDFs/CSVs using Gemini, detects data quality errors, performs LLM-based root cause analysis, auto-fixes valid issues, and generates an RCA PDF + audit logs.

---

## 🚀 Features
- PDF/CSV table extraction using Gemini API (with fallback to mock extractor)
- Data quality validations (missing values, invalid dates, quantity errors)
- LLM-based reasoning for Root Cause Analysis
- Auto-fixing when safe
- Generates:
  - `final_cleaned_output.csv`
  - `rca_report.pdf`
  - `audit_log.json`

---

## 📦 Installation
pip install -r requirements.txt

## 🔑 Setting API Key
Set environment variable:

Linux/macOS:
export GOOGLE_API_KEY="your-key"

Windows PowerShell: $env:GOOGLE_API_KEY="your-key"


## ▶️ Running the Pipeline

python main.py --input data/sample_input.pdf


---

## 📁 Output
After running, the folder will contain:

- `cleaned_output.csv`
- `rca_report.pdf`
- `audit_log.json`

---

## 🧩 Fallback Mode
If no Gemini API key is available, the pipeline runs in **MOCK mode**, useful for:
- Developers
- Testing ETL flows
- CI/CD pipelines

---


