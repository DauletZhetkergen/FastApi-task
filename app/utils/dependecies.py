from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.users import UserModel
from app.utils.logger import get_logger
from app.utils.users import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/auth")

logger = get_logger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await get_user_by_token(token)
    if not user:
        logger.warn("Unauthorized ping")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def check_admin_role(current_user: UserModel = Depends(get_current_user)):
    logger.info("Check admin role")
    if not current_user.is_admin:
        logger.warn(f"{current_user.id} tried admin routes")
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
