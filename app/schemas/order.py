from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from fastapi import Query

from app.models.order import StatusEnum


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
    total_price: float


class OrderCreate(BaseModel):
    customer_name: str
    products: List[OrderItem]


class Order(OrderBase):
    products: List[OrderItem]

    class Config:
        orm_mode = True
