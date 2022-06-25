from typing import List

from pydantic import BaseModel

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


class ProfessionList(BaseModel):
    professions: List[ProfessionBase]
