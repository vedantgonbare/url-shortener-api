import redis.asyncio as redis
import json
from app.core import settings

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client

async def get_cached_url(short_code: str) -> str | None:
    cached = await get_redis_client().get(f"url:{short_code}")
    return cached

async def cache_url(short_code: str, original_url: str, expire_seconds: int = 3600):
    await get_redis_client().setex(f"url:{short_code}", expire_seconds, original_url)

async def delete_cached_url(short_code: str):
    await get_redis_client().delete(f"url:{short_code}")
