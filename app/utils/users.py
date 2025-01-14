import hashlib
import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import and_, select, insert

from app import database
from app.database.db import database_controller
from app.models.users import User, Token
from app.schemas import users as user_schema
from app.schemas.users import UserCreate


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


async def check_for_username(username: str):
    query = select(User).where(User.username == username)
    return await database_controller.fetch_one(query)


async def get_user_by_token(token: str):
    query = Token.join(User).select().where(
        and_(
            Token.token == token,
            Token.expires > datetime.now()
        )
    )
    return await database_controller.fetch_one(query)


async def create_user_token(user_id: int):
    query = (
        insert(Token)
        .values(expires=datetime.now() + timedelta(minutes=10), user_id=user_id)
        .returning(Token.token, Token.expires)
    )

    return await database_controller.fetch_one(query)


async def create_user(user: UserCreate):
    if await check_for_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = insert(User).values(
        username=user.username,
        hashed_password=f"{salt}${hashed_password}",
        created_at=datetime.utcnow(),
        is_admin=user.admin
    )
    user_id = await database_controller.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}
