import asyncio

from core.database import drop_models, init_models


async def main():
    await drop_models()
    await init_models()


if __name__ == '__main__':
    asyncio.run(main())
