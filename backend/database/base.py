import re

from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import declared_attr, as_declarative


@as_declarative()
class Base:
    __name__: str

    id = Column(BigInteger, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()

    def update_from_dict(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
