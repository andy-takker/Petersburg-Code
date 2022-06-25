from datetime import timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from database.base import Base
from database.mixins import TimestampMixin


class Contest(TimestampMixin, Base):
    name = Column(String, nullable=False)
    source_url = Column(URLType, nullable=False)
    url = Column(URLType, nullable=True, comment="Сайт конкурса")
    published_date = Column(DateTime(timezone=timezone.utc), nullable=True, comment="Дата публикации")
    deadline_date = Column(DateTime, nullable=True, comment="Дата дедлайна")
    comment = Column(String, nullable=True)
    content = Column(String, nullable=True)
    source_id = Column(ForeignKey('source.id'), index=True, nullable=False)
    source = relationship("Source", back_populates="contests")


class Source(TimestampMixin, Base):
    name = Column(String, nullable=False)
    url = Column(URLType, nullable=False)
    enable = Column(Boolean, default=True)

    contests = relationship('Contest', back_populates='source')
