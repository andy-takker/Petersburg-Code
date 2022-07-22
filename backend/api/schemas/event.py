import datetime
from typing import Optional

from pydantic import BaseModel

from api.schemas.source import ImportSource


class EventBase(BaseModel):
    name: str
    source_url: str
    url: Optional[str]
    published_date: Optional[datetime.datetime]
    deadline_date: Optional[datetime.datetime]
    source_id: int
    comment: Optional[str]

    class Config:
        orm_mode = True


class ImportEvent(EventBase):
    pass


class AddUpdateEvent(BaseModel):
    id: int
    is_favorite: bool
    is_involved: bool


class ExportEvent(BaseModel):
    id: int
    name: str
    source_url: str
    deadline_date: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class FullEvent(ExportEvent):
    url: Optional[str]
    published_date: Optional[datetime.datetime]
    source_id: int
    comment: Optional[str]
    source: ImportSource


