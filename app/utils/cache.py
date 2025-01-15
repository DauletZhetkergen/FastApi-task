from cachetools import TTLCache

from app.schemas.users import User
from app.utils.logger import get_logger

cache = TTLCache(maxsize=100, ttl=3600)
logger = get_logger(__name__)

async def get_order_from_cache(order_id: int, user: User):  # Берем заказ с кэша
    print("getting")
    cache_key = f"order_{order_id}_user_{user.id}"
    if user.is_admin:
        cache_key = f"order_{order_id}"
    logger.info(f"Get order_id:{order_id} from cache")
    return cache.get(cache_key)


async def set_order_in_cache(order_id: int, order_data, user: User):  # Добавляем заказ в кэш
    print("adding")
    cache_key = f"order_{order_id}_user_{user.id}"
    if user.is_admin:
        cache_key = f"order_{order_id}"
    logger.info(f"Add order_id:{order_id} to cache")
    cache[cache_key] = order_data


async def delete_from_cache(
        order_id: int):  # Удаляем с кэша заказы которые начинаются с order_id используем при любом изменении заказа
    print("deleting")
    keys_to_delete = [key for key in cache.keys() if key.startswith(f"order_{order_id}")]
    for key in keys_to_delete:
        del cache[key]
    logger.info(f"Delete order_id:{order_id} from cache")
