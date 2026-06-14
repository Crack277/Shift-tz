import time
import jwt

from jwt import ExpiredSignatureError, InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database_helper import db_helper
from core.api.schemas.user_schemas import PrintToken
from core.config import settings
from core.models import User

security = HTTPBearer()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(user: User):
    """
    Создает JWT токен для пользователя.
    """

    current_time = int(time.time())
    expire_time = current_time + settings.token.expire_time * 60

    encode_data = {
        "user_id": user.id,
        "login": user.login,
        "exp": expire_time,
        "created_at": current_time,
    }
    token = jwt.encode(
        encode_data, 
        settings.token.secret_key, 
        settings.token.algorithm
    )

    message = PrintToken(access_token=token)

    return message


async def get_current_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    credential: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Dependency для получения текущего аутентифицированного пользователя.
    Проверяет JWT токен и возвращает пользователя из БД.
    """
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не авторизирован!",
        )

    try:
        payload = jwt.decode(
            credential.credentials,
            settings.token.secret_key,
            algorithms=[settings.token.algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен",
        )

    current_id = payload.get("user_id")
    if current_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
        )

    stmt = select(User).where(User.id == current_id)
    user = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден!",
        )

    return user
