"""
API tests
"""
import pytest

from test_helper import create_user

pytestmark = pytest.mark.asyncio


async def test_create_valid_user(test_client):
    response = await create_user(test_client)

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


async def test_create_invalid_user(test_client):
    response = await test_client.post(
        '/v1/users',
        json={'username_invalid': 'invalid'}
    )
    assert response.status_code == 422


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
