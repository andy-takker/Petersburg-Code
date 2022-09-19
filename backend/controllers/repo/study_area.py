from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import StudyArea
from database.engine import get_async_session


class StudyAreaRepo:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_study_area_list(self, limit: int, offset: int, q: str | None):
        query = select(StudyArea)
        if q is not None:
            query = query.where(StudyArea.name.ilike(f'%{q}%'))
        return await paginate(
            self.session,
            query=query.order_by(StudyArea.id),
            params=Params(limit=limit, offset=offset),
        )

    async def get_study_area(self, study_area_id: int) -> StudyArea:
        return await self.session.get(StudyArea, study_area_id)
