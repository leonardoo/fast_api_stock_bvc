from config import jwt_authentication

def config_user():
    from fastapi_users.db import OrmarUserDatabase
    from fastapi_users import FastAPIUsers
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

fastapi_users = config_user()
