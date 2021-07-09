from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from models.stock import Stock
from models.users import User
from serialization.responses import Message
from plugins.fastapi_users import fastapi_users


router = APIRouter(
    prefix="/stock",
    tags=["stock"],
)


@router.post("/", response_model=Stock)
async def create_stock(stock: Stock, user: User = Depends(fastapi_users.current_user(verified=True))):
    await stock.save()
    return stock


@router.get("/", response_model=List[Stock])
async def list_stock():
    stocks = await Stock.objects.all()
    return stocks


@router.get("/{stock_id}", response_model=Stock)
async def get_stock(stock_id: UUID):
    stock_data = await Stock.object.get_or_none(id=stock_id)
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {stock_id} not found")
    return stock_data


@router.post("/{stock_id}", response_model=Stock)
async def update_stock(stock_id: UUID, stock_data: Stock, user: User = Depends(fastapi_users.current_user(verified=True))):
    stock = await Stock.objects.get_or_none(id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {stock_id} not found")
    data = stock_data.dict()
    data.pop("id", None)
    return await stock.update(**data)


@router.delete("/{stock_id}", response_model=Message)
async def delete_stock(stock_id: UUID, user: User = Depends(fastapi_users.current_user(verified=True))):
    stock = await Stock.objects.get_or_none(id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {stock_id} not found")
    await stock.delete()
    return Message(message=f"Deleted stock {stock_id}")
