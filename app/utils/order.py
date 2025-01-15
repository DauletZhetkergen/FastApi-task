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