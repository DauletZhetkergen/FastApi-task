from pydantic import BaseModel
from typing import List
from decimal import Decimal

from app.models.order import StatusEnum


# Схема для продукта
class ProductBase(BaseModel):
    name: str
    price: Decimal
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int

    class Config:
        orm_mode = True




class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_name: str
    status: StatusEnum

class OrderCreate(OrderBase):
    products: List[OrderItem]

class Order(OrderBase):
    order_id: int
    total_price: Decimal
    products: List[OrderItem]

    class Config:
        orm_mode = True