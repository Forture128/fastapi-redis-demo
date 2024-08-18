# app/main.py
from fastapi import FastAPI, Depends, HTTPException
import asyncpg
import redis.asyncio as redis
from app.config import settings
from app.database import get_db
from app.crud.user import create_user, get_user, get_user_by_email
from app.schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.event_sourcing import acknowledge_event, add_event_to_stream, create_consumer_group, read_from_stream
from app.services.leaderboard import add_score, get_leaderboard
from app.services.proximity_search import add_location, find_nearby_locations
from app.services.redis_lock import distributed_lock

app = FastAPI()


@app.on_event("startup")
async def startup():
    # Connect to Redis using redis-py with asyncio
    app.state.redis = redis.Redis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )

    # Connect to PostgreSQL
    # Adjust the DSN for asyncpg
    asyncpg_dsn = settings.database_url.replace("postgresql+asyncpg", "postgresql")

    # Connect to PostgreSQL using the adjusted DSN
    app.state.db = await asyncpg.create_pool(dsn=asyncpg_dsn)


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
    await app.state.db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI with Redis and PostgreSQL Demo!"}


@app.get("/cache/")
async def cache_example():
    await app.state.redis.set("my_key", "Hello, Redis! 2")
    cached_value = await app.state.redis.get("my_key")
    return {"cached_value": cached_value}


@app.post("/users/", response_model=User)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user=user)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


##############################
####### API Redis Lock #######
##############################
@app.post("/lock/")
async def example_distributed_lock(key: str):
    async with distributed_lock(app.state.redis, key) as lock_acquired:
        if not lock_acquired:
            return {"message": "Resource is locked"}
        # Perform the operation that requires the lock
        return {"message": "Operation completed successfully with lock"}


@app.post("/leaderboard/")
async def add_to_leaderboard(user_id: str, score: int):
    await add_score(app.state.redis, user_id, score)
    return {"message": "Score added"}


@app.get("/leaderboard/")
async def get_top_leaderboard(top_n: int = 10):
    leaderboard = await get_leaderboard(app.state.redis, top_n)
    return {"leaderboard": leaderboard}


##############################
####### API Proximity ########
##############################
@app.post("/locations/")
async def add_new_location(name: str, longitude: float, latitude: float):
    await add_location(app.state.redis, name, longitude, latitude)
    return {"message": f"Location '{name}' added."}


@app.get("/locations/")
async def get_nearby_locations(
    longitude: float, latitude: float, radius: float, unit: str = "km"
):
    locations = await find_nearby_locations(
        app.state.redis, longitude, latitude, radius, unit
    )
    return {"nearby_locations": locations}

#####################################
####### API Event Sourcing Stream ###
#####################################


@app.post("/streams/{stream_name}/events/")
async def add_stream_event(stream_name: str, event_data: dict):
    event_id = await add_event_to_stream(app.state.redis, stream_name, event_data)
    return {"event_id": event_id}


@app.post("/streams/{stream_name}/groups/{group_name}/")
async def create_group(stream_name: str, group_name: str):
    await create_consumer_group(app.state.redis, stream_name, group_name)
    return {
        "message": f"Consumer group '{group_name}' created for stream '{stream_name}'."
    }


@app.get("/streams/{stream_name}/groups/{group_name}/events/")
async def get_events_from_stream(
    stream_name: str,
    group_name: str,
    consumer_name: str = "consumer-1",
    count: int = 10,
):
    events = await read_from_stream(
        app.state.redis, stream_name, group_name, consumer_name, count
    )
    return {"events": events}


@app.post("/streams/{stream_name}/groups/{group_name}/acknowledge/")
async def acknowledge_stream_event(stream_name: str, group_name: str, event_id: str):
    await acknowledge_event(app.state.redis, stream_name, group_name, event_id)
    return {"message": f"Event '{event_id}' acknowledged."}
