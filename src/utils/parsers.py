import asyncio
from datetime import date, timedelta
from io import BytesIO
from typing import AsyncGenerator, Generator
from urllib.parse import urljoin

import pandas as pd
from httpx import AsyncClient, Client


class SyncParser:
    def __init__(self):
        self.__client = Client()
        self.__base_url = 'https://spimex.com'
        self.__target_url_sample = '/upload/reports/oil_xls/oil_xls_{}162000.xls'

    @staticmethod
    def _dates_gen(start_date: date) -> Generator[date, None, None]:
        end_date = date.today()
        delta = timedelta(days=1)

        if start_date > end_date:
            raise ValueError('The date is invalid.')

        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += delta

    def _target_urls_gen(self, start_date: date) -> Generator[tuple[str, date], None, None]:
        for date_ in self._dates_gen(start_date):
            date_str = date_.strftime('%Y%m%d')
            yield (
                urljoin(self.__base_url, self.__target_url_sample.format(date_str)),
                date_,
            )

    def _fetch_excel(self, start_date: date) -> Generator[tuple[pd.DataFrame, date], None, None]:
        for url, date_ in self._target_urls_gen(start_date):
            try:
                response = self.__client.get(url)

                if response.status_code == 200:
                    excel_bytes = response.content
                    df = pd.read_excel(BytesIO(excel_bytes))
                    yield (df, date_)
                else:
                    print(f'Skipped for {date_} (HTTP Response: {response.status_code})')

            except Exception as e:
                print(f'Error when parsing {url}: {e}')

    def _check_df(self, df: pd.DataFrame) -> bool:
        check_str = 'Единица измерения: Метрическая тонна'
        df_str = df.astype(str)
        if not df_str.map(lambda cell: check_str in cell).any().any():
            return False
        return True

    def parse(self, start_date: date) -> Generator[tuple[pd.DataFrame, date], None, None]:
        column_mapping = {
            'Код Инструмента': 'exchange_product_id',
            'Наименование Инструмента': 'exchange_product_name',
            'Базис поставки': 'delivery_basis_name',
            'Объем Договоров в единицах измерения': 'volume',
            'Обьем Договоров, руб.': 'total',
            'Количество Договоров, шт.': 'count',
        }

        for df, date_ in self._fetch_excel(start_date):
            if not self._check_df(df):
                print(f'Skipped for {date_}')
                continue

            df_slice = df.iloc[5:, 1:].dropna(how='all')
            df_slice.columns = (
                df_slice.iloc[0].astype(str).str.replace('\n', ' ', regex=False).str.strip()
            )
            df_slice = df_slice[1:]

            first_column = df_slice.columns[0]
            df_slice = df_slice[
                ~df_slice[first_column].astype(str).str.contains('Итого', case=False, na=False)
            ]

            try:
                df_slice = df_slice[list(column_mapping.keys())]
                df_slice = df_slice.rename(columns=column_mapping)

                filter_column_name = 'count'
                df_slice[filter_column_name] = pd.to_numeric(
                    df_slice[filter_column_name],
                    errors='coerce',
                )

                df_slice = df_slice[df_slice[filter_column_name] > 0]
                df_slice = df_slice.reset_index(drop=True)
            except KeyError as e:
                print(f'Error when filter {date_}: {e}')
                continue

            yield (df_slice, date_)


class AsyncParser:
    def __init__(self):
        self.__client = AsyncClient()
        self.__base_url = 'https://spimex.com'
        self.__target_url_sample = '/upload/reports/oil_xls/oil_xls_{}162000.xls'

    @staticmethod
    async def _dates_gen(start_date: date) -> AsyncGenerator[date, None]:
        end_date = date.today()
        delta = timedelta(days=1)

        if start_date > end_date:
            raise ValueError('The date is invalid.')

        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += delta

    async def _target_urls_gen(self, start_date: date) -> AsyncGenerator[tuple[str, date], None]:
        async for date_ in self._dates_gen(start_date):
            date_str = date_.strftime('%Y%m%d')
            yield (
                urljoin(self.__base_url, self.__target_url_sample.format(date_str)),
                date_,
            )

    async def _fetch_excel(
        self, start_date: date
    ) -> AsyncGenerator[tuple[pd.DataFrame, date], None]:
        semaphore = asyncio.Semaphore(20)

        async def fetch_one(url: str, date_: date) -> tuple[pd.DataFrame, date] | None:
            async with semaphore:
                try:
                    response = await self.__client.get(url)
                    if response.status_code == 200:
                        excel_bytes = response.content
                        df = pd.read_excel(BytesIO(excel_bytes))
                        return (df, date_)
                    else:
                        print(f'Skipped for {date_} (HTTP Response: {response.status_code})')
                except Exception as e:
                    print(f'Error when parsing {url}: {e}')
            return None

        tasks = []
        async for url, date_ in self._target_urls_gen(start_date):
            tasks.append(fetch_one(url, date_))

        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result is not None:
                yield result

    def _check_df(self, df: pd.DataFrame) -> bool:
        check_str = 'Единица измерения: Метрическая тонна'
        df_str = df.astype(str)
        if not df_str.map(lambda cell: check_str in cell).any().any():
            return False
        return True

    async def parse(self, start_date: date) -> AsyncGenerator[tuple[pd.DataFrame, date], None]:
        column_mapping = {
            'Код Инструмента': 'exchange_product_id',
            'Наименование Инструмента': 'exchange_product_name',
            'Базис поставки': 'delivery_basis_name',
            'Объем Договоров в единицах измерения': 'volume',
            'Обьем Договоров, руб.': 'total',
            'Количество Договоров, шт.': 'count',
        }

        async for df, date_ in self._fetch_excel(start_date):
            if not self._check_df(df):
                print(f'Skipped for {date_}')
                continue

            df_slice = df.iloc[5:, 1:].dropna(how='all')
            df_slice.columns = (
                df_slice.iloc[0].astype(str).str.replace('\n', ' ', regex=False).str.strip()
            )
            df_slice = df_slice[1:]

            first_column = df_slice.columns[0]
            df_slice = df_slice[
                ~df_slice[first_column].astype(str).str.contains('Итого', case=False, na=False)
            ]

            try:
                df_slice = df_slice[list(column_mapping.keys())]
                df_slice = df_slice.rename(columns=column_mapping)

                filter_column_name = 'count'
                df_slice[filter_column_name] = pd.to_numeric(
                    df_slice[filter_column_name],
                    errors='coerce',
                )

                df_slice = df_slice[df_slice[filter_column_name] > 0]
                df_slice = df_slice.reset_index(drop=True)
            except KeyError as e:
                print(f'Error when filter {date_}: {e}')
                continue

            yield (df_slice, date_)
