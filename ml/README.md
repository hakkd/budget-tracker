## Transaction Categorization

### Phase 1: baseline model using labelled data

- metrics:
    - Macro F1 (important for smaller categories)
    - Per-category precision/recall
    - Top-2 accuracy (useful for UI suggestions)
    - Coverage above confidence threshold
        - Predict category + confidence.
        - Auto-apply if confidence >= threshold (for example 0.85).
        - Send 0.5-0.85 to review queue with top 2 suggestions.
        - Below 0.5 -> Needs Review.
        - Feed reviewed corrections back into next training cycle.

### Phase 2: rule engine as guardrails and for hard constraints

- transfers
- known fees
- explicit payments

### Phase 3: active learning review for low-confidence predictions

- human review for low confidence predictions
- retrain monthly
- version model and category taxonomy together

## Development

### Python Virtual Environment Setup

From the repo root:

```
python -m venv ml/ml

source ml/ml/bin/activate

pip install -r ml/requirements.txt
```

### Run Scripts

From the repo root:

1. `source ml/ml/bin/activate`
2. `python -m ml.scripts.process_data_and_train_baseline_model`
