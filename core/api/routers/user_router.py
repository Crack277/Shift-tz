from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.user_schemas import UserCreate
from core.api.services.user_service import UserService
from core.config import settings
from core.database_helper import db_helper

router = APIRouter(prefix=settings.api.v1.users, tags=["USERS"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_dependency)):
    """Получить список всех пользователей"""
    service = UserService(session)
    return await service.get_users()


@router.get("/{user_id}/")
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить пользователя по ID"""
    service = UserService(session)
    return await service.get_user_by_id(user_id=user_id)


@router.post("/")
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Регистрация нового пользователя"""
    service = UserService(session)
    return await service.create_user(user_in=user_in)
