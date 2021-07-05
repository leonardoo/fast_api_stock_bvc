from typing import List
from datetime import datetime

from fastapi import APIRouter
from starlette.responses import JSONResponse

from models.stock import Stock
from models.stock_dividends import StockDividends
from serialization.responses import Message

router = APIRouter(
    prefix="/dividends",
    tags=["dividends"],
)

def get_current_year():
    return datetime.now().year


@router.post("/", response_model=StockDividends)
async def create_dividend(dividend: StockDividends):
    stock = await Stock.objects.get_or_none(nemo=dividend.nemo)
    if not stock:
        return JSONResponse(status_code=404, content={"message": "Stock not found"})
    dividend_data = dividend.dict(exclude_unset=True)
    total = dividend_data.pop("total")
    paid_amount = dividend_data.pop("paid_amount")
    dividend_data.pop("nemo")
    dividend_data["ex_dividend_date"] = str(dividend_data["ex_dividend_date"])
    dividend_data["paid_at"] = str(dividend_data["paid_at"])
    dividend_data["stock_id"] = stock.id
    dividend_obj = await StockDividends.objects.get_or_create(**dividend_data)
    dividend_obj.total = total
    dividend_obj.paid_amount = paid_amount
    await dividend_obj.update()
    return dividend_obj


@router.get("/", response_model=List[StockDividends])
async def get_list_dividends():
    year = get_current_year()
    data = StockDividends.objects.filter(paid_at__gte=f"{year}-01-01", paid_at__lt=f"{year+1}-01-01")
    data = data.order_by("paid_at")
    return await data.all()


@router.get("/{nemo}", response_model=List[StockDividends])
async def get_stock(nemo: str):
    stock = await Stock.objects.get_or_none(nemo=nemo)
    if not stock:
        return JSONResponse(status_code=404, content={"message": "Stock not found"})
    data = StockDividends.objects
    data = data.filter(stock_id=stock.id)
    return await data.all()


