"""
View Business Logic
"""
from wallet_service.repository import TestRepository
from wallet_service.config import session


@session
async def create_user_view(a_session, payload: dict):
    async with a_session.begin():
        repo = TestRepository(session)
        # validate payload
        return await repo.create_test(**payload)
