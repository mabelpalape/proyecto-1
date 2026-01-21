import pandas as pd
from sqlmodel import Session, select
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.analysis import RFMProfile
from app.core.db import engine

def run_rfm_analysis():
    print("Starting RFM Analysis...")
    with Session(engine) as session:
        # Load data into DataFrame
        # We need a join of OrderItem -> Order -> Product
        # SQL: select * from orderitem join order on ...
        
        statement = select(
            models.OrderItem.quantity,
            models.Order.customer_id,
            models.Order.order_date,
            Product.product_id,
            Product.price
        ).join(models.Order).join(Product)
        
        # SQLModel doesn't execute join to dict easily for pandas without iteration, 
        # but pandas read_sql is easier if we have the connection.
        # Let's use pandas read_sql with the engine.
        
        query = """
        SELECT 
            o.customer_id, 
            oi.product_id, 
            o.order_date, 
            oi.quantity,
            p.price
        FROM orderitem oi
        JOIN "order" o ON oi.order_id = o.order_id
        JOIN product p ON oi.product_id = p.product_id
        """
        
        try:
            df = pd.read_sql(query, engine)
        except Exception as e:
            print(f"Error loading data: {e}")
            return
            
        if df.empty:
            print("No data to analyze.")
            return

        # Ensure datetime
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['total_value'] = df['quantity'] * df['price']
        
        # Group by Customer + Product
        rfm = df.groupby(['customer_id', 'product_id']).agg({
            'order_date': lambda x: (pd.Timestamp.now() - x.max()).days, # Recency
            'quantity': 'count', # Frequency (count of orders/items)
            'total_value': 'sum' # Monetary
        }).reset_index()
        
        rfm.rename(columns={
            'order_date': 'recency_days', 
            'quantity': 'frequency', 
            'total_value': 'monetary'
        }, inplace=True)
        
        # Save to DB
        # First, clear old profiles? Or update? For MVP, clear old.
        session.query(RFMProfile).delete()
        
        profiles = []
        for _, row in rfm.iterrows():
            # Basic scoring (1-5 scale logic could go here, for now just store raw)
            # Example "score" string logic
            score_str = "Standard"
            if row['frequency'] > 3: score_str = "Loyal"
            if row['recency_days'] > 100: score_str = "At Risk"
            
            profile = RFMProfile(
                customer_id=row['customer_id'],
                product_id=row['product_id'],
                recency_days=int(row['recency_days']),
                frequency=int(row['frequency']),
                monetary=float(row['monetary']),
                rfm_score=score_str
            )
            session.add(profile)
        
        session.commit()
        print(f"RFM Analysis complete. Generated {len(rfm)} profiles.")

# Helper to fix module reference in string query if needed
import app.models.order as models
import app.models.product as p_models
