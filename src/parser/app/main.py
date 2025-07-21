import asyncio
from datetime import date
from time import time

from core.database import init_models
from utils.loaders import start_async_data_loader


async def main():
    start_date = date(year=2025, month=1, day=1)

    await init_models()

    start = time()
    await start_async_data_loader(start_date)
    delta = time() - start
    print(f'start_async_data_loader() was completed for {delta:.4f} seconds')


if __name__ == '__main__':
    asyncio.run(main())
