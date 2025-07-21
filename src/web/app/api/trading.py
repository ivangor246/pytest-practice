from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas.trading import DateSchema, TradingSchema
from app.services.trading import TradingService, get_trading_service

trading_router = APIRouter(prefix='/trading', tags=['trading'])


@trading_router.get('/dates')
async def get_last_trading_dates(
    service: Annotated[TradingService, Depends(get_trading_service)],
    limit: Annotated[int, Query(ge=0, le=200)] = 200,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[DateSchema]:
    dates = await service.get_dates(limit=limit, offset=offset)
    return dates


@trading_router.get('/last-trades')
async def get_trading_results(
    service: Annotated[TradingService, Depends(get_trading_service)],
    limit: Annotated[int, Query(ge=0, le=200)] = 200,
    offset: Annotated[int, Query(ge=0)] = 0,
    oil_id: Annotated[str | None, Query()] = None,
    delivery_type_id: Annotated[str | None, Query()] = None,
    delivery_basis_id: Annotated[str | None, Query()] = None,
) -> list[TradingSchema]:
    trades = await service.get_last_trades(
        limit=limit,
        offset=offset,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )
    return trades


@trading_router.get('/range-trades')
async def get_dynamics(
    service: Annotated[TradingService, Depends(get_trading_service)],
    limit: Annotated[int, Query(ge=0, le=200)] = 200,
    offset: Annotated[int, Query(ge=0)] = 0,
    oil_id: Annotated[str | None, Query()] = None,
    delivery_type_id: Annotated[str | None, Query()] = None,
    delivery_basis_id: Annotated[str | None, Query()] = None,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> list[TradingSchema]:
    trades = await service.get_range_trades(
        limit=limit,
        offset=offset,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        start_date=start_date,
        end_date=end_date,
    )
    return trades
