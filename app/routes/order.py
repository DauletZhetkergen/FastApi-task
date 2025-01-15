from typing import Optional, List

from fastapi import APIRouter, Depends

from app.models.order import StatusEnum
from app.schemas.users import UserCreate, TokenBase, AuthData, UserBase, User
from app.schemas.order import Order, OrderCreate
from app.utils.dependecies import get_current_user
from app.utils.logger import get_logger
from app.utils.order import create_order_util, get_orders_filter

order_router = APIRouter()
logger = get_logger(__name__)


@order_router.post("/orders")
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    logger.info("Creating a new order")
    return await create_order_util(order, current_user)


@order_router.get("/orders", response_model=List[Order])
async def get_orders(status: Optional[StatusEnum] = None,
                     min_price: Optional[float] = None,
                     max_price: Optional[float] = None, current_user: User = Depends(get_current_user)):
    logger.info(f"User:{current_user.id} GET orders")
    return await get_orders_filter(status, min_price, max_price, current_user)


@order_router.put("/orders/{order_id}")
async def update_order():
    return


@order_router.get("/orders/{order_id}")
def get_order():
    return


@order_router.delete("/orders/{order_id}")
def delete_order():
    return
