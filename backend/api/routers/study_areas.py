from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi_pagination import LimitOffsetPage
from loguru import logger

from api.schemas.study_area import ExportStudyArea, BaseStudyArea
from controllers.repo.study_area import StudyAreaRepo

router = APIRouter(prefix='/study-areas', tags=['Предметные области'])


@router.get(path='/',
            response_model=LimitOffsetPage[BaseStudyArea],
            name='Список предметных областей'
            )
async def get_study_area_list(
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
        study_area_dao: StudyAreaRepo = Depends()):
    """Возвращает список все событий постранично"""
    logger.info(f'{limit = } {offset = }')
    return await study_area_dao.get_study_area_list(
        limit=limit,
        offset=offset,
        q=q,
    )


@router.get(
    path='/{study_area_id}',
    response_model=ExportStudyArea,
    name='Предметная область',
)
async def get_study_area(
        study_area_id: int = Path(
            title='Study Area ID',
            description='ID from database',
        ),
        study_area_dao: StudyAreaRepo = Depends()) -> Any:
    """Возвращает всю информацию о событии"""
    logger.info(f'Get study area {study_area_id}')
    study_area = await study_area_dao.get_study_area(study_area_id)
    if study_area is None:
        raise HTTPException(status_code=404, detail='Study area not found!')
    return study_area
