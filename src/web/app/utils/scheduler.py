from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

scheduler = AsyncIOScheduler()


def scheduler_cache_clear(redis: Redis):
    @scheduler.scheduled_job('cron', hour=14, minute=11)
    async def clear_cache():
        await redis.flushdb()

    scheduler.start()
