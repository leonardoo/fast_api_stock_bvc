
import asyncio

from fastapi.testclient import TestClient
from models.stock import Stock
from models.stock_dividends import StockDividends


def test_create_stock_dividend(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        return await Stock.objects.create(
            name="name", nemo="nemo"
        )

    stock = event_loop.run_until_complete(add_to_db())

    response = client.post(
        "/dividends/", json={
            "nemo": stock.nemo,
            "currency": "COP",
            "total": 10,
            "paid_amount": 10,
            "ex_dividend_date": "2021-01-01",
            "paid_at": "2021-01-03"

        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_id"]["id"] == str(stock.id)
    assert data["currency"] == "COP"
    assert data["ex_dividend_date"] == "2021-01-01"
    assert data["paid_at"] == "2021-01-03"
    assert int(data["total"]) == 10
    assert int(data["paid_amount"]) == 10
    assert "id" in data

    _id = data["id"]

    async def get_by_db(pk):
        return await StockDividends.objects.get(id=pk)

    obj = event_loop.run_until_complete(get_by_db(_id))
    assert str(obj.id) == _id


def test_list_stock_dividend(client: TestClient, event_loop: asyncio.AbstractEventLoop, monkeypatch):  # nosec
    monkeypatch.setattr("routers.stock_dividends", 2021)

    async def add_to_db():
        return await Stock.objects.create(
            name="name", nemo="nemo"
        )

    async def add_dividends_to_db(stock_id, ex_dividend_date, paid_at, total, paid_amount, currency="COP"):
        data = {**locals()}
        return await StockDividends.objects.create(
            **data
        )

    stock = event_loop.run_until_complete(add_to_db())
    event_loop.run_until_complete(add_dividends_to_db(str(stock.id), "2021-01-01", "2021-01-03", 20, 10))
    event_loop.run_until_complete(add_dividends_to_db(str(stock.id), "2021-07-01", "2021-07-03", 20, 10))
    event_loop.run_until_complete(add_dividends_to_db(str(stock.id), "2022-01-01", "2022-01-03", 20, 10))

    response = client.get("/dividends/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["ex_dividend_date"] == "2021-01-01"
    assert data[1]["ex_dividend_date"] == "2021-07-01"
