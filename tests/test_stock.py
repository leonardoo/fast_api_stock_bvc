
import asyncio

from fastapi.testclient import TestClient
from models.stock import Stock


def test_create_stock(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    response = client.post(
        "/stock/", json={
            "name": "stock_test",
            "nemo": "1234",

        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "stock_test"
    assert data["nemo"] == "1234"
    assert "id" in data

    _id = data["id"]

    async def get_by_db(pk):
        return await Stock.objects.get(id=pk)

    stock_obj = event_loop.run_until_complete(get_by_db(_id))
    assert str(stock_obj.id) == _id


def test_list_stock(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        await Stock.objects.create(
            name="name", nemo="nemo"
        )

    event_loop.run_until_complete(add_to_db())

    response = client.get(
        "/stock/"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "name"
    assert data[0]["nemo"] == "nemo"


def test_get_stock(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        await Stock.objects.create(
            name="name", nemo="nemo"
        )

    event_loop.run_until_complete(add_to_db())

    response = client.get(
        "/stock/"
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "name"
    assert data[0]["nemo"] == "nemo"


def test_delete_stock(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        return await Stock.objects.create(
            name="name", nemo="nemo"
        )

    stock = event_loop.run_until_complete(add_to_db())

    response = client.delete(
        f"/stock/{stock.id}"
    )
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == f"Deleted stock {stock.id}"


def test_update_stock(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    async def add_to_db():
        return await Stock.objects.create(
            name="name", nemo="nemo"
        )

    stock = event_loop.run_until_complete(add_to_db())

    response = client.post(
        f"/stock/{stock.id}", json={
            "name": "stock_test",
            "nemo": "1234",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "stock_test"
    assert data["nemo"] == "1234"
    assert data["id"] == str(stock.id)

    async def get_by_db(pk):
        return await Stock.objects.get_or_none(id=pk)

    stock_obj = event_loop.run_until_complete(get_by_db(data["id"]))
    assert str(stock_obj.id) == data["id"]
    assert str(stock_obj.name) == "stock_test"