"""
Comment Model
=============
Модель комментариев с поддержкой вложенных ответов.
"""

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Comment(Base):
    """
    Модель комментария.
    
    Поддерживает:
    - Вложенные ответы (parent_id)
    - Модерацию (is_approved)
    """
    
    __tablename__ = "comments"
    
    # Связи
    post_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Родительский комментарий для ответов
    parent_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    
    # Контент
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Модерация
    is_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=True,  # Авто-одобрение. Для модерации поставить False
        nullable=False,
    )
    
    # Отношения
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    
    # Вложенные ответы
    replies = relationship(
        "Comment",
        back_populates="parent",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    parent = relationship(
        "Comment",
        back_populates="replies",
        remote_side="Comment.id",
    )
    
    def __repr__(self) -> str:
        return f"<Comment {self.id} by {self.user_id}>"
