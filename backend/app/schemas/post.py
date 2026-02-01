"""
Post Schemas
============
Pydantic модели для статей.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.post import PostStatus
from app.schemas.user import UserResponse
from app.schemas.tag import TagResponse


class PostBase(BaseModel):
    """Базовые поля статьи."""
    
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=10)
    excerpt: str | None = Field(None, max_length=500)
    cover_image: str | None = None
    meta_title: str | None = Field(None, max_length=70)
    meta_description: str | None = Field(None, max_length=160)


class PostCreate(PostBase):
    """Создание статьи."""
    
    status: PostStatus = PostStatus.DRAFT
    tag_ids: list[UUID] = []


class PostUpdate(BaseModel):
    """Обновление статьи."""
    
    title: str | None = Field(None, min_length=3, max_length=255)
    content: str | None = Field(None, min_length=10)
    excerpt: str | None = Field(None, max_length=500)
    cover_image: str | None = None
    status: PostStatus | None = None
    meta_title: str | None = Field(None, max_length=70)
    meta_description: str | None = Field(None, max_length=160)
    tag_ids: list[UUID] | None = None


class PostResponse(BaseModel):
    """Ответ с данными статьи (список)."""
    
    id: UUID
    title: str
    slug: str
    excerpt: str | None
    cover_image: str | None
    status: PostStatus
    view_count: int
    likes_count: int
    comments_count: int
    published_at: datetime | None
    created_at: datetime
    author: UserResponse
    tags: list["TagResponse"]
    
    class Config:
        from_attributes = True


class PostDetailResponse(PostResponse):
    """Ответ с полными данными статьи."""
    
    content: str
    meta_title: str | None
    meta_description: str | None
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """Пагинированный список статей."""
    
    items: list[PostResponse]
    total: int
    page: int
    per_page: int
    pages: int


class PostSEO(BaseModel):
    """SEO данные для статьи."""
    
    title: str
    description: str
    og_image: str | None
    canonical_url: str
    author: str
    published_time: datetime | None
    modified_time: datetime
    tags: list[str]
