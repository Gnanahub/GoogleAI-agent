import json
import traceback

try:
    import google.generativeai as genai
    SDK_AVAILABLE = True
except:
    SDK_AVAILABLE = False


def _local_heuristic(err):
    issue = err["issue"]

    out = {
        "row": err["row"],
        "column": err["column"],
        "value": err["value"],
        "severity": "Warning",
        "root_cause": "",
        "recommended_fix": "",
        "autofix": "NO",
        "suggested_value": None
    }

    if issue == "InvalidDate":
        out.update({
            "severity": "Warning",
            "root_cause": "Invalid date format",
            "recommended_fix": "Convert to YYYY-MM-DD",
        })
        v = err["value"]
        if v.isdigit() and len(v) == 8:
            out["autofix"] = "YES"
            out["suggested_value"] = f"{v[:4]}-{v[4:6]}-{v[6:]}"
    elif issue in ["BadQty", "NegativeQty"]:
        out.update({
            "severity": "Error",
            "root_cause": "Quantity issue",
            "recommended_fix": "Enter valid number"
        })
    elif issue == "MissingValue":
        out.update({
            "severity": "Error",
            "root_cause": "Missing value",
            "recommended_fix": "Fill from source system"
        })

    return out


def analyze_error_with_llm(error, use_api=True, model="gemini-1.5-pro"):
    if not use_api or not SDK_AVAILABLE:
        return _local_heuristic(error)

    try:
        prompt = f"""
        Analyze this error and return JSON only:
        {json.dumps(error)}
        Fields: root_cause, severity, recommended_fix, autofix, suggested_value
        """

        resp = genai.generate_content(
            model=model,
            contents=[prompt],
            temperature=0
        )

        data = json.loads(resp.text)
        data.update({"row": error["row"], "column": error["column"], "value": error["value"]})
        return data

    except:
        traceback.print_exc()
        return _local_heuristic(error)
