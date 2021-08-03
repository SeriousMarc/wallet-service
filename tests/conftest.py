"""
Tests pre configuration
"""
import pytest
from httpx import AsyncClient

from wallet_service.app import app
from wallet_service.utils import init_models, drop_models

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope='session', autouse=True)
async def startup():
    async with AsyncClient(app=app, base_url=BASE_URL):
        await drop_models()
        await init_models()


@pytest.fixture
async def test_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        yield ac


#  TODO redo db teardown mechanism
# @pytest.fixture(scope='function', autouse=True)
# async def teardown():
#     async with AsyncClient(app=app, base_url=BASE_URL):
#         await drop_models()


# async def pytest_sessionstart(session)
# async def pytest_sessionfinish(session, exitstatus):
#     async with AsyncClient(app=app, base_url=BASE_URL):
#         await drop_models()


# @pytest.fixture
# async def app(db_uri: str) -> WebApp:
#     yield WebApp(db_uri=db_uri)
