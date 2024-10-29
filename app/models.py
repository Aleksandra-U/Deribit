
from app.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func

class Prices(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key= True, nullable=False) 
    ticker = Column(String, nullable=False) 
    price = Column(Float, nullable=False) 
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)