import hashlib
import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy import and_, select, insert

from app import database
from app.database.db import database_controller
from app.models.users import UserModel, TokenModel
from app.schemas import users as user_schema
from app.schemas.users import UserCreate, AuthData, TokenBase


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_username(username: str):
    query = select(UserModel).where(UserModel.username == username)
    return await database_controller.fetch_one(query)


async def get_user_by_token(token: str):
    query = (
        select(UserModel)  # Выбираем только username из UserModel
        .join(TokenModel, TokenModel.user_id == UserModel.id)  # Джоин по user_id
        .where(
            and_(
                TokenModel.token == token,  # Условие для токена
                TokenModel.expires > datetime.now()  # Проверка, что токен не истек
            )
        )
    )
    return await database_controller.fetch_one(query)


async def create_user_token(user_id: int):
    query = (
        insert(TokenModel)
        .values(expires=datetime.now() + timedelta(minutes=10), user_id=user_id)
        .returning(TokenModel.token, TokenModel.expires)
    )
    query_result = await database_controller.fetch_one(query)
    token_data = TokenBase(
        access_token=query_result.token,
        expires=query_result.expires
    )
    return token_data


async def create_user(user: UserCreate):
    if await get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = insert(UserModel).values(
        username=user.username,
        hashed_password=f"{salt}${hashed_password}",
        created_at=datetime.utcnow(),
        is_admin=user.admin
    )
    user_id = await database_controller.execute(query)
    token_data = await create_user_token(user_id)

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_data}


async def authentication(user_data):
    user = await get_user_by_username(user_data.username)
    if not user or not validate_password(password=user_data.password, hashed_password=user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return await create_user_token(user_id=user["id"])
