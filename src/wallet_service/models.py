"""
DB models
"""
from decimal import Decimal
from enum import IntEnum

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    BigInteger,
    String,
    ForeignKey,
    SmallInteger,
    Boolean,
)

from wallet_service.config import Base


class Currency(IntEnum):
    USD = 1


class TransactionType(IntEnum):
    POP_UP = 1
    TRANSFER = 2


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False, unique=True)
    amount = Column(Numeric, nullable=True, default=Decimal(0))
    currency = Column(SmallInteger, nullable=False, default=Currency.USD.value)


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(BigInteger, primary_key=True)
    from_wallet = Column(ForeignKey(Wallet.id), nullable=True)
    to_wallet = Column(ForeignKey(Wallet.id), nullable=False)
    amount = Column(Numeric, nullable=False)
    type = Column(SmallInteger, nullable=False)
    is_success = Column(Boolean, nullable=False, default=False)
