from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.root import root_router
from app.core.config import config
from app.core.redis import redis_client
from app.utils.scheduler import scheduler_cache_clear


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler_cache_clear(redis_client)
    yield


app = FastAPI(
    title=config.TITLE,
    docs_url=config.DOCS_URL,
    openapi_url=config.OPENAPI_URL,
    lifespan=lifespan,
)

app.include_router(root_router)
