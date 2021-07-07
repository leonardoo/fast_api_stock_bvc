import uuid

from fastapi_users.password import get_password_hash

from config import jwt_authentication
from models.users import UserModel


async def verified_user() -> UserModel:
    user = UserModel(
        id=uuid.uuid4(),
        email="test@test.com",
        hashed_password=get_password_hash("12345"),
        is_active=True,
        is_verified=True,
    )
    await user.save()
    return user


async def generate_jwt(user):
    return await jwt_authentication._generate_token(user)
