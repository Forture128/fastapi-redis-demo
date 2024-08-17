# app/main.py
from fastapi import FastAPI, Depends, HTTPException
import asyncpg
import redis.asyncio as redis
from app.config import settings
from app.database import get_db
from app.crud.user import create_user, get_user, get_user_by_email
from app.schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.leaderboard import add_score, get_leaderboard
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
