from pathlib import Path

PROJECT_ML_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ML_ROOT / "data"
CSV_PATH = PROJECT_ML_ROOT / "data" / "raw" / "activity.csv"
CLEAN_CSV_PATH = PROJECT_ML_ROOT / "data" / "clean" / "transactions_clean.csv"
