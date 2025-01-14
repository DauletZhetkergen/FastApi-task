from app.routes.auth import user_router
from app.routes.order import order_router


def include_routers(app):
    app.include_router(user_router,tags=["user"])
    app.include_router(order_router,tags=["order"])