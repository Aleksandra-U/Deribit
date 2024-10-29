from app.models import Prices  
from app.dao.base import BaseDAO


class PricesDAO(BaseDAO): 
    model = Prices