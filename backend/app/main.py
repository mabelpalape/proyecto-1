from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources
    print("Startup: Loading models...")
    yield
    # Clean up resources
    print("Shutdown: Cleaning up...")

app = FastAPI(
    title="E-commerce Predictive Analytics API",
    description="API for RFM analysis and marketing recommendations",
    version="0.1.0",
    lifespan=lifespan
)

from app.api.routes import router
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "System Operational", "status": "active"}
