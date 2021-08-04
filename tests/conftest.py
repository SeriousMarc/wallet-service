"""
Tests pre configuration
"""
import asyncio
import pytest
from httpx import AsyncClient
#
from wallet_service.app import app
from wallet_service.utils import init_models, drop_models

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop


@pytest.fixture(autouse=True)
async def db_wrapper():
    await init_models()
    yield
    await drop_models()


@pytest.fixture
async def async_client() -> AsyncClient:
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
