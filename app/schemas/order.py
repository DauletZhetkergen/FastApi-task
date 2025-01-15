from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from fastapi import Query

from app.models.order import StatusEnum


class ProductBase(BaseModel):
    name: str
    price: Decimal
    quantity: int


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
    order_id: int
    total_price: float


class OrderCreate(BaseModel):
    customer_name: str
    products: List[OrderItem]


class Order(OrderBase):
    products: List[OrderItem]

    class Config:
        orm_mode = True


class OrderShow(BaseModel):
    order: OrderBase
    products: List[ProductBase]
    class Config:
        orm_mode = True


class OrderDeleted(BaseModel):
    order_id: int