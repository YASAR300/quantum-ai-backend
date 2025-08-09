import os
from pathlib import Path
from dotenv import load_dotenv

# Locate project root and force-load .env from there
APP_DIR = Path(__file__).resolve().parent        # .../app
ROOT_DIR = APP_DIR.parent                        # project root
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

class Settings:
    API_KEY: str = os.getenv("API_KEY", "changeme")
    ENABLE_QUANTUM: bool = os.getenv("ENABLE_QUANTUM", "true").lower() == "true"
    QUANTUM_BLEND_ALPHA: float = float(os.getenv("QUANTUM_BLEND_ALPHA", "0.7"))
    CLASSIQ_ENABLED: bool = os.getenv("CLASSIQ_ENABLED", "false").lower() == "true"
    DATA_PATH: str = os.getenv("DATA_PATH", str(ROOT_DIR / "data" / "heart.csv"))
    ARTIFACTS_DIR: str = os.getenv("ARTIFACTS_DIR", str(ROOT_DIR / "artifacts"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)
