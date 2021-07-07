# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
import asyncio
import os
from typing import Generator

import pytest
import sqlalchemy

from config import metadata
from create_app import create_app
from tests.client import TestClientApi


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture(scope="session")
def generate_engine():
    DATABASE_URL = os.getenv("TEST_DB", "postgres://postgres:12345@localhost:5432/bvcstock_test")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    return engine


@pytest.fixture(autouse=True)
def create_test_database(generate_engine):
    engine = generate_engine
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture
def client(event_loop) -> Generator:
    with TestClientApi(create_app(), loop=event_loop) as c:
        yield c


