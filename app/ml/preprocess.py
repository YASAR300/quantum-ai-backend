import numpy as np
import pandas as pd

EXPECTED_FEATURES = [
    "age","sex","chest_pain","high_bp","high_cholesterol","smoking","diabetes"
]

def to_numeric_row(features: dict) -> pd.DataFrame:
    row = {}
    for k in EXPECTED_FEATURES:
        v = features.get(k)
        if k == "sex":
            row[k] = {"male":1, "female":0, "other":0.5}.get(str(v).lower(), 0.5)
        else:
            if isinstance(v, bool):
                row[k] = 1 if v else 0
            else:
                try:
                    row[k] = float(v)
                except:
                    row[k] = 0.0
    return pd.DataFrame([row])

def generate_synthetic(n=400) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    df = pd.DataFrame({
        "age": rng.integers(25, 80, n),
        "sex": rng.integers(0, 2, n),
        "chest_pain": rng.integers(0, 2, n),
        "high_bp": rng.integers(0, 2, n),
        "high_cholesterol": rng.integers(0, 2, n),
        "smoking": rng.integers(0, 2, n),
        "diabetes": rng.integers(0, 2, n),
    })
    # linear risk score
    scores = (
        0.03*df["age"] + 0.9*df["high_bp"] + 0.7*df["high_cholesterol"] +
        0.6*df["smoking"] + 0.5*df["diabetes"] + 0.4*df["chest_pain"] + 0.1*df["sex"]
    )
    # ✅ 50/50 label balance
    thr = scores.median()
    df["label"] = (scores > thr).astype(int)
    return df
