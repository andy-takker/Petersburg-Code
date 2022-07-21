from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.schemas.event import AddUpdateEvent
from api.schemas.user import ShortUserEvent, FullUserEvent
from database.dao.user import UserDAO

router = APIRouter(prefix='/users')


@router.get("/{user_id}/events", response_model=list[ShortUserEvent])
async def get_user_events(
        user_id: int,
        is_favorite: Optional[bool] = None,
        is_involved: Optional[bool] = None,
        user_dao: UserDAO = Depends(),
):
    """События пользователя"""
    return await user_dao.get_user_events(
        user_id=user_id,
        is_favorite=is_favorite,
        is_involved=is_involved,
    )


@router.post("/{user_id}/events", response_model=FullUserEvent)
async def update_user_events(
        user_id: int,
        event: AddUpdateEvent,
        user_dao: UserDAO = Depends(),
) -> None:
    result = await user_dao.create_or_update_user_event(user_id=user_id,
                                                        event=event)
    return result


@router.get("/{user_id}/events/{event_id}", response_model=FullUserEvent)
async def get_user_event(user_id: int, event_id: int,
                         user_dao: UserDAO = Depends()):
    user_event = await user_dao.get_user_event(
        user_id=user_id,
        event_id=event_id)
    if user_event is None:
        raise HTTPException(status_code=404, detail="UserEvent not found!")
    return user_event


@router.delete('/{user_id}/events/{event_id}', response_model=None)
async def delete_user_event(user_id: int, event_id: int,
                            user_dao: UserDAO = Depends()):
    await user_dao.delete_user_event(user_id=user_id, event_id=event_id)
    return
