def auto_fix_errors(df, fixes):
    df2 = df.copy()

    for entry in fixes:
        if entry.get("autofix") == "YES":
            row = entry["row"]
            col = entry["column"]
            val = entry["suggested_value"]
            df2.at[row, col] = val

    return df2
