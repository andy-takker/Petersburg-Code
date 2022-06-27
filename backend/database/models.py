from datetime import timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, \
    UniqueConstraint
from sqlalchemy.orm import relationship, Session
from sqlalchemy_utils import URLType

from database.base import Base
from database.mixins import TimestampMixin


class Event(TimestampMixin, Base):
    name = Column(String, nullable=False)
    source_url = Column(URLType, nullable=False)
    url = Column(URLType, nullable=True, comment="Сайт конкурса")
    published_date = Column(DateTime(timezone=timezone.utc), nullable=True,
                            comment="Дата публикации")
    deadline_date = Column(DateTime, nullable=True, comment="Дата дедлайна")
    comment = Column(String, nullable=True)
    content = Column(String, nullable=True)
    source_id = Column(ForeignKey('source.id'), index=True, nullable=False)

    source = relationship("Source", back_populates="events")
    users = relationship('User', secondary='user_event',
                         back_populates='events')


class Source(TimestampMixin, Base):
    name = Column(String, nullable=False)
    url = Column(URLType, nullable=False)
    enable = Column(Boolean, default=True)

    events = relationship('Event', back_populates='source')


class User(TimestampMixin, Base):
    events = relationship('Event', secondary='user_event',
                          back_populates='users')

    def favorite_events(self, session: Session):
        return session.query(Event).join(UserEvent).filter(
            UserEvent.user_id == self.id, UserEvent.is_favorite).order_by(UserEvent.created_at).all()

    def involved_events(self, session: Session):
        return session.query(Event).join(UserEvent).filter(
            UserEvent.user_id == self.id, UserEvent.is_involved).order_by(UserEvent.created_at).all()


class UserEvent(TimestampMixin, Base):
    __table_args__ = (
        UniqueConstraint('user_id','event_id', name='_user_event_uc_')
    )
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    event_id = Column(ForeignKey('event.id'), index=True, nullable=False)
    is_favorite = Column(Boolean, default=False)
    is_involved = Column(Boolean, default=False)
