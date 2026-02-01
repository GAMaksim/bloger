"""
Post Service
============
Бизнес-логика статей с полнотекстовым поиском.
"""

from datetime import datetime
from uuid import UUID

from slugify import slugify
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundException, PermissionDeniedException
from app.db.redis import cache_post, get_cached_post, invalidate_post_cache
from app.models.post import Post, PostStatus
from app.models.tag import Tag
from app.models.like import Like
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """Сервис для работы со статьями."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_posts(
        self,
        page: int = 1,
        per_page: int = 10,
        status: PostStatus | None = PostStatus.PUBLISHED,
        author_id: UUID | None = None,
        tag_slug: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Post], int]:
        """
        Получить список статей с фильтрами и пагинацией.
        """
        query = select(Post).options(
            selectinload(Post.author),
            selectinload(Post.tags),
            selectinload(Post.likes),
            selectinload(Post.comments),
        )
        
        # Фильтры
        if status:
            query = query.where(Post.status == status)
        
        if author_id:
            query = query.where(Post.author_id == author_id)
        
        if tag_slug:
            query = query.join(Post.tags).where(Tag.slug == tag_slug)
        
        if search:
            # PostgreSQL Full-Text Search
            query = query.where(
                Post.search_vector.match(search)
            )
        
        # Подсчёт общего количества
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Пагинация и сортировка
        query = query.order_by(Post.published_at.desc().nullsfirst())
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await self.db.execute(query)
        posts = result.scalars().unique().all()
        
        return list(posts), total
    
    async def get_post_by_slug(self, slug: str) -> Post:
        """
        Получить статью по slug.
        Использует Redis кэш.
        """
        result = await self.db.execute(
            select(Post)
            .options(
                selectinload(Post.author),
                selectinload(Post.tags),
                selectinload(Post.likes),
                selectinload(Post.comments).selectinload(
                    # Загружаем пользователей комментариев
                ),
            )
            .where(Post.slug == slug)
        )
        post = result.scalar_one_or_none()
        
        if post is None:
            raise NotFoundException("Post")
        
        return post
    
    async def get_post_by_id(self, post_id: UUID) -> Post:
        """Получить статью по ID."""
        result = await self.db.execute(
            select(Post)
            .options(
                selectinload(Post.author),
                selectinload(Post.tags),
            )
            .where(Post.id == post_id)
        )
        post = result.scalar_one_or_none()
        
        if post is None:
            raise NotFoundException("Post")
        
        return post
    
    async def create_post(self, user: User, data: PostCreate) -> Post:
        """
        Создать новую статью.
        """
        # Генерируем уникальный slug
        slug = await self._generate_unique_slug(data.title)
        
        post = Post(
            author_id=user.id,
            title=data.title,
            slug=slug,
            content=data.content,
            excerpt=data.excerpt or self._generate_excerpt(data.content),
            cover_image=data.cover_image,
            status=data.status,
            meta_title=data.meta_title or data.title[:70],
            meta_description=data.meta_description or self._generate_excerpt(data.content, 160),
        )
        
        # Публикация
        if data.status == PostStatus.PUBLISHED:
            post.published_at = datetime.utcnow()
        
        # Добавляем теги
        if data.tag_ids:
            result = await self.db.execute(
                select(Tag).where(Tag.id.in_(data.tag_ids))
            )
            tags = result.scalars().all()
            post.tags = list(tags)
        
        self.db.add(post)
        await self.db.flush()
        await self.db.refresh(post)
        
        return post
    
    async def update_post(
        self,
        post_id: UUID,
        user: User,
        data: PostUpdate,
    ) -> Post:
        """
        Обновить статью.
        Только автор или админ.
        """
        post = await self.get_post_by_id(post_id)
        
        # Проверка прав
        if post.author_id != user.id and not user.is_admin:
            raise PermissionDeniedException()
        
        # Обновляем поля
        update_data = data.model_dump(exclude_unset=True)
        
        if "title" in update_data:
            post.title = update_data["title"]
            post.slug = await self._generate_unique_slug(
                update_data["title"],
                exclude_id=post.id
            )
        
        if "content" in update_data:
            post.content = update_data["content"]
            if not post.excerpt:
                post.excerpt = self._generate_excerpt(update_data["content"])
        
        if "excerpt" in update_data:
            post.excerpt = update_data["excerpt"]
        
        if "cover_image" in update_data:
            post.cover_image = update_data["cover_image"]
        
        if "status" in update_data:
            post.status = update_data["status"]
            if update_data["status"] == PostStatus.PUBLISHED and not post.published_at:
                post.published_at = datetime.utcnow()
        
        if "meta_title" in update_data:
            post.meta_title = update_data["meta_title"]
        
        if "meta_description" in update_data:
            post.meta_description = update_data["meta_description"]
        
        if "tag_ids" in update_data:
            result = await self.db.execute(
                select(Tag).where(Tag.id.in_(update_data["tag_ids"]))
            )
            tags = result.scalars().all()
            post.tags = list(tags)
        
        await self.db.flush()
        
        # Сбрасываем кэш
        await invalidate_post_cache(post.slug)
        
        return post
    
    async def delete_post(self, post_id: UUID, user: User) -> None:
        """
        Удалить статью.
        Только автор или админ.
        """
        post = await self.get_post_by_id(post_id)
        
        if post.author_id != user.id and not user.is_admin:
            raise PermissionDeniedException()
        
        await invalidate_post_cache(post.slug)
        await self.db.delete(post)
        await self.db.flush()
    
    async def increment_views(self, post_id: UUID) -> None:
        """Увеличить счётчик просмотров."""
        post = await self.get_post_by_id(post_id)
        post.view_count += 1
        await self.db.flush()
    
    async def toggle_like(self, post_id: UUID, user: User) -> bool:
        """
        Поставить/убрать лайк.
        Возвращает True если лайк добавлен, False если убран.
        """
        # Проверяем существующий лайк
        result = await self.db.execute(
            select(Like).where(
                Like.post_id == post_id,
                Like.user_id == user.id,
            )
        )
        existing_like = result.scalar_one_or_none()
        
        if existing_like:
            await self.db.delete(existing_like)
            await self.db.flush()
            return False
        else:
            like = Like(post_id=post_id, user_id=user.id)
            self.db.add(like)
            await self.db.flush()
            return True
    
    async def _generate_unique_slug(
        self,
        title: str,
        exclude_id: UUID | None = None,
    ) -> str:
        """Генерация уникального slug."""
        base_slug = slugify(title, max_length=200)
        slug = base_slug
        counter = 1
        
        while True:
            query = select(Post).where(Post.slug == slug)
            if exclude_id:
                query = query.where(Post.id != exclude_id)
            
            result = await self.db.execute(query)
            if result.scalar_one_or_none() is None:
                return slug
            
            slug = f"{base_slug}-{counter}"
            counter += 1
    
    def _generate_excerpt(self, content: str, max_length: int = 200) -> str:
        """Генерация excerpt из content."""
        # Убираем HTML теги (простая версия)
        import re
        clean = re.sub(r'<[^>]+>', '', content)
        clean = clean.strip()
        
        if len(clean) <= max_length:
            return clean
        
        return clean[:max_length].rsplit(' ', 1)[0] + '...'
