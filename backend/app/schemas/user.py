"""
User Schemas
============
Pydantic модели для пользователей.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    """Базовые поля пользователя."""
    
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    """Создание пользователя (внутреннее)."""
    
    password_hash: str


class UserUpdate(BaseModel):
    """Обновление профиля пользователя."""
    
    username: str | None = Field(None, min_length=3, max_length=50)
    bio: str | None = Field(None, max_length=500)
    avatar_url: str | None = None


class UserResponse(BaseModel):
    """Ответ с данными пользователя (публичный)."""
    
    id: UUID
    username: str
    avatar_url: str | None
    bio: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserMeResponse(UserResponse):
    """Ответ для текущего пользователя (приватный)."""
    
    email: EmailStr
    role: UserRole
    is_verified: bool
    
    class Config:
        from_attributes = True


class UserAdminResponse(UserMeResponse):
    """Ответ для админов (полный)."""
    
    is_active: bool
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """Статистика пользователя."""
    
    posts_count: int = 0
    comments_count: int = 0
    likes_received: int = 0
    total_views: int = 0
