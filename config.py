import os

from fastapi_users.authentication import JWTAuthentication

import databases
import sqlalchemy


origins = ["*"]

DATABASE = os.getenv("URL_DB")
database = databases.Database(DATABASE)
metadata = sqlalchemy.MetaData()

SECRET = os.getenv("SECRET_KEY")
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")



