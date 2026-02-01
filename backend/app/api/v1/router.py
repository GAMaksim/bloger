"""
API v1 Router
=============
Объединение всех роутеров API v1.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.posts import router as posts_router


router = APIRouter(prefix="/v1")

# Подключаем все роутеры
router.include_router(auth_router)
router.include_router(posts_router)

# TODO: Добавить позже
# router.include_router(users_router)
# router.include_router(comments_router)
# router.include_router(tags_router)
