from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Quantum-AI")

# 1) exact origins list (comma-separated) from env
FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)
allowed_origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

# 2) if you need to allow dynamic preview URLs (like webcontainer), use regex:
ALLOW_ORIGIN_REGEX = os.getenv("ALLOW_ORIGIN_REGEX", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,        # exact list (recommended)
    allow_origin_regex=ALLOW_ORIGIN_REGEX or None,  # optional regex for wildcard origins
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
