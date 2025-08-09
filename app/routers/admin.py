from fastapi import APIRouter, Depends
from ..utils.security import require_api_key

router = APIRouter(prefix="", tags=["admin"])

@router.get("/health")
async def health():
    return {"ok": True}

# Allow both GET and POST for key check
@router.api_route("/check-key", methods=["GET", "POST"], dependencies=[Depends(require_api_key)])
async def check_key():
    return {"ok": True, "msg": "API key accepted"}
