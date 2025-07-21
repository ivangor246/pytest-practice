from typing import Annotated

from fastapi import Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.trading import TradingResult
from app.schemas.trading import DateSchema


class TradingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dates(self, days: int, offset: int) -> list[DateSchema]:
        stmt = (
            select(TradingResult.date)
            .distinct()
            .order_by(desc(TradingResult.date))
            .limit(days)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        dates = result.all()
        return [DateSchema(date=date_) for date_ in dates]


def get_trading_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TradingService:
    return TradingService(session)
