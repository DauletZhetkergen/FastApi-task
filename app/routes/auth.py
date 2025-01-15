from fastapi import APIRouter, Depends

from app.schemas.users import UserCreate, TokenBase, User
from app.utils.logger import get_logger
from app.utils.users import create_user, authentication
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/user")

logger = get_logger(__name__)


@user_router.post("/sign-up", summary="Creating a new user", description="Creates a new user and returns token",
                  response_model=User)
async def signup(user: UserCreate = Depends()):
    logger.info("Creating a new user")
    return await create_user(user)


@user_router.post("/auth", response_model=TokenBase, summary="Authenticating to system",
                  description="Authenticates to system and returns token")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Authenticating {form_data.username}")
    return await authentication(form_data)


