from datetime import date

from core.database import sync_session
from models import TradingResult

from utils.parsers import SyncParser


def start_sync_data_loader(start_date: date):
    parser = SyncParser()
    success_count = 0

    with sync_session() as session:
        for df, date_ in parser.parse(start_date):
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
                session.commit()
                success_count += 1
            except Exception:
                print(f'Error in table for {date_}')
                session.rollback()

    print(f'Successfully loaded {success_count} tables')
