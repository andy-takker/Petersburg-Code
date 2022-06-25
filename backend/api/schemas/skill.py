from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class Media(BaseModel):
    poster: HttpUrl


class SkillBase(BaseModel):
    id: int
    title: str
    type: int
    keyword: Optional[str]
    sort: int
    media: Media


class SkillList(BaseModel):
    skills: List[SkillBase]
