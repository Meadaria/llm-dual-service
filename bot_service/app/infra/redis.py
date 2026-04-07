import redis.asyncio as redis
from functools import lru_cache

from app.core.config import settings


@lru_cache(maxsize=1)
def get_redis() -> redis.Redis:
    """
    Возвращает асинхронный Redis клиент.
    """
    return redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        encoding="utf-8"
    )