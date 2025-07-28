import os

import redis.asyncio as redis

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=6379,
    db=0,
)
