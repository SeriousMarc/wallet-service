"""
API tests
"""
import pytest

from httpx import AsyncClient

from wallet_service.app import app
from test_helper import create_user

BASE_URL = "http://localhost:8000"
pytestmark = pytest.mark.asyncio


async def test_create_valid_user(async_client):
    response = await create_user(async_client)

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


async def test_create_invalid_user(async_client):
    response = await async_client.post(
        '/v1/users',
        json={'username_invalid': 'invalid'}
    )
    assert response.status_code == 422


async def test_wallet_pop_up_positive_amount(async_client):
    await create_user(async_client)
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 1, 'amount': '123.123'}
    )
    assert response.status_code == 200


async def test_wallet_pop_up_negative_amount(async_client):
    await create_user(async_client)
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 1, 'amount': '-123.123'}
    )
    assert response.status_code == 402


async def test_invalid_wallet_pop_up(async_client):
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 999, 'amount': '123.123'}
    )
    assert response.status_code == 404


async def test_wallet_pop_up_balance_precision(async_client):
    await create_user(async_client, username='test1')
    response = None

    for _ in range(3):
        response = await async_client.put(
            '/v1/wallets/pop-up',
            json={'wallet_id': 1, 'amount': '0.1'}
        )

    assert response is not None
    assert response.json().get('balance') == 0.3
    # check balance by repository
