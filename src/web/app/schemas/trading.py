from datetime import date

from .base import BaseSchema


class DateSchema(BaseSchema):
    date: date


class TradingSchema(BaseSchema):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: date
