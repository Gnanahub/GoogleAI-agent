import os
import argparse
import pandas as pd
import json

from agents.extractor_agent import extract_data_from_document, json_to_dataframe
from agents.error_detector import detect_errors
from agents.llm_agent import analyze_error_with_llm
from agents.auto_fix import auto_fix_errors

from utils.pdf_report import generate_pdf
from utils.audit_logger import write_audit_log


def load_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def detect_file_type(filename):
    ext = filename.lower().split(".")[-1]
    if ext in ["pdf"]:
        return "pdf"
    if ext in ["csv"]:
        return "csv"
    return "unknown"


def main(input_path):
    print(f"📄 Loading file: {input_path}")
    file_bytes = load_file_bytes(input_path)
    ftype = detect_file_type(input_path)

    # --- Extraction ---
    print("🔍 Extracting tables...")
    extracted = extract_data_from_document(
        file_bytes=file_bytes,
        file_type=ftype,
        use_api=bool(os.environ.get("GOOGLE_API_KEY")),
    )

    dfs = json_to_dataframe(extracted)
    if not dfs:
        print("❌ No tables found. Stopping.")
        return

    # Use first table
    table_name, df = next(iter(dfs.items()))
    print(f"📊 Extracted table: {table_name} ({len(df)} rows)")

    # --- Error Detection ---
    print("⚠ Running validations...")
    errors = detect_errors(df)

    # --- LLM Root Cause & Fixes ---
    print("🧠 LLM analyzing errors...")
    rca_entries = []
    for err in errors:
        ans = analyze_error_with_llm(
            err,
            use_api=bool(os.environ.get("GOOGLE_API_KEY"))
        )
        rca_entries.append(ans)

    # --- Auto Fix ---
    print("🔧 Applying auto-fixes...")
    fixed_df = auto_fix_errors(df, rca_entries)

    fixed_df.to_csv("cleaned_output.csv", index=False)
    print("✅ Saved: cleaned_output.csv")

    # --- PDF Report ---
    print("📑 Generating PDF RCA Report...")
    generate_pdf(rca_entries, "rca_report.pdf")
    print("📄 Saved: rca_report.pdf")

    # --- Audit Log ---
    print("📝 Writing audit log...")
    write_audit_log("audit_log.json", errors, rca_entries)
    print("📁 Saved: audit_log.json")

    print("\n🎉 Pipeline Completed Successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to PDF or CSV input file")
    args = parser.parse_args()

    main(args.input)


