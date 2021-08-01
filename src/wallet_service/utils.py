"""
App Utility
"""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from wallet_service.config import engine, Base


def session(f):
    async def wrapper(*args, **kwargs):
        async with AsyncSession(engine) as a_session:
            result = None

            try:
                result = await f(a_session, *args, **kwargs)
                await a_session.commit()
            except SQLAlchemyError:
                await a_session.rollback()
                raise SQLAlchemyError

            return result
    return wrapper


@session
async def db_hearbeat(a_session):
    hb = (await a_session.execute(select(func.count(1).label('count')))).first()
    print(f'Hearbeat: {bool(hb.count)}')


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
