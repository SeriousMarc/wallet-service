import pytest
from httpx import AsyncClient

from wallet_service.app import app
from wallet_service.utils import init_models, drop_models

pytestmark = pytest.mark.asyncio
BASE_URL = "http://localhost:8000"
# 1. try fixture db
# 2. try flow without create delete


@pytest.fixture(autouse=True)
async def startup():
    async with AsyncClient(app=app, base_url=BASE_URL):
        await drop_models()
        await init_models()


# @pytest.fixture(scope='function', autouse=True)
# async def teardown():
#     async with AsyncClient(app=app, base_url=BASE_URL):
#         await drop_models()


# async def pytest_sessionfinish(session, exitstatus):
#     async with AsyncClient(app=app, base_url=BASE_URL):
#         await drop_models()

@pytest.fixture
async def app(db_uri: str) -> WebApp:
    yield WebApp(db_uri=db_uri)


@pytest.fixture
async def test_client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


def db(f):
    async def wrapper(*args, **kwargs):
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            await init_models()
            await f(ac, *args, **kwargs)
            # await drop_models()

    return wrapper


async def create_user(ac):
    return await ac.post(
        '/v1/users',
        json={'username': 'test'}
    )


# @db
async def test_create_valid_user():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await create_user(ac)

        assert response.status_code == 201
        assert response.json() == {
            "user": {
                "id": 1,
                "username": "test"
            },
            "wallet": {
                "id": 1,
                "balance": 0
            }
        }




# @pytest.mark.asyncio
# @db
# async def test_create_invalid_user(ac):
#     response = await ac.post(
#         '/v1/users',
#         json={'username_invalid': 'invalid'}
#     )
#     assert response.status_code == 422
#
#
# @pytest.mark.asyncio
# @db
# async def test_wallet_pop_up_positive_amount(ac):
#     await create_user(ac)
#     response = await ac.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 1, 'amount': '123.123'}
#     )
#     assert response.status_code == 200
#
#
# @pytest.mark.asyncio
# @db
# async def test_wallet_pop_up_negative_amount(ac):
#     await create_user(ac)
#     response = await ac.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 1, 'amount': '-123.123'}
#     )
#     assert response.status_code == 402
#
#
# @pytest.mark.asyncio
# @db
# async def test_invalid_wallet_pop_up(ac):
#     await create_user(ac)
#     response = await ac.put(
#         '/v1/wallets/pop-up',
#         json={'wallet_id': 999, 'amount': '123.123'}
#     )
#     assert response.status_code == 404
#
#
# @pytest.mark.asyncio
# @db
# async def test_wallet_pop_up_balance_precision(ac):
#     await create_user(ac)
#     response = None
#
#     for _ in range(3):
#         response = await ac.put(
#             '/v1/wallets/pop-up',
#             json={'wallet_id': 1, 'amount': '0.1'}
#         )
#
#     assert response is not None
#     assert response.json().get('balance') == 0.3
#     # check balance by repository
