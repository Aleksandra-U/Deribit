import aiohttp
import asyncio
from datetime import datetime

from app.client.dao import PricesDAO


# функция для получения текущих цен 
async def fetch_price(session, currency): 
    async with session.get('https://test.deribit.com/api/v2/public/get_index_price', params={"index_name": currency}, ssl=False) as response: 
        result = await response.json() 
        return result['result']['index_price'] 


#основная функция. заносит данные по монетам в базу данных
async def get_data_minute(): 
    currency_pairs = ['btc_usd', 'eth_usd'] 

    last_min = datetime.now().minute

    async with aiohttp.ClientSession() as session: 
        while True:
            now = datetime.now()
            if last_min != now.minute:
                last_min = now.minute
                for currency in currency_pairs: 
                    price = await fetch_price(session, currency) 
                    await PricesDAO.add_to_db(ticker=currency, price=price, timestamp=now.replace(second=0, microsecond=0))
                    print(f"Save {currency} {price} {now.replace(second=0, microsecond=0)}")
            await asyncio.sleep(1)