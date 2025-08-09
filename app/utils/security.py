from fastapi import Header, HTTPException, status
from ..config import settings
from ..utils.logger import logger

async def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.API_KEY:
        logger.warning(f"API key mismatch. header='{x_api_key}' env='{settings.API_KEY}'")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
