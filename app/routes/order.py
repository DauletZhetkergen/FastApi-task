from fastapi import APIRouter





order_router = APIRouter()

@order_router.post("/orders")
def create_order():
    return

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

