from app.models import Prices  
from app.dao.base import BaseDAO


class PricesDAO(BaseDAO): 
    model = Prices



async def get_prices_dao(): 
    return PricesDAO()
