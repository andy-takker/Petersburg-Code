from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from loguru import logger

from api.schemas.event import ExportEvent, FullEvent
from database.dao.event import EventDAO

router = APIRouter(prefix='/events', tags=['События'])


@router.get('/', response_model=LimitOffsetPage[ExportEvent],
            name='Список событий')
async def get_events(limit: int, offset: int,
                     event_dao: EventDAO = Depends()) -> Any:
    """Возвращает список всех событий постранично"""
    logger.info(f'{limit = } {offset = }')
    return await event_dao.get_all_events(limit=limit, offset=offset)


@router.get('/{event_id}', response_model=FullEvent, name='Событие')
async def get_event(event_id: int, event_dao: EventDAO = Depends()) -> Any:
    """Возвращает всю информацию о событии"""
    logger.info(f'Get event {event_id}')
    event = await event_dao.get_event(event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found!")
    return event
