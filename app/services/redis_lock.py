import redis.asyncio as redis
from contextlib import asynccontextmanager


@asynccontextmanager
async def distributed_lock(
    redis_client: redis.Redis, lock_name: str, timeout: int = 10
):
    acquired = await redis_client.set(lock_name, "locked", ex=timeout, nx=True)
    try:
        if acquired:
            yield True
        else:
            yield False
    except Exception as e:
        print(f"Exception raised within context: {e}")
    print("Exited context.")
