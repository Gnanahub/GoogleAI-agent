import json

def write_audit_log(path, raw_errors, rca_results):
    log = {
        "raw_errors": raw_errors,
        "analysis": rca_results
    }

    with open(path, "w") as f:
        json.dump(log, f, indent=4)
