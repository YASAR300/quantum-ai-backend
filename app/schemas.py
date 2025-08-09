from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class SymptomInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    sex: str = Field(..., pattern="^(male|female|other)$")
    chest_pain: Optional[bool] = False
    high_bp: Optional[bool] = False
    high_cholesterol: Optional[bool] = False
    smoking: Optional[bool] = False
    diabetes: Optional[bool] = False

class PredictRequest(BaseModel):
    features: Dict[str, Any]

# ✅ Define a proper model for feature importance items
class FeatureWeight(BaseModel):
    feature: str
    weight: float

class PredictResponse(BaseModel):
    diagnosis: str
    final_probability: float
    ai_probability: float
    quantum_refined_probability: float
    used_quantum: bool
    # ✅ Use List[FeatureWeight] instead of Dict[str, float]
    feature_importance: Optional[List[FeatureWeight]] = None
