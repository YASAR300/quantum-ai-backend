from fastapi import APIRouter, HTTPException, Depends
from ..schemas import PredictRequest, PredictResponse
from ..ml.preprocess import to_numeric_row, EXPECTED_FEATURES
from ..ml.model import load_model, predict_proba, top_feature_importance, load_meta
from ..quantum.q_feature_select import quantum_feature_mask
from ..quantum.q_refine import refine_probability_with_quantum, blend
from ..config import settings
from ..utils.security import require_api_key

router = APIRouter(prefix="", tags=["prediction"])

@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    model = load_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Model not trained yet. Call /train first.")

    X = to_numeric_row(req.features)
    mask = quantum_feature_mask(len(EXPECTED_FEATURES))
    X_masked = X.copy()
    for i, keep in enumerate(mask):
        if keep == 0:
            X_masked.iloc[0, i] = 0.0

    ai_p = predict_proba(model, X_masked)

    used_quantum = False
    q_p = ai_p
    if settings.ENABLE_QUANTUM:
        used_quantum = True
        q_p = refine_probability_with_quantum(ai_p)

    final_p = blend(ai_p, q_p) if used_quantum else ai_p
    diagnosis = "High risk" if final_p >= 0.5 else "Low risk"

    fi = top_feature_importance(model, k=5)

    return PredictResponse(
        diagnosis=f"{diagnosis} of heart disease",
        final_probability=round(final_p, 4),
        ai_probability=round(ai_p, 4),
        quantum_refined_probability=round(q_p, 4),
        used_quantum=used_quantum,
        feature_importance=fi
    )

@router.get("/models/status")
async def status():
    meta = load_meta()
    return {"trained": meta is not None, "meta": meta}

# 🔐 Train endpoint (API key required)
@router.post("/train", dependencies=[Depends(require_api_key)])
async def train():
    from ..ml.train import train_pipeline
    meta = train_pipeline()
    return {"status": "ok", "meta": meta}

# 🧠 Explain endpoint (top feature importances)
@router.post("/explain")
async def explain(req: PredictRequest):
    model = load_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Model not trained yet.")
    fi = top_feature_importance(model, k=7)
    return {"top_features": fi}
