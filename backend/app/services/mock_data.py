import random
import uuid
from datetime import date, timedelta
from sqlmodel import Session, select
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.core.db import engine

def create_mock_data():
    with Session(engine) as session:
        # Check if data exists
        if session.exec(select(Customer)).first():
            print("Data already exists. Skipping mock generation.")
            return

        print("Generating mock data...")

        # 1. Products
        products = []
        cycles = [30, 45, 60, 90]
        seasons = ["all_year", "summer", "winter"]
        for i in range(1, 21):
            p = Product(
                product_id=f"PROD-{i:03d}",
                product_name=f"Product {i}",
                consumption_cycle_days=random.choice(cycles),
                seasonality=random.choice(seasons),
                is_pack=False
            )
            session.add(p)
            products.append(p)
        session.commit()

        # 2. Customers
        customers = []
        for i in range(1, 51):
            c = Customer(
                customer_id=f"CUST-{i:03d}",
                email=f"customer{i}@example.com",
                total_orders=0,
                total_spent=0.0
            )
            session.add(c)
            customers.append(c)
        session.commit()

        # 3. Orders (History: 4 years)
        start_date = date.today() - timedelta(days=365*4)
        orders = []
        
        for _ in range(500): # 500 random orders
            cust = random.choice(customers)
            # Random date in the last 4 years
            days_offset = random.randint(0, 365*4)
            order_date = start_date + timedelta(days=days_offset)
            
            order = Order(
                order_id=str(uuid.uuid4()),
                customer_id=cust.customer_id,
                order_date=order_date
            )
            session.add(order)
            
            # Add line items
            num_items = random.randint(1, 3)
            current_products = random.sample(products, num_items)
            order_total = 0
            
            for p in current_products:
                qty = random.randint(1, 2)
                item = OrderItem(
                    order=order,
                    product=p,
                    quantity=qty
                )
                session.add(item)
                order_total += qty * p.price
            
            # Update customer stats (naive)
            cust.total_orders += 1
            cust.total_spent += order_total
            if not cust.first_purchase_date or order_date < cust.first_purchase_date:
                cust.first_purchase_date = order_date
            if not cust.last_purchase_date or order_date > cust.last_purchase_date:
                cust.last_purchase_date = order_date
            
            session.add(cust)
        
        session.commit()
        print("Mock data generated successfully.")

if __name__ == "__main__":
    from app.core.db import create_db_and_tables
    create_db_and_tables()
    create_mock_data()
