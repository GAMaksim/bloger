"""
API Dependencies
================
FastAPI dependencies для инъекции в эндпоинты.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import (
    CredentialsException,
    InactiveUserException,
    PermissionDeniedException,
    TokenBlacklistedException,
    UnverifiedEmailException,
)
from app.core.security import decode_token
from app.db.redis import is_blacklisted
from app.db.session import get_db
from app.models.user import User, UserRole


# Bearer token схема
security = HTTPBearer(auto_error=False)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security)
    ],
) -> User:
    """
    Получить текущего аутентифицированного пользователя.
    
    Проверяет:
    1. Наличие токена
    2. Валидность токена
    3. Не в blacklist
    4. Пользователь существует
    5. Пользователь активен
    
    Использование:
        @router.get("/me")
        async def get_me(user: User = Depends(get_current_user)):
            return user
    """
    if credentials is None:
        raise CredentialsException("Authorization header missing")
    
    token = credentials.credentials
    
    # Декодируем токен
    payload = decode_token(token)
    if payload is None:
        raise CredentialsException("Invalid token")
    
    # Проверяем тип токена
    if payload.get("type") != "access":
        raise CredentialsException("Invalid token type")
    
    # Проверяем blacklist
    if await is_blacklisted(token):
        raise TokenBlacklistedException()
    
    # Получаем user_id
    user_id = payload.get("sub")
    if user_id is None:
        raise CredentialsException("Invalid token payload")
    
    # Ищем пользователя
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise CredentialsException("Invalid user ID")
    
    result = await db.execute(
        select(User).where(User.id == user_uuid)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise CredentialsException("User not found")
    
    if not user.is_active:
        raise InactiveUserException()
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Получить активного пользователя.
    Алиас для get_current_user с явной проверкой.
    """
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


async def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Получить пользователя с подтверждённым email.
    Для операций требующих верификации.
    """
    if not current_user.is_verified:
        raise UnverifiedEmailException()
    return current_user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Получить пользователя-администратора.
    Для защиты админских эндпоинтов.
    
    Использование:
        @router.delete("/users/{id}")
        async def delete_user(admin: User = Depends(get_current_admin)):
            ...
    """
    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedException("Admin access required")
    return current_user


def get_optional_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security)
    ],
):
    """
    Опционально получить пользователя.
    Для эндпоинтов где авторизация опциональна.
    
    Возвращает None если токен отсутствует или невалидный.
    """
    async def _get_optional_user() -> User | None:
        if credentials is None:
            return None
        
        try:
            token = credentials.credentials
            payload = decode_token(token)
            
            if payload is None or payload.get("type") != "access":
                return None
            
            user_id = payload.get("sub")
            if user_id is None:
                return None
            
            result = await db.execute(
                select(User).where(User.id == UUID(user_id))
            )
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    return _get_optional_user


# Type aliases для удобства
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
CurrentVerifiedUser = Annotated[User, Depends(get_current_verified_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
