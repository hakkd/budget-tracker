import pandas as pd


TARGET_COL = "category"
TEXT_COL = "merchant"
NUM_COL = "amount"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [col.strip().lower() for col in out.columns]
    out = out.rename(columns={"description": "merchant"})

    required = {TEXT_COL, NUM_COL, TARGET_COL}
    missing = required.difference(out.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return out
