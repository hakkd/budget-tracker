import pandas as pd
from sklearn.model_selection import train_test_split

from ml.config import DATA_DIR, CLEAN_CSV_PATH

if __name__ == "__main__":
    df = pd.read_csv(CLEAN_CSV_PATH)

    stratify = df["category"] if "category" in df.columns else None

    train, test = train_test_split(
        df,
        test_size=0.30,
        random_state=42,
        stratify=stratify,
    )

    output_dir = DATA_DIR / "processed"
    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    train.to_csv(
        train_path,
        index=False,
    )
    print(f"Training data written to {train_path} and has {train.shape[0]} rows")

    test.to_csv(
        test_path,
        index=False,
    )
    print(f"Test data written to {test_path} and has {test.shape[0]} rows")
