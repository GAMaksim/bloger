"""
Tag Schemas
===========
Pydantic модели для тегов.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    """Создание тега."""
    
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(None, max_length=200)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class TagUpdate(BaseModel):
    """Обновление тега."""
    
    name: str | None = Field(None, min_length=2, max_length=50)
    description: str | None = Field(None, max_length=200)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class TagResponse(BaseModel):
    """Ответ с тегом."""
    
    id: UUID
    name: str
    slug: str
    description: str | None
    color: str | None
    posts_count: int = 0
    
    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """Список тегов."""
    
    items: list[TagResponse]
    total: int
