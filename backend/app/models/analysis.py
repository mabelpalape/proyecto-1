from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class RFMProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id", index=True)
    product_id: str = Field(foreign_key="product.product_id", index=True)
    
    recency_days: int
    frequency: int
    monetary: float
    rfm_score: str # e.g. "555" or "High-Value"

    __table_args__ = {"extend_existing": True}

    # We might interpret "per CUSTOMER-PRODUCT pair" as:
    # frequency of THIS product, monetary of THIS product.
    
class Recommendation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id")
    product_id: str = Field(foreign_key="product.product_id")
    
    recommended_contact_window: str # Early, On-time, Late
    confidence_level: str # low, medium, high
    reasoning: str # LLM generated text
    generated_date: date = Field(default_factory=date.today)

    __table_args__ = {"extend_existing": True}

    customer: "Customer" = Relationship(back_populates="recommendations")
