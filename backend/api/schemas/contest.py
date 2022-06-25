import datetime
from typing import Optional

from pydantic import BaseModel


class ContestBase(BaseModel):
    name: str
    source_url: str
    url: Optional[str]
    published_date: datetime.datetime
    deadline_date: Optional[datetime.datetime]
    source_id: int
    comment: Optional[str]

    class Config:
        orm_mode = True


class ImportContest(ContestBase):
    pass
