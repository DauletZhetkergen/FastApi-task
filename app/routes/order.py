from fastapi import APIRouter, Depends
from app.schemas.users import UserCreate, TokenBase, AuthData, UserBase, User
from app.schemas.order import Order
from app.utils.dependecies import get_current_user

order_router = APIRouter()


@order_router.post("/orders")
def create_order(order: Order, current_user: User = Depends(get_current_user)):
    print(order)


@order_router.put("/orders/{order_id}")
def update_order():
    return


@order_router.get("/orders")
def get_order():
    return


@order_router.get("/orders/{order_id}")
def get_order():
    return


@order_router.delete("/orders/{order_id}")
def delete_order():
    return
