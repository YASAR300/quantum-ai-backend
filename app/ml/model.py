import os
import joblib
import pandas as pd
from typing import Optional, Dict, List
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import roc_auc_score, accuracy_score

from .preprocess import EXPECTED_FEATURES
from ..config import settings

MODEL_PATH = os.path.join(settings.ARTIFACTS_DIR, "model.joblib")
META_PATH = os.path.join(settings.ARTIFACTS_DIR, "meta.joblib")


def make_pipeline() -> Pipeline:
    """Standardized Logistic Regression with class imbalance handling."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                max_iter=300,
                class_weight="balanced",
                solver="liblinear",   # robust for small tabular sets
                random_state=42
            )),
        ]
    )


def _safe_auc(y_true, y_score) -> Optional[float]:
    """Return AUC only if both classes present."""
    try:
        if len(set(y_true)) < 2:
            return None
        return float(roc_auc_score(y_true, y_score))
    except Exception:
        return None


def train_from_df(df: pd.DataFrame) -> Dict:
    """Train with multiple stratified splits and keep best model by accuracy."""
    X = df[EXPECTED_FEATURES]
    y = df["label"]

    # Guard: dataset must have both classes overall
    if len(set(y)) < 2:
        raise ValueError(
            "Dataset has only one class in 'label'. Need both classes (0 and 1)."
        )

    splitter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
    best_meta: Optional[Dict] = None
    best_pipe: Optional[Pipeline] = None

    for train_idx, test_idx in splitter.split(X, y):
        Xtr, Xte = X.iloc[train_idx], X.iloc[test_idx]
        ytr, yte = y.iloc[train_idx], y.iloc[test_idx]

        pipe = make_pipeline()
        pipe.fit(Xtr, ytr)

        proba = pipe.predict_proba(Xte)[:, 1]
        auc = _safe_auc(yte, proba)
        acc = float(accuracy_score(yte, (proba > 0.5).astype(int)))

        meta = {"auc": auc, "acc": acc, "features": EXPECTED_FEATURES}

        # choose best by accuracy; ties naturally go to first best
        if best_meta is None or acc > best_meta["acc"]:
            best_meta = meta
            best_pipe = pipe

    # Persist best model + meta
    assert best_pipe is not None and best_meta is not None, "Training failed to produce a model."
    joblib.dump(best_pipe, MODEL_PATH)
    joblib.dump(best_meta, META_PATH)
    return best_meta


def load_model() -> Optional[Pipeline]:
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def load_meta() -> Optional[Dict]:
    if not os.path.exists(META_PATH):
        return None
    return joblib.load(META_PATH)


def predict_proba(model: Pipeline, X: pd.DataFrame) -> float:
    return float(model.predict_proba(X)[:, 1][0])


def top_feature_importance(model: Pipeline, k: int = 5) -> List[Dict[str, float]]:
    """
    For LogisticRegression: coefficient magnitudes as importance.
    Returns list of dicts: [{feature, weight}, ...] sorted by |weight|.
    """
    clf: LogisticRegression = model.named_steps["clf"]
    coefs = clf.coef_[0]

    meta = load_meta()
    feats = meta["features"] if meta and "features" in meta else EXPECTED_FEATURES

    # Safety: align lengths if mismatch
    n = min(len(feats), len(coefs))
    pairs = sorted(
        ({"feature": feats[i], "weight": float(coefs[i])} for i in range(n)),
        key=lambda x: abs(x["weight"]),
        reverse=True,
    )
    return pairs[:k]
