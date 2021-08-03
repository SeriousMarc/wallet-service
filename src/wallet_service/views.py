"""
View Business Logic
"""
from asyncio import gather
from http import HTTPStatus

from fastapi import HTTPException

from wallet_service.repository import UserRepository, WalletRepository, TransactionRepository
from wallet_service.schemas import (
    User,
    UserWallet,
    WalletPopUp,
    Wallet as _Wallet,
    Transfer,
    TransferWallets
)
from wallet_service.models import Wallet, TransactionType
from wallet_service.utils import session


@session
async def create_client_and_wallet_view(a_session, payload: User) -> UserWallet:
    user_repo = UserRepository(a_session)
    wallet_repo = WalletRepository(a_session)

    user = await user_repo.create(payload.dict(exclude_unset=True))
    wallet = await wallet_repo.create({'user_id': user.id})

    return UserWallet(user=user, wallet=wallet)


@session
async def pop_up_wallet_view(a_session, payload: WalletPopUp) -> _Wallet:
    wallet_repo = WalletRepository(a_session)
    trx_repo = TransactionRepository(a_session)

    exists = await wallet_repo.get_balance(payload.wallet_id)

    if exists is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail='Invalid wallet')
    elif payload.amount <= 0:
        raise HTTPException(status_code=HTTPStatus.PAYMENT_REQUIRED.value, detail='Inappropriate transfer amount')

    wallet, trx = await gather(
        wallet_repo.update(
            payload.wallet_id,
            {'balance': Wallet.balance + payload.amount}
        ),
        trx_repo.create({
            'amount': payload.amount,
            'to_wallet': payload.wallet_id,
            'type': TransactionType.POP_UP.value,
            'is_success': True
        }),
    )

    return _Wallet(**wallet)


@session
async def transfer_btw_wallets_view(a_session, payload: Transfer) -> TransferWallets:
    wallet_repo = WalletRepository(a_session)
    trx_repo = TransactionRepository(a_session)

    from_balance, to_balance = await gather(
        wallet_repo.get_balance(payload.from_wallet),
        wallet_repo.get_balance(payload.to_wallet),
    )

    if from_balance is None or to_balance is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail='Invalid wallet')
    elif payload.amount > from_balance.balance or from_balance.balance <= 0:
        raise HTTPException(status_code=HTTPStatus.PAYMENT_REQUIRED.value, detail='Inappropriate transfer amount')

    from_wallet, to_wallet, _ = await gather(
        wallet_repo.update(
            payload.from_wallet,
            {'balance': Wallet.balance - payload.amount}
        ),
        wallet_repo.update(
            payload.to_wallet,
            {'balance': Wallet.balance + payload.amount}
        ),
        trx_repo.create({
            **payload.dict(include={'from_wallet', 'to_wallet', 'amount'}),
            'type': TransactionType.TRANSFER.value,
            'is_success': True
        }),
    )

    return TransferWallets(from_wallet=from_wallet, to_wallet=to_wallet)
