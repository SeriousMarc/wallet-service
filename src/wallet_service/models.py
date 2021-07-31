"""
DB models
"""
from sqlalchemy import Column, Integer, Numeric

from wallet_service.config import Base


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)
