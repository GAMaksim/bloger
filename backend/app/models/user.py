"""
User Model
==========
Модель пользователя с ролями и email verification.
"""

import enum
from datetime import datetime

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User roles."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    Модель пользователя.
    
    Attributes:
        email: Уникальный email
        username: Уникальное имя пользователя
        password_hash: Хеш пароля (bcrypt)
        role: Роль (user/admin)
        avatar_url: URL аватара
        bio: Биография
        is_active: Активен ли аккаунт
        is_verified: Подтверждён ли email
        verification_token: Токен для подтверждения email
    """
    
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='userrole', create_type=False),
        default=UserRole.USER,
        nullable=False,
    )
    
    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    
    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    verification_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Отношения
    posts = relationship("Post", back_populates="author", lazy="selectin")
    comments = relationship("Comment", back_populates="user", lazy="selectin")
    likes = relationship("Like", back_populates="user", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
