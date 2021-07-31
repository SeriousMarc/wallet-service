"""
Data Access Layer
"""
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from wallet_service.models import Test


class TestRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_test(self, amount: Decimal):
        test = Test(amount=amount)
        self.db_session.add(test)
        await self.db_session.flush()

    async def pop_up_amount(self, user_id: int, amount: Decimal):
        q = update(Test).where(Test.id == user_id).values(amount=amount)
        await self.db_session.execute(q)
