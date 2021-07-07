
from fastapi_users.authentication import JWTAuthentication


import databases
import sqlalchemy


DATABASE = ""
database = databases.Database(DATABASE)
metadata = sqlalchemy.MetaData()

SECRET = ""
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")



