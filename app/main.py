from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import predict, admin, quantum

app = FastAPI(
    title="Quantum-AI Medical Diagnosis API",
    version="1.0.0"
)

# ✅ CORS setup (allow all origins for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials (like cookies)
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ✅ Routers
app.include_router(admin.router)
app.include_router(predict.router)
app.include_router(quantum.router)

@app.get("/")
def root():
    return {"message": "Welcome to Quantum-AI Medical Diagnosis API"}

@app.get("/health")
def health():
    return {"status": "ok"}
