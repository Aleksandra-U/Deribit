import aiohttp
import asyncio
from datetime import datetime

from app.client.dao import PricesDAO


from sqlalchemy.exc import SQLAlchemyError #базовая ошибка

from app.logger import logger




# функция для получения текущих цен 
async def fetch_price(session, currency): 
    try:
        async with session.get('https://test.deribit.com/api/v2/public/get_index_price', params={"index_name": currency}, ssl=False) as response: 

            #проверка, что HTTP-статус ответа равен 200 (успешно)
            if response.status != 200: 
                print(f"Error fetching price for {currency}: HTTP {response.status}") 
                return None
            
            result = await response.json()

            #вот в таком виде взвращается ответ 
            #{
            #     "jsonrpc": "2.0",
            #     "result": {
            #         "estimated_delivery_price": 11628.81,
            #         "index_price": 11628.81
            #     }
            # }

            # валидирует структуру ответа. проверка result - словарь и содержит ключ 'result'(и он тоже словарь)
            # помоет избежать ошибок если структура ответа изменится. Вместо прямого доступа 
            # к result['result']['index_price'] мы используем метод .get(), 
            # который возвращает None, если ключ не найден. Это также предотвращает KeyError.

            #а не так 

            # if 'result' in result and 'index_price' in result['result']:
            #    return result['result']['index_price'] 

            if isinstance(result, dict) and 'result' in result and isinstance(result['result'], dict): 
                index_price = result['result'].get('index_price') 
                if index_price is not None: 
                    return index_price 
                else: 
                    logger.warning(f"Index price not found for {currency}: {result}")  # Логируем отсутствие индекса цены 
            else:  
                logger.error(f"Unexpected response format for {currency}: {result}")  # Логируем неожиданный ответ

            


    #любая ошибка клиента например с соединением 
    except aiohttp.ClientError as e: 
        logger.error(f"Client error occurred while fetching price for {currency}: {e}")
        
    #ошибка ожидания тайм-аут     
    except asyncio.TimeoutError: 
        logger.error(f"Timeout while fetching price for {currency}") 

    #любая другая ошибка    
    except Exception as e: 
        logger.error(f"An unexpected error occurred while fetching price for {currency}: {e}")






#основная функция. заносит данные по монетам в базу данных
async def get_data_minute(): 
    currency_pairs = ['btc_usd', 'eth_usd'] 

    #текущая минута 
    last_min = datetime.now().minute

    price_dao_object = PricesDAO() #создание экземпляра PricesDAO

    #запуск сессии для асинхронной связи с через http c другим сервером
    async with aiohttp.ClientSession() as session: 
        while True:
            now = datetime.now()
            if last_min != now.minute:
                last_min = now.minute
                #берет по очереди каждую монету
                for currency in currency_pairs: 
                    price = await fetch_price(session, currency) 

                    if price is not None:  # проверка, что цена получена 
                        await price_dao_object.add_to_db(ticker=currency, price=price, timestamp=now.replace(second=0, microsecond=0)) 
                        logger.info(f"Save {currency} {price} at {now.replace(second=0, microsecond=0)}") #добавили
                    else: 
                        logger.warning(f"Price for {currency} could not be fetched. Skipping.")
            await asyncio.sleep(1)