from app.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError #базовая ошибка

from app.logger import logger

class BaseDAO:
    model = None


    # Асинхронная функция для сохранения данных в базу данных
    @classmethod
    async def add_to_db(cls, **data): #тикер валюты, текущая цена и время
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit() 
        except (SQLAlchemyError, Exception) as e: #конструукция ловит все ошибки
            if isinstance(e, SQLAlchemyError):
                msg = 'Database Exc'
            elif isinstance(e, Exception):
                msg = 'Unknown Exc'    
            msg += ': Cannot add data'  
 
            logger.error( #можно написать info 
                msg, exc_info=True #появится текст ошибка прямо в логе
            )

    #Получение всех сохраненных данных по указанной валюте 
    @classmethod
    async def all_prices(cls, ticker):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).where(cls.model.ticker == ticker)
                result = await session.execute(query)
                return result.scalars().all()    
        except (SQLAlchemyError, Exception) as e:  # ловим все ошибки 
            if isinstance(e, SQLAlchemyError): 
                msg = 'Database Exc' 
            elif isinstance(e, Exception): 
                msg = 'Unknown Exc' 
            msg += ': Cannot fetch prices for ticker {}'.format(ticker) 
    
            logger.error(  # логи ошибок 
                msg, exc_info=True  # добавляет текст ошибки в лог 
            ) 
            return []  # возвращаем пустой список в случае ошибки    

    #Получение последней цены валюты 
    @classmethod
    async def last_price(cls, ticker):
        try:
            async with async_session_maker() as session:
                query = (
                    select(cls.model)
                    .where(cls.model.ticker == ticker)
                    .order_by(cls.model.timestamp.desc())
                    .limit(1)
                )
                result = await session.execute(query)
                price = result.scalars().first() 
                return price
        except SQLAlchemyError as e: 
            msg = f'Database Error in last_price: {str(e)}' 
            logger.error(msg, exc_info=True) 
            # можно выборосить ошибку или или вернуть какое-либо значение по умолчанию 
        except Exception as e: 
            msg = f'Unknown Error in last_price: {str(e)}' 
            logger.error(msg, exc_info=True) 




    #Получение цены валюты с фильтром по дате  
    @classmethod
    async def price_depends_on_datetime(cls, ticker, date_from=None, date_to=None):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).where(cls.model.ticker == ticker)


                if date_from: 
                    query = query.where(cls.model.timestamp >= date_from) 
                if date_to: 
                    query = query.where(cls.model.timestamp <= date_to) 
    
                result = await session.execute(query) 
                return result.scalars().all()
        except (SQLAlchemyError, Exception) as e: 
            if isinstance(e, SQLAlchemyError): 
                msg = 'Database Exception' 
            elif isinstance(e, Exception): 
                msg = 'Unknown Exception'     
            msg += ': Cannot retrieve data'   
    
            logger.error(  # Вы можете изменить уровень логирования на info, если необходимо 
                msg, exc_info=True  # Появится текст ошибки прямо в логе 
            ) 
            return []  # Возврат пустого списка или обработка ошибки по вашему усмотрению