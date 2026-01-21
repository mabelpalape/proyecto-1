from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class CustomerBase(SQLModel):
    customer_id: str = Field(primary_key=True) # Shopify ID
    email: str
    first_purchase_date: Optional[date] = None
    last_purchase_date: Optional[date] = None
    total_orders: int = 0
    total_spent: float = 0.0

class Customer(CustomerBase, table=True):
    __table_args__ = {"extend_existing": True}
    orders: List["Order"] = Relationship(back_populates="customer")
    recommendations: List["Recommendation"] = Relationship(back_populates="customer")
