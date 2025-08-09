from fastapi import FastAPI
from .routers import predict, admin, quantum

app = FastAPI(title="Quantum-AI Medical Diagnosis API", version="1.0.0")

app.include_router(admin.router)
app.include_router(predict.router)
app.include_router(quantum.router)

@app.get("/")
def root():
    return {"message": "Welcome to Quantum-AI Medical Diagnosis API"}
