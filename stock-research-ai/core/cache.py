import json
from typing import Any

from redis.asyncio import Redis
from loguru import logger

from core.config import settings

_client: Redis | None = None
_available: bool = False


def _get_client() -> Redis | None:
    global _client, _available
    if _client is not None:
        return _client
    try:
        _client = Redis.from_url(settings.redis_url, decode_responses=True)
        _available = True
        return _client
    except Exception as exc:
        _available = False
        logger.warning(f"Redis unavailable: {exc}")
        return None


async def cache_get(namespace: str, key: str) -> Any:
    if not _available:
        return None
    try:
        client = _get_client()
        if client is None:
            return None
        val = await client.get(f"{namespace}:{key}")
        return json.loads(val) if val else None
    except Exception as exc:
        logger.warning(f"Redis get failed ({namespace}:{key}): {exc}")
        return None


async def cache_set(namespace: str, key: str, value: Any, ttl: int) -> None:
    if not _available:
        return
    try:
        client = _get_client()
        if client is None:
            return
        await client.setex(f"{namespace}:{key}", ttl, json.dumps(value))
    except Exception as exc:
        logger.warning(f"Redis set failed ({namespace}:{key}): {exc}")


async def cache_delete(namespace: str, key: str) -> None:
    if not _available:
        return
    try:
        client = _get_client()
        if client is None:
            return
        await client.delete(f"{namespace}:{key}")
    except Exception as exc:
        logger.warning(f"Redis delete failed ({namespace}:{key}): {exc}")


async def cache_ping() -> bool:
    try:
        client = _get_client()
        if client is None:
            return False
        return await client.ping()
    except Exception:
        return False