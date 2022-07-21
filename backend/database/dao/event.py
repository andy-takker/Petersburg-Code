from fastapi import Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.limit_offset import Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.engine import get_session
from database.models import Event


class EventDAO:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_all_events(self, limit: int, offset: int):
        return await paginate(
            self.session,
            select(Event),
            params=Params(limit=limit, offset=offset),
        )

    async def get_event(self, event_id: int) -> Event:
        return await self.session.get(Event, event_id,options=(selectinload(Event.source),))
