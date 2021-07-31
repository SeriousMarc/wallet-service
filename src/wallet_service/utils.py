"""
App Utility
"""
from sqlalchemy import select, func

from wallet_service.config import session


@session
async def db_hearbeat(a_session):
    hb = (await a_session.execute(select(func.count(1).label('count')))).first()
    print(f'Hearbeat: {bool(hb.count)}')
