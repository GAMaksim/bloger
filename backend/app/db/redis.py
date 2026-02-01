"""
Redis Client
============
Асинхронный клиент Redis для кэширования и JWT blacklist.
"""

from redis import asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings

# Глобальный пул соединений
redis_pool: Redis | None = None


async def get_redis() -> Redis:
    """
    Получить Redis клиент.
    Использует пул соединений для эффективности.
    """
    global redis_pool
    
    if redis_pool is None:
        redis_pool = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    
    return redis_pool


async def close_redis() -> None:
    """Закрыть соединение с Redis."""
    global redis_pool
    
    if redis_pool is not None:
        await redis_pool.close()
        redis_pool = None


# === JWT Blacklist операции ===

async def add_to_blacklist(token: str, ttl_seconds: int) -> None:
    """
    Добавить токен в blacklist.
    
    Args:
        token: JWT токен для блокировки
        ttl_seconds: Время жизни записи (должно = exp токена)
    """
    redis = await get_redis()
    await redis.setex(f"blacklist:{token}", ttl_seconds, "1")


async def is_blacklisted(token: str) -> bool:
    """Проверить, находится ли токен в blacklist."""
    redis = await get_redis()
    result = await redis.get(f"blacklist:{token}")
    return result is not None


# === Кэширование постов ===

async def cache_post(slug: str, data: str, ttl: int = 300) -> None:
    """Кэшировать пост на 5 минут."""
    redis = await get_redis()
    await redis.setex(f"post:{slug}", ttl, data)


async def get_cached_post(slug: str) -> str | None:
    """Получить пост из кэша."""
    redis = await get_redis()
    return await redis.get(f"post:{slug}")


async def invalidate_post_cache(slug: str) -> None:
    """Удалить пост из кэша при обновлении."""
    redis = await get_redis()
    await redis.delete(f"post:{slug}")


# === Rate Limiting ===

async def check_rate_limit(key: str, limit: int, window: int = 60) -> tuple[bool, int]:
    """
    Проверить rate limit.
    
    Args:
        key: Идентификатор (например, IP или user_id)
        limit: Максимум запросов
        window: Временное окно в секундах
    
    Returns:
        (allowed, remaining): Разрешён ли запрос и сколько осталось
    """
    redis = await get_redis()
    redis_key = f"ratelimit:{key}"
    
    current = await redis.get(redis_key)
    
    if current is None:
        await redis.setex(redis_key, window, 1)
        return True, limit - 1
    
    count = int(current)
    
    if count >= limit:
        return False, 0
    
    await redis.incr(redis_key)
    return True, limit - count - 1
