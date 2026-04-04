import pandas as pd
from sklearn.model_selection import train_test_split

from ml.config import DATA_DIR, CLEAN_CSV_PATH

if __name__ == "__main__":
    df = pd.read_csv(CLEAN_CSV_PATH)

    train, test = train_test_split(df, test_size=0.30)

    output_dir = DATA_DIR / "processed"
    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(train).to_csv(
        train_path,
        index=False,
    )
    print(f"Training data written to {train_path} and has {train.shape[0]} rows")

    pd.DataFrame(test).to_csv(
        test_path,
        index=False,
    )
    print(f"Test data written to {test_path} sand has {test.shape[0]} rows")
