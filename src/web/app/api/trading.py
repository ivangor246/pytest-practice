from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas.trading import DateSchema
from app.services.trading import TradingService, get_trading_service

trading_router = APIRouter(prefix='/trading', tags=['trading'])


@trading_router.get('/dates')
async def get_last_trading_dates(
    service: Annotated[TradingService, Depends(get_trading_service)],
    days: Annotated[int, Query(ge=0, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[DateSchema]:
    dates = await service.get_dates(days, offset)
    return dates
