"""
App Utility
"""
import simplejson as json

from contextlib import suppress
from json import JSONDecodeError

from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
from pydantic.error_wrappers import ValidationError
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from wallet_service import SECRET
from wallet_service.config import engine, Base
from wallet_service.schemas import Transfer


def session(f):
    async def wrapper(*args, **kwargs):
        async with AsyncSession(engine) as a_session:
            result = None

            try:
                result = await f(a_session, *args, **kwargs)
                await a_session.commit()
            except SQLAlchemyError as e:
                await a_session.rollback()

            return result
    return wrapper


@session
async def db_hearbeat(a_session):
    hb = (await a_session.execute(select(func.count(1).label('count')))).first()
    print(f'Hearbeat: {bool(hb.count)}')


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def dencrypt_payload(key: bytes, token: bytes) -> dict:
    with suppress(TypeError, InvalidToken, JSONDecodeError):
        f = Fernet(key)

        return json.loads(f.decrypt(token), use_decimal=True)


def encrypt_payload(key: bytes, payload: dict) -> bytes:
    with suppress(TypeError, InvalidSignature, JSONDecodeError):
        f = Fernet(key)

        return f.encrypt(json.dumps(payload, use_decimal=True).encode('utf-8'))


def validate_payload(payload: dict) -> Transfer:
    with suppress(TypeError, ValidationError):
        return Transfer(**payload)
