"""
Auth API Routes
===============
Эндпоинты аутентификации.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DbSession, CurrentUser, get_current_user
from app.core.security import decode_token
from app.schemas.auth import (
    EmailVerification,
    TokenPair,
    TokenRefresh,
    UserLogin,
    UserRegister,
)
from app.schemas.user import UserMeResponse
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserMeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def register(
    data: UserRegister,
    db: DbSession,
):
    """
    Регистрация нового пользователя.
    
    После регистрации на email будет отправлено письмо 
    для подтверждения адреса.
    """
    service = AuthService(db)
    user = await service.register(data)
    
    # TODO: Отправить email verification
    # await send_verification_email(user.email, user.verification_token)
    
    return user


@router.post(
    "/login",
    response_model=TokenPair,
    summary="Вход в систему",
)
async def login(
    data: UserLogin,
    db: DbSession,
):
    """
    Аутентификация пользователя.
    
    Возвращает:
    - access_token: короткоживущий токен для API (15 мин)
    - refresh_token: долгоживущий токен для обновления (7 дней)
    """
    service = AuthService(db)
    user, tokens = await service.login(data)
    
    return tokens


@router.post(
    "/refresh",
    response_model=TokenPair,
    summary="Обновление access token",
)
async def refresh_token(
    data: TokenRefresh,
    db: DbSession,
):
    """
    Обновить access token используя refresh token.
    
    Старый refresh token будет добавлен в blacklist.
    """
    service = AuthService(db)
    tokens = await service.refresh_tokens(data.refresh_token)
    
    return tokens


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Выход из системы",
)
async def logout(
    current_user: CurrentUser,
    db: DbSession,
    data: TokenRefresh | None = None,
):
    """
    Выход из системы.
    
    Добавляет токены в blacklist.
    """
    # Получаем access token из заголовка
    # (в реальности нужно извлечь из request)
    service = AuthService(db)
    
    if data:
        await service.logout(
            access_token="",  # Будет извлечён из middleware
            refresh_token=data.refresh_token,
        )


@router.post(
    "/verify-email",
    response_model=UserMeResponse,
    summary="Подтверждение email",
)
async def verify_email(
    data: EmailVerification,
    db: DbSession,
):
    """
    Подтверждение email адреса по токену из письма.
    """
    service = AuthService(db)
    user = await service.verify_email(data.token)
    
    return user


@router.post(
    "/resend-verification",
    status_code=status.HTTP_200_OK,
    summary="Повторная отправка verification email",
)
async def resend_verification(
    email: str,
    db: DbSession,
):
    """
    Повторно отправить письмо для подтверждения email.
    """
    service = AuthService(db)
    token = await service.resend_verification(email)
    
    # TODO: Отправить email
    # await send_verification_email(email, token)
    
    return {"message": "Verification email sent"}


@router.get(
    "/me",
    response_model=UserMeResponse,
    summary="Текущий пользователь",
)
async def get_me(
    current_user: CurrentUser,
):
    """
    Получить данные текущего аутентифицированного пользователя.
    """
    return current_user
