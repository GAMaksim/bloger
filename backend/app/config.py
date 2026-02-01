"""
Application Configuration
========================
Использует Pydantic BaseSettings для загрузки и валидации переменных окружения.
Автоматически читает из .env файла.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.
    Все значения можно переопределить через переменные окружения.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Основные настройки
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@example.com"
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Создаёт и кэширует экземпляр настроек.
    lru_cache гарантирует, что настройки читаются только один раз.
    """
    return Settings()


# Глобальный экземпляр для удобного импорта
settings = get_settings()
