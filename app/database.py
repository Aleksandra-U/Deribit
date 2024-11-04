from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import asyncio

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL,echo=True)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase): 
    pass
