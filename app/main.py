from fastapi import FastAPI
import uvicorn
from app.database.db import database_controller
from app.routes import include_routers
from app.utils.middleware import MetricsMiddleware
from alembic.config import Config
import subprocess
from alembic import command
app = FastAPI()
include_routers(app)
app.add_middleware(MetricsMiddleware)



@app.on_event("startup")
async def startup():
    await database_controller.connect()


@app.on_event("shutdown")
async def shutdown():
    await database_controller.disconnect()



