from fastapi import APIRouter

from api.schemas.profession import ProfessionList
from api.schemas.skill import SkillList
from controllers.proektoria import ProektoriaAPI

router = APIRouter(prefix='/proektoria', tags=['Проектория'])


@router.get(path='/skills', response_model=SkillList, name='Список навыков')
def get_skills():
    """Возвращает список всевозможных навыков определяющих профессию"""
    proektoria = ProektoriaAPI()
    return proektoria.get_suits()


@router.post(path='/skills', response_model=ProfessionList,
             name='Подбор профессии')
def post_skills(skills: SkillList):
    """Определяет подходящие под навыки профессии"""
    proektoria = ProektoriaAPI()
    return proektoria.post_suits(skills=skills)