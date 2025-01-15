from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base


BaseUser = declarative_base()

class UserModel(BaseUser):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    is_admin = Column(Boolean, default=False)


class TokenModel(BaseUser):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(UUID(as_uuid=False), nullable=False, unique=True, index=True, server_default=func.uuid_generate_v4())
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
