import asyncio

from fastapi.testclient import TestClient
from models.stock import Stock
from models.stock_dividends import StockDividends
from models.stock_value import StockValue


def test_create_stock_data(client: TestClient, headers: dict, event_loop: asyncio.AbstractEventLoop):  # nosec

    #stock = event_loop.run_until_complete(add_to_db())

    response = client.post(
        "/stock/data/", json={
            "name": "name",
            "nemo": "nemo",
            "day": "2021-01-01",
            "value": 10,
            "currency": "COP",
            "total": 10,
            "paid_amount": 10,
            "ex_dividend_date": "2021-01-01",
            "paid_at": "2021-01-03"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Created data for stock nemo"

    async def get_stock():
        return await Stock.objects.first()

    obj = event_loop.run_until_complete(get_stock())
    assert str(obj.nemo) == "nemo"

    async def get_stock_value_count():
        return await StockValue.objects.count()

    assert event_loop.run_until_complete(get_stock_value_count()) == 1

    async def get_stock_dividends_count():
        return await StockDividends.objects.count()

    assert event_loop.run_until_complete(get_stock_dividends_count()) == 1
