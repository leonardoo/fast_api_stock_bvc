from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse

from models.portfolio import Portfolio, PortfolioOperation
from models.stock import Stock
from models.users import User
from serialization.responses import Message
from plugins.fastapi_users import fastapi_users


router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio"],
)

@router.post("/", response_model=Portfolio)
async def create_portfolio(portfolio: Portfolio, user: User = Depends(fastapi_users.current_user(verified=True))):
    portfolio.owner = user.id
    await portfolio.save()
    return portfolio


@router.get("/", response_model=List[Portfolio])
async def list_portfolios(user: User = Depends(fastapi_users.current_user(verified=True))):
    portfolio = await Portfolio.objects.filter(
        owner=user.id
    ).all()
    return portfolio

@router.delete("/{portfolio_id}", response_model=Message)
async def list_portfolios(portfolio_id: UUID, user: User = Depends(fastapi_users.current_user(verified=True))):
    portfolio = Portfolio.objects.filter(
        owner=user.id,
        id=id
    ).get_or_none()
    if not portfolio:
        raise HTTPException(status_code=404, detail=f"portfolio {portfolio_id} not found")
    await portfolio.delete()
    return Message(message=f"Deleted portfolio {portfolio_id}")


@router.post("/{portfolio_id}/add", response_model=PortfolioOperation)
async def add_operation_portfolio(operation: PortfolioOperation, user: User = Depends(fastapi_users.current_user(verified=True))):
    portfolio: Portfolio = Portfolio.objects.filter(
        owner=user.id,
        id=operation.portfolio
    ).get_or_none()
    if not portfolio:
        return JSONResponse(status_code=404, content={"message": f"portfolio {operation.portfolio} not found"})
    stock: Stock = await Stock.objects.get_or_none(nemo=operation.nemo)
    if not stock:
        return JSONResponse(status_code=404, content={"message": f"Stock not found with {operation.nemo}"})
    operation.stock_id = stock.id
    operation.created_by = user.id
    await operation.save()
    return operation

