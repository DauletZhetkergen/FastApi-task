from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime,func, Enum as sql_enum,Float,DECIMAL,JSON
from sqlalchemy.orm import relationship


BaseOrder = declarative_base()
class StatusEnum(Enum):
    confirmed = "confirmed"
    pending = "pending"
    cancelled = "cancelled"

class OrderModel(BaseOrder):
    __tablename__ = "Order"#FIXME
    order_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    status = Column(sql_enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    products = Column(JSON, nullable=False)

class ProductModel(BaseOrder):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
