import pandas as pd

from ml.config import CSV_PATH, CLEAN_CSV_PATH

"""
Expects input data to have columns Description,
Amount, Category
"""

CATEGORY_MAP = {
    "misc. fees": "misc_fees",
    "dining out": "dining_out",
}


if __name__ == "__main__":
    df = pd.read_csv(CSV_PATH, dtype=str)

    df["merchant"] = df["Description"].fillna("").str.strip()
    df["amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["category"] = df["Category"].fillna("").str.strip().replace(CATEGORY_MAP)

    # Keep only labeled, valid spend rows for supervised training
    df = df[df["category"] != ""]
    df = df[df["amount"].notna()]
    df = df[df["amount"] >= 0]

    df = df[["merchant", "amount", "category"]].drop_duplicates()

    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)

    print(df.head())
    print(f"Saved cleaned data to {CLEAN_CSV_PATH}")
