from datetime import date

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from .base import Base


class TradingResult(Base):
    __tablename__ = 'trading_results'

    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[date]

    __table_args__ = (
        UniqueConstraint('exchange_product_id', 'date', name='uq_exchange_product_id_date'),
    )
