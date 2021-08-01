"""
View Business Logic
"""
from asyncio import gather

from fastapi import HTTPException

from wallet_service.repository import TestRepository, BaseRepository, WalletRepository
from wallet_service.schemas import Test, User as UserSchema, WalletPopUp, Transfer, TransferWallets
from wallet_service.models import User, Wallet
from wallet_service.utils import session


@session
async def create_test_view(a_session, test: Test) -> Test:
    async with a_session.begin():
        repo = TestRepository(a_session)

        return Test(**(await repo.create_test(test.dict())))


@session
async def create_client_and_wallet_view(a_session, user: UserSchema) -> UserSchema:
    user_repo = BaseRepository(a_session, User)
    wallet_repo = WalletRepository(a_session)

    user = await user_repo.create(user.dict(exclude_unset=True))
    wallet = await wallet_repo.create({'user_id': user.id})

    return UserSchema(**user)



@session
async def pop_up_wallet_view(a_session, payload: WalletPopUp) -> WalletPopUp:
    wallet_repo = WalletRepository(a_session)

    wallet = await wallet_repo.update(
        payload.user_id,
        {'amount': Wallet.amount + payload.amount}
    )

    return WalletPopUp(**wallet)


@session
async def transfer_btw_wallets_view(a_session, payload: Transfer) -> TransferWallets:
    wallet_repo = WalletRepository(a_session)

    amount = await wallet_repo.get_amount(payload.from_user)

    if amount is None or payload.amount > amount.amount or amount.amount <= 0:
        raise HTTPException(status_code=402, detail="Inappropriate wallet balance")

    from_wallet, to_wallet = await gather(
        wallet_repo.update(
            payload.from_user,
            {'amount': Wallet.amount - payload.amount}
        ),
        wallet_repo.update(
            payload.to_user,
            {'amount': Wallet.amount + payload.amount}
        )
    )


    return TransferWallets(from_wallet=from_wallet, to_wallet=to_wallet)
