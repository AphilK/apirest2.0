import os
import redis.asyncio as aioredis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASS = os.getenv("REDIS_PASS", "")

if REDIS_PASS:
    REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_redis() -> aioredis.Redis:
    return redis_client