import logging
from ..config import settings

logger = logging.getLogger("quantum-ai")
level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=level, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
