from fastapi import FastAPI

from config import database, jwt_authentication, SECRET
from plugins.fastapi_users import fastapi_users
from routers import stock_router, dividend_router, stock_value_router, stock_data_router


def init_db(app):
    app.state.database = database

    @app.on_event("startup")
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()


def register_routers(app):
    app.include_router(stock_router)
    app.include_router(stock_value_router)
    app.include_router(dividend_router)
    app.include_router(stock_data_router)

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication, requires_verification=True),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(SECRET),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(),
        prefix="/users",
        tags=["users"],
    )


def create_app():
    app = FastAPI()
    init_db(app)
    register_routers(app)
    return app
