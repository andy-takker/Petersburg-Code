from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage

from api.schemas.profession import Proektoria, CareerTestSchema, CareerTestShortSchema
from api.schemas.skill import SkillList
from controllers.proektoria import ProektoriaAPI
from controllers.repo.user import UserRepo

career_test_router = APIRouter(prefix='/{user_id}/career-tests', tags=['Профориентационные тесты пользователей'])


@career_test_router.get(
    path='/',
    response_model=LimitOffsetPage[CareerTestShortSchema],
    name='Возвращает список пройденных профориентационных тестов',
)
async def get_user_career_tests(
        limit: int,
        offset: int,
        user_id: int,
        user_dao: UserRepo = Depends()
) -> Any:
    """
    Возвращает постранично список пройденных тестов пользователя
    """
    return await user_dao.get_user_career_tests(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )


@career_test_router.get(
    path='/{career_test_id}',
    response_model=CareerTestSchema,
    name='Возвращает результат профориентационного теста',
)
async def get_user_career_test(user_id: int, career_test_id: int, user_repo: UserRepo = Depends()) -> Any:
    career_test = await user_repo.get_user_career_test(user_id=user_id,career_test_id=career_test_id)
    return career_test


@career_test_router.post(
    path='/',
    response_model=CareerTestSchema,
    name='Обрабатывает и сохраняет тест от пользователя',
)
async def post_user_career_test(user_id: int, skills: SkillList, user_repo: UserRepo = Depends()) -> Any:
    proektoria_api = ProektoriaAPI()
    p = proektoria_api.post_suits(skills=skills)
    if p is None:
        raise HTTPException(status_code=400, detail='Result is ')
    career_test = await user_repo.save_career_test(user_id=user_id, proektoria=p)
    return career_test
