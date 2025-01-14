from fastapi import APIRouter
from app.schemas.users import UserCreate
from app.utils.users import create_user

user_router = APIRouter()


@user_router.post("/sign-up")
async def signup(user: UserCreate):
    return await create_user(user)


