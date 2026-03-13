from fastapi import FastAPI, Request
from app.api.routes import router
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

app = FastAPI(
    title="Mini Cloud Platform API"
)

app.include_router(router)

#metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of requests in seconds", ["endpoint"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    return response

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}

@app.get("/metrics", tags=["Metrics"])
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)