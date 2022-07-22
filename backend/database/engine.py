from typing import AsyncGenerator

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()
async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(url=settings.CELERY_DBURI)
Session = sessionmaker(engine, autocommit=False)


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except (SQLAlchemyError, HTTPException) as exc:
            await session.rollback()
            logger.exception(exc)
            raise exc
        finally:
            await session.close()
