from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as sql_enum, DECIMAL, JSON, ForeignKey

from app.models import Base


class StatusEnum(Enum):
    confirmed = "confirmed"
    pending = "pending"
    cancelled = "cancelled"

class OrderModel(Base):
    __tablename__ = "Order"#FIXME
    order_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    status = Column(sql_enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    products = Column(JSON, nullable=False)

class ProductModel(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
