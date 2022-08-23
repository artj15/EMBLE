import os

import pytest
from asgi_lifespan import LifespanManager
from async_asgi_testclient import TestClient  # type: ignore
from fastapi import (
    FastAPI,
)

from misc import config
from misc.ctrl import CONFIG_ENV_KEY
from services.main import factory


@pytest.fixture
async def app():
    instance = factory()
    async with LifespanManager(instance):
        yield instance


@pytest.fixture
async def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
async def db_pool(app: FastAPI):
    return app.state.db_pool


@pytest.fixture
async def conf():
    config_path = os.environ[CONFIG_ENV_KEY]
    return config.read_config(config_path)
