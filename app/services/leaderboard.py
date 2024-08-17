import redis.asyncio as redis


async def add_score(redis_client: redis.Redis, user_id: str, score: int):
    await redis_client.zadd("leaderboard", {user_id: score})


async def get_leaderboard(redis_client: redis.Redis, top_n: int):
    return await redis_client.zrevrange("leaderboard", 0, top_n - 1, withscores=True)
