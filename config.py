from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase

from models.users import UserDB, UserModel, User, UserCreate, UserUpdate

import databases
import sqlalchemy



DATABASE = ""
database = databases.Database(DATABASE)
metadata = sqlalchemy.MetaData()

SECRET = ""
AUTH_BACKENDS = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")
]

def config_user():
    user_db = TortoiseUserDatabase(UserDB, UserModel)
    return FastAPIUsers(
        user_db,
        AUTH_BACKENDS,
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )


fastapi_users = config_user()
