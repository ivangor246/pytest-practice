from datetime import date
from typing import Annotated

from fastapi import Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.trading import TradingResult
from app.schemas.trading import DateSchema, TradingSchema


class TradingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dates(self, limit: int, offset: int) -> list[DateSchema]:
        stmt = (
            select(TradingResult.date)
            .distinct()
            .order_by(desc(TradingResult.date))
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.scalars(stmt)
        dates = result.all()

        return [DateSchema(date=date_) for date_ in dates]

    async def get_last_trades(
        self,
        limit: int,
        offset: int,
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
    ) -> list[TradingSchema]:
        stmt = select(TradingResult)
        if oil_id:
            stmt = stmt.where(TradingResult.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(TradingResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(TradingResult.delivery_basis_id == delivery_basis_id)
        stmt = stmt.order_by(desc(TradingResult.date)).limit(limit).offset(offset)

        result = await self.session.scalars(stmt)
        trades = result.all()

        return [TradingSchema.model_validate(trading) for trading in trades]

    async def get_range_trades(
        self,
        limit: int,
        offset: int,
        oil_id: str | None,
        delivery_type_id: str | None,
        delivery_basis_id: str | None,
        start_date: date | None,
        end_date: date | None,
    ) -> list[TradingSchema]:
        stmt = select(TradingResult)
        if oil_id:
            stmt = stmt.where(TradingResult.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(TradingResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(TradingResult.delivery_basis_id == delivery_basis_id)
        if start_date:
            stmt = stmt.where(TradingResult.date >= start_date)
        if end_date:
            stmt = stmt.where(TradingResult.date <= end_date)
        stmt = stmt.order_by(desc(TradingResult.date)).limit(limit).offset(offset)

        result = await self.session.scalars(stmt)
        trades = result.all()

        return [TradingSchema.model_validate(trading) for trading in trades]


def get_trading_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TradingService:
    return TradingService(session)
