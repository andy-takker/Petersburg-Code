import html
import re
from typing import Optional, Literal, List

from pydantic import Field, HttpUrl, EmailStr, validator

from api.schemas.utils import HashableBaseModel, clear_from_tags

BASE_SOURCE_URL = 'https://copp.petersburgedu.ru/'


class OrganizationBase(HashableBaseModel):
    name: str

    class Config:
        orm_mode = True


class OrganizationSchema(OrganizationBase):
    id: int


class OrganizationAddress(HashableBaseModel):
    district: str
    address: str
    latitude: float
    longitude: float
    address_type: Literal['Фактический', 'Юридический']
    metro: List[str]


class FullOrganizationSchema(HashableBaseModel):
    external_id: int = Field(alias='id')
    name: str
    full_name: str
    short_name: str
    ogrn: str
    study_area_type: str
    description: str
    web_site: Optional[HttpUrl]
    public_email: Optional[EmailStr]
    phone: str
    vk: Optional[HttpUrl]
    logo: Optional[HttpUrl]
    image: Optional[HttpUrl]
    addresses: List[OrganizationAddress]

    @validator('logo', pre=True)
    def update_logo_url(cls, v):
        return BASE_SOURCE_URL + v

    @validator('image', pre=True)
    def update_image_url(cls, v):
        return BASE_SOURCE_URL + v

    @validator('description', pre=True)
    def clear_description(cls, v):
        return clear_from_tags(v)
