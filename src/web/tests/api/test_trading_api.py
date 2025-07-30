from datetime import date

import pytest
import pytest_asyncio
from app.main import app
from app.models.trading import TradingResult
from httpx import ASGITransport, AsyncClient
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
class TestTradingAPI:
    async def test_get_last_trading_dates(self, session: AsyncSession, fill_trading_data):
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
            response = await ac.get(
                '/api/trading/dates',
                params={'limit': 10, 'offset': 0},
            )
            assert response.status_code == 200

            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 10
            assert all('date' in item for item in data)

            stmt = (
                select(TradingResult.date)
                .distinct()
                .order_by(desc(TradingResult.date))
                .limit(10)
                .offset(0)
            )
            db_result = await session.scalars(stmt)
            db_dates = db_result.all()
            db_dates_formatted = [d.isoformat() for d in db_dates]

            api_dates = [item['date'] for item in data]

            assert api_dates == db_dates_formatted

    async def test_get_trading_results(self, session: AsyncSession, fill_trading_data):
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
            response = await ac.get(
                '/api/trading/last-trades',
                params={'limit': 10, 'offset': 0},
            )
            assert response.status_code == 200

            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 10
            assert all('exchange_product_id' in item for item in data)

            stmt = select(TradingResult).order_by(desc(TradingResult.date)).limit(10).offset(0)
            db_result = await session.scalars(stmt)
            db_trades = db_result.all()

            for api_trade, db_trade in zip(data, db_trades):
                assert api_trade['exchange_product_id'] == db_trade.exchange_product_id
                assert api_trade['exchange_product_name'] == db_trade.exchange_product_name
                assert api_trade['oil_id'] == db_trade.oil_id
                assert api_trade['delivery_basis_id'] == db_trade.delivery_basis_id
                assert api_trade['count'] == db_trade.count

    async def test_get_dynamics(self, session: AsyncSession, fill_trading_data):
        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 5)

        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
            response = await ac.get(
                '/api/trading/range-trades',
                params={
                    'limit': 10,
                    'offset': 0,
                    'start_date': start_date,
                    'end_date': end_date,
                },
            )
            assert response.status_code == 200

            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 5
            assert all('exchange_product_id' in item for item in data)

            stmt = (
                select(TradingResult)
                .where(TradingResult.date >= start_date, TradingResult.date <= end_date)
                .order_by(desc(TradingResult.date))
                .limit(10)
                .offset(0)
            )
            db_result = await session.scalars(stmt)
            db_trades = db_result.all()

            for api_trade, db_trade in zip(data, db_trades):
                assert api_trade['exchange_product_id'] == db_trade.exchange_product_id
                assert api_trade['exchange_product_name'] == db_trade.exchange_product_name
                assert api_trade['oil_id'] == db_trade.oil_id
                assert api_trade['delivery_basis_id'] == db_trade.delivery_basis_id
                assert api_trade['count'] == db_trade.count
