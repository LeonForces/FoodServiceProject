from fastapi import APIRouter, Depends, Request

from src.models.user import User
from src.services.auth import AuthService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_users(
    current_user: User = Depends(AuthService.get_current_user)
):
    return current_user


@router.get("/items")
async def get_items(request: Request):
    request.session['user'] = dict({'user': 'abubakir_user'})
    return request.json()
