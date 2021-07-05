import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID

import ormar

from config import database, metadata
from models.stock import Stock


class StockDividends(ormar.Model):
    class Meta:
        tablename = "stockdividendmodel"
        database = database
        metadata = metadata

    id: UUID = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1)
    nemo: Optional[str]
    stock_id: Stock = ormar.ForeignKey(Stock, skip_reverse=True)
    currency: str = ormar.String(max_length=100)
    total: Decimal = ormar.Decimal(max_digits=16, decimal_places=4, default=0)
    paid_amount: Decimal = ormar.Decimal(max_digits=16, decimal_places=4, default=0)
    ex_dividend_date: date = ormar.Date()
    paid_at: date = ormar.Date()
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)
