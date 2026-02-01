"""
Post Model
==========
Модель статьи с полнотекстовым поиском PostgreSQL.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PostStatus(str, enum.Enum):
    """Статусы публикации."""
    DRAFT = "draft"
    PUBLISHED = "published"


class Post(Base):
    """
    Модель статьи.
    
    Поддерживает:
    - Черновики и опубликованные статьи
    - Полнотекстовый поиск PostgreSQL
    - Счётчик просмотров
    - Теги через many-to-many
    """
    
    __tablename__ = "posts"
    
    # Автор статьи
    author_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Основные поля
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    excerpt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    cover_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    
    # Статус и метаданные
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus),
        default=PostStatus.DRAFT,
        nullable=False,
        index=True,
    )
    
    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Полнотекстовый поиск PostgreSQL
    # Будет заполняться автоматически через триггер в миграции
    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR,
        nullable=True,
    )
    
    # SEO поля
    meta_title: Mapped[str | None] = mapped_column(
        String(70),
        nullable=True,
    )
    
    meta_description: Mapped[str | None] = mapped_column(
        String(160),
        nullable=True,
    )
    
    # Отношения
    author = relationship("User", back_populates="posts", lazy="selectin")
    comments = relationship(
        "Comment",
        back_populates="post",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    likes = relationship(
        "Like",
        back_populates="post",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    tags = relationship(
        "Tag",
        secondary="post_tags",
        back_populates="posts",
        lazy="selectin",
    )
    
    # Индексы
    __table_args__ = (
        # GIN индекс для полнотекстового поиска
        Index("ix_posts_search_vector", search_vector, postgresql_using="gin"),
    )
    
    def __repr__(self) -> str:
        return f"<Post {self.slug}>"
    
    @property
    def is_published(self) -> bool:
        return self.status == PostStatus.PUBLISHED
    
    @property
    def likes_count(self) -> int:
        return len(self.likes) if self.likes else 0
    
    @property
    def comments_count(self) -> int:
        return len(self.comments) if self.comments else 0
