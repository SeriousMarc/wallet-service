"""
Tests help functions
"""
from httpx import AsyncClient, Response
from decimal import Decimal

from wallet_service import SECRET
from wallet_service.utils import encrypt_payload


async def create_user(ac: AsyncClient, username='test') -> Response:
    return await ac.post(
        '/v1/users',
        json={'username': username}
    )


async def pop_up_wallet(ac: AsyncClient, amount: Decimal = Decimal(300)) -> Response:
    return await ac.put(
        '/v1/wallets/pop-up',
        json={'wallet_id': 1, 'amount': str(amount)}
    )


def make_transfer_token(amount: Decimal = Decimal(50)) -> bytes:
    payload = {
        'from_wallet': 1,
        'to_wallet': 2,
        'amount': amount
    }

    return encrypt_payload(SECRET, payload)


async def prepare_transfer_data(async_client: AsyncClient):
    await create_user(async_client)
    await create_user(async_client, username='test1')
    await pop_up_wallet(async_client)


async def transfer_client(async_client: AsyncClient, amount: Decimal) -> Response:
    await prepare_transfer_data(async_client)

    token = make_transfer_token(amount)
    return await async_client.put(
        '/v1/wallets/transfer',
        json={'token': str(token, 'utf-8')}
    )
