"""
Comment Schemas
===============
Pydantic модели для комментариев.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.user import UserResponse


class CommentCreate(BaseModel):
    """Создание комментария."""
    
    content: str = Field(min_length=1, max_length=2000)
    parent_id: UUID | None = None  # Для ответов


class CommentUpdate(BaseModel):
    """Обновление комментария."""
    
    content: str = Field(min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    """Ответ с комментарием."""
    
    id: UUID
    content: str
    is_approved: bool
    created_at: datetime
    user: UserResponse
    replies: list["CommentResponse"] = []
    
    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    """Список комментариев с пагинацией."""
    
    items: list[CommentResponse]
    total: int


# Для forward reference
CommentResponse.model_rebuild()
