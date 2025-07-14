from fastapi import FastAPI
import redis.asyncio as redis

main_app = FastAPI()

@main_app.get("/")
async def read_root(app: FastAPI, init_redis=None):
    redis_client= await init_redis()