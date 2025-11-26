import pandas as pd
import re

def detect_errors(df):
    errors = []

    for col in df.columns:
        for idx, val in df[col].items():

            if pd.isna(val) or str(val).strip() == "":
                errors.append({"row": idx, "column": col, "value": val, "issue": "MissingValue"})
                continue

            v = str(val)

            if "date" in col.lower():
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", v) and not re.match(r"^\d{8}$", v):
                    errors.append({"row": idx, "column": col, "value": v, "issue": "InvalidDate"})

            if col.lower() == "qty":
                try:
                    if float(v) < 0:
                        errors.append({"row": idx, "column": col, "value": v, "issue": "NegativeQty"})
                except:
                    errors.append({"row": idx, "column": col, "value": v, "issue": "BadQty"})

    return errors
