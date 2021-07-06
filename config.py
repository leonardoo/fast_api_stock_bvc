from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import OrmarUserDatabase

import databases
import sqlalchemy


DATABASE = ""
database = databases.Database(DATABASE)
metadata = sqlalchemy.MetaData()

SECRET = ""
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")


def config_user():
    from models.users import UserDB, UserModel, User, UserCreate, UserUpdate
    user_db = OrmarUserDatabase(UserDB, UserModel)
    return FastAPIUsers(
        user_db,
        [jwt_authentication],
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )
