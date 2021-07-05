import asyncio

from fastapi.testclient import TestClient
from models.stock import Stock
from models.stock_value import StockValue


def test_create_stock_value(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        await Stock.objects.create(
            name="name", nemo="nemo"
        )

    event_loop.run_until_complete(add_to_db())

    response = client.post(
        "/stockvalue/", json={
            "nemo": "nemo",
            "value": 100,
            "day": "2021-01-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert str(data["day"]) == "2021-01-01"
    assert int(data["value"]) == 100
    assert "id" in data

    _id = data["id"]

    async def get_by_db():
        stock = await StockValue.objects.get(id=_id)
        return stock

    stock_value_obj = event_loop.run_until_complete(get_by_db())
    assert str(stock_value_obj.id) == _id


def test_list_stock_value(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db(name, nemo):
        return await Stock.objects.create(
            name=name, nemo=nemo
        )

    async def add_value(stock_id, value, day):
        return await StockValue.objects.create(
            stock_id=stock_id,
            value=value,
            day=day
        )

    stock_1 = event_loop.run_until_complete(add_to_db("name", "nemo"))
    stock_2 = event_loop.run_until_complete(add_to_db("name2", "nemo2"))
    event_loop.run_until_complete(add_value(stock_1.id, 10, "2021-01-01"))
    event_loop.run_until_complete(add_value(stock_1.id, 10, "2021-01-02"))
    event_loop.run_until_complete(add_value(stock_1.id, 11, "2021-01-03"))
    event_loop.run_until_complete(add_value(stock_2.id, 11, "2021-01-01"))
    event_loop.run_until_complete(add_value(stock_2.id, 11, "2021-01-04"))

    response = client.get(
        "/stockvalue/"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["stock_id"]["id"] == str(stock_1.id)
    assert str(data[0]["day"]) == str("2021-01-03")
    assert data[1]["stock_id"]["id"] == str(stock_2.id)
    assert str(data[1]["day"]) == str("2021-01-04")


def test_get_stock_value(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db(name, nemo):
        return await Stock.objects.create(
            name=name, nemo=nemo
        )

    async def add_value(stock_id, value, day):
        return await StockValue.objects.create(
            stock_id=stock_id,
            value=value,
            day=day
        )

    stock_1 = event_loop.run_until_complete(add_to_db("name", "nemo"))
    stock_2 = event_loop.run_until_complete(add_to_db("name2", "nemo2"))
    event_loop.run_until_complete(add_value(stock_1.id, 10, "2021-01-01"))
    event_loop.run_until_complete(add_value(stock_1.id, 10, "2021-01-02"))
    event_loop.run_until_complete(add_value(stock_1.id, 11, "2021-01-03"))
    event_loop.run_until_complete(add_value(stock_2.id, 11, "2021-01-01"))
    event_loop.run_until_complete(add_value(stock_2.id, 11, "2021-01-04"))

    response = client.get(
        f"/stockvalue/{stock_1.nemo}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_id"]["id"] == str(stock_1.id)
    assert data["day"] == "2021-01-03"
