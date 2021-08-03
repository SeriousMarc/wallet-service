"""
Tests help functions
"""
# from httpx import AsyncClient
#
# from wallet_service.utils import init_models, drop_models
# from wallet_service.app import app


async def create_user(ac, username='test'):
    return await ac.post(
        '/v1/users',
        json={'username': username}
    )


# def db(f):
#     async def wrapper(*args, **kwargs):
#         async with AsyncClient(app=app, base_url=BASE_URL) as ac:
#             await init_models()
#             await f(ac, *args, **kwargs)
#             await drop_models()
#
#     return wrapper
