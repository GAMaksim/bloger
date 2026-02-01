"""
Posts API Routes
================
Эндпоинты для работы со статьями.
"""

from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, DbSession
from app.models.post import PostStatus
from app.schemas.post import (
    PostCreate,
    PostDetailResponse,
    PostListResponse,
    PostResponse,
    PostUpdate,
)
from app.services.post_service import PostService


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "",
    response_model=PostListResponse,
    summary="Список статей",
)
async def get_posts(
    db: DbSession,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=50, description="Статей на странице"),
    status: PostStatus | None = Query(PostStatus.PUBLISHED, description="Статус"),
    author_id: UUID | None = Query(None, description="ID автора"),
    tag: str | None = Query(None, description="Slug тега"),
    search: str | None = Query(None, description="Поисковый запрос"),
):
    """
    Получить список статей с фильтрами и пагинацией.
    
    По умолчанию возвращает только опубликованные статьи.
    Для просмотра черновиков нужны права автора или админа.
    """
    service = PostService(db)
    posts, total = await service.get_posts(
        page=page,
        per_page=per_page,
        status=status,
        author_id=author_id,
        tag_slug=tag,
        search=search,
    )
    
    pages = (total + per_page - 1) // per_page
    
    return PostListResponse(
        items=posts,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get(
    "/{slug}",
    response_model=PostDetailResponse,
    summary="Получить статью",
)
async def get_post(
    slug: str,
    db: DbSession,
):
    """
    Получить статью по slug.
    
    Автоматически увеличивает счётчик просмотров.
    """
    service = PostService(db)
    post = await service.get_post_by_slug(slug)
    
    # Увеличиваем просмотры
    await service.increment_views(post.id)
    
    return post


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать статью",
)
async def create_post(
    data: PostCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Создать новую статью.
    """
    service = PostService(db)
    post = await service.create_post(current_user, data)
    
    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="Обновить статью",
)
async def update_post(
    post_id: UUID,
    data: PostUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Обновить статью.
    
    Только автор статьи или администратор.
    """
    service = PostService(db)
    post = await service.update_post(post_id, current_user, data)
    
    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить статью",
)
async def delete_post(
    post_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Удалить статью.
    
    Только автор статьи или администратор.
    """
    service = PostService(db)
    await service.delete_post(post_id, current_user)


@router.post(
    "/{post_id}/like",
    summary="Лайкнуть/убрать лайк",
)
async def toggle_like(
    post_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Поставить или убрать лайк на статью.
    
    Возвращает текущее состояние (liked: true/false).
    """
    service = PostService(db)
    liked = await service.toggle_like(post_id, current_user)
    
    return {"liked": liked}
