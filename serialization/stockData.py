from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class StockData(BaseModel):

    name: str
    nemo: str
    value: Optional[Decimal]
    day: date
    currency: Optional[str]
    total: Optional[Decimal]
    paid_amount: Optional[Decimal]
    ex_dividend_date: Optional[date]
    paid_at: Optional[date]

