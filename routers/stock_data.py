from fastapi import APIRouter, Depends

from models.stock import Stock
from models.stock_dividends import StockDividends
from models.stock_value import StockValue
from models.users import User
from plugins.fastapi_users import fastapi_users
from serialization.responses import Message
from serialization.stockData import StockData
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/stock/data",
    tags=["stock"],
)


async def save_model(model):
    if not model.id:
        await model.save()
    else:
        await model.update()


@router.post("/", response_model=Message)
async def create_stock(stock_data: StockData, background_tasks: BackgroundTasks, user: User = Depends(fastapi_users.current_user(verified=True))):
    stock = await Stock.objects.get_or_none(nemo=stock_data.nemo)
    if not stock:
        stock = await Stock.objects.create(name=stock_data.name, nemo=stock_data.nemo)
    if stock_data.value and stock_data.day:
        stock_value = await StockValue.objects.get_or_none(stock_id=stock.id, day=str(stock_data.day))
        if not stock_value:
            stock_value = await StockValue.objects.create(stock_id=stock.id, day=str(stock_data.day), value=0)

        stock_value.value = stock_data.value
        background_tasks.add_task(save_model, stock_value)
        #await stock_value.save()
    if all([
        stock_data.currency, stock_data.total, stock_data.paid_amount, stock_data.ex_dividend_date,
        stock_data.paid_at
    ]):
        stock_dividends = await StockDividends.objects.get_or_none(
            stock_id=stock.id,
            ex_dividend_date=str(stock_data.ex_dividend_date),
            paid_at=str(stock_data.paid_at),
        )
        if not stock_dividends:
            stock_dividends = await StockDividends.objects.create(
                stock_id=stock.id,
                ex_dividend_date=stock_data.ex_dividend_date,
                paid_at=stock_data.paid_at,
                currency=stock_data.currency
            )
        stock_dividends.total = stock_data.total
        stock_dividends.paid_amount = stock_data.paid_amount
        background_tasks.add_task(save_model, stock_dividends)
        #await stock_dividends.save()
    return Message(message=f"Created data for stock {stock.nemo}")