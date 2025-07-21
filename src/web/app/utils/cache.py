import hashlib
import pickle
from functools import wraps
from typing import Awaitable, Callable

from app.core.redis import redis_client


def async_cache(ttl: int = 60 * 60 * 24):
    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_data = {
                'args': args[1:],
                'kwargs': kwargs,
            }
            key_str = f'{func.__name__}:{key_data}'
            key_hash = hashlib.md5(key_str.encode()).hexdigest()

            cached = await redis_client.get(key_hash)
            if cached:
                return pickle.loads(cached)

            result = await func(*args, **kwargs)
            await redis_client.set(key_hash, pickle.dumps(result), ex=ttl)
            return result

        return wrapper

    return decorator
