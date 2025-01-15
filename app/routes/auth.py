from fastapi import APIRouter,Depends
from app.schemas.users import UserCreate, TokenBase, AuthData, UserBase, User
from app.utils.dependecies import get_current_user
from app.utils.users import create_user, authentication
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()


@user_router.post("/sign-up")
async def signup(user: UserCreate = Depends()):
    return await create_user(user)

@user_router.post("/auth",response_model=TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    return await authentication(form_data)

@user_router.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: User = Depends(get_current_user)):
    print(current_user)
    return current_user



