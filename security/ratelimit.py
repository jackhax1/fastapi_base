import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

import os
from dotenv import load_dotenv
load_dotenv()

REDIS_ENDPOINT = os.getenv('REDIS_ENDPOINT')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


RATE_LIMIT_TIMES = int(os.getenv('RATE_LIMIT_TIMES'))
RATE_LIMIT_SECS = int(os.getenv('RATE_LIMIT_SECS'))


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.Redis(host=REDIS_ENDPOINT,
                                   port=REDIS_PORT,
                                   password=REDIS_PASSWORD)
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()