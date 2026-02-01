"""
Auth Schemas
============
Pydantic модели для аутентификации.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserRegister(BaseModel):
    """Схема регистрации пользователя."""
    
    email: EmailStr
    username: str = Field(
        min_length=3,
        max_length=50,
        description="Username 3-50 символов, только буквы, цифры и _"
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль минимум 8 символов"
    )
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v.lower()
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserLogin(BaseModel):
    """Схема логина."""
    
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    """Пара токенов access + refresh."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Запрос на обновление access токена."""
    
    refresh_token: str


class PasswordReset(BaseModel):
    """Запрос на сброс пароля."""
    
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Подтверждение сброса пароля."""
    
    token: str
    new_password: str = Field(min_length=8, max_length=128)
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        return v


class EmailVerification(BaseModel):
    """Подтверждение email."""
    
    token: str
