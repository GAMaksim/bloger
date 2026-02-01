"""
Security Module
===============
JWT токены, password hashing, и утилиты безопасности.
"""

import secrets
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings


# === Password Hashing ===

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Cost factor для bcrypt
)


def hash_password(password: str) -> str:
    """
    Хешировать пароль с bcrypt.
    
    Args:
        password: Открытый пароль
        
    Returns:
        Хеш пароля
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверить пароль против хеша.
    
    Args:
        plain_password: Открытый пароль для проверки
        hashed_password: Сохранённый хеш
        
    Returns:
        True если пароль верный
    """
    return pwd_context.verify(plain_password, hashed_password)


# === JWT Tokens ===

def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Создать access token.
    
    Args:
        subject: Идентификатор пользователя (обычно user_id)
        expires_delta: Время жизни токена
        extra_claims: Дополнительные claims (role, etc.)
        
    Returns:
        Закодированный JWT
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow(),
    }
    
    if extra_claims:
        to_encode.update(extra_claims)
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Создать refresh token.
    Refresh токены живут дольше и используются только для обновления access.
    
    Args:
        subject: Идентификатор пользователя
        expires_delta: Время жизни токена
        
    Returns:
        Закодированный JWT
    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
    
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(32),  # Уникальный ID для blacklist
    }
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Декодировать и валидировать JWT токен.
    
    Args:
        token: JWT токен
        
    Returns:
        Payload токена или None если невалидный
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None


def get_token_expiry(token: str) -> int:
    """
    Получить оставшееся время жизни токена в секундах.
    Используется для TTL в Redis blacklist.
    
    Args:
        token: JWT токен
        
    Returns:
        Секунды до истечения (0 если уже истёк)
    """
    payload = decode_token(token)
    if payload is None:
        return 0
    
    exp = payload.get("exp", 0)
    remaining = exp - int(datetime.utcnow().timestamp())
    
    return max(0, remaining)


# === Email Verification Token ===

def create_verification_token() -> str:
    """
    Создать токен для email verification.
    
    Returns:
        URL-safe токен
    """
    return secrets.token_urlsafe(32)


# === Password Validation ===

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Проверить надёжность пароля.
    
    Требования:
    - Минимум 8 символов
    - Хотя бы одна цифра
    - Хотя бы одна буква
    
    Args:
        password: Пароль для проверки
        
    Returns:
        (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter"
    
    return True, ""
