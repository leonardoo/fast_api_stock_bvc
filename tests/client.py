import asyncio

import typing
from fastapi.testclient import TestClient


class TestClientApi(TestClient):

    def __init__(
        self,
        app,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
        loop=None
    ) -> None:
        super().__init__(app, base_url, raise_server_exceptions, root_path)
        self.loop = loop or asyncio.get_event_loop()

    def __enter__(self) -> "TestClient":
        self.send_queue = asyncio.Queue()  # type: asyncio.Queue
        self.receive_queue = asyncio.Queue()  # type: asyncio.Queue
        self.task = self.loop.create_task(self.lifespan())
        self.loop.run_until_complete(self.wait_startup())
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self.loop.run_until_complete(self.wait_shutdown())
