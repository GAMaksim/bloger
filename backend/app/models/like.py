"""
Like Model
==========
Модель лайков с уникальным ограничением user + post.
"""

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Like(Base):
    """
    Модель лайка.
    Один пользователь может лайкнуть пост только один раз.
    """
    
    __tablename__ = "likes"
    
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    post_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Отношения
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    
    # Уникальное ограничение: один лайк от пользователя на пост
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),
    )
    
    def __repr__(self) -> str:
        return f"<Like user={self.user_id} post={self.post_id}>"
