import enum
from datetime import timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, \
    UniqueConstraint, Float, Integer, PickleType
from sqlalchemy.orm import relationship, Session
from sqlalchemy_utils import URLType, ChoiceType

from database.base import Base
from database.mixins import TimestampMixin


class PaymentType(str, enum.Enum):
    only_paid = "Только платно"
    paid = "Платно"
    free = "Бесплатно"
    part_free = 'Есть бесплатные места'


class Directivity(Base):
    name = Column(String(127), index=True, nullable=False)

    programs = relationship('Program', back_populates='directivity')

    def __repr__(self):
        return f'{self.name} ({self.id})'


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
                         back_populates='events', viewonly=True)

    user_events = relationship('UserEvent', back_populates='event',
                               viewonly=True)


class Source(TimestampMixin, Base):
    name = Column(String, nullable=False)
    url = Column(URLType, nullable=False)
    enable = Column(Boolean, default=True)

    events = relationship('Event', back_populates='source')


class User(TimestampMixin, Base):
    events = relationship('Event', secondary='user_event',
                          back_populates='users')
    career_tests = relationship('CareerTest', back_populates='user')

    def favorite_events(self, session: Session):
        return session.query(Event).join(UserEvent).filter(
            UserEvent.user_id == self.id, UserEvent.is_favorite).order_by(
            UserEvent.created_at).all()

    def involved_events(self, session: Session):
        return session.query(Event).join(UserEvent).filter(
            UserEvent.user_id == self.id, UserEvent.is_involved).order_by(
            UserEvent.created_at).all()


class UserEvent(TimestampMixin, Base):
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', ),
    )
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    event_id = Column(ForeignKey('event.id'), index=True, nullable=False)
    is_favorite = Column(Boolean, default=False)
    is_involved = Column(Boolean, default=False)

    event = relationship('Event', back_populates='user_events', viewonly=True)


class StudyArea(Base):
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    programs = relationship('Program', secondary='study_area_program',
                            back_populates='study_areas')

    def __repr__(self):
        return f'{self.name} ({self.id})'


class Organization(TimestampMixin, Base):
    name = Column(String, index=True, nullable=False)

    programs = relationship('Program', back_populates='organization')

    def __repr__(self):
        return f'{self.name} ({self.id})'


class Program(TimestampMixin, Base):
    name = Column(String, nullable=False)
    organization_id = Column(ForeignKey('organization.id'), index=True,
                             nullable=False)
    directivity_id = Column(ForeignKey('directivity.id'), index=True,
                            nullable=False)
    education_type = Column(String(255), nullable=True)
    payment = Column(ChoiceType(PaymentType, impl=String()))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_favorite = Column(Boolean, default=False)
    group_with_online_signup_count = Column(Integer, default=0)

    organization = relationship('Organization', back_populates='programs')

    study_areas = relationship('StudyArea', secondary='study_area_program',
                               back_populates='programs')

    directivity = relationship('Directivity', back_populates='programs')


class StudyAreaProgram(Base):
    program_id = Column(ForeignKey('program.id'), index=True, nullable=False)
    study_area_id = Column(ForeignKey('study_area.id'), index=True,
                           nullable=False)


class CareerTest(TimestampMixin, Base):
    """Пройденные проф. ориентационные тесты"""
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    suitable_profession = Column(String(255), index=True, nullable=False)
    match_percentage = Column(Float, index=True, nullable=False)
    data = Column(PickleType, nullable=False)

    user = relationship('User', back_populates='career_tests')
