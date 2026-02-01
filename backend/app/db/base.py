"""
Base Model for SQLAlchemy
========================
Общий базовый класс для всех моделей БД.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей.
    Автоматически добавляет:
    - id (UUID)
    - created_at
    - updated_at
    """
    
    # Общие типы для аннотаций
    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }
    
    # UUID как первичный ключ
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Автоматические временные метки
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Преобразование модели в словарь."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
