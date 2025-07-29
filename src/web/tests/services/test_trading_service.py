from datetime import date

import pytest
import pytest_asyncio
from app.models.trading import TradingResult
from app.services.trading import TradingService
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def fill_trading_data(session: AsyncSession) -> None:
    trading_data = []
    for i in range(1, 11):
        trading_data.append(
            TradingResult(
                exchange_product_id=f'epid{i}',
                exchange_product_name=f'epn{i}',
                oil_id=f'oid{i}',
                delivery_basis_id=f'dbid{i}',
                delivery_basis_name=f'dbn{i}',
                delivery_type_id=f'dtid{i}',
                volume=i,
                total=i,
                count=i,
                date=date(2025, 1, i % 30),
            )
        )
    session.add_all(trading_data)
    await session.commit()


@pytest.mark.asyncio
class TestTradingService:
    async def test_get_dates(self, session: AsyncSession, fill_trading_data):
        service = TradingService(session)

        service_result = await service.get_dates(limit=10, offset=0)
        service_result_dates = [item.date for item in service_result]

        stmt = (
            select(TradingResult.date)
            .distinct()
            .order_by(desc(TradingResult.date))
            .limit(10)
            .offset(0)
        )
        db_result = await session.scalars(stmt)
        db_result_dates = db_result.all()

        assert service_result_dates == db_result_dates
