"""
Validation Schemas
"""
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import BaseModel, validator, ValidationError


class Test(BaseModel):
    id: int
    amount: Decimal


class User(BaseModel):
    id: Optional[int]
    name: str


class WalletPopUp(BaseModel):
    user_id: int
    amount: Decimal


class Transfer(BaseModel):
    from_user: int
    to_user: int
    amount: Decimal


class TransferWallets(BaseModel):
    from_wallet: WalletPopUp
    to_wallet: WalletPopUp
