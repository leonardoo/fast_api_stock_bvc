import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

import ormar

from models.base import BaseMeta
from models.stock import Stock


class StockValue(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stockvaluemodel"

    id: uuid.UUID = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1)
    nemo: Optional[str]
    stock_id: Stock = ormar.ForeignKey(Stock, skip_reverse=True)
    value: Decimal = ormar.Decimal(max_digits=16, decimal_places=4)
    day: date = ormar.Date()
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)
