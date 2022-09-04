from functools import wraps

from fastapi import HTTPException

from database import User, Event, CareerTest


def check_user(func):
    @wraps(func)
    async def wrapped(dao, user_id, *args, **kwargs):
        if await dao.session.get(User, user_id) is None:
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


def check_career_test(func):
    @wraps(func)
    async def wrapped(dao, career_test_id: int, *args, **kwargs):
        if await dao.session.get(CareerTest, career_test_id) is None:
            raise HTTPException(status_code=404, detail='CareerTest not found!')
        return await func(dao, career_test_id=career_test_id, *args, **kwargs)
