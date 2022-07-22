from functools import wraps
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.limit_offset import Params
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.schemas.event import AddUpdateEvent
from database import User, Event, UserEvent
from database.dao.utils import check_user, check_event
from database.engine import get_session


class UserDAO:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    @check_user
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    @check_user
    async def get_user_events(self, user_id: int, limit: int, offset: int, is_favorite: bool,
                              is_involved: bool):
        """Возвращает список событий пользователя"""
        query = select(UserEvent) \
            .options(selectinload(UserEvent.event)) \
            .filter(UserEvent.user_id == user_id)
        if is_involved is not None:
            query.filter(UserEvent.is_involved == is_involved)
        if is_favorite is not None:
            query.filter(UserEvent.is_favorite == is_favorite)
        return await paginate(
            self.session,
            query=query,
            params=Params(limit=limit, offset=offset),
        )

    @check_user
    @check_event
    async def get_user_event(self, user_id: int, event_id: int) -> Optional[
        Event]:
        query = select(UserEvent).options(
            selectinload(UserEvent.event),
            selectinload(UserEvent.event, Event.source)
        ).filter_by(user_id=user_id, event_id=event_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    @check_user
    async def create_or_update_user_event(self, user_id: int,
                                          event: AddUpdateEvent):
        """Создает или обновляет событие"""
        if await self.session.get(Event,event.id) is None:
            raise HTTPException(status_code=404, detail='Event not found!')
        query = select(UserEvent).filter_by(user_id=user_id, event_id=event.id)
        user_event: UserEvent = (
            await self.session.execute(query)).scalars().first()
        if user_event is None:
            user_event = UserEvent()
            user_event.user_id = user_id
            user_event.event_id = event.id
        user_event.is_involved = event.is_involved
        user_event.is_favorite = event.is_favorite
        self.session.add(user_event)
        return await self.get_user_event(user_id=user_id, event_id=event.id)

    @check_user
    @check_event
    async def delete_user_event(self, user_id: int, event_id: int) -> None:
        """Удаляет событие пользователя"""
        await self.session.execute(delete(UserEvent).where(UserEvent.event_id == event_id, UserEvent.user_id == user_id))

