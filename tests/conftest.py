# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
import asyncio
import os
from typing import Generator

import pytest
import sqlalchemy

from config import metadata, DATABASE
from create_app import create_app
from tests.client import TestClientApi
from tests.generators import verified_user, generate_jwt


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture(scope="session")
def generate_engine():
    engine = sqlalchemy.create_engine(DATABASE)
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


@pytest.fixture
def token(client, event_loop):
    user = event_loop.run_until_complete(verified_user())
    token = event_loop.run_until_complete(generate_jwt(user))
    return token


@pytest.fixture
def headers(token):
    return {'Authorization': f'Bearer {token}'}

