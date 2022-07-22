from pydantic import BaseModel

from api.schemas.event import ExportEvent, FullEvent


class UserEvent(BaseModel):
    user_id: int
    event_id: int
    is_favorite: bool
    is_involved: bool

    class Config:
        orm_mode = True


class ShortUserEvent(UserEvent):
    event: ExportEvent

class FullUserEvent(UserEvent):
    event: FullEvent
