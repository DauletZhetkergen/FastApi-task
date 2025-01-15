from fastapi import HTTPException
from sqlalchemy import and_, select, insert, update

from app.database.db import database_controller
from app.models.order import ProductModel, OrderModel, StatusEnum
from app.schemas.order import OrderShow, OrderBase, OrderDeleted
from app.utils.cache import get_order_from_cache, set_order_in_cache, delete_from_cache
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
                logger.warn(f"Product with ID {item.product_id} not found")
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
            if product_model.quantity < item.quantity:
                logger.warn(f"Not enough quantity for product ID {item.product_id}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough quantity for product ID {item.product_id}"
                )
            total_price += product_model.price * item.quantity
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
        order = OrderBase(customer_name=order_data.customer_name,
                          total_price=total_price,
                          order_id=order_id,
                          status=StatusEnum.pending,
                          )
        return order


# FIXME down
async def get_orders_filter(status, min_price, max_price, current_user):
    query = select(OrderModel).where(OrderModel.deleted == False)
    filters = ""
    if not current_user.is_admin:
        query = query.where(OrderModel.user_id == current_user.id)

    if status is not None:
        filters += f"status -> {status.value}"
        query = query.where(OrderModel.status == status)

    if min_price is not None:
        filters += f"min_price -> {min_price}"
        query = query.where(OrderModel.total_price >= min_price)
    if max_price is not None:
        filters += f"max_price -> {max_price}"
        query = query.where(OrderModel.total_price <= max_price)

    order_list = await database_controller.fetch_all(query)
    logger.info(f"GET orders with: {filters}")

    return order_list


async def updating_order(order_id, status, current_user):
    await check_for_own_exists(order_id, current_user)
    get_older_status_query = select(OrderModel.status).where(OrderModel.order_id == order_id)
    older_status = await database_controller.fetch_one(get_older_status_query)
    update_query = update(OrderModel).where(OrderModel.order_id == order_id).values(status=status).returning(OrderModel)
    updated_order = await database_controller.fetch_one(update_query)
    await delete_from_cache(order_id)
    logger.info(f"Changing order id:{order_id} status {older_status.status}->{status}")
    return updated_order


async def get_one_order(order_id, current_user):
    cached_order = await get_order_from_cache(order_id, current_user)
    if cached_order:
        return cached_order

    await check_for_own_exists(order_id, current_user)

    order_query = select(OrderModel).where(OrderModel.order_id == order_id)
    order = await database_controller.fetch_one(order_query)

    ordered_products = {item["product_id"]: item["quantity"] for item in order.products}
    product_query = select(ProductModel).where(ProductModel.product_id.in_(ordered_products.keys()))
    products = await database_controller.fetch_all(product_query)
    products_list = [
        {**dict(product), "quantity": ordered_products[product["product_id"]]} for product in products]

    result = OrderShow(order=dict(order), products=products_list)
    await set_order_in_cache(order_id, result, current_user)
    return result


async def delete_softly_order(order_id, current_user):
    await check_for_own_exists(order_id, current_user)
    delete_quert = update(OrderModel).where(OrderModel.order_id == order_id).values(deleted=True)
    await database_controller.execute(delete_quert)
    await delete_from_cache(order_id)
    logger.info(f"Order id:{order_id} deleted")
    order = OrderDeleted(order_id=order_id)
    return order


async def check_for_own_exists(order_id, current_user):
    get_order_query = select(OrderModel).where(and_(OrderModel.order_id == order_id,
                                                    OrderModel.deleted == False))
    order_exist = await database_controller.fetch_one(get_order_query)
    if not order_exist:
        logger.warn(f"Order with ID {order_id} not found")
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    if not current_user.is_admin:
        get_order_query = get_order_query.where(OrderModel.user_id == current_user.id)
        check_order_user = await database_controller.fetch_one(get_order_query)
        if not check_order_user:
            logger.warn(f"User:{current_user.id} Not enough permissions")
            raise HTTPException(status_code=404, detail=f"Not enough permissions")
