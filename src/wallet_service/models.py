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
    DateTime,
    func,
)

from wallet_service.config import Base


class Currency(IntEnum):
    USD = 1


class TransactionType(IntEnum):
    POP_UP = 1
    TRANSFER = 2


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False)


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False, unique=True)
    balance = Column(Numeric, nullable=True, default=Decimal(0))
    currency = Column(SmallInteger, nullable=False, default=Currency.USD.value)


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(BigInteger, primary_key=True)
    stamp = Column(DateTime(timezone=True), server_default=func.now())
    from_wallet = Column(ForeignKey(Wallet.id), nullable=True)
    to_wallet = Column(ForeignKey(Wallet.id), nullable=False)
    amount = Column(Numeric, nullable=False)
    type = Column(SmallInteger, nullable=False)
    is_success = Column(Boolean, default=False)
