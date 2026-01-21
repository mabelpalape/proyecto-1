from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.analysis import Recommendation
from app.models.customer import Customer
from app.services.mock_data import create_mock_data
from app.services.rfm import run_rfm_analysis
from app.services.recommendation import run_recommendation_engine

router = APIRouter()

@router.post("/ingest/mock")
async def generate_mock_data():
    """Generate 4 years of historical data."""
    create_mock_data()
    return {"message": "Mock data generation triggered."}

@router.post("/analytics/run")
async def run_analytics():
    """Run full analytics pipeline (RFM + Recommendations)."""
    # 1. RFM
    run_rfm_analysis()
    # 2. Recommendations
    run_recommendation_engine()
    return {"message": "Analytics pipeline completed."}

@router.get("/recommendations", response_model=List[Recommendation])
async def read_recommendations(session: Session = Depends(get_session)):
    """Get all recommendations."""
    return session.exec(select(Recommendation)).all()

@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: str, session: Session = Depends(get_session)):
    return session.get(Customer, customer_id)
