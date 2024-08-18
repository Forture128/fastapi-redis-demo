import redis.asyncio as redis


async def add_location(
    redis_client: redis.Redis, name: str, longitude: float, latitude: float
):
    coords = (longitude, latitude, name)
    await redis_client.geoadd("locations", coords)


async def find_nearby_locations(
    redis_client: redis.Redis,
    longitude: float,
    latitude: float,
    radius: float,
    unit: str = "km",
):
    # GEORADIUSBYMEMBER or GEORADIUS can be used to find nearby locations
    return await redis_client.georadius(
        "locations", longitude, latitude, radius, unit, withdist=True, withcoord=True
    )
