import asyncio
from datetime import date
from time import time

from core.database import drop_models, init_models
from utils.loaders import start_async_data_loader, start_sync_data_loader


async def main():
    start_date = date(year=2025, month=4, day=1)

    await drop_models()
    await init_models()

    start = time()
    start_sync_data_loader(start_date)
    delta = time() - start
    print(f'start_sync_data_loader() was completed for {delta:.4f} seconds')

    await drop_models()
    await init_models()

    start = time()
    await start_async_data_loader(start_date)
    delta = time() - start
    print(f'start_async_data_loader() was completed for {delta:.4f} seconds')


if __name__ == '__main__':
    asyncio.run(main())
