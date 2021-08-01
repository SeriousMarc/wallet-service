"""
Data Access Layer
"""
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select, update, insert, literal_column
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from wallet_service.models import Test, User, Base, Wallet


class TestRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_test(self, test: dict) -> dict:
        record =  await self.db_session.execute(
            insert(Test).values(**test)
        )

        if record.is_insert is False:
            raise SQLAlchemyError('Insertion failed')

        return test

    async def pop_up_amount(self, user_id: int, amount: Decimal):
        q = update(Test).where(Test.id == user_id).values(amount=amount)
        await self.db_session.execute(q)


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


class WalletRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Wallet)

    async def update(self, user_id: int, data: dict) -> dict:
        record = await self.db_session.execute(
            update(self.model).where(
                self.model.user_id == user_id
            ).values(**data).returning(literal_column('*'))
        )

        return record.first()

    async def get_amount(self, user_id: int) -> dict:
        record = await self.db_session.execute(
            select(self.model.amount).where(
                self.model.user_id == user_id
            ).limit(1)
        )

        return record.first()