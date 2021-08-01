"""
Application Routes
"""
from decimal import Decimal

from fastapi import Response
from fastapi.routing import APIRouter
from http import HTTPStatus

from wallet_service.views import (
    create_test_view,
    create_client_and_wallet_view,
    pop_up_wallet_view,
    transfer_btw_wallets_view,
)
from wallet_service.schemas import Test, User, WalletPopUp, Transfer, TransferWallets

router = APIRouter(redirect_slashes=False)
v1 = '/v1'


@router.post(f'{v1}/tests')
async def create_test(test: Test) -> Test:
    return await create_test_view(test)


@router.post(f'{v1}/users')
async def create_user(user: User) -> User:
    return await create_client_and_wallet_view(user)


@router.patch(f'{v1}/wallets/pop-up')
async def pop_up_wallet(payload: WalletPopUp) -> WalletPopUp:
    return await pop_up_wallet_view(payload)


@router.patch(f'{v1}/wallets/transfer')
async def wallets_transfer(payload: Transfer) -> TransferWallets:
    return await transfer_btw_wallets_view(payload)
