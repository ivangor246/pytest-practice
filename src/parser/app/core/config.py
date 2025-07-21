import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Config:
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')

    @property
    def ASYNC_DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


@lru_cache
def get_config() -> Config:
    return Config()


config = get_config()
