from app.routes.auth import user_router
from app.routes.order import order_router
from app.routes.admin import admin_router


def include_routers(app):
    app.include_router(prefix="/api", router=user_router, tags=["user"])
    app.include_router(prefix="/api", router=order_router, tags=["order"])
    app.include_router(prefix="/api", router=admin_router, tags=["admin"])
