"""
Custom Exceptions
=================
HTTP исключения для API с детальными сообщениями.
"""

from fastapi import HTTPException, status


class BlogException(HTTPException):
    """Base exception для всех ошибок приложения."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )


# === Auth Exceptions ===

class CredentialsException(BlogException):
    """Неверные учётные данные."""
    
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(BlogException):
    """Токен истёк."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenBlacklistedException(BlogException):
    """Токен в blacklist (logout)."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserException(BlogException):
    """Пользователь деактивирован."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )


class UnverifiedEmailException(BlogException):
    """Email не подтверждён."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address has not been verified",
        )


class PermissionDeniedException(BlogException):
    """Нет прав доступа."""
    
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


# === Resource Exceptions ===

class NotFoundException(BlogException):
    """Ресурс не найден."""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class AlreadyExistsException(BlogException):
    """Ресурс уже существует."""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
        )


# === Validation Exceptions ===

class ValidationException(BlogException):
    """Ошибка валидации данных."""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


# === Rate Limiting ===

class RateLimitExceededException(BlogException):
    """Превышен лимит запросов."""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )
