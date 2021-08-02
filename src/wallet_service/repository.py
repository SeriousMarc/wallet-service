"""
Data Access Layer
"""
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select, update, insert, literal_column, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from wallet_service.models import Base, User, Wallet, Transaction


class BaseRepository:
    def __init__(self, db_session: Session, model: Base):
        self.db_session = db_session
        self.model = model

    async def create(self, data: dict) -> dict:
        record =  await self.db_session.execute(
            insert(self.model).values(**data).returning(literal_column('*'))
        )

        if record.is_insert is False:
            raise SQLAlchemyError('Insertion failed')

        return record.first()


class UserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = User


class WalletRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Wallet)

    async def update(self, wallet_id: int, data: dict) -> dict:
        record = await self.db_session.execute(
            update(self.model).where(
                self.model.id == wallet_id
            ).values(**data).returning(literal_column('*'))
        )

        return record.first()

    async def get_balance(self, wallet_id: int) -> dict:
        record = await self.db_session.execute(
            select(self.model.balance).where(
                self.model.id == wallet_id
            ).limit(1)
        )

        return record.first()


class TransactionRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = Transaction
