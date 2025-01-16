import re
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from app.config import metric_logger_path
from app.models.order import StatusEnum
from app.schemas.users import User
from app.schemas.order import Order, OrderCreate, OrderShow, OrderBase, OrderDeleted
from app.utils.dependecies import check_admin_role
from app.utils.logger import get_logger
from app.utils.order import create_order_util, get_orders_filter, updating_order, get_one_order, delete_softly_order

admin_router = APIRouter(prefix="/admin")
logger = get_logger(__name__)


@admin_router.post("/orders", summary="Create a new order", description="Creating a new order",
                   response_model=OrderBase)
async def create_order(order: OrderCreate, admin_user: User = Depends(check_admin_role), ):
    logger.info("Creating a new order")
    return await create_order_util(order, admin_user)


@admin_router.get("/orders", response_model=List[Order], summary="Get list of orders",
                  description="Returning list of orders with filtering by status,min price,max price")
async def get_orders(status: Optional[StatusEnum] = None,
                     min_price: Optional[float] = None,
                     max_price: Optional[float] = None, admin_user: User = Depends(check_admin_role)):
    logger.info(f"User:{admin_user.id} GET orders")
    return await get_orders_filter(status, min_price, max_price, admin_user)


@admin_router.put("/orders", response_model=Order, summary="Get info about order",
                  description="Returns detailed information about a specific order by ID.")
async def update_order(order_id: int,
                       status: Optional[StatusEnum], admin_user: User = Depends(check_admin_role)):
    logger.info(f"Updating order id:{order_id}")
    return await updating_order(order_id, status, admin_user)


@admin_router.get("/orders/{order_id}", response_model=OrderShow, summary="Update order status",
                  description="Updates the status of a specific order by its ID.")
async def get_order(order_id: int, admin_user: User = Depends(check_admin_role)):
    return await get_one_order(order_id, admin_user)


@admin_router.delete("/orders", summary="Delete an order", description="Soft deletion of an order by ID.",
                     response_model=OrderDeleted)
async def delete_order(order_id: int, admin_user: User = Depends(check_admin_role)):
    return await delete_softly_order(order_id, admin_user)


@admin_router.get("/metrics")
async def get_metrics(admin_user: User = Depends(check_admin_role)):
    try:
        with open(metric_logger_path, "r") as file:
            lines = file.readlines()

        endpoint_counts = {}
        for line in lines:
            match = re.search(r"Endpoint: (/api/[\w/]+?)(?:/\d+)?\s*\| Status: (\d+) \| Time: (\S+)s", line)
            if match:
                endpoint = match.group(1)
                status = match.group(2)
                if endpoint not in endpoint_counts:
                    endpoint_counts[endpoint] = {"total": 0, "success": 0, "failure": 0}
                endpoint_counts[endpoint]["total"] += 1

                if status.startswith("2"):
                    endpoint_counts[endpoint]["success"] += 1
                else:
                    endpoint_counts[endpoint]["failure"] += 1
        logger.info("Getting metrics")
        return JSONResponse(content=endpoint_counts)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
