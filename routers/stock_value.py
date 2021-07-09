from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from models.stock import Stock
from models.stock_value import StockValue
from models.users import User
from plugins.fastapi_users import fastapi_users

router = APIRouter(
    prefix="/stockvalue",
    tags=["stockvalue"],
)


@router.post("/", response_model=StockValue)
async def create_stock_value(stock_value: StockValue, user: User = Depends(fastapi_users.current_user(verified=True))):
    nemo = stock_value.nemo
    stock: Stock = await Stock.objects.get_or_none(nemo=nemo)
    if not stock:
        return JSONResponse(status_code=404, content={"message": f"Stock not found with {nemo}"})
    data = stock_value.dict(exclude_unset=True)
    data.pop("nemo")
    data["stock_id"] = stock.id
    data["day"] = str(data["day"])
    stock_value_obj = await StockValue.objects.get_or_create(**data)
    return stock_value_obj


@router.get("/", response_model=List[StockValue])
async def list_stock():
    query = """
        SELECT 
            id
        FROM public.stockvaluemodel as stock_value
        inner join (
	        SELECT distinct on (stock_id) stock_id, max(day) as date
	        FROM public.stockvaluemodel
	        group by stock_id
        ) as day_select on 
	    stock_value.day = day_select.date and
	    stock_value.stock_id = day_select.stock_id
	"""
    rows = await StockValue.Meta.database.fetch_all(query=query)
    return await StockValue.objects.order_by("stock_id").all(
        id__in=[record["id"] for record in rows]
    )


@router.get("/{nemo}", response_model=StockValue)
async def get_stock(nemo: str):
    stock: Stock = await Stock.objects.get_or_none(nemo=nemo)
    if not stock:
        return JSONResponse(status_code=404, content={"message": f"Stock not found with {nemo}"})
    data = await StockValue.objects.order_by("-day").filter(stock_id=stock.id).limit(1).all()
    if not data:
        return JSONResponse(status_code=404, content={"message": f"Stock data for {nemo}"})
    return data[0]
