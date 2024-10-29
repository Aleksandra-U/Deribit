from app.database import async_session_maker
from sqlalchemy import select, insert

class BaseDAO:
    model = None


    # Асинхронная функция для сохранения данных в базу данных
    @classmethod
    async def add_to_db(cls, **data): #тикер валюты, текущая цена и время
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit() 


    #Получение всех сохраненных данных по указанной валюте 
    @classmethod
    async def all_prices(cls, ticker):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.ticker == ticker)
            result = await session.execute(query)
            return result.scalars().all()    
        

    #Получение последней цены валюты 
    @classmethod
    async def last_price(cls, ticker):
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
        


    #Получение цены валюты с фильтром по дате  
    @classmethod
    async def price_depends_on_datetime(cls, ticker, date_from=None, date_to=None):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.ticker == ticker)


            if date_from: 
                query = query.where(cls.model.timestamp >= date_from) 
            if date_to: 
                query = query.where(cls.model.timestamp <= date_to) 
 
            result = await session.execute(query) 
            return result.scalars().all()
