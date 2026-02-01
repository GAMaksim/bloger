"""
Schemas Package
===============
Экспорт всех Pydantic схем.
"""

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenPair,
    TokenRefresh,
    PasswordReset,
    PasswordResetConfirm,
    EmailVerification,
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserMeResponse,
    UserAdminResponse,
    UserStats,
)
from app.schemas.post import (
    PostBase,
    PostCreate,
    PostUpdate,
    PostResponse,
    PostDetailResponse,
    PostListResponse,
    PostSEO,
)
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentListResponse,
)
from app.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse,
    TagListResponse,
)

__all__ = [
    # Auth
    "UserRegister",
    "UserLogin",
    "TokenPair",
    "TokenRefresh",
    "PasswordReset",
    "PasswordResetConfirm",
    "EmailVerification",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserMeResponse",
    "UserAdminResponse",
    "UserStats",
    # Post
    "PostBase",
    "PostCreate",
    "PostUpdate",
    "PostResponse",
    "PostDetailResponse",
    "PostListResponse",
    "PostSEO",
    # Comment
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    "CommentListResponse",
    # Tag
    "TagCreate",
    "TagUpdate",
    "TagResponse",
    "TagListResponse",
]
