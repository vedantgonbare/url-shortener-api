import redis.asyncio as redis
import json
from app.core import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_cached_url(short_code: str) -> str | None:
    cached = await redis_client.get(f"url:{short_code}")
    return cached

async def cache_url(short_code: str, original_url: str, expire_seconds: int = 3600):
    await redis_client.setex(f"url:{short_code}", expire_seconds, original_url)

async def delete_cached_url(short_code: str):
    await redis_client.delete(f"url:{short_code}")