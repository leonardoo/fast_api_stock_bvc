from fastapi_users import models
from fastapi_users.db import OrmarBaseUserModel

from models.base import BaseMeta


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserModel(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "users"


