import pandas as pd
import numpy as np


def validate_with_vocabulary(data_path: str, vocab_path: str = 'penguin_vocabulary.csv'):
    """
    Validate a CSV dataset against a vocabulary CSV.

    Returns
    -------
    clean_df : pd.DataFrame
        DataFrame with standardized types (categoricals coerced, numerics coerced)
    report : dict
        { 'errors': [..], 'warnings': [..], 'row_count': int, 'invalid_row_indices': list }
    """
    df = pd.read_csv(data_path)
    vocab = pd.read_csv(vocab_path)
    errors = []
    warnings = []
    invalid_rows = set()

    # 1) Required columns
    req = vocab[vocab['required'].astype(str).str.lower()=='yes']['column_name']
    missing = [c for c in req if c not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {missing}")
        # Can't proceed robustly without them; return early
        return df, {'errors': errors, 'warnings': warnings, 'row_count': len(df), 'invalid_row_indices': sorted(invalid_rows)}

    # 2) Iterate vocabulary rows and validate
    for _, row in vocab.iterrows():
        col = row['column_name']
        dtype = row['data_type']
        unit = row.get('unit', '')
        allowed = str(row.get('allowed_values', '')).split('|') if pd.notna(row.get('allowed_values')) and row.get('allowed_values')!='' else []
        required = str(row['required']).lower()=='yes'

        if col not in df.columns:
            continue

        if dtype == 'categorical':
            # Normalize missing sex to Unknown if sex
            if col == 'sex':
                df[col] = df[col].fillna('Unknown')
            # Coerce to str
            df[col] = df[col].astype(str)
            if allowed:
                mask_invalid = ~df[col].isin(allowed)
                if mask_invalid.any():
                    bad_vals = sorted(df.loc[mask_invalid, col].unique().tolist())
                    idxs = df.index[mask_invalid].tolist()
                    invalid_rows.update(idxs)
                    errors.append(f"Invalid categorical values in {col}: {bad_vals}")
        elif dtype == 'float':
            # Coerce numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Missing numeric in required columns -> error
            if required:
                miss_mask = df[col].isna()
                if miss_mask.any():
                    idxs = df.index[miss_mask].tolist()
                    invalid_rows.update(idxs)
                    errors.append(f"Missing/Non-numeric values in required numeric column {col} at rows: {idxs[:10]}{'...' if len(idxs)>10 else ''}")
            # Range checks
            try:
                vmin = float(row['min_value']) if row['min_value'] != '' and not pd.isna(row['min_value']) else None
                vmax = float(row['max_value']) if row['max_value'] != '' and not pd.isna(row['max_value']) else None
            except Exception:
                vmin, vmax = None, None
            if vmin is not None:
                low_mask = df[col] < vmin
                if low_mask.any():
                    idxs = df.index[low_mask].tolist()
                    invalid_rows.update(idxs)
                    warnings.append(f"Values below min in {col} (min={vmin}): sample {df.loc[low_mask, col].head(5).tolist()}")
            if vmax is not None:
                high_mask = df[col] > vmax
                if high_mask.any():
                    idxs = df.index[high_mask].tolist()
                    invalid_rows.update(idxs)
                    warnings.append(f"Values above max in {col} (max={vmax}): sample {df.loc[high_mask, col].head(5).tolist()}")
        else:
            warnings.append(f"Unknown data_type '{dtype}' for column {col}—skipping.")

    report = {
        'errors': errors,
        'warnings': warnings,
        'row_count': len(df),
        'invalid_row_indices': sorted(invalid_rows)
    }
    return df, report

def clean_errors_and_warnings(df: pd.DataFrame,
                              report: dict,
                              vocab_path: str = "penguin_vocabulary.csv",
                              method: str = "clip"):
    """
    Cleans ALL values responsible for errors or warnings in `validate_with_vocabulary()`.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame returned from validate_with_vocabulary()
    report : dict
        Report dictionary from validate_with_vocabulary()
    vocab_path : str
        Path to vocabulary CSV (penguin_vocabulary.csv)
    method : str
        'clip'   -> numeric outliers are clipped to min/max
        'remove' -> rows with any warning/error are removed entirely

    Returns
    -------
    cleaned_df : pd.DataFrame
        Cleaned dataset
    info : dict
        {
          'rows_removed': int,
          'rows_remaining': int,
          'columns_cleaned': [...],
          'mode': method
        }
    """
    vocab = pd.read_csv(vocab_path)

    cleaned = df.copy()
    rows_to_remove = set()

    # If validator marked any rows invalid → always consider removing them if method="remove"
    invalid_from_validator = report.get("invalid_row_indices", [])
    rows_to_remove.update(invalid_from_validator)

    # Process numeric outliers based on vocabulary limits
    num_vocab = vocab[vocab["data_type"] == "float"]

    for _, v in num_vocab.iterrows():
        col = v["column_name"]
        if col not in cleaned.columns:
            continue

        # Extract limits
        vmin = float(v["min_value"]) if v["min_value"] != "" else None
        vmax = float(v["max_value"]) if v["max_value"] != "" else None

        x = pd.to_numeric(cleaned[col], errors="coerce")

        # Identify outliers
        low_mask = (x < vmin) if vmin is not None else pd.Series([False]*len(x))
        high_mask = (x > vmax) if vmax is not None else pd.Series([False]*len(x))
        out_mask = low_mask | high_mask

        if method == "clip":
            # Clip instead of removing rows
            if vmin is not None:
                x = x.clip(lower=vmin)
            if vmax is not None:
                x = x.clip(upper=vmax)
            cleaned[col] = x

        elif method == "remove":
            # Fully remove any rows with outliers
            rows_to_remove.update(cleaned.index[out_mask].tolist())

    # Handle categorical invalids: remove any rows where invalid categorical occurred
    cat_vocab = vocab[vocab["data_type"] == "categorical"]
    for _, v in cat_vocab.iterrows():
        col = v["column_name"]
        allowed = str(v["allowed_values"]).split("|") if isinstance(v["allowed_values"], str) else []
        if allowed == [""] or not allowed:
            continue

        if col not in cleaned.columns:
            continue

        invalid_mask = ~cleaned[col].astype(str).isin(allowed)
        rows_to_remove.update(cleaned[invalid_mask].index.tolist())

    # Final row removal if method == "remove"
    rows_removed = 0
    if method == "remove" and len(rows_to_remove) > 0:
        cleaned = cleaned.drop(index=sorted(rows_to_remove))
        rows_removed = len(rows_to_remove)

    info = {
        "rows_removed": rows_removed,
        "rows_remaining": len(cleaned),
        "columns_cleaned": list(vocab["column_name"]),
        "mode": method
    }

    return cleaned, info