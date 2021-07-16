import asyncio

from fastapi.testclient import TestClient

from models.portfolio import Portfolio, OperationStockEnum, PortfolioStock
from models.stock import Stock
from models.users import UserModel


def test_portfolio_stock(client: TestClient, headers: dict, event_loop: asyncio.AbstractEventLoop):  # nosec

    response = client.post(
        "/portfolio/", json={
            "name": "trii",
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "trii"
    assert data["last_value"] == 0
    assert "id" in data

    _id = data["id"]

    async def get_by_db(pk):
        return await Portfolio.objects.get(id=pk)

    obj = event_loop.run_until_complete(get_by_db(_id))
    assert str(obj.id) == _id


def test_get_portfolio_stock_user(client: TestClient, headers: dict, event_loop: asyncio.AbstractEventLoop, token):  # nosec
    async def generate_portfolio_by_user():
        users = await UserModel.objects.all()
        for i, user in enumerate(users):
            await Portfolio.objects.create(owner=user, name=f"portfolio {i}")

    event_loop.run_until_complete(generate_portfolio_by_user())

    response = client.get(
        "/portfolio/",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "portfolio 0"


def test_add_stock_to_portfolio(client: TestClient, headers: dict, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        return await Stock.objects.create(
            name="name", nemo="nemo"
        )

    stock = event_loop.run_until_complete(add_to_db())

    async def generate_portfolio_by_user():
        user = await UserModel.objects.first()
        return await Portfolio.objects.create(owner=user, name=f"portfolio")

    portfolio = event_loop.run_until_complete(generate_portfolio_by_user())

    response = client.post(
        f"/portfolio/{portfolio.id}/add",
        json={
            "nemo": stock.nemo,
            "operation": OperationStockEnum.buy.value,
            "portfolio": str(portfolio.id),
            "value_by_stock": 10,
            "amount": 10,
            "commission": 0
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_id"]["id"] == str(stock.id)
    assert data["portfolio"]["id"] == str(portfolio.id)
    assert int(data["amount"]) == 10
    assert int(data["value_by_stock"]) == 10

    async def get_by_db(stock_id, portfolio_id):
        return await PortfolioStock.objects.get_or_none(
            stock_id=stock_id, portfolio=portfolio_id
        )

    stock = event_loop.run_until_complete(get_by_db(
        data["stock_id"]["id"], data["portfolio"]["id"]
    ))
    assert int(stock.amount) == 10
    assert str(stock.owner.id) == data["created_by"]["id"]