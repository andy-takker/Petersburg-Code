from pydantic import BaseModel, HttpUrl


class ImportSource(BaseModel):
    name: str
    url: HttpUrl
    enable: bool

    class Config:
        orm_mode = True


class ExportSource(ImportSource):
    id: int
