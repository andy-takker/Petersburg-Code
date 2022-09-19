from typing import Optional

from pydantic import Field

from api.schemas.utils import HashableBaseModel


class StudyAreaSchema(HashableBaseModel):
    name: str = Field(alias='display_name',)


class BaseStudyArea(HashableBaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ExportStudyArea(BaseStudyArea):
    description: Optional[str]
