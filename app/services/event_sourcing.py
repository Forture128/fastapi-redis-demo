from typing import Dict
import redis.asyncio as redis


async def record_event(redis_client: redis.Redis, stream_name: str, event: str):
    await redis_client.lpush(stream_name, event)


async def get_events(redis_client: redis.Redis, stream_name: str, count: int = 10):
    return await redis_client.lrange(stream_name, 0, count - 1)


#################### Event Sourcing Stream ####################
async def add_event_to_stream(
    redis_client: redis.Redis, stream_name: str, event_data: Dict[str, str]
):
    """
    Adds an event to a Redis stream. Converts all values in the event_data to strings.
    """
    # Convert all values in event_data to strings to ensure compatibility with XADD
    formatted_event_data = {key: str(value) for key, value in event_data.items()}

    # Add the event to the Redis stream
    event_id = await redis_client.xadd(stream_name, formatted_event_data)
    return event_id


async def create_consumer_group(
    redis_client: redis.Redis,
    stream_name: str,
    group_name: str,
    consumer_name: str = "consumer-1",
):
    """
    Creates a consumer group for a Redis stream.
    """
    try:
        await redis_client.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except redis.exceptions.ResponseError as e:
        # If the group already exists, we'll ignore the error
        if "BUSYGROUP" not in str(e):
            raise e


async def read_from_stream(
    redis_client: redis.Redis,
    stream_name: str,
    group_name: str,
    consumer_name: str = "consumer-1",
    count: int = 10,
):
    """
    Reads events from a Redis stream using a consumer group.
    """
    events = await redis_client.xreadgroup(
        group_name, consumer_name, {stream_name: ">"}, count=count
    )
    return events


async def acknowledge_event(
    redis_client: redis.Redis, stream_name: str, group_name: str, event_id: str
):
    """
    Acknowledges that an event has been processed.
    """
    await redis_client.xack(stream_name, group_name, event_id)
