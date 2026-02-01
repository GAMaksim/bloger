"""
FastAPI Main Application
========================
Точка входа приложения.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.router import router as api_router
from app.config import settings
from app.core.exceptions import BlogException
from app.db.redis import close_redis


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager для startup/shutdown events.
    """
    # Startup
    print("🚀 Starting Blog API...")
    yield
    # Shutdown
    print("👋 Shutting down...")
    await close_redis()


# Создаём приложение
app = FastAPI(
    title="Blog Platform API",
    description="Production-ready blog platform with FastAPI",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["*"] if settings.debug 
        else [settings.frontend_url]
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(BlogException)
async def blog_exception_handler(request: Request, exc: BlogException):
    """Handler для кастомных исключений."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


# Подключаем роутеры
app.include_router(api_router, prefix="/api")


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint для мониторинга.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment,
    }


# Root redirect
@app.get("/", tags=["Root"])
async def root():
    """Redirect to docs."""
    return {
        "message": "Blog Platform API",
        "docs": "/docs",
        "health": "/health",
    }
