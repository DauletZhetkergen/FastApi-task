from fastapi import APIRouter,Depends

from app.schemas.users import UserCreate, TokenBase, UserBase, User
from app.utils.dependecies import get_current_user
from app.utils.logger import get_logger
from app.utils.users import create_user, authentication
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()

logger = get_logger(__name__)

@user_router.post("/sign-up")
async def signup(user: UserCreate = Depends()):
    logger.info("Creating a new user")
    return await create_user(user)

@user_router.post("/auth",response_model=TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Authenticating {form_data.username}")
    return await authentication(form_data)




