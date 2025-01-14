from fastapi import FastAPI
from sqlalchemy import select

from app.database.db import  database_controller
from app.models.users import User
from app.routes import include_routers


app = FastAPI()
include_routers(app)


@app.on_event("startup")
async def startup():
    await database_controller.connect()

@app.on_event("shutdown")
async def shutdown():
    await database_controller.disconnect()





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
