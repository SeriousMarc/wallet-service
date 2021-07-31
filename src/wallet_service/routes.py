"""
Application Routes
"""
from fastapi.routing import APIRouter

from wallet_service.views import create_user_view


router = APIRouter(redirect_slashes=False)
v1 = 'v1'

@router.post(f'{v1}/tests')
async def create_book(amount):
    return await create_user_view(amount)
