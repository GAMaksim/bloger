"""
Models Package
==============
Экспорт всех моделей для удобного импорта.
"""

from app.models.user import User, UserRole
from app.models.post import Post, PostStatus
from app.models.comment import Comment
from app.models.like import Like
from app.models.tag import Tag, post_tags

__all__ = [
    "User",
    "UserRole",
    "Post",
    "PostStatus",
    "Comment",
    "Like",
    "Tag",
    "post_tags",
]
