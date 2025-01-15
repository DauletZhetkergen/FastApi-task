from fastapi import HTTPException
from sqlalchemy import and_, select, insert, update

from app.database.db import database_controller
from app.models.order import ProductModel, OrderModel, StatusEnum
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def create_order_util(order_data, current_user):
    total_price = 0
    async with database_controller.transaction():
        order_items = []
        for item in order_data.products:
            order_items.append({"product_id": item.product_id,
                                "quantity": item.quantity})
            product = select(ProductModel).filter(ProductModel.product_id == item.product_id)
            product_model = await database_controller.fetch_one(product)
            if not product_model:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
            if product_model.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough quantity for product ID {item.product_id}"
                )
            total_price = product_model.price * item.quantity

            substract_query = (
                update(ProductModel)
                .where(ProductModel.product_id == item.product_id)
                .values(quantity=ProductModel.quantity - item.quantity)
            )
            await database_controller.execute(substract_query)
        order_query = insert(OrderModel).values(
            customer_name=order_data.customer_name,
            user_id=current_user.id,
            status=StatusEnum.pending,
            total_price=total_price,
            products=order_items
        )
        order_id = await database_controller.execute(order_query)
        logger.info(f"Order created id:{order_id}")
        return {"Order id:": order_id, "Total price": total_price, "Status": StatusEnum.pending}


async def get_orders_filter(status, min_price, max_price, current_user):
    query = select(OrderModel).where(OrderModel.user_id == current_user.id)

    if status is not None:
        query = query.where(OrderModel.status == status)

    if min_price is not None:
        query = query.where(OrderModel.total_price >= min_price)
    if max_price is not None:
        query = query.where(OrderModel.total_price <= max_price)

    order_list = await database_controller.fetch_all(query)


    return order_list