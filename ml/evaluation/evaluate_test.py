import joblib
import json
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

from ml.config import DATA_DIR, PROJECT_ML_ROOT


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
        raise ValueError(f"Missing required columns in test set: {sorted(missing)}")

    return out


if __name__ == "__main__":
    model_dir = PROJECT_ML_ROOT / "models" / "baseline"
    pipeline_path = model_dir / "pipeline.joblib"
    test_path = DATA_DIR / "processed" / "test.csv"

    pipeline = joblib.load(pipeline_path)
    test_df = normalize_columns(pd.read_csv(test_path))

    x_test = test_df[[TEXT_COL, NUM_COL]]
    y_test = test_df[TARGET_COL]
    y_pred = pipeline.predict(x_test)

    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    accuracy = float(accuracy_score(y_test, y_pred))

    labels = sorted(set(y_test).union(set(y_pred)))
    print(labels)
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_df.index.name = "actual"
    cm_df.columns.name = "predicted"

    model_dir.mkdir(parents=True, exist_ok=True)
    cm_path = model_dir / "test_confusion_matrix.csv"
    metrics_path = model_dir / "test_metrics.json"

    cm_df.to_csv(cm_path)

    metrics = {
        "split": "held_out_test",
        "n_test": int(len(y_test)),
        "macro_f1": macro_f1,
        "accuracy": accuracy,
        "pipeline_path": str(pipeline_path),
        "test_data_path": str(test_path),
        "confusion_matrix_csv": str(cm_path),
    }
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Macro F1: {macro_f1:.4f}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Confusion matrix saved to: {cm_path}")
    print(f"Metrics saved to: {metrics_path}")
