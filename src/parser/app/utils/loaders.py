from datetime import date

from core.database import async_session
from models import TradingResult

from utils.parsers import AsyncParser


async def start_async_data_loader(start_date: date):
    parser = AsyncParser()
    success_count = 0

    print('\nStart async loader')

    async with async_session() as session:
        async for df, date_ in parser.parse(start_date):
            try:
                for _, row in df.iterrows():
                    obj = TradingResult(
                        exchange_product_id=str(row.get('exchange_product_id')),
                        exchange_product_name=str(row.get('exchange_product_name')),
                        oil_id=str(row.get('exchange_product_id'))[:4],
                        delivery_basis_id=str(row.get('exchange_product_id'))[4:7],
                        delivery_basis_name=str(row.get('delivery_basis_name')),
                        delivery_type_id=str(row.get('exchange_product_id'))[-1],
                        volume=int(row.get('volume', 0)),
                        total=int(row.get('total', 0)),
                        count=int(row.get('count')),
                        date=date_,
                    )
                    session.add(obj)
                await session.commit()
                success_count += 1
            except Exception:
                print(f'Error in table for {date_}')
                await session.rollback()

    print(f'\nSuccessfully loaded {success_count} tables by async loader')
