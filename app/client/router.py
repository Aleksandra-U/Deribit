
from fastapi import APIRouter, Request, Response, Query, Depends
from datetime import datetime
from app.client.dao import PricesDAO, get_prices_dao

from sqlalchemy.exc import SQLAlchemyError #базовая ошибка

from app.logger import logger

router = APIRouter(
    tags=['Фронтэнд']
) 



#получает все сохраненные данные по указанной валюте 
@router.get("/get_all_prices")
#экземпляр PricesDAO передается в обработчик через Depends.
async def all_prices_currency(request: Request, ticker: str = Query(...), 
                              prices_dao_object: PricesDAO = Depends(get_prices_dao)):
    try: 
        res = await prices_dao_object.all_prices(ticker) 
        if res is None:  # Проверка на случай, если данных нет 
            logger.info(f"No prices found for ticker: {ticker}") 
        return res 
    except SQLAlchemyError as e: 
        msg = 'Database Exception: Cannot fetch data' 
        logger.error(msg, exc_info=True) 
    except Exception as e: 
        msg = 'Unknown Exception: Cannot fetch data' 
        logger.error(msg, exc_info=True) 
    


#получает последнюю цену валюты 
@router.get("/last_price")
async def last_price_currency(request: Request, ticker: str = Query(...), 
                              prices_dao_object: PricesDAO = Depends(get_prices_dao)):
    try:    
        res = await prices_dao_object.last_price(ticker)
        return res
    
    except (SQLAlchemyError, Exception) as e:  # Ловим все возможные ошибки 
        if isinstance(e, SQLAlchemyError): 
            msg = 'Database Exc' 
        elif isinstance(e, Exception): 
            msg = 'Unknown Exc' 
        msg += ': Cannot retrieve last price'   
         
        logger.error(msg, exc_info=True)  # Логируем ошибку 







#получает цену валюты с фильтром по дате  
@router.get("/price_depends_on")
async def price_currency_datetime(request: Request, ticker: str = Query(...), 
                                date_from: str = Query(None), date_to: str = Query(None), 
                                prices_dao_object: PricesDAO = Depends(get_prices_dao)):
    try:
        date_from = datetime.fromisoformat(date_from) if date_from else None 
        date_to = datetime.fromisoformat(date_to) if date_to else None 
        res = await prices_dao_object.price_depends_on_datetime(ticker, date_from, date_to)
        return res
    except (SQLAlchemyError, Exception) as e:  # Ловим все возможные ошибки 
        if isinstance(e, SQLAlchemyError): 
            msg = 'Database Exc' 
        elif isinstance(e, Exception): 
            msg = 'Unknown Exc' 
        msg += ': Cannot retrieve price by date'   
         
        logger.error(msg, exc_info=True)  # Логируем ошибку 