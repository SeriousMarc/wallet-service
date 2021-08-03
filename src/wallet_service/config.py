"""
DB configuration
"""
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


DB_URI = os.getenv('DB_URI', 'postgresql+asyncpg://test:test@localhost:5432/test')

engine = create_async_engine(DB_URI, future=True, echo=True)
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()
