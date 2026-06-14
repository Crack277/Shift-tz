from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.user_schemas import UserAuthorize
from core.api.services.auth_service import AuthService
from core.api.utils import safety
from core.config import settings
from core.database_helper import db_helper
from core.models import User

router = APIRouter(prefix=settings.api.v1.auth, tags=["AUTH"])


@router.post("/")
async def login_user(
    user_in: UserAuthorize,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Аутентификация пользователя.
    Принимает логин и пароль, возвращает JWT токен.
    """
    service = AuthService(session)
    return await service.login_user(user_in=user_in)


@router.get("/me")
async def get_auth_user(
    current_user: User = Depends(safety.get_current_user),
):
    """
    Получить информацию о текущем авторизованном пользователе.
    """
    return current_user
