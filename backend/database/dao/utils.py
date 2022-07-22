from functools import wraps

from fastapi import HTTPException

from database import User, Event


def check_user(func):
    @wraps(func)
    async def wrapped(dao, user_id, *args, **kwargs):
        if await dao.session.get(User,user_id) is None:
            raise HTTPException(status_code=404, detail='User not found!')
        return await func(dao, user_id=user_id, *args, **kwargs)

    return wrapped


def check_event(func):
    @wraps(func)
    async def wrapped(dao, event_id, *args, **kwargs):
        if await dao.session.get(Event, event_id) is None:
            raise HTTPException(status_code=404, detail='Event not found!')
        return await func(dao, event_id=event_id, *args, **kwargs)

    return wrapped
