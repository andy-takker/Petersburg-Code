from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import Base

settings = get_settings()
async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI)

async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False,
)
engine = create_engine(url=settings.CELERY_DBURI)
Session = sessionmaker(engine, autocommit=False)


async def init_models():
    # async with async_engine.begin() as connection:
    #     await connection.run_sync(Base.metadata.drop_all)
    #     await connection.run_sync(Base.metadata.create_all)
    pass
