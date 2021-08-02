"""
Validation Schemas
"""
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import BaseModel, validator, ValidationError


class User(BaseModel):
    id: Optional[int]
    username: str


class Wallet(BaseModel):
    id: int
    balance: Decimal


class UserWallet(BaseModel):
    user: User
    wallet: Wallet


class WalletPopUp(BaseModel):
    wallet_id: int
    amount: Decimal


class Transfer(BaseModel):
    from_wallet: int
    to_wallet: int
    amount: Decimal


class TransferWallets(BaseModel):
    from_wallet: Wallet
    to_wallet: Wallet
