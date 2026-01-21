from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class OrderBase(SQLModel):
    order_id: str = Field(primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id")
    order_date: date

class Order(OrderBase, table=True):
    __table_args__ = {"extend_existing": True}
    customer: "Customer" = Relationship(back_populates="orders")
    line_items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItemBase(SQLModel):
    product_id: str = Field(foreign_key="product.product_id")
    quantity: int

class OrderItem(OrderItemBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str = Field(foreign_key="order.order_id")
    
    order: "Order" = Relationship(back_populates="line_items")
    product: "Product" = Relationship(back_populates="order_items")
