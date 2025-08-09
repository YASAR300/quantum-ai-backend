from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import predict, admin, quantum

app = FastAPI(
    title="Quantum-AI Medical Diagnosis API",
    version="1.0.0"
)

# ✅ CORS setup (Routers se pehle)
FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)
allowed_origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

ALLOW_ORIGIN_REGEX = os.getenv("ALLOW_ORIGIN_REGEX", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,          # Specific origins
    allow_origin_regex=ALLOW_ORIGIN_REGEX or None,  # Optional regex for dynamic origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(admin.router)
app.include_router(predict.router)
app.include_router(quantum.router)

@app.get("/")
def root():
    return {"message": "Welcome to Quantum-AI Medical Diagnosis API"}

# ✅ Health endpoint (CORS check ke liye)
@app.get("/health")
def health():
    return {"status": "ok"}
