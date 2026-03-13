from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Mini Cloud Platform API"
)

app.include_router(router)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}