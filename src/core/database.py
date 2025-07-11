from models import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import config

sync_engine = create_engine(config.SYNC_DB_URL)
sync_session = sessionmaker(sync_engine)

async_engine = create_async_engine(config.ASYNC_DB_URL)
async_session = async_sessionmaker(async_engine)


async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
