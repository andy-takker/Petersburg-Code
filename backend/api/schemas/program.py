from typing import List, Optional

from pydantic import BaseModel, validator, Field

from database import PaymentType


class Hashable:

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class StudyAreaBase(Hashable, BaseModel):
    name: str

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class OrganizationBase(Hashable, BaseModel):
    name: str

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class ProgramInput(BaseModel):
    id: int
    name: str
    study_areas: List[str]
    organization: str
    payment: PaymentType
    latitude: Optional[float]
    longitude: Optional[float]
    is_favorite: bool
    group_with_online_signup_count: int
    directivity_id: Optional[int]
    education_type: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        use_enum_values = True
