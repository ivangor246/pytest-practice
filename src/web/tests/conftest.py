from typing import AsyncGenerator

import pytest_asyncio
from app.core.database import engine, get_session
from app.models.base import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async for db_session in get_session():
        yield db_session
        break


@pytest_asyncio.fixture(autouse=True)
async def clean_database(session: AsyncSession):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))

    await session.commit()
