from typing import TYPE_CHECKING, cast

import redis.asyncio as _async_redis  # type: ignore

from app.infra.config import settings

# https://github.com/python/typeshed/issues/7597#issuecomment-1117551641
# Redis is generic at type checking, but not at runtime...
if TYPE_CHECKING:
    Redis = _async_redis.Redis[str]  # type: ignore
    ConnectionPool = _async_redis.ConnectionPool[_async_redis.Connection]  # type: ignore
else:
    Redis = _async_redis.Redis
    ConnectionPool = _async_redis.ConnectionPool


def create_async_connection_pool() -> ConnectionPool:  # type: ignore
    return _async_redis.ConnectionPool.from_url(
        settings.redis_url, decode_responses=True
    )


async_pool = create_async_connection_pool()


def get_redis() -> Redis:  # type: ignore
    return cast(Redis, _async_redis.Redis(connection_pool=async_pool))  # type: ignore


redis = get_redis()

__all__ = ["redis", "Redis"]
