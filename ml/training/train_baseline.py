import json
import joblib
import pandas as pd
import sys
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict

ML_ROOT = Path(__file__).resolve().parents[1]
if str(ML_ROOT) not in sys.path:
    sys.path.insert(0, str(ML_ROOT))

from config import DATA_DIR, PROJECT_ML_ROOT


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


def build_pipeline(scale_numeric: bool = True) -> Pipeline:
    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"

    features = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(), TEXT_COL),
            ("num", numeric_transformer, [NUM_COL]),
        ],
        remainder="drop",
    )

    model = LogisticRegression(max_iter=2000, class_weight="balanced")

    return Pipeline(
        steps=[
            ("features", features),
            ("model", model),
        ]
    )


def evaluate_cv(pipe: Pipeline, x_train: pd.DataFrame, y_train: pd.Series) -> dict:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_validate(
        pipe,
        x_train,
        y_train,
        cv=cv,
        scoring={"macro_f1": "f1_macro"},
        n_jobs=-1,
        return_train_score=False,
    )
    y_pred = cross_val_predict(pipe, x_train, y_train, cv=cv, n_jobs=-1)

    return {
        "cv": {
            "n_splits": 5,
            "macro_f1_mean": float(scores["test_macro_f1"].mean()),
            "macro_f1_std": float(scores["test_macro_f1"].std()),
            "macro_f1_per_fold": [float(v) for v in scores["test_macro_f1"]],
        },
        "oof_macro_f1": float(f1_score(y_train, y_pred, average="macro")),
        "classification_report": classification_report(
            y_train, y_pred, output_dict=True, zero_division=0
        ),
        "n_train": int(len(y_train)),
    }


def main() -> None:
    train_df = normalize_columns(pd.read_csv(DATA_DIR / "processed" / "train.csv"))

    x_train = train_df[[TEXT_COL, NUM_COL]]
    y_train = train_df[TARGET_COL]

    pipeline = build_pipeline(scale_numeric=True)
    metrics = evaluate_cv(pipeline, x_train, y_train)

    # Fit on all training data after CV so the saved artifact is production-ready.
    pipeline.fit(x_train, y_train)

    model_dir = PROJECT_ML_ROOT / "models" / "baseline"
    model_dir.mkdir(parents=True, exist_ok=True)

    pipeline_path = model_dir / "pipeline.joblib"
    metrics_path = model_dir / "metrics.json"

    joblib.dump(pipeline, pipeline_path)

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with metrics_path.open("r", encoding="utf-8") as f:
        json.load(f)

    print(f"Saved pipeline: {pipeline_path}")
    print(f"Saved metrics : {metrics_path}")
    print(f"CV Macro F1   : {metrics['cv']['macro_f1_mean']:.4f}")


if __name__ == "__main__":
    main()
