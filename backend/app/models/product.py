from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ProductBase(SQLModel):
    product_id: str = Field(primary_key=True)
    product_name: str
    price: float = 10.0 # Default price
    consumption_cycle_days: int = 30
    seasonality: str = "all_year" # Comma separated if multiple or JSON
    is_pack: bool = False

class Product(ProductBase, table=True):
    __table_args__ = {"extend_existing": True}
    order_items: List["OrderItem"] = Relationship(back_populates="product")
