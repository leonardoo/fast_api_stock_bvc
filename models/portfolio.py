import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

import ormar
from ormar import post_save

from models.base import BaseMeta
from models.stock import Stock

from enum import Enum

from models.users import UserModel


class OperationStockEnum(Enum):
    buy = 'Buy'
    sell = 'Sell'


class Portfolio(ormar.Model):
    class Meta(BaseMeta):
        tablename = "portfolio"

    id: Optional[UUID] = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1, nullable=True)
    name: str = ormar.String(max_length=100)
    last_value: Decimal = ormar.Decimal(default=0, max_digits=16, decimal_places=2)
    owner: UserModel = ormar.ForeignKey(UserModel, skip_reverse=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)


class PortfolioOperation(ormar.Model):
    class Meta(BaseMeta):
        tablename = "portfolio_operation"

    id: Optional[UUID] = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1, nullable=True)
    portfolio: Portfolio = ormar.ForeignKey(Portfolio, skip_reverse=True)
    nemo: str
    operation: str = ormar.String(max_length=10, choices=list(OperationStockEnum))
    stock_id: Stock = ormar.ForeignKey(Stock, skip_reverse=True)
    value_by_stock: Decimal = ormar.Decimal(default=0, max_digits=16, decimal_places=2)
    amount: Decimal = ormar.Decimal(default=0, max_digits=16, decimal_places=2)
    commission: Decimal = ormar.Decimal(default=0, max_digits=16, decimal_places=2)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    created_by: UserModel = ormar.ForeignKey(UserModel, skip_reverse=True)


class PortfolioStock(ormar.Model):
    class Meta(BaseMeta):
        tablename = "portfolio_stock"

    id: Optional[UUID] = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1, nullable=True)
    portfolio: Portfolio = ormar.ForeignKey(Portfolio, skip_reverse=True)
    nemo: Optional[str]
    stock_id: Stock = ormar.ForeignKey(Stock, skip_reverse=True)
    amount: Decimal = ormar.Decimal(default=0, max_digits=16, decimal_places=2)
    owner: Optional[UserModel] = ormar.ForeignKey(UserModel, skip_reverse=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)


# signals

@post_save(PortfolioOperation)
async def after_save(sender, instance: PortfolioOperation, **kwargs):
    portfolio_stock = await PortfolioStock.objects.get_or_create(
        portfolio=instance.portfolio,
        stock_id=instance.stock_id,
        owner=instance.created_by
    )

    if instance.operation == OperationStockEnum.buy.value:
        portfolio_stock.amount += instance.amount
    else:
        portfolio_stock.amount -= instance.amount
    await portfolio_stock.update()
    portfolio = await Portfolio.objects.get(
        portfolio=instance.portfolio
    )
    
    if instance.operation == OperationStockEnum.buy.value:
        portfolio.last_value += instance.amount * instance.value_by_stock
    else:
        portfolio.last_value -= instance.amount * instance.value_by_stock
    await portfolio.update()
