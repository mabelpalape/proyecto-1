from app.core.db import create_db_and_tables, engine 
from sqlmodel import Session, select
from app.models.analysis import Recommendation    
from app.models.customer import Customer
from app.services.mock_data import create_mock_data
from app.services.rfm import run_rfm_analysis
from app.services.recommendation import run_recommendation_engine
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

def verify():
    print("=== Verification Start ===")
    
    # 1. Setup DB
    print("[1] Creating DB tables...")
    create_db_and_tables()
    
    # 2. Mock Data
    print("[2] Generating Mock Data...")
    create_mock_data()
    
    with Session(engine) as session:
        cust_count = len(session.exec(select(Customer)).all())
        print(f"    -> Customers in DB: {cust_count}")
        
    # 3. Analytics
    print("[3] Running Analytics Pipeline...")
    run_rfm_analysis()
    run_recommendation_engine()
    
    # 4. Check Output
    print("[4] Checking Recommendations...")
    with Session(engine) as session:
        recs = session.exec(select(Recommendation).limit(5)).all()
        print(f"    -> Total Recommendations generated: {len(session.exec(select(Recommendation)).all())}")
        print("    -> Sample output:")
        for r in recs:
            print(f"       - Cust: {r.customer_id} | Prod: {r.product_id} | Window: {r.recommended_contact_window} | Reason: {r.reasoning}")

    print("=== Verification Complete ===")

if __name__ == "__main__":
    verify()
