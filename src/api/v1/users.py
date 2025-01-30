from fastapi import APIRouter, Depends
from src.models.user import User
from src.services.auth import AuthService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_users(
    current_user: User = Depends(AuthService.get_current_user)
):
    return current_user
