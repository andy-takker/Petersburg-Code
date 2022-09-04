from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage

from api.schemas.event import AddUpdateEvent
from api.schemas.user import ShortUserEvent, FullUserEvent
from controllers.repo.user import UserRepo

user_event_router = APIRouter(prefix='/{user_id}/events', tags=['События пользователей'])


@user_event_router.get(
    '/',
    response_model=LimitOffsetPage[ShortUserEvent],
    name='Возвращает события пользователя',
)
async def get_user_events(limit: int, offset: int,
                          user_id: int,
                          is_favorite: Optional[bool] = None,
                          is_involved: Optional[bool] = None,
                          user_dao: UserRepo = Depends(),
                          ):
    """
    Возвращает по странично список событий у пользователя
    """
    return await user_dao.get_user_events(
        user_id=user_id,
        limit=limit,offset=offset,
        is_favorite=is_favorite,
        is_involved=is_involved,
    )


@user_event_router.post(
    '/',
    response_model=FullUserEvent,
    name='Создает или обновляет события пользователя'
)
async def create_or_update_user_events(
        user_id: int,
        event: AddUpdateEvent,
        user_dao: UserRepo = Depends(),
) -> None:
    """
    Создает или обновляет событие в списке пользователя
    """
    result = await user_dao.create_or_update_user_event(user_id=user_id,
                                                        event=event)
    return result


@user_event_router.get(
    path='/{event_id}',
    response_model=FullUserEvent,
    name='Возвращает полную информацию о событии пользователя',
)
async def get_user_event(user_id: int, event_id: int,
                         user_dao: UserRepo = Depends()):
    """
    Возвращает связанную информацию о событии пользователя, включая источник.
    """
    user_event = await user_dao.get_user_event(
        user_id=user_id,
        event_id=event_id)
    if user_event is None:
        raise HTTPException(status_code=404, detail="UserEvent not found!")
    return user_event


@user_event_router.delete(
    path='/',
    response_model=None,
    name='Удаляет событие у пользователя'
)
async def delete_user_event(user_id: int, event_id: int,
                            user_dao: UserRepo = Depends()):
    """
    Удаляет событие из списка пользователя.
    При повторном вызове ошибку не выдает!
    """
    await user_dao.delete_user_event(user_id=user_id, event_id=event_id)
    return
