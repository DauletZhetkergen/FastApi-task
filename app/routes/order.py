from typing import Optional, List

from fastapi import APIRouter, Depends

from app.models.order import StatusEnum
from app.schemas.users import User
from app.schemas.order import Order, OrderCreate, OrderShow
from app.utils.dependecies import get_current_user
from app.utils.logger import get_logger
from app.utils.order import create_order_util, get_orders_filter, updating_order, get_one_order, delete_softly_order

order_router = APIRouter()
logger = get_logger(__name__)


@order_router.post("/orders", summary="Создание нового заказа", description="Создает новый заказ")
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    logger.info("Creating a new order")
    return await create_order_util(order, current_user)


@order_router.get("/orders", response_model=List[Order], summary="Получение списка заказов",
                  description="Возвращает список заказов с возможностью фильтрации по статусу, минимальной и "
                              "максимальной цене.", )
async def get_orders(status: Optional[StatusEnum] = None,
                     min_price: Optional[float] = None,
                     max_price: Optional[float] = None, current_user: User = Depends(get_current_user)):
    logger.info(f"User:{current_user.id} GET orders")
    return await get_orders_filter(status, min_price, max_price, current_user)


@order_router.get("/orders/{order_id}", response_model=OrderShow)
async def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    return await get_one_order(order_id, current_user)


@order_router.put("/orders", response_model=Order)
async def update_order(order_id: int,
                       status: Optional[StatusEnum], current_user: User = Depends(get_current_user)):
    logger.info(f"Updating order id:{order_id}")
    return await updating_order(order_id, status, current_user)


@order_router.delete("/orders")
async def delete_order(order_id: int, current_user: User = Depends(get_current_user)):
    return await delete_softly_order(order_id, current_user)
