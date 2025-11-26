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

