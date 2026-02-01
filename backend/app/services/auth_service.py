"""
Auth Service
============
Бизнес-логика аутентификации и регистрации.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AlreadyExistsException,
    CredentialsException,
    NotFoundException,
    ValidationException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_verification_token,
    decode_token,
    get_token_expiry,
    hash_password,
    verify_password,
)
from app.db.redis import add_to_blacklist, is_blacklisted
from app.models.user import User, UserRole
from app.schemas.auth import TokenPair, UserLogin, UserRegister


class AuthService:
    """Сервис аутентификации."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register(
        self,
        data: UserRegister,
        role: UserRole = UserRole.USER,
    ) -> User:
        """
        Регистрация нового пользователя.
        
        1. Проверяем уникальность email и username
        2. Хешируем пароль
        3. Создаём пользователя
        4. Генерируем verification token
        """
        # Проверка email
        existing = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise AlreadyExistsException("User with this email")
        
        # Проверка username
        existing = await self.db.execute(
            select(User).where(User.username == data.username.lower())
        )
        if existing.scalar_one_or_none():
            raise AlreadyExistsException("User with this username")
        
        # Создаём пользователя
        user = User(
            email=data.email,
            username=data.username.lower(),
            password_hash=hash_password(data.password),
            role=role,
            verification_token=create_verification_token(),
        )
        
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        
        return user
    
    async def login(self, data: UserLogin) -> tuple[User, TokenPair]:
        """
        Аутентификация пользователя.
        
        1. Ищем пользователя по email
        2. Проверяем пароль
        3. Генерируем токены
        """
        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise CredentialsException("Invalid email or password")
        
        if not verify_password(data.password, user.password_hash):
            raise CredentialsException("Invalid email or password")
        
        if not user.is_active:
            raise CredentialsException("Account is deactivated")
        
        # Генерируем токены
        tokens = self._create_tokens(user)
        
        return user, tokens
    
    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        """
        Обновление access token по refresh token.
        
        1. Декодируем refresh token
        2. Проверяем что не в blacklist
        3. Проверяем что пользователь активен
        4. Генерируем новые токены
        5. Добавляем старый refresh в blacklist
        """
        payload = decode_token(refresh_token)
        
        if payload is None:
            raise CredentialsException("Invalid refresh token")
        
        if payload.get("type") != "refresh":
            raise CredentialsException("Invalid token type")
        
        if await is_blacklisted(refresh_token):
            raise CredentialsException("Token has been revoked")
        
        user_id = payload.get("sub")
        if user_id is None:
            raise CredentialsException("Invalid token")
        
        result = await self.db.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        
        if user is None or not user.is_active:
            raise CredentialsException("User not found or inactive")
        
        # Blacklist старый refresh token
        ttl = get_token_expiry(refresh_token)
        if ttl > 0:
            await add_to_blacklist(refresh_token, ttl)
        
        # Генерируем новые токены
        return self._create_tokens(user)
    
    async def logout(self, access_token: str, refresh_token: str | None = None) -> None:
        """
        Выход пользователя.
        Добавляем токены в blacklist.
        """
        # Blacklist access token
        ttl = get_token_expiry(access_token)
        if ttl > 0:
            await add_to_blacklist(access_token, ttl)
        
        # Blacklist refresh token если передан
        if refresh_token:
            ttl = get_token_expiry(refresh_token)
            if ttl > 0:
                await add_to_blacklist(refresh_token, ttl)
    
    async def verify_email(self, token: str) -> User:
        """
        Подтверждение email по токену.
        """
        result = await self.db.execute(
            select(User).where(User.verification_token == token)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise ValidationException("Invalid verification token")
        
        user.is_verified = True
        user.verification_token = None
        
        await self.db.flush()
        
        return user
    
    async def resend_verification(self, email: str) -> str:
        """
        Переотправить email verification.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise NotFoundException("User")
        
        if user.is_verified:
            raise ValidationException("Email is already verified")
        
        user.verification_token = create_verification_token()
        await self.db.flush()
        
        return user.verification_token
    
    def _create_tokens(self, user: User) -> TokenPair:
        """Создать пару токенов для пользователя."""
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role.value},
        )
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
