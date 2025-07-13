import asyncio
from datetime import date

from core.database import drop_models, init_models
from utils.loaders import start_sync_data_loader


async def main():
    start_date = date(year=2025, month=7, day=5)

    await drop_models()
    await init_models()
    start_sync_data_loader(start_date)


if __name__ == '__main__':
    asyncio.run(main())
