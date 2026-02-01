"""
Tag Model
=========
Модель тегов с many-to-many связью к постам.
"""

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# Промежуточная таблица для many-to-many
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column(
        "post_id",
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tag(Base):
    """
    Модель тега.
    
    Attributes:
        name: Название тега (уникальное)
        slug: URL-friendly версия названия
        description: Описание тега
    """
    
    __tablename__ = "tags"
    
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    
    slug: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Цвет для UI (hex)
    color: Mapped[str | None] = mapped_column(
        String(7),
        default="#3B82F6",
        nullable=True,
    )
    
    # Отношения
    posts = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
    
    @property
    def posts_count(self) -> int:
        return len(self.posts) if self.posts else 0
