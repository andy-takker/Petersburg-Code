from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Organization
from database.engine import get_async_session


class OrganizationRepo:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_organization_list(self, limit: int, offset: int, q: str):
        query = select(Organization)
        if q is not None:
            query = query.where(Organization.name.ilike(f'%{q}%'))
        return await paginate(
            self.session,
            query=query.order_by(Organization.name),
            params=Params(limit=limit, offset=offset),
        )