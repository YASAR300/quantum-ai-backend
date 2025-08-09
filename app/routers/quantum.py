from fastapi import APIRouter, Depends
from ..utils.security import require_api_key
from ..quantum.q_refine import refine_probability_with_quantum

router = APIRouter(prefix="", tags=["quantum"])

@router.post("/quantum/run", dependencies=[Depends(require_api_key)])
async def quantum_run(p: float = 0.62):
    q = refine_probability_with_quantum(p)
    return {"input_p": p, "refined_p": q}
