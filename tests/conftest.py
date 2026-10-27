import os
import pytest
import asyncio
import redis.asyncio as aioredis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")

if REDIS_PASS:
    REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

def _flush_redis_sync():
    async def _flush():
        client = aioredis.from_url(REDIS_URL, decode_responses=True)
        await client.flushdb()
        await client.aclose()

    asyncio.run(_flush())

@pytest.fixture(autouse=True)
def clear_redis_cache():
    _flush_redis_sync()
    yield
    _flush_redis_sync()
