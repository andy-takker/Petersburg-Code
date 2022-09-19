import enum
from datetime import timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, \
    UniqueConstraint, Float, Integer, PickleType, Table, Index
from sqlalchemy.orm import relationship, Session
from sqlalchemy_utils import URLType, ChoiceType

from database.base import Base
from database.mixins import TimestampMixin


class PaymentType(str, enum.Enum):
    ONLY_PAID = 'Только платно'
    PAID = 'Платно'
    FREE = 'Бесплатно'
    PART_FREE = 'Есть бесплатные места'


class EducationType(str, enum.Enum):
    ADDITIONAL_EDUCATION = 'Дополнительное образование'
    ADDITIONAL_PROFESSIONAL_EDUCATION = 'Дополнительное профессиональное образование'
    CAREER_GUIDANCE_FOR_SCHOOLCHILDREN = 'Профориентация для школьников'
    HIGHER_EDUCATION = 'Высшее образование'
    OTHER = 'Другое'
    PREPARATION_FOR_ADMISSION_TO_UNIVERSITY = 'Подготовка к поступлению в вуз'
    PROFESSIONAL_EDUCATION = 'Профессиональное обучение'
    SECONDARY_VOCATIONAL_EDUCATION = 'Среднее профессиональное образование'


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

    programs = relationship(
        'Program',
        secondary='study_area_program',
        back_populates='study_areas',
        viewonly=True,
    )

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
    education_type = Column(ChoiceType(EducationType, impl=String()),
                            nullable=True)
    payment = Column(ChoiceType(PaymentType, impl=String()))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_favorite = Column(Boolean, default=False)
    group_with_online_signup_count = Column(Integer, default=0)

    organization = relationship('Organization', back_populates='programs')

    study_areas = relationship(
        'StudyArea',
        secondary='study_area_program',
        back_populates='programs',
        order_by='StudyArea.name',
    )

    education_profiles = relationship(
        'EducationProfile',
        secondary='education_profile_program',
        back_populates='programs',
        order_by='EducationProfile.name',
    )

    directivity = relationship('Directivity', back_populates='programs')


Table(
    'study_area_program',
    Base.metadata,
    Column(
        'program_id',
        ForeignKey('program.id'),
        index=True,
        nullable=False,
    ),
    Column(
        'study_area_id',
        ForeignKey('study_area.id'),
        index=True,
        nullable=False,
    ),
)


class EducationProfile(Base):
    name = Column(String, index=True, nullable=False)

    programs = relationship(
        'Program',
        secondary='education_profile_program',
        back_populates='education_profiles',
        viewonly=True,
    )


Table(
    'education_profile_program',
    Base.metadata,
    Column(
        'program_id',
        ForeignKey('program.id'),
        index=True,
        nullable=False,
    ),
    Column(
        'education_profile_id',
        ForeignKey('education_profile.id'),
        index=True,
        nullable=False,
    ),
)


class CareerTest(TimestampMixin, Base):
    """Пройденные проф. ориентационные тесты"""
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    suitable_profession = Column(String(255), index=True, nullable=False)
    match_percentage = Column(Float, index=True, nullable=False)
    data = Column(PickleType, nullable=False)

    user = relationship('User', back_populates='career_tests')
