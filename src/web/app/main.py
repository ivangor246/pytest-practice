from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.core.database import get_session
from app.models.trading import TradingResult

app = FastAPI(
    title=config.TITLE,
    docs_url=config.DOCS_URL,
    openapi_url=config.OPENAPI_URL,
)


@app.get('/')
async def hello(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.scalar(select(TradingResult))
    return result
