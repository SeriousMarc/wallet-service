"""
API tests
"""
import pytest

from decimal import Decimal
from http import HTTPStatus

from test_helper import create_user, transfer_client, make_transfer_token, prepare_transfer_data

BASE_URL = "http://localhost:8000"
pytestmark = pytest.mark.asyncio


async def test_create_valid_user(async_client):
    response = await create_user(async_client)

    assert response.status_code == HTTPStatus.CREATED
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
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_wallet_pop_up_positive_amount(async_client):
    await create_user(async_client)
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 1, 'amount': '123.123'}
    )
    assert response.status_code == HTTPStatus.OK


async def test_wallet_pop_up_negative_amount(async_client):
    await create_user(async_client)
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 1, 'amount': '-123.123'}
    )
    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


async def test_invalid_wallet_pop_up(async_client):
    response = await async_client.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 999, 'amount': '123.123'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_wallet_pop_up_balance_precision(async_client):
    await create_user(async_client)
    response = None

    for _ in range(3):
        response = await async_client.put(
            '/v1/wallets/pop-up',
            json={'wallet_id': 1, 'amount': '0.1'}
        )

    # assert response is not None
    assert response.json().get('balance') == 0.3
    # check balance by repository


async def test_valid_transfer_btw_wallets(async_client):
    await prepare_transfer_data(async_client)

    token = make_transfer_token()
    response = await async_client.put(
        '/v1/wallets/transfer',
        json={'token': str(token, 'utf-8')}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['from_wallet']['balance'] == 250
    assert response.json()['to_wallet']['balance'] == 50


async def test_zero_amount_transfer_btw_wallets(async_client):
    response = await transfer_client(async_client, Decimal('0'))  # zero amount

    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


async def test_negative_balance_transfer_btw_wallets(async_client):
    response = await transfer_client(async_client, Decimal('-350'))  # negative balance

    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


async def test_amount_gt_balance_transfer_btw_wallets(async_client):
    response = await transfer_client(async_client, Decimal('350'))  # balance < amount

    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


async def test_amount_lte_balance_transfer_btw_wallets(async_client):
    response = await transfer_client(async_client, Decimal('300'))   # balance >= amount

    assert response.status_code == HTTPStatus.OK


async def test_amount_precision_gt_balance_transfer_btw_wallets(async_client):
    response = await transfer_client(async_client, Decimal('300.00000004'))  # amount precision > balance

    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED
