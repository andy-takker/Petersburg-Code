from typing import Optional

from fastapi import APIRouter, Depends, Query, Path
from fastapi_pagination import LimitOffsetPage

from api.schemas.organization import OrganizationSchema
from controllers.repo.organization import OrganizationRepo

router = APIRouter(prefix='/organizations', tags=['Организации'])


@router.get(
    path='/',
    response_model=LimitOffsetPage[OrganizationSchema],
    name='Список организаций',
)
async def get_organization_list(
        limit: int = Query(
            title='Limit',
            description='Maximum number of returned values per request',
            gt=0,
            lt=101,
            default=50,
        ),
        offset: int = Query(
            title='Offset',
            description='The number of shifted values starting from the next one will be returned',
            gt=-1,
            default=0,
        ),
        q: str | None = Query(
            title='Query',
            description='Search string',
            default=None,
        ),
        organization_dao: OrganizationRepo = Depends(),
):
    """Возвращает список всех организаций постранично"""
    return await organization_dao.get_organization_list(
        limit=limit,
        offset=offset,
        q=q,
    )