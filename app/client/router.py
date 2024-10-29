
from fastapi import APIRouter, Request, Response, Query
from datetime import datetime
from app.client.dao import PricesDAO


router = APIRouter(
    tags=['Фронтэнд']
) 



#получает все сохраненные данные по указанной валюте 
@router.get("/get_all_prices")
async def all_prices_currency(request: Request, ticker: str = Query(None)):
    res = await PricesDAO.all_prices(ticker)
    return res

#получает последнюю цену валюты 
@router.get("/last_price")
async def last_price_currency(request: Request, ticker: str = Query(None)):
    res = await PricesDAO.last_price(ticker)
    return res

#получает цену валюты с фильтром по дате  
@router.get("/price_depends_on")
async def price_currency_datetime(request: Request, ticker: str = Query(None), 
                                date_from: str = Query(None), date_to: str = Query(None)):
    date_from = datetime.fromisoformat(date_from) if date_from else None 
    date_to = datetime.fromisoformat(date_to) if date_to else None 
    res = await PricesDAO.price_depends_on_datetime(ticker, date_from, date_to)
    return res