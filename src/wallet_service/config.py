"""
DB configuration
"""
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker


DB_URI = os.getenv('DB_URI', '')

engine = create_async_engine(DB_URI, future=True, echo=True)
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def session(f):
    async def wrapper(*args, **kwargs):
        async with AsyncSession(engine) as a_session:
            result = None

            try:
                result = await f(a_session, *args, **kwargs)
                await a_session.commit()
            except SQLAlchemyError:
                await a_session.rollback()

            return result
    return wrapper


