from datetime import date, timedelta
from sqlmodel import Session, select
from app.models.analysis import RFMProfile, Recommendation
from app.models.product import Product
from app.core.db import engine
from app.services.explanation import generate_explanation

def run_recommendation_engine():
    print("Starting Recommendation Engine...")
    with Session(engine) as session:
        # Get all RFM profiles
        profiles = session.exec(select(RFMProfile)).all()
        
        # Get products for cycle info
        products = {p.product_id: p for p in session.exec(select(Product)).all()}
        
        recommendations = []
        session.query(Recommendation).delete() # Clear old recommendations
        
        today = date.today()
        
        for profile in profiles:
            product = products.get(profile.product_id)
            if not product: continue
            
            # 1. Calc expected repurchase
            # Last purchase was 'recency_days' ago
            last_purchase_date = today - timedelta(days=profile.recency_days)
            cycle = product.consumption_cycle_days
            expected_date = last_purchase_date + timedelta(days=cycle)
            
            days_until_expected = (expected_date - today).days
            
            # 2. Seasonality Check
            current_month = today.month
            season = "all_year"
            if current_month in [12, 1, 2]: season = "winter"
            elif current_month in [6, 7, 8]: season = "summer"
            
            # If product is seasonal and not current season, skip or delay
            if product.seasonality != "all_year" and product.seasonality != season:
                 # Logic: If miss-matched season, don't recommend or mark 'Off-Season'
                 # Prompt said: "delay recommendation"
                 # We will just skip generating a "Contact" recommendation for now
                 continue
            
            # 3. Generate Contact Window
            # Early: -5 days (Target is within next 5 days)
            # On-time: exact cycle (Target is today)
            # Late: +7 days (Target was 7 days ago)
            
            # Let's define "Recommended Window" logic based on prompt:
            # "Predict WHEN... output is recommendated contact window"
            
            rec_window = ""
            # If we are 5 days before expected date:
            if 0 <= days_until_expected <= 5:
                rec_window = "Early Reminder"
            elif days_until_expected == 0:
                rec_window = "On-time"
            elif days_until_expected < 0 and days_until_expected >= -7:
                rec_window = "Follow-up (Late)"
            elif days_until_expected < -7:
                rec_window = "Churn Risk / Win-back"
            else:
                # Too early to contact (> 5 days away)
                continue

            # 4. Assign Confidence
            # High: Freq > 2 and Recency not too far off
            # Medium: Freq == 2 or deviation
            confidence = "low"
            if profile.frequency >= 5:
                confidence = "high"
            elif profile.frequency >= 2:
                confidence = "medium"
                
            # 5. Reasoning (LLM)
            # We call the explainer here
            explanation = generate_explanation(
                customer_id=profile.customer_id,
                product_name=product.product_name,
                days_until_due=days_until_expected,
                confidence=confidence,
                window=rec_window
            )
            
            rec = Recommendation(
                customer_id=profile.customer_id,
                product_id=profile.product_id,
                recommended_contact_window=rec_window,
                confidence_level=confidence,
                reasoning=explanation
            )
            session.add(rec)
            recommendations.append(rec)
            
        session.commit()
        print(f"Generated {len(recommendations)} recommendations.")
