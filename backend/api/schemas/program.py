import datetime
from typing import List, Optional

from pydantic import validator, Field

from api.schemas.organization import FullOrganizationSchema
from api.schemas.study_area import StudyAreaSchema
from api.schemas.utils import HashableBaseModel, clear_from_tags, \
    display_name_from_obj
from database import EducationType


class ProgramInput(HashableBaseModel):
    id: int
    name: str
    study_areas: List[str]
    organization: str
    education_type: EducationType
    payment: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_favorite: bool
    group_with_online_signup_count: int
    directivity_id: Optional[int]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        use_enum_values = True


class ProfileSchema(HashableBaseModel):
    name: str
    subjects: List[str]


class GroupSchema(HashableBaseModel):
    name: str
    members_limit: int
    min_age: str
    max_age: str
    is_age_limit: bool
    timetable_type: str
    entry_period_type: str
    date_start: Optional[datetime.date]
    date_end: Optional[datetime.date]
    lesson_start: Optional[datetime.date]
    lesson_end: Optional[datetime.date]
    duration_years: Optional[int]
    duration_months: Optional[int]
    duration_days: Optional[int]
    status: str

    @validator('entry_period_type', 'status', pre=True)
    def format_display_name_from_obj(cls, v):
        if isinstance(v, str):
            return v
        return display_name_from_obj(v)


class FullProgramSchema(HashableBaseModel):
    id: int
    name: str
    district: str
    address: str
    latitude: float
    longitude: float
    description: str
    competence: str
    skills: str
    content: str
    study_form: str
    class_mode: str
    qualification: str

    profiles: List[ProfileSchema]

    industry: str
    education_level: str
    directivity: str

    study_areas: List[str]

    education_type: str

    groups: List[GroupSchema]

    material_technical_base: str
    difficulty_level: str
    program_type_odo: str

    organization: FullOrganizationSchema

    @validator(
        'description', 'competence', 'skills', 'content',
        'material_technical_base', pre=True)
    def clear_description(cls, v):
        return clear_from_tags(v)

    @validator('study_form', 'industry', 'education_level', 'directivity',
               'program_type_odo', 'education_type', 'difficulty_level',
               'program_type_odo', pre=True)
    def format_display_name_from_obj(cls, v):
        if isinstance(v, str):
            return v
        return display_name_from_obj(v)

    @validator('study_areas', pre=True, each_item=True)
    def each_study_area_to_str(cls, v):
        if isinstance(v, dict):
            return v['display_name']
        return v
