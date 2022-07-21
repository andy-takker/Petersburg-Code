import re

from celery_sqlalchemy_scheduler.session import ModelBase
from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import declared_attr, as_declarative


@as_declarative()
class Base():
    __metadata__ = ModelBase
    __name__: str

    id = Column(BigInteger, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()
