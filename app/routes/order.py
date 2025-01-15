from fastapi import APIRouter, Depends
from app.schemas.users import UserCreate, TokenBase, AuthData, UserBase, User
from app.schemas.order import Order
from app.utils.dependecies import get_current_user
from app.utils.logger import get_logger
from app.utils.order import create_order_util

order_router = APIRouter()
logger = get_logger(__name__)

@order_router.post("/orders")
async def create_order(order: Order, current_user: User = Depends(get_current_user)):
    logger.info("Creating a new order")
    return await create_order_util(order)

@order_router.get("/orders")
def get_orders():
    pass

@order_router.put("/orders/{order_id}")
def update_order():
    return





@order_router.get("/orders/{order_id}")
def get_order():
    return


@order_router.delete("/orders/{order_id}")
def delete_order():
    return
