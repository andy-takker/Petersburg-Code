import datetime
from typing import List

from pydantic import BaseModel, Field

from api.schemas.skill import SkillList, Media, SkillBase


class ProfessionBase(SkillList):
    id: int
    title: str
    slug: str
    description: str
    percent: int
    _type: str
    skills: List[SkillBase]
    media: Media


class Proektoria(BaseModel):
    professions: List[ProfessionBase]


class CareerTestShortSchema(BaseModel):
    id: int
    suitable_profession: str
    match_percentage: float
    created_at: datetime.datetime

    class Config:
        orm_mode =True


class CareerTestSchema(CareerTestShortSchema):
    result: Proektoria = Field(alias='data')

